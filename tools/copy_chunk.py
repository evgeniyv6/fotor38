#!/usr/bin/env python

#py 2

import os,sys

maxfl=1000000
blksz=1024*500

def cpfl(fromdir,todir,verbose=True):
	if os.path.getsize(fromdir) <= maxfl:
		btfrom=open(fromdir,'rb').read()
		open(todir,'wb').write(btfrom)
	else:
		flfrrom=open(fromdir,'rb')
		flto=open(todir,'wb')
		while True:
			btfom=flfrrom.read(blksz)
			if not btfom:break
			flto.write(btfom)
			
def copytree(dfr,dto,verbose=0):
	fc=dc=0
	for file in os.listdir(dfr):
		pathFr=os.path.join(dfr,file)
		pathT=os.path.join(dto,file)
		if not os.path.isdir(pathFr):
			try:
				if verbose>1: print ('copying ',pathFr,'to',pathT)
				cpfl(pathFr,pathT)
				fc+=1
			except:
				print ('error copying',pathT,'--skipped')
				print (sys.exc_info()[0],sys.exc_info()[1])
		else:
			if verbose:print ('copying ',pathFr,'to',pathT)
			try:
				os.mkdir(pathT)
				below= copytree(pathFr,pathT)
				fc+=below[0]
				dc+=below[1]
				dc+=1
			except:
				print ('error copying',pathT,'--skipped')
				print (sys.exc_info()[0],sys.exc_info()[1])
		return (fc,dc)
		
def getargs():
	try:
		df,dt=sys.argv[1:]
	except:
		print ('usage dirFrom dirTo')
	if not os.path.exists(dt):
		os.mkdir(dt)
		print ('dir to was created')
		return (df,dt)
	else:
		print ('dir to already exist')
		if hasattr(os.path,'samefile'):
			same = os.path.samefile(df,dt)
		else:
			same = os.path.abspath(df) == os.path.abspath(dt)
		if same: print ('error dirf = dirto')
		else:
			return (df,dt)
			
if __name__=='__main__':
	ar=getargs()
	if ar:
		 copytree(*ar)
		 print ('done')
	
	
