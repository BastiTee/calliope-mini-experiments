#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A Python3 script to copy a HEX-file to the calliope."""

from os import path, walk, chdir
import re
import sys
import readline
import getpass
from shutil import copyfile

MINI_PROJECTS = []
PROJECTS_DIR = 'projects'


def _find_mini_projects(root_path, filepattern):
    for dirname, _, src_files in walk(root_path):
        for src_file in src_files:
            filepath = path.join(dirname, src_file)
            if re.match(filepattern, filepath, re.IGNORECASE):
                MINI_PROJECTS.append(src_file)
    return MINI_PROJECTS


def _change_to_scriptdir():
    chdir(path.dirname(path.abspath(__file__)))


def _completer(prefix, index):
    # print('|{}|'.format(prefix))
    options = [x for x in MINI_PROJECTS if x.startswith(prefix)]
    try:
        return options[index]
    except IndexError:
        return None


def _copy_to_calliope(src_file):
    src_file = path.abspath(src_file)
    print('[INFILE] {}'.format(src_file))
    target_dir = None
    target_candidates = [
        '/' + path.join('media', 'MINI'),
        '/' + path.join('media', getpass.getuser(), 'MINI'),
        '/' + path.join('media', 'MINI1'),
        '/' + path.join('media', getpass.getuser(), 'MINI1')
    ]
    for target_candidate in target_candidates:
        if path.exists(target_candidate):
            target_dir = path.abspath(target_candidate)
            target_file = path.join(target_dir, path.basename(src_file))
            calliope = re.sub('.*/', '', target_candidate)
            print('[{}] {}'.format(calliope, path.basename(target_file)))
            copyfile(src_file, target_file)

    if not target_dir:
        print('calliope appears to be not present.')
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        _copy_to_calliope(sys.argv[1])
        sys.exit(0)

    print('         _ _ _                   _     _ ')
    print(' ___ ___| | |_|___ ___ ___ _____|_|___|_|')
    print('|  _| .\'| | | | . | . | -_|     | |   | |')
    print('|___|__,|_|_|_|___|  _|___|_|_|_|_|_|_|_|')
    print('                  |_|                    ')

    try:
        _change_to_scriptdir()
        _find_mini_projects(PROJECTS_DIR, '.*\.hex')
        readline.set_completer(_completer)
        readline.set_completer_delims(' ')
        readline.parse_and_bind("tab: complete")
        while 1:
            iput = input('> ')
            iput = iput.strip()
            if iput not in MINI_PROJECTS:
                print('!!! Unknown mini project: {}'.format(iput))
            else:
                _copy_to_calliope(path.join(PROJECTS_DIR, iput))
                sys.exit(0)
    except KeyboardInterrupt:
        print()
        sys.exit(0)
