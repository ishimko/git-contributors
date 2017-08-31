# Git Contributors

Super small and simple tool for generating contribution statistics for your git repositories. Includes merging users, produced by `git shortlog -n -e`, by emails and names to simplify statistics analysis.

## Requirements
- python 3
- `git` executable in your `PATH`

## Usage
```
usage: main.py [-h] [-z] [path]

positional arguments:
  path

optional arguments:
  -h, --help           show this help message and exit
  -z, --include-zeros  include contributors with zero contributions
```