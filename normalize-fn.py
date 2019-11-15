from argparse import ArgumentParser, RawDescriptionHelpFormatter
from platform import python_version
from operator import itemgetter
from tempfile import _get_candidate_names
from subprocess import run
import sys
import os
import re
import time
import json
import atexit
import urllib.request

module_name = '%(prog)s: Normalizes filenames downloaded from sharing services'
script_name = os.path.basename(__file__)
config_name = f'{script_name}.json'
config_url = 'https://raw.githubusercontent.com/gsscoder/normalize-fn/master/normalize-fn.py.json'
temp_scheme = None
__version__ = '0.1.0'


def get_acronyms_re(args, config):
    acronyms = (
        r'(?:^|(?<=))('
        r'CAM|TS|TC|DV|MiniDV|R3|R4|R5|R6|VHSSCR|DVDSCR|DVDRip|DVDMux|WEBMux|DLMux|'
        r'DVD5|DVD9|BRRip|BDRip|BDMux|BluRay|VU|SBS|WEB-DL|WEBRip|WEB-RIP|HDTV|HDTS|PDTV|'
        r'SATRip|SAT RIP|DVBRip|DVDRip|DRip|DVB-S|DTTRip|TVRip|TV TIP|WP|SCREENER|'
        r'HQ|TV|RIP|SUBS|1080p|HEVC|720p|'
        r'AAC|AC3|MP3|DTS|MD|LD|DD|DSP|DSP2|AVC|'
        r'H 264|HD|HD 720|DivX|XviD|x264|x265)|')

    config_acronyms = []

    if args.remove_langs and config != None:
        config_acronyms.extend(config['lang.codes'])
        config_acronyms.extend(config['lang.descs'])

    if args.remove_noise and config != None:
        config_acronyms.extend(config['extra.acronyms'])

    if len(config_acronyms) > 0:
        acronyms += r'\b(' + '|'.join(config_acronyms) + r')\b'

    return acronyms + r'(?:(?=)|$)'


def normalize(filename, acronyms_re, remove_noise):
    basename, ext = itemgetter(0,1)(os.path.splitext(filename))
    
    # Turn dots to spaces
    basename = re.sub(r'[.]', ' ', basename)
    # Remove text in parenthesis
    basename = re.sub(r'(\().+?(\))', '', basename)
    basename = re.sub(r'(\[).+?(\])', '', basename)
    # Remove acronyms
    basename = acronyms_re.sub('', basename)
     # Remove noise
    if remove_noise:
        # Remove chars repeated more than 3 times
        basename = re.sub(r'(.)\1{3,}', '', basename)
        # Remove beginning and trailing dashes 
        basename = re.sub(r'^(-)|(-)$', '', basename)
        # Remove underscores
        basename = basename.replace('_', '')
    # Remove exceeding spaces
    basename = ' '.join(basename.split())

    return f'{basename}{ext}'


def init_config():
    try:
        if not os.path.exists(config_name):
            print(f'{script_name}: Configuration file not found. Downloading...\n')
            urllib.request.urlretrieve(config_url, os.path.join('.', config_name))
    except:
        die('Can\'t download configuration file')    


def load_config():
    try:
        return json.loads(open(config_name).read())
    except:
        return None


def shorten(filename):
    if len(filename) >= 30:
        return f'{filename[:15]}...{filename[len(filename)-15:]}'
    return filename


def print_preview(normalized):
    preview = normalized[:10]
    total = len(normalized) 

    if len(normalized) > 10:
        print(f'Operations on first 10 files on a total of {total}:')

    for oldname, newname in preview:
        print(f'{shorten(oldname)} -> {newname}')

    if len(preview) > 0:
        print('')
        print(f'Hit \'e\' to edit the list.')


def print_failed(failed):
    print('\n')
    print(f'{script_name}: impossible to rename the following file(s):')
    for f in failed:
        print(f)


def die(message):
    print(f'{script_name}: {message}')
    sys.exit(1)


def dump_scheme(rename_scheme):
    temp_name =  os.path.join('.', next(_get_candidate_names()))
    try:
        names = [f'{new_name}\n' for _, new_name in rename_scheme]
        help_text = f'\n# Adjust filenames and/or comment the ones to exclude.\n' + \
            '# Use \'#\' character to comment a filename.\n' + \
            '# Please don\'t change the order or remove any line.\n'
        with open(temp_name, 'w') as temp_file:
            temp_file.writelines(names)
            temp_file.write(help_text)
        return temp_name
    except:
        return None


def load_scheme(temp_name, rename_scheme):
    try:
        with open(temp_name, 'r') as temp_file:
            names = temp_file.readlines()
        names = [l[:-1] for l in names if len(l.strip()) > 0]
        # Strip 3 lines of built-in trailing comments
        names = names[:-3]
        if len(names) != len(rename_scheme):
            return None
        new_scheme = []
        for i, (old_name, _) in enumerate(rename_scheme):
            if names[i][:1] != '#':
                new_scheme.append((old_name, names[i]))
        return new_scheme
    except:
        return None


def confirm(target_dir, rename_scheme):
    global temp_scheme
    file_count = len(rename_scheme)
    what_to_rename = f'all {file_count} files' if file_count > 1 else 'the file'

    proceed = input(f'{script_name}: sure you want to rename {what_to_rename} in {target_dir} [yne]?')

    if len(proceed) == 1 and proceed == 'y':
        return True
    elif len(proceed) == 1 and proceed == 'e':
        temp_file = dump_scheme(rename_scheme)
        if (temp_file == None):
            die('Can\'t create the temporary file.')
        completed = run([shell_editor(), temp_file])
        if completed.returncode != 0:
            die('Can\'t start the shell text editor.')
        temp_scheme = temp_file
        return True
    elif len(proceed) == 1 and (proceed == 'n' or proceed == 'q'):
        return False

    return confirm(target_dir, rename_scheme)


def is_hidden(filepath):
    return os.path.basename(filepath)[:1] == '.'


def is_subtitle(filepath):
    ext = os.path.splitext(filepath)[1][1:]
    return ext.lower() in ['srt', 'ssa', 'ttml', 'sbv', 'dfxp', 'vtt', 'cap', 'mcc', 'sami', 'stl', 'qt.txt']


def try_rename(oldname, newname):
    try:
        os.rename(oldname, newname)
        return True
    except:
        return False


def remove_temp_scheme():
    try:
        os.remove(temp_scheme)
    except:
        pass


def exit_and_hints(target_dir, args):
    message = f'{script_name}: {target_dir}: contains no filenames to normalize\n' + \
        'Try to edit \'extra.acronyms\' in {script_name}.json.'
    if not args.remove_langs:
        message += '\nPlease try with --remove-langs option.'
    if not args.remove_noise:
        message += '\nPlease try with --remove-noise option.'
    die(message)


def is_a_tty():
    # Ripped from: https://github.com/django/django/blob/master/django/core/management/color.py#L12

    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or 'ANSICON' in os.environ)

    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    return supported_platform and is_a_tty


def shell_editor():
    if sys.platform == 'win32':
        return "Notepad"
    else:
        return os.environ['VISUAL'] if 'VISUAL' in os.environ else "nano"


def progress_anim():
    return [10251, 10265, 10266, 10259] if is_a_tty() else [124, 47, 45, 92]  


def update_progess(actual, step, perc_text, anim_frame):
    completed = round(actual + step)
    completed = 32 if completed > 32 else completed
    full = chr(9617) * completed if is_a_tty() else \
        '#' * completed
    empty = ' ' * (32 - completed)
    bar = f'     {chr(11816)}{full}{empty}{chr(11817)} ' \
        if is_a_tty() else \
            f'     ({full}{empty}) '
    print(f'{bar} {anim_frame} ', perc_text, end="\r", flush=True)


def main():
    atexit.register(remove_temp_scheme)
    init_config()

    version_string = f'{module_name}\n' + \
                     f'Version: {__version__}\n' + \
                     f'Python:  {python_version()}'

    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description=f'{module_name} (Version {__version__})')
    parser.add_argument('--version',
                        action='version',  version=version_string,
                        help='display version information')
    parser.add_argument('--force', '-f',
                        action='store_true',  dest='force', default=False,
                        help='attempt to rename the files without prompting for confirmation')
    parser.add_argument('--skip-subtitle', '-s',
                        action='store_true',  dest='skip_subtitle', default=False,
                        help='skip files with common subtitle extensions')
    parser.add_argument('--remove-langs', '-l',
                        action='store_true',  dest='remove_langs', default=False,
                        help='remove language codes from filename')
    parser.add_argument('--remove-noise', '-n',
                        action='store_true', dest='remove_noise', default=False,
                        help='remove excess chars repetition')
    parser.add_argument('directory',
                        nargs='?', metavar='DIRECTORY',
                        action='store',
                        help='directory containg the files to rename')

    args = parser.parse_args()

    target_dir = os.path.realpath(args.directory if args.directory != None else '.')
    if not os.path.exists(target_dir):
        die(f'{target_dir}: no such file or directory')

    # Filter files excluding directories
    files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
    if len(files) == 0:
        die(f'{target_dir}: contains no files')

    # Skip subtitle files if requested
    if args.skip_subtitle:
        files = [f for f in files if not is_subtitle(f)]

    # Normalize excluding hidden files
    acronyms_re = re.compile(get_acronyms_re(args, load_config()), re.IGNORECASE)
    normalized = [(f, normalize(f, acronyms_re, args.remove_noise)) \
                    for f in files if not is_hidden(os.path.join(target_dir, f))]

    # Remove files that don't need rename
    normalized = [(oldname, newname) for oldname, newname in normalized if oldname != newname]

    file_count = len(normalized)
    if file_count == 0:
        exit_and_hints(target_dir, args)

    proceed = True
    if not args.force:
        print_preview(normalized)
        proceed = confirm(target_dir, normalized)

    if proceed:
        if temp_scheme != None:
            normalized = load_scheme(temp_scheme, normalized) 
            if len(normalized) == 0:
                die("Nothing done")

        print(f'Renaming into \'{target_dir}\'...')
 
        completed = 0
        step_perc = 32 / file_count
        failed = []
        anim = progress_anim()
        frame = 0

        update_progess(0, step_perc, f'0%/{file_count}', chr(anim[frame]))
        for n, (oldname, newname) in enumerate(normalized):
            time.sleep(0.1)
            if not try_rename(os.path.join(target_dir, oldname), os.path.join(target_dir, newname)):
                failed.append(oldname)

            completed += step_perc
            frame += 1
            frame = 0 if frame == 4 else frame
            update_progess(completed, step_perc, f'{int(completed)}% {n + 1}/{file_count}', chr(anim[frame]))     

        update_progess(100, step_perc, f'100% {n + 1}/{file_count}, done.', chr(anim[frame]))
        print('')

        if len(failed) > 0:
            print_failed(failed)


if __name__ == '__main__':
    main()