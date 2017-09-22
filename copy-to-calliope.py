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
    for dirname, _, filenames in walk(root_path):
        for filename in filenames:
            filepath = path.join(dirname, filename)
            if re.match(filepattern, filepath, re.IGNORECASE):
                MINI_PROJECTS.append(filename)
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


def _copy_to_calliope(filename):
    filename = path.abspath(filename)
    print('copying file \'{}\' to calliope mini...'.format(filename))
    target_dir = None
    target_candidates = [
        '/' + path.join('media', 'MINI'),
        '/' + path.join('media', getpass.getuser(), 'MINI')
    ]
    for target_candidate in target_candidates:
        print('testing path {}'.format(target_candidate))
        if path.exists(target_candidate):
            target_dir = path.abspath(target_candidate)
            print('path {} available'.format(target_dir))
            break
    if not target_dir:
        print('calliope appears to be not present.')
        sys.exit(1)
    copyfile(filename, path.join(target_dir, path.basename(filename)))

    # if [ -d /media/$( whoami )/MINI ]
    # then
    # 	minidir="/media/$( whoami )/MINI"
    # elif [ -d /media/MINI ]
    # then
    # 	minidir="/media/MINI"
    # fi


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
