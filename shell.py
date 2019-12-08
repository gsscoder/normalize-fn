import sys
import os


def try_rename(oldname, newname):
    try:
        os.rename(oldname, newname)
        return True
    except:
        return False


def is_hidden(filepath):
    return os.path.basename(filepath)[:1] == '.'


def is_subtitle(filepath):
    ext = os.path.splitext(filepath)[1][1:]
    return ext.lower() in [
        'srt', 'ssa', 'ttml', 'sbv', 'dfxp', 'vtt', 'cap', 'mcc',
        'sami', 'stl', 'qt.txt'
        ]


def is_a_tty():
    # Ripped from: https://github.com/django/django/blob/master/django/core/management/color.py#L12

    plat = sys.platform
    supported_platform = plat != 'Pocket PC' \
        and (plat != 'win32' or 'ANSICON' in os.environ)

    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    return supported_platform and is_a_tty


def editor():
    if sys.platform == 'win32':
        return "Notepad"
    else:
        return os.environ['VISUAL'] \
            if 'VISUAL' in os.environ else "nano"