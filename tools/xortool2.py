#!/usr/bin/env python

# only for py2
import base64, itertools
'''
use key = '_' for websphere xor
'''

def XorFunc(password, key='secretword', encode = False, decode = False):
    if decode:
    	try:
    		password = base64.decodestring(password)
    	except:
    		print ('Can\'t decode password')

    xored = ''.join((chr(ord(x)^ord(y)) for (x,y) in itertools.izip(password,itertools.cycle(key))))

    if encode:
    	return base64.encodestring(xored).strip()
    return xored



if __name__=='__main__':
    print (XorFunc('testpass',key='_', encode=True)) #-> HDkJOG5tbGtq
    print (XorFunc('KzosKy8+LCw=',key='_', decode=True))
