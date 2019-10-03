#!/usr/bin/env python

neolog=[ 'login1@test.ru', 'login2@test.ru']

try:
    l=[]
    with open('login.txt','r') as f
    with open('loginresult.txt','w') as g
    g.write('HOST,GOOD,WARNING\n')
    line = f.readlines()
    for x in line:
        xspl=x.split()[0]
        xsrv=l.append(xspl)
    xset = set(l)
    d={}
    for g in xset:
        ov = []
        nv = []
        ne = []
        for y in line:
            ysplsrv = y.split()[0]
            ysplusr = y.split()[1]
            if ysplsrv==g:
                if ysplusr in neolog:
                    nv.append(ysplusr)
                else:
                    ov.append(ysplusr)
                d[ysplsrv]=dict([('nsupport',nv),('notnsupport',ov)])
except:
    print ('error')


with open('loginresult.txt','a') as g
for k,v in d.items():
        g.write(k+',,\n')
        hj=map(None,v.values()[0],v.values()[1])
        for ho in hj:
            g.write(','+str(ho).strip('()')+'\n')
