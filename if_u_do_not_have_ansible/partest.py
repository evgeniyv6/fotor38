#!/usr/bin/env python

import os
import sys
import logging
from datetime import datetime
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
from parconnect import ParamikoSSH
from diffcolors import PrintColor

CONFIG = configparser.ConfigParser()
CONFIG_FILE = os.path.dirname(__file__)+ '/' +'parsettings.ini'
try:
    CONFIG.read(CONFIG_FILE)
except IOError as configerr:
    PrintColor.fail('Error reading config file. Exit 1.', configerr)
    sys.exit(1)
else:
    try:
        log_mask = CONFIG.get('GLOBAL', 'log_mask')
        paramiko_log_path = CONFIG.get('GLOBAL', 'paramiko_log_path')
        paramiko_log_ext = CONFIG.get('GLOBAL', 'paramiko_log_ext')
    except IOError as getconfigerr:
        PrintColor.fail('Get parameter from config file error. Exit 1.')
        sys.exit(1)
    except configparser.NoSectionError as nserr:
        PrintColor.fail('No sections error ', nserr)
        sys.exit(1)

LOG_DATE_TIME = datetime.strftime(datetime.now(), log_mask)
PARAMIKO_LOG_FILE = os.path.dirname(__file__) + paramiko_log_path + LOG_DATE_TIME + paramiko_log_ext
try:
    with open(PARAMIKO_LOG_FILE, 'a') as lf: paramiko_log = True
except IOError as logioerr:
    paramiko_log = False

try:
    py_getusrhome = CONFIG.get('SHELL_CMD', 'py_getusrhome')
except IOError as getconfigerr:
    print('Get parameter from config file error. Exit 1.', getconfigerr)
    sys.exit(1)

def testWorker(host):
    '''
    :param host:
    :user_name ALL=(ALL) NOPASSWD:ALL in /etc/sudoers
    '''
    if len(sys.argv) < 0:
        print('Usage: ' + sys.argv[0] + ' user private_key passphrase superuser')
        print('Exit 0.')
        sys.exit(0)
    else:
        user = sys.argv[1]
        private_key = sys.argv[2]
        passphrase = sys.argv[3]
        superuser = sys.argv[4]
    PrintColor.blue('STEP_1. Connect to the host.')
    myssh = ParamikoSSH(host, user, sshPrivateKey = private_key, passphrase = passphrase)
    PrintColor.blue('STEP_2. Get user $HOME: ', myssh.execWorker(py_getusrhome))
    PrintColor.blue('STEP_3. Get sudo user $HOME: ', myssh.execWorker(py_getusrhome, sudo = True, sudouser = superuser))
    PrintColor.blue('STEP_4.FTP put futur.py to the remote host.')
    myssh.ftpWorker('/tmp/sample.txt', 'sample.txt', 'put')
    PrintColor.blue('STEP_5. Add +x to exec scripts.')
    myssh.execWorker('chmod +x /tmp/sample.txt')
    PrintColor.blue('STEP_6. Run copied script under sudo user.')

if __name__=='__main__':
    import time
    start_time = time.time()
    hosts = ['<ip or hostname 1>','<ip or hostname 2>','<ip or hostname 3>']

# multiprocessing section
#     import multiprocessing
#     procs=[]
#     for index, num in enumerate(hosts):
#         proc = multiprocessing.Process(target=testWorker, args=(num,))
#         print(index, multiprocessing.current_process().name)
#         procs.append(proc)
#         proc.start()
#     for pr in procs:
#         proc.join()

# threading section
    import threading
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s (%(threadName)-8s) %(message)s'
    )
    def worker():
        logging.info('sleep')
        time.sleep(1)
        logging.info('stop sleep')
    for h in range(2):
        t = threading.Thread(target=testWorker, args=(h,), daemon=True)
        t.start()
    main_thread = threading.main_thread()
    for t in threading.enumerate():
        if t is main_thread: continue
        logging.info('joining - %s', t.getName())
        t.join()

# get elapsed time
    elapsed_time = time.time() - start_time
    msg = 'Elapsed time: {:<3}'.format(str(elapsed_time))
    PrintColor.bold(msg)




