#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket,sys,re

def chk_web(adr,port = 80,resourse = 'index.html'):
    if not resourse.startswith('/'):
        resourse = '/' + resourse
    req_str = 'GET {} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(resourse,adr)

    print ('HTTP request')
    print ('|||{}|||'.format(req_str))


    s = socket.socket()
    print ('Attempting to connect {} on port {:>10d}'.format(adr,port))
    try:
        s.connect((adr,port))
        print ('Connected to {} on port {:>10d}'.format(adr,port))
        s.send(req_str)
        rsp = s.recv(100)
        print ('Receieved 100bytes of HTTP req from webserver')
        print ('|||{}|||'.format(rsp))
    except socket.error,e:
        print ('Connection to {} on port {} failed: {}'.format(adr,port,e))
        return False
    finally:
        s.close()
    lines = rsp.splitlines()
    print ('1st line of HTTP response: {}'.format(lines[0]))
    try:
        ver, stat, msg = re.split(r'\s+',lines[0],2)
        print ('Version: {}, status: {}, message: {}'.format(ver, stat, msg))
    except ValueError:
        print ('Failed to split status line')
        return False
    if stat in ['200']:
        print ('Success - status was {}'.format(stat))
        return True
    else:
        print ('Status was {}'.format(stat))
        return False

if __name__=='__main__':
    chk_web('somehost.ru',80,'index.html')