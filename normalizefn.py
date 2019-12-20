from argparse import ArgumentParser, RawDescriptionHelpFormatter
from platform import python_version
from operator import itemgetter
import os
import re
import time
import atexit

from scheme import load_scheme, \
                   remove_scheme
from acronyms import build_re
from common import die
from ui import progress_anim, \
               update_progess, \
               confirm, \
               print_preview, \
               print_failed, \
               list_dir, \
               exit_and_hints
from shell import try_rename, \
                  is_hidden, \
                  is_subtitle


MODULE_NAME = '%(prog)s: Normalizes filenames downloaded from sharing services'
__version__ = '0.6.0'


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

    return '{}{}'.format(basename, ext)


def main():
    version_string = ('{}\n'
                      'Version: {}\n'
                      'Python:  {}').format(MODULE_NAME, __version__, python_version())

    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description='{} (Version {})'.format(MODULE_NAME, __version__))
    parser.add_argument('--version',
                        action='version',  version=version_string,
                        help='display version information')
    parser.add_argument('--force', '-f',
                        action='store_true',  dest='force', default=False,
                        help='attempt to rename files without prompting for confirmation')
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
        die('{}: No such file or directory'.format(target_dir))

    # Filter files excluding directories
    files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
    if not files:
        die('{}: Contains no files'.format(target_dir))

    # Skip subtitle files if requested
    if args.skip_subtitle:
        files = [f for f in files if not is_subtitle(f)]

    # Normalize excluding hidden files
    acronyms_re = re.compile(build_re(args), re.IGNORECASE)
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
        proceed, temp_scheme = confirm(target_dir, normalized)
        if temp_scheme:
            atexit.register(lambda : remove_scheme(temp_scheme))

    if proceed:
        if temp_scheme:
            normalized = load_scheme(temp_scheme, normalized) 
            if not normalized:
                die("Nothing done")

        print('Renaming into \'{}\'...'.format(target_dir))
 
        completed = 0
        step_perc = 32 / file_count
        failed = []
        anim = progress_anim()
        frame = 0

        update_progess(0, step_perc, '0% 0/{}'.format(file_count), chr(anim[frame]))
        for n, (oldname, newname) in enumerate(normalized):
            time.sleep(0.1)
            if not try_rename(os.path.join(target_dir, oldname), os.path.join(target_dir, newname)):
                failed.append(oldname)

            completed += step_perc
            frame += 1
            frame = 0 if frame == 4 else frame
            update_progess(completed, step_perc, '{}% {}/{}'.format(int(completed), n + 1, file_count), chr(anim[frame]))     

        update_progess(100, step_perc, '100% {}/{}, done.'.format(n + 1, file_count), chr(anim[frame]))
        print('')

        if failed:
            print_failed(failed)

        if args.list_dir:
            list_dir(target_dir)


if __name__ == '__main__':
    main()