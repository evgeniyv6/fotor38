#!/usr/bin/env python

import sys, os
import timeit
#import ConfParser

def findMaxF(sizeMb,path='/opt/dis', getFolder = False):
    '''Using:   u need specify first parameter path  ('/tmp', for example)
                if set the second parameter <getFolder> to True, u get folder size
    '''
    visited={}
    allsizes=[]
    folderSize = 0
    kb = 1024
    mb = float(kb**2)
    gb = float(kb**3)
    for (dir, subdir, files) in os.walk(path):
        normPath = os.path.normpath(dir)
        normCase = os.path.normcase(dir)
        if normCase in visited: continue
        else:
            visited[normCase] = True
            for file in files:
                filePath = os.path.join(normPath,file)
                try:
                    fileSize = os.path.getsize(filePath)
                    if getFolder:
                        folderSize+=fileSize
                    if fileSize > int(sizeMb)*mb:
                        mbFileSize = fileSize/mb
                        allsizes.append(("{0:.2f}".format(mbFileSize),'MegaBytes', filePath))
                except os.error:
                    print ('Skip bad file...',filePath, sys.exc_info()[0])

    if getFolder is True:
        mbFolderSize = "{:.2f}".format(folderSize/mb)
        return mbFolderSize
    else:
        allsizes.sort()
        return allsizes

if __name__=='__main__':
    import pprint
    import subprocess, socket
    hostname = socket.gethostname()

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-s', '--size', dest='size', default=500, help='SIZE', metavar='SIZE')
    parser.add_option('-p', '--path', dest='path', default='/tmp', help='PATH', metavar='PATH')
    parser.add_option('-f','--folder', dest='folder', default=True, help='Folder size',metavar='FOLDER')
    (opts,args)=parser.parse_args()
    sz = opts.size
    op = opts.path
    of = opts.folder

    chkTime = timeit.Timer('pprint.pprint(findMaxF(sz,op,of))', 'from __main__ import findMaxF,sz,op,of,pprint')
    print ("Execution time {:.2f} seconds".format(chkTime.timeit(number=1)))


