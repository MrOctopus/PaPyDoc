#!/usr/bin/env python

__author__ = "NeverLost"
__version__ = "1.0.0"

from argparse import ArgumentParser
from os import path
from glob import iglob
from itertools import chain

from common.defines import FILE_EXT
from common.exceptions import ParsingFailed
from papyrus.p_file import PapyDoc

def is_dir(string):
    if not path.isdir(string):
        raise NotADirectoryError(string)
    return string

def main():
    # Create arg_pargse
    arg_parser = ArgumentParser(prog = "PaPyDoc")
    arg_parser.add_argument("-o", dest = "output", help = "Output directory", type = is_dir)
    arg_parser.add_argument("path", help = "Path (Globa format)", type = str)

    # Parse
    args = arg_parser.parse_args()

    # Get files
    files = iglob(args.path, recursive = True)

    print(f"{arg_parser.prog}:")

    try:
        first_file = next(files)
    except StopIteration:
        print('File does not exist: ')

    for filename in chain([first_file], files):
        if not filename.lower().endswith(FILE_EXT):
            continue

        try:
            papy_doc = PapyDoc.from_file(filename)

            if args.output:
                papy_doc.create_md_at(args.output)
            else:
                papy_doc.create_md_at(path.dirname(filename))

            print(f"Generated markdown file for: {filename}")
        except ParsingFailed as e:
            print(f"Parsing failed ({e.error}) for: {filename}")

if __name__ == "__main__":
    main()