#!/usr/bin/env python

__author__ = "NeverLost"
__version__ = "1.0.0"

import argparse
import glob
import itertools

from os import path
from papyrus.p_file import PapyDoc

FILE_EXT = '.psc'

def is_dir(string):
    if not path.isdir(string):
        raise NotADirectoryError(string)
    return string

def main():
    arg_parser = argparse.ArgumentParser(prog = "PaPyDoc")
    arg_parser.add_argument("-o", dest = "output", help = "Output path", type = is_dir)
    arg_parser.add_argument("path", help = "specifies the file path", type = str)

    args = arg_parser.parse_args()

    is_recursive = True if args.path.find('**') else False
    files = glob.iglob(args.path, recursive = is_recursive)

    print(arg_parser.prog + ':')

    try:
        first_file = next(files)
    except StopIteration:
        print('File does not exist: ')
    
    readFiles = 0

    for filename in itertools.chain([first_file], files):
        if not filename.lower().endswith(FILE_EXT):
            continue

        try:
            papy_doc = PapyDoc.from_file(filename)

            #if args.output:
            #    papy_doc.create_md_at(args.output)
            #else:
            #    papy_doc.create_md_at(path.dirname(filename))

            readFiles += 1
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()