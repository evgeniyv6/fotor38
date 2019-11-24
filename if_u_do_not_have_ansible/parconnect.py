#!/usr/bin/env python

import sys
import logging
import paramiko
from diffcolors import PrintColor

SSH_TIMEOUT = 30.0
logging.getLogger('paramiko')

# decorator for the utf8 output
def utfdecoder(f):
    def utfwrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs).decode('utf-8')
        except:
            return f(*args, **kwargs)
    return utfwrapper

class ParamikoSSH:
    def __init__(self, host, user, password=None, sshPrivateKey = None, passphrase = None, port=22):
        self.host = host
        self.port = port
        self.user = user
        if sshPrivateKey is None and passphrase is None:
            if user is None and password is None:
                PrintColor.warning('You must specify ssh private key with passphrase or user with password. Exit 1.')
                sys.exit(1)
            else:
                self.password = password
        else:
            self.sshPrivateKey = sshPrivateKey
            self.passphrase = passphrase

    def _private_key_worker(self):
        logging.debug('Begin to load private key')
        try:
            rsakey = paramiko.RSAKey.from_private_key_file(filename = self.sshPrivateKey, password = self.passphrase)
            logging.debug(rsakey)
            return rsakey
        except paramiko.ssh_exception.SSHException as rsaer:
            logging.debug('Can\'t load RSA private key: ' + str(rsaer) + '. Trying to load DSS private key')
            try:
                dsskey = paramiko.DSSKey.from_private_key_file(filename = self.sshPrivateKey, password = self.passphrase)
                logging.debug(dsskey)
                return dsskey
            except paramiko.ssh_exception.SSHException as err:
                logging.debug('Can\'t load DSS private key. Exit 1')
                return

    def ftpWorker(self, remote_file, local_file, action):
        '''
        :param remote_file:
        :param local_file:
        :param method: get or put
        '''
        transport = paramiko.Transport((self.host, self.port))
        try:
            pkey = self._private_key_worker()
        except:
            pkey = False
        try:
            if pkey:
                transport.connect(username=self.user, pkey = pkey)
                PrintColor.green('Private Key FTP Connection to the host {} succeeded'.format(self.host))
            elif self.password:
                transport.connect(username=self.user, password=self.password)
                PrintColor.green('User/password FTP Connection to the host {} succeeded'.format(self.host))
            else:
                PrintColor.fail('Primary key is empty. Exit 1')
                sys.exit(1)
        except ConnectionError as connerr:
            PrintColor.fail('ConnectionError', connerr)
            PrintColor.fail('Host {}'.format(self.host))
        except paramiko.ssh_exception.SSHException as ssherr:
            PrintColor.fail('SSHError', ssherr)
            PrintColor.fail('Host {}'.format(self.host))
        except AttributeError as attrerr:
            PrintColor.fail('Attribute error', attrerr)
            PrintColor.fail('Host {}'.format(self.host))
        except paramiko.ssh_exception.AuthenticationException as autherr:
            PrintColor.fail('Auth error', autherr)
            PrintColor.fail('Host {}'.format(self.host))
        else:
            try:
                sftp = paramiko.SFTPClient.from_transport(transport)
                if action == 'get':
                    sftp.get(remote_file, local_file)
                    PrintColor.green('File successfully downloaded from host {}'.format(self.host), end=' ')
                elif action == 'put':
                    sftp.put(local_file, remote_file)
                    PrintColor.green('File successfully uploaded to the remote folder {} on the remote host'.format(remote_file,self.host))
            except:
                sftp.close()
        finally:
            transport.close()

    @utfdecoder
    def execWorker(self, cmd, sudo = False, sudouser = None,logfile = None, log_level = 'INFO'):
        '''
        :param cmd: command to execute on a remote host
        :param logfile: if absent - no logging
        :param log_level: default = INFO
        :param sudo: you need to specify sudouser if sudo=True. default = False
        :param sudouser: name
        :return: cmd shell output in utf-8
        '''
        if sudo:
            if sudouser is not None:
                cmd = 'sudo -u ' + sudouser + ' ' + cmd + '\n'
            else:
                PrintColor.fail('Sudo user name is absent. Exit 1.')
                sys.exit(1)
        if logfile is not None:
            paramiko.util.log_to_file(logfile, log_level)
        else:
            logging.debug('Paramiko logging to a file disabled')
        ssh = paramiko.client.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            pkey = self._private_key_worker()
        except:
            pkey=False
        try:
            if pkey:
                ssh.connect(hostname=self.host, pkey = pkey)
                PrintColor.green('Private Key SSH Connection to the host {} succeeded'.format(self.host))
            elif self.password:
                ssh.connect(hostname=self.host, username=self.user, password=self.password)
        except ConnectionError as connerr:
            PrintColor.fail('ConnectionError', connerr)
            PrintColor.fail('Host {}'.format(self.host))
        except paramiko.ssh_exception.SSHException as ssherr:
            PrintColor.fail('SSHError', ssherr)
            PrintColor.fail('Host {}'.format(self.host))
        except AttributeError as attrerr:
            PrintColor.fail('Attribute error', attrerr)
            PrintColor.fail('Host {}'.format(self.host))
        except paramiko.ssh_exception.AuthenticationException as autherr:
            PrintColor.fail('Auth error', autherr)
            PrintColor.fail('Host {}'.format(self.host))
        else:
            try:
                new_channel = ssh.get_transport().open_session()
                new_channel.settimeout(SSH_TIMEOUT)
                new_channel.get_pty()
                new_channel.exec_command(cmd)
                get_recv_bytes = new_channel.recv(2048)
                exit_status = new_channel.recv_exit_status()
                if exit_status == 0:
                    PrintColor.green('Remote command execution success.')
                    return get_recv_bytes
                else:
                    PrintColor.fail('Response code not ZERO.')
                    return get_recv_bytes
            except paramiko.ssh_exception.SSHException as ssherr:
                PrintColor.fail('Remote execute error', ssherr)
            except Exception as excerr:
                PrintColor.fail('ExecutionErr', excerr)
            finally:
                new_channel.close()
        finally:
            ssh.close()

if __name__=='__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s (%(message)-10s)',
    )
    host='<ip or hostname>'
    user='<username>'
    pk = '<key name>'
    pf='<passphrase>'
    myssh = ParamikoSSH(host, user, sshPrivateKey=pk, passphrase=pf)
    myssh.ftpWorker('/tmp/sample.txt', 'sample.txt', 'put')
    print(myssh.execWorker('uname -a'))

