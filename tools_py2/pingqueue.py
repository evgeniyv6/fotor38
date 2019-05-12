#!/usr/bin/env python

from checkweb import chk_web
from multiprocessing import Process, Queue, Pool
import time
import subprocess
import sys


q = Queue()
oq = Queue()
ips = ['192.168.2.25','192.168.2.27']
num = 10

class HostRec:
    def __init__(self, ip=None, port=80, req='index.html', webresp=None):
        self.ip = ip
        self.port = port
        self.req = req
        self.webresp = webresp
    def __repr__(self):
        return '[Host Record ("{}","{}","{}")]'.format(self.ip,self.port, self.webresp)


def f(i,q,oq):
    while True:
        time.sleep(.1)
        if q.empty():
            sys.exit()
            print ('Process #: {} Exit'.format(i))
        ip = q.get()
        print ('Process #: {}'.format(i))
        ret = subprocess.call('ping -c 1 {}'.format(ip), shell=True, stdout=open('/dev/null','w'), stderr=subprocess.STDOUT)
        if ret == 0:
            print ('{}: is alive'.format(ip))
            oq.put(ip)
        else:
            print ('Process #: {} did not find a response for for ip - {}'.format(i,ip))
            pass

def chkweb_q(i,out):
    while True:
        time.sleep(.1)
        if out.empty():
            sys.exit()
            print ('Process #:{}'.format(i))
        ipaddr = out.get()
        cw = HostRec()
        cw.ip = ipaddr
        cw.webresp = chk_web(ipaddr)
        print (cw)
        return cw

try:
    map(q.put,ips)
finally:
    for i in range(num):
        p = Process(target = f,args=[i,q,oq])
        p.start()
    for i in range(num):
        pp = Process(target=chkweb_q, args=[i,oq])
        pp.start()
print ('main process joins on queue')
p.join()

print ('Main program finished')


