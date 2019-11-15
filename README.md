# normalize-fn

Makes filenames downloaded from sharing services more readable.

[![asciicast](https://asciinema.org/a/281509.svg)](https://asciinema.org/a/281509)

## Install
```sh
$ wget https://raw.githubusercontent.com/gsscoder/normalize-fn/master/normalize-fn.py
```

## Usage
```sh
$ python3 normalize-fn.py --help
usage: normalize-fn.py [-h] [--version] [--force] [--skip-subtitle]
                       [--remove-langs] [--remove-noise]
                       [DIRECTORY]

normalize-fn.py: Normalizes filenames downloaded from sharing services (Version 0.1.0)

positional arguments:
  DIRECTORY            directory containg the files to rename

optional arguments:
  -h, --help           show this help message and exit
  --version            display version information
  --force, -f          attempt to rename the files without prompting for
                       confirmation
  --skip-subtitle, -s  skip files with common subtitle extensions
  --remove-langs, -l   remove language codes from filename
  --remove-noise, -n   remove excess chars repetition

$ python3 normalize-fn.py -sl /somewhere/your/movies/scif-fi
[DVDRip] Star W...) Episode I.avi -> Star Wars Episode I.avi
HD BluRay Star W...Episode II.avi -> Star Wars Episode II.avi
(PERFECT) Alien ... 254] AAC3.mkv -> Alien VS Predator.mkv

Hit 'e' to edit the list.
normalize-fn.py: sure you want to rename all 3 files in /somewhere/your/movies/scif-fi [yne]?y
Renaming into '/somewhere/your/movies/scif-fi'...
Renaming files 100% 3/3, done.
```

## Editor
When you're prompted to proceed you could choose to review file names for customizations, hitting **E key**. When running on Windows the editor used is always **Notepad**. In ***nix** systems is the shell one, configured using `VISUAL` environment variable.

### Disclaimer
- You should not download any kind of media illegally.