#!/usr/bin/env python

import sys
import os

ANSIBLE_DIR_TREE_FULL=['defaults','files','handlers','meta','tasks','templates','tests','vars']
ANSIBLE_FILES_TREE=[]
ANSIBLE_DIR_TREE_SHORT=['defaults','files','tasks','templates','vars']

 

def createSampleYml(path=None):
    if path is None:
        print('U should specify path')
        sys.exit(0)
#     with open(path.replace('\\','/').rsplit('/',1)[0]+'/site.yml','w') as siteyml:
#         siteyml.write('''---
# # example for testrole
# #- hosts: all
# #  gather_facts: False
# #  vars:
# #    ansible_user: "{{ user }}"
# #    ansible_password: "{{ pass }}"
# #  roles:
# #      - '''+path.replace('\\','/').split('/')[-1])
    for root, subdir, files in os.walk(path):
        for dir in subdir:
            if dir == 'defaults':
                with open(path+'/defaults/main.yml','w') as defaultmainyml:
                    defaultmainyml.write('''---
# defaults file for testrole''')
            if dir =='tasks':
                with open(path + '/tasks/main.yml', 'w') as tasksmainyml:
                    tasksmainyml.write('''---
# tasks file for testrole
#- name: uname test
#  shell: "uname -a"''')
            if dir == 'vars':
                with open(path + '/vars/main.yml', 'w') as varsmainyml:
                    varsmainyml.write('''---
# vars file for testrole''')

def createAnsibleTree(path=None, rolename='test_role', mode=None):
    if not os.name=='nt':
        dirname = '{}'.format(path) + '/' + rolename
    else:
        dirname = r'{}'.format(path)+'\\'+rolename
    if mode is None:
        anslist=ANSIBLE_DIR_TREE_SHORT
    elif mode=='long':
        anslist=ANSIBLE_DIR_TREE_FULL
    else:
        print('No such mode')
        sys.exit(0)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        print('Directory {} was created'.format(dirname))
       print('Start to create ansible tree...')
        for item in anslist:
            os.makedirs(dirname+'/'+item)
        print('Done.')
    else:
        print('Directory {} already exists'.format(dirname))
    createSampleYml(dirname)

def main():
   if len(sys.argv)<3:
        print('ERROR with parameters. Usage of {} {} {} {}'.format(sys.argv[0],'<directory for role>','<role name>',r'<optional - "long" - parameter for full ansible folders tree>'))
        sys.exit(0)
    if len(sys.argv)==3:
        createAnsibleTree(sys.argv[1],sys.argv[2])
    elif len(sys.argv)==4:
        createAnsibleTree(sys.argv[1],sys.argv[2],sys.argv[3])

if __name__=='__main__':
    main()