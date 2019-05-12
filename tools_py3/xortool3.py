#!/usr/bin/env python

# for py 3, doesn't work in py2 because of iteration
import base64, itertools
'''
use key = '_' for websphere xor
'''

def XorFunc(password, key='secretword', encode = False, decode = False):
    if decode:
    	try:
    		password = base64.b64decode(password).decode('utf-8')
    	except:
    		print ('Can\'t decode password')

    xored = ''.join((chr(ord(x)^ord(y)) for (x,y) in zip(password,itertools.cycle(key))))
    xoredenc = xored.encode('utf-8')

    if encode:
    	return base64.encodebytes(xoredenc).decode('utf-8').replace('\n','')
    return xored



if __name__=='__main__':
    print (XorFunc('testpass',key='_',encode=True))
    print (XorFunc('KzosKy8+LCw=',key='_', decode=True))
