#!~/.virtualenvs/tt/bin/python

import os
from subprocess import call, STDOUT, Popen, PIPE

class pip_local_install:
    def __init__(self, pac_path = os.curdir, pip = None):
        self.pac_path = pac_path
        if pip is None:
            try:
                which_pip = Popen('which pip', shell=True, stdout=PIPE)
                self.pip = which_pip.stdout.read()
            except OSError as e:
                print (e)
                self.pip = 'pip'
        else:
            self.pip = pip

    def list_files(self):
        for Dir, SubDir, Files in os.walk(self.pac_path):
            return Files

    def package_install(self, lf = None):
        early_list = []
        if lf is None:
            lf = self.list_files()
        print (lf)
        for pac in lf:
            if pac.endswith('whl') or pac.endswith('gz'):
                try:
                    res = call('{} install {}'.format(self.pip, pac), shell=True)
                    print ('res = ', res)
                except OSError as e:
                    print ('OSError = ',e)
                if res != 0:
                    early_list.append(pac)
            else:
                pass
        if not len(early_list) == 0:
            print (early_list)
            self.package_install(early_list)

    def __repr__(self):
        return '{} default pip'.format(self.pip_path)

if __name__=='__main__':
    fe = pip_local_install(pip = '~/.virtualenvs/ty/bin/pip')
    fe.package_install()

