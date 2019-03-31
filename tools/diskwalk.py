#!/usr/bin/env python
import os
class diskwalk(object):
    def __init__(self,path):
        self.path=path

    def numpath(self):
        '''returns path way in catalog in list view'''
        path_col = []
        for dirpath, dirname, filename in os.walk(self.path):
            for file in filename:
                fullpath = os.path.join(dirpath, file)
                path_col.append(fullpath)
        return path_col

    def numfiles(self):
        '''returns all file names in list view'''
        file_col = []
        for dirpath, dirname, filename in os.walk(self.path):
            for file in filename:
                file_col.append(file)
        return file_col

    def numdir(self):
        '''returns all dir names in list view'''
        dir_col = []
        for dirpath, dirname, filename in os.walk(self.path):
            for dir in dirname:
                dir_col.append(dir)
        return dir_col

if __name__=='__main__':
    import os
    print (os.path.basename(__file__))
    path='/tmp'
    tmpdir = diskwalk(path)
    print (tmpdir.numpath())