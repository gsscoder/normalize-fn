from __future__ import print_function
import sys
if sys.version_info.major == 2:
    from builtins import raw_input as input
import os

import shell
import scheme


SCRIPT_NAME = 'normalizefn.py'


def print_preview(normalized):
    preview = normalized[:10]
    total = len(normalized) 

    if len(normalized) > 10:
        print('Operations on first 10 files on a total of {}:'.format(total))

    for oldname, newname in preview:
        print('{} -> {}'.format(_shorten(oldname), newname))

    if preview:
        print('')
        print('Hit \'e\' to edit the list.')


def print_failed(failed):
    print('\n')
    print('{}: impossible to rename the following file(s):'.format(SCRIPT_NAME))
    for f in failed:
        print(f)


def confirm(target_dir, rename_scheme):
    file_count = len(rename_scheme)
    what_to_rename = 'all {} files'.format(file_count) if file_count > 1 else 'the file'

    proceed = input(
        '{}: sure you want to rename {} in {} [yne]?'.format(SCRIPT_NAME, what_to_rename, target_dir))

    if len(proceed) == 1 and proceed == 'y':
        return (True, None)
    elif len(proceed) == 1 and proceed == 'e':
        temp_file = scheme.save(rename_scheme)
        if (not temp_file):
            die('Can\'t create the temporary file.')
        if not _open_editor(temp_file):
            die('Can\'t start the shell text editor.')
        return (True, temp_file)
    elif len(proceed) == 1 and (proceed == 'n' or proceed == 'q'):
        return (False, None)

    return confirm(target_dir, rename_scheme)


def shell_editor():
    if sys.platform == 'win32':
        return 'Notepad'
    else:
        return os.environ['VISUAL'] if 'VISUAL' in os.environ else 'nano'


def list_dir(path):
    print('Files in {}:'.format(path))
    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)
        if os.path.isfile(entry_path) and not shell.is_hidden(entry_path):
            print('  {}'.format(entry))


def progress_anim():
    return [10251, 10265, 10266, 10259] if _better_ui() else [124, 47, 45, 92]  


def update_progess(actual, step, perc_text, anim_frame):
    completed = int(round(actual + step))
    completed = 32 if completed > 32 else completed
    full = chr(9617) * completed if _better_ui() else \
        '#' * completed
    empty = ' ' * (32 - completed)
    bar = '     {}{}{}{} '.format(chr(11816), full, empty, chr(11817)) \
        if _better_ui() else \
            '     ({}{}) '.format(full, empty)
    print('{} {} {}'.format(bar, anim_frame, perc_text), end="\r")
    sys.stdout.flush()


def exit_and_hints(target_dir, args):
    message = ('{}: {}: Contains no filenames to normalize\n'
               'Try to edit \'extra.json\'.').format(SCRIPT_NAME, target_dir)
    if not args.remove_langs:
        message += '\nPlease try with --remove-langs option.'
    if not args.remove_noise:
        message += '\nPlease try with --remove-noise option.'
    die(message)


def die(message):
    print('{}: {}'.format(SCRIPT_NAME, message))
    sys.exit(1)


def _shorten(filename):
    if len(filename) >= 30:
        return '{}...{}'.format(filename[:15], filename[len(filename)-15:])
    return filename
    
def _better_ui():
    return shell.is_a_tty() and sys.version_info.major >= 3

def _open_editor(filename):
    if sys.version_info.major > 2:
        from subprocess import run
        return run([shell.editor(), filename]).returncode == 0
    from subprocess import call
    return call([shell.editor(), filename]) == 0