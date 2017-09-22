#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A Python3 script to auto-deploy new calliope projects."""

from os import path, walk, chdir, stat, makedirs
import re
import sys
import subprocess
from time import sleep, time as t
import datetime as dt
from shutil import move

MINI_PROJECTS = []
PROJECTS_DIR = 'projects'
INTERVAL = 5


def _get_new_files(directory, seconds):
    new_files = []
    now = dt.datetime.now()
    ago = now - dt.timedelta(seconds=seconds)
    for root, dirs, files in walk(directory):
        for fname in files:
            pathstring = path.join(root, fname)
            st = stat(pathstring)
            mtime = dt.datetime.fromtimestamp(st.st_mtime)
            if mtime > ago:
                new_files.append(path.abspath(pathstring))
    return new_files


def _handle_files(input_file, target_dir):
    try:
        makedirs(target_dir)
    except FileExistsError:
        pass  # ignore
    i = 1
    now_filesave = dt.datetime.fromtimestamp(t()).strftime('%Y%m%d_%H%M%S')
    tfiles = []
    for ifile in input_file:
        bn = re.sub('^mini-', '', path.basename(ifile))
        bn = re.sub(' .*', '', bn)
        bn = re.sub('\.hex$', '', bn)
        tfile = path.join(target_dir, '{}-{}-{}.hex'.format(
            bn, now_filesave, i))
        print('[DL] {} [{}]\n[PROJECT] {}'.format(ifile, i, tfile))
        move(ifile, tfile)
        tfiles.append(tfile)
        i += 1
    return tfiles


def _deploy_file(file):
    print('>>> {}'.format(file))
    subprocess.Popen('./copy-to-calliope.py {}'.format(file), shell=True)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Path to watch folder not provided.')
        sys.exit(1)
    if not path.exists(sys.argv[1]):
        print('Path to watch folder does not exist.')
        sys.exit(1)
    wfolder = path.abspath(sys.argv[1])
    chdir(path.dirname(path.abspath(__file__)))
    target_dir = path.abspath('projects_new')
    print('-- watching folder {}'.format(wfolder))
    print('-- writing to {}'.format(target_dir))

    try:
        while 1:
            newf = _get_new_files(wfolder, INTERVAL)
            if len(newf) > 0:
                tfiles = _handle_files(newf, target_dir)
                if tfiles and len(tfiles) > 0:
                    _deploy_file(tfiles[0])
            sleep(INTERVAL)
    except KeyboardInterrupt:
        print()
        sys.exit(0)
