#!/usr/bin/env python

# did not work, prefer to use archive module with ansible
import os
import sys
from zipfile import ZipFile, ZIP_DEFLATED

def listf(path = '',mask = ''):
    return [os.path.join(path,file) for file in os.listdir(path) if file.startswith(mask) or file.endswith(mask)]

def zipfiles(zipfile, fileslist=None):
    if fileslist is None: sys.exit(0)
    else: flist=list(fileslist)
    with ZipFile(zipfile,'w',ZIP_DEFLATED) as zip:
        for i in flist:
            if os.path.getsize(i) > 0: zip.write(i)

if __name__=='__main__':
    zipfiles('diffzip.zip',listf("{{ diffolder }}",'diff'))
    zipfiles('logszip.zip',listf("{{ logfolder }}",'log'))
    print('END ZIP PY SCRIPT')
