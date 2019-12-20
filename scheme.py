import os
from tempfile import _get_candidate_names


def save_scheme(rename_scheme):
    temp_name =  os.path.join('.', next(_get_candidate_names()))
    
    try:
        names = ['{}\n'.format(new_name) for _, new_name in rename_scheme]
        help_text = ('\n# Adjust filenames and/or comment the ones to exclude.\n'
                     '# Use \'#\' character to comment a filename.\n'
                     '# Please don\'t change the order or remove any line.\n')
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


def remove_scheme(temp_scheme):
    try:
        os.remove(temp_scheme)
    except:
        pass