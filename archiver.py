#!/usr/bin/python

import os
import glob

class Tarfile():
    def __init__(self,filename):
        self.filename=filename
        self.append=False
    def add(self,files):
        if isinstance(files,str):
            files=[files]
        for f in files:
            print 'adding',f
            if not os.path.exists(f):
                continue
            command='tar '
            if not self.append:
                command+='-c'
            else:
                command+='-r'
            command+='f '+self.filename+' '+f
            os.system(command)
            self.append=True

def images(rootname):
    list=[rootname+'.'+f+'.fits' for f in ['dirty','app.restored','int.restored','smooth.int.restored','int.model','int.residual']]
    n=1
    while os.path.isfile(rootname+'.mask%02i.fits' % n):
        n+=1
    if n>1:
        list.append(rootname+'.mask%02i.fits' % (n-1))
    return list

t=Tarfile('archive.tar')
t.add(['summary.txt','logs'])
t.add(images('image_full_ampphase1m'))
t.add(images('image_full_ampphase2'))
t.add(images('image_full_low_m'))
t.add(glob.glob('*ms/killMS.killms_f_ap?.sols.npz'))
t.add(glob.glob('*.cfg'))
t.add(glob.glob('*.png'))
t.add(glob.glob('*crossmatch*2*'))