import sys
import os
from subprocess import run

import shell
import storage


script_name = os.path.basename(__file__)


def print_preview(normalized):
    preview = normalized[:10]
    total = len(normalized) 

    if len(normalized) > 10:
        print(f'Operations on first 10 files on a total of {total}:')

    for oldname, newname in preview:
        print(f'{_shorten(oldname)} -> {newname}')

    if len(preview) > 0:
        print('')
        print(f'Hit \'e\' to edit the list.')


def print_failed(failed):
    print('\n')
    print(f'{script_name}: impossible to rename the following file(s):')
    for f in failed:
        print(f)


def confirm(target_dir, rename_scheme):
    file_count = len(rename_scheme)
    what_to_rename = f'all {file_count} files' if file_count > 1 else 'the file'

    proceed = input(f'{script_name}: sure you want to rename {what_to_rename} in {target_dir} [yne]?')

    if len(proceed) == 1 and proceed == 'y':
        return (True, None)
    elif len(proceed) == 1 and proceed == 'e':
        temp_file = storage.dump_scheme(rename_scheme)
        if (temp_file == None):
            die('Can\'t create the temporary file.')
        completed = run([shell.editor(), temp_file])
        if completed.returncode != 0:
            die('Can\'t start the shell text editor.')
        return (True, temp_file)
    elif len(proceed) == 1 and (proceed == 'n' or proceed == 'q'):
        return (False, None)

    return confirm(target_dir, rename_scheme)


def shell_editor():
    if sys.platform == 'win32':
        return "Notepad"
    else:
        return os.environ['VISUAL'] if 'VISUAL' in os.environ else "nano"


def list_dir(path):
    print(f'Files in {path}:')
    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)
        if os.path.isfile(entry_path) and not shell.is_hidden(entry_path):
            print(f'  {entry}')


def progress_anim():
    return [10251, 10265, 10266, 10259] if shell.is_a_tty() else [124, 47, 45, 92]  


def update_progess(actual, step, perc_text, anim_frame):
    completed = round(actual + step)
    completed = 32 if completed > 32 else completed
    full = chr(9617) * completed if shell.is_a_tty() else \
        '#' * completed
    empty = ' ' * (32 - completed)
    bar = f'     {chr(11816)}{full}{empty}{chr(11817)} ' \
        if shell.is_a_tty() else \
            f'     ({full}{empty}) '
    print(f'{bar} {anim_frame} ', perc_text, end="\r", flush=True)


def exit_and_hints(target_dir, args):
    message = f'{script_name}: {target_dir}: contains no filenames to normalize\n' + \
        'Try to edit \'extra.json\'.'
    if not args.remove_langs:
        message += '\nPlease try with --remove-langs option.'
    if not args.remove_noise:
        message += '\nPlease try with --remove-noise option.'
    die(message)


def die(message):
    print(f'{script_name}: {message}')
    sys.exit(1)


def _shorten(filename):
    if len(filename) >= 30:
        return f'{filename[:15]}...{filename[len(filename)-15:]}'
    return filename