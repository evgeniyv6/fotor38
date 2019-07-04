#!/usr/bin/env python

from jira import JIRA
import datetime
import sys,os
from xortool import XorFunc
import ConfigParser

logfile = os.path.dirname(__file__)+'/logfile.txt'
dt = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
configfile = os.path.dirname(__file__) + '/properties.ini'
ZIPFILESFOLDER = "/path/to/buffer"

class JiraRep:
    def __init__(self, server, login, password, project,files=None):
        self.server = server
        self.login = login
        self.password = password
        self.project = project
        if files is None:
            self.files=[]
        else:
            self.files=files
            
    def jiraconn(self):
        unxorpwd = XorFunc(self.password, key='some_secret', decode=True)
        try:
            jconn = JIRA(server=self.server, basic_auth=(self.login, unxorpwd))
            issue = jconn.issue(self.project)
        except:
            try:
                with open(logfile, 'a') as al:
                    al.write(dt + '\n')
                    al.write('Failed to connect to jira: \n')
                    sys.exit(1)
            except IOError as e:
                print ('Work with file')
        try:
            for file in self.files:
                jconn.add_attachment(issue, file) # os.path.dirname(__file__)+'/'+file)
        except e:
            try:
                with open(logfile, 'a') as al:
                    al.write(dt + '\n')
                    al.write('Failed to attach files: \n')
                    sys.exit(1)
            except IOError as e:
                print ('Work with file {} {}'.format(e.errno, e.strerror))


if __name__=='__main__':
    config = ConfigParser.ConfigParser()
    try:
        config.read(configfile)
    except Exception as err:
        try:
            with open(logfile, 'a') as al:
                al.write(dt + '\n')
                al.write('Error config file: {}\n'.format(err))
                sys.exit(1)
        except IOError as e:
            print ('Work with file {} {}'.format(e.errno, e.strerror))
    try:
        user = config.get('credentials', "user")
        pwd = config.get('credentials', "pwd")
        jsrv = config.get('credentials', "jiraserver")
    except Exception as err:
        try:
            with open(logfile, 'a') as al:
                al.write(dt + '\n')
                al.write('Error reading parameters from file: {} \n'.format(err))
                sys.exit(1)
        except IOError as e:
            print ('Work with file {} {}'.format(e.errno, e.strerror))
    repfls=['report.pdf']
    try:
        zipf = [os.path.join(ZIPFILESFOLDER,file) for file in os.listdir(ZIPFILESFOLDER) if file.endswith('zip')]
    except (FileNotFoundError, IOError):
        print('file or dir not found')
        zipf=[]
    jrep=JiraRep(jsrv,user,pwd,sys.argv[1],repfls+zipf)
    jrep.jiraconn()
