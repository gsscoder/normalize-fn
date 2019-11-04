# normalize-fn

Makes filenames downloaded from sharing services more readable.

## Install
```sh
$ wget https://raw.githubusercontent.com/gsscoder/normalize-fn/master/normalize-fn.py
```

## Usage
```sh
$ python3 normalize-fn.py --help
usage: normalize-fn.py [-h] [--version] [--force] [--skip-subtitle]
                       [--remove-langs]
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

$ python3 normalize-fn.py -sl /Users/you/movies/scif-fi
[DVDRip] Star W...) Episode I.avi -> Star Wars Episode I.avi
HD BluRay Star W...Episode II.avi -> Star Wars Episode II.avi
(PERFECT) Alien ... 254] AAC3.mkv -> Alien VS Predator.mkv

normalize-fn.py: sure you want to rename all 3 files in /Users/you/movies/scif-fi [yn]?y
Renaming into '/Users/you/movies/scif-fi'...
Renaming files 100% 3/3, done.
```

### Disclaimer
- You should not download any kind of media illegally.

### Notes
- This script is thought for making certain filenames more readable. May save you a lot of time, but for now doesn't do miracles!