# normalize-fn

Makes filenames downloaded from sharing services more readable.

[![asciicast](https://asciinema.org/a/286197.svg)](https://asciinema.org/a/286197)

## Install
```sh
# clone the repository
$ git clone https://github.com/gsscoder/normalize-fn.git

# change the working directory
$ cd normalize-fn

# verify if it runs
$ python3 normalizefn.py --version
```

## Usage
```
$ python3 normalizefn.py --help
usage: normalizefn.py [-h] [--version] [--force] [--skip-subtitle]
                      [--remove-langs] [--remove-noise] [--list-dir]
                      [DIRECTORY]

normalizefn.py: Normalizes filenames downloaded from sharing services (Version 0.2.0)

positional arguments:
  DIRECTORY            directory containg the files to rename

optional arguments:
  -h, --help           show this help message and exit
  --version            display version information
  --force, -f          attempt to rename files without prompting for
                       confirmation
  --skip-subtitle, -s  skip files with common subtitle extensions
  --remove-langs, -l   remove language codes from filename
  --remove-noise, -n   remove excess chars repetition
  --list-dir, -d       list directory of renamed files

$ python3 normalize-fn.py -sl /somewhere/your/movies/scif-fi
[DVDRip] Star W...) Episode I.avi -> Star Wars Episode I.avi
HD BluRay Star W...Episode II.avi -> Star Wars Episode II.avi
(PERFECT) Alien ... 254] AAC3.mkv -> Alien VS Predator.mkv

Hit 'e' to edit the list.
normalizefn.py: sure you want to rename all 3 files in /somewhere/your/movies/scif-fi [yne]?y
Renaming into '/somewhere/your/movies/scif-fi'...
Renaming files 100% 3/3, done.
```

## Editor
When you're prompted to proceed you could choose to review file names for customizations, hitting **E key**. When running on Windows the editor used is always **Notepad**. In ***nix** systems is the shell one, configured using `VISUAL` environment variable.

### Disclaimer
- You should not download any kind of media illegally.