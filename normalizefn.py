from argparse import ArgumentParser, RawDescriptionHelpFormatter
from platform import python_version
from operator import itemgetter
import sys
import os
import re
import time
import json
import atexit
import urllib.request

import acronyms
import ui
import shell
import storage


module_name = '%(prog)s: Normalizes filenames downloaded from sharing services'
__version__ = '0.2.0'

temp_scheme = None


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
        basename = re.sub(r'([^\s])\1{3,}', '', basename)
        # Remove beginning and trailing dashes 
        basename = re.sub(r'^(-)|(-)$', '', basename)
        # Remove underscores
        basename = basename.replace('_', '')
    # Remove exceeding spaces
    basename = ' '.join(basename.split())

    return f'{basename}{ext}'


def remove_temp_scheme():
    try:
        os.remove(temp_scheme)
    except:
        pass


def main():
    atexit.register(remove_temp_scheme)

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
    parser.add_argument('--list-dir', '-d',
                        action='store_true', dest='list_dir', default=False,
                        help='list directory of renamed files')
    parser.add_argument('directory',
                        nargs='?', metavar='DIRECTORY',
                        action='store',
                        help='directory containg the files to rename')

    args = parser.parse_args()

    target_dir = os.path.realpath(args.directory if args.directory != None else '.')
    if not os.path.exists(target_dir):
        ui.die(f'{target_dir}: No such file or directory')

    # Filter files excluding directories
    files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
    if len(files) == 0:
        ui.die(f'{target_dir}: Contains no files')

    # Skip subtitle files if requested
    if args.skip_subtitle:
        files = [f for f in files if not shell.is_subtitle(f)]

    # Normalize excluding hidden files
    acronyms_re = re.compile(acronyms.build_re(args), re.IGNORECASE)
    normalized = [(f, normalize(f, acronyms_re, args.remove_noise)) \
                    for f in files if not shell.is_hidden(os.path.join(target_dir, f))]

    # Remove files that don't need rename
    normalized = [(oldname, newname) for oldname, newname in normalized if oldname != newname]

    file_count = len(normalized)
    if file_count == 0:
        ui.exit_and_hints(target_dir, args)

    proceed = True
    if not args.force:
        ui.print_preview(normalized)
        proceed = ui.confirm(target_dir, normalized)

    if proceed:
        if temp_scheme != None:
            normalized = storage.load_scheme(temp_scheme, normalized) 
            if len(normalized) == 0:
                ui.die("Nothing done")

        print(f'Renaming into \'{target_dir}\'...')
 
        completed = 0
        step_perc = 32 / file_count
        failed = []
        anim = ui.progress_anim()
        frame = 0

        ui.update_progess(0, step_perc, f'0%/{file_count}', chr(anim[frame]))
        for n, (oldname, newname) in enumerate(normalized):
            time.sleep(0.1)
            if not shell.try_rename(os.path.join(target_dir, oldname), os.path.join(target_dir, newname)):
                failed.append(oldname)

            completed += step_perc
            frame += 1
            frame = 0 if frame == 4 else frame
            ui.update_progess(completed, step_perc, f'{int(completed)}% {n + 1}/{file_count}', chr(anim[frame]))     

        ui.update_progess(100, step_perc, f'100% {n + 1}/{file_count}, done.', chr(anim[frame]))
        print('')

        if len(failed) > 0:
            ui.print_failed(failed)

        if args.list_dir:
            ui.list_dir(target_dir)


if __name__ == '__main__':
    main()