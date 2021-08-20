#!/usr/bin/python
import os

path='/srv/media/radio'
files = []
extensions = ('.m4a','.mp3')

def listfiles(path,extensions):
    flist = []
    for f in os.listdir(path):
        fpath = os.path.join(path,f)
        if os.path.isfile(fpath) and fpath.endswith(extensions):
            flist.append(fpath)
        if os.path.isdir(fpath):
            flist = flist + listfiles(fpath,extensions)
    return flist

