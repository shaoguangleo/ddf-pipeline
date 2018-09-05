#!/usr/bin/python
# Upload to archive directory
# To store on Leiden systems in /disks/paradata/shimwell/LoTSS-DR2/archive

# version 2 -- simple rsync wrapper with timeout

from subprocess import call
import os
import glob
from time import sleep
from surveys_db import update_status

def myglob(g,workdir):
    f=glob.glob(workdir+'/'+g)
    return [os.path.basename(file) for file in f]

def images(rootname):
    l=[rootname+'.'+f+'.fits' for f in ['app.restored','int.restored','int.model','int.residual']]
    n=1
    while os.path.isfile(rootname+'.mask%02i.fits' % n):
        n+=1
    if n>1:
        l.append(rootname+'.mask%02i.fits' % (n-1))
    l.append(rootname+'.DicoModel')
    l.append(rootname+'.tessel.reg')
    return l

def shiftimages(rootname):
    return [rootname+f+'.fits' for f in ['_shift.app.facetRestored','_shift.int.facetRestored']]

def do_upload(name,basedir):
    if os.environ['DDF_PIPELINE_CLUSTER']!='paracluster':
        target=os.environ['DDF_PIPELINE_LEIDENUSER']+'@ssh.strw.leidenuniv.nl:'
    else:
        target=''

    workdir=basedir+'/'+name

    f=['summary.txt']
    f+=['logs','SOLSDIR']
    f+=['astromap.fits','panstarrs-fit_state.pickle','facet-offset.txt']
    f+=['image_dirin_SSD_m.npy.ClusterCat.npy']
    f+=myglob('DynSpecs*.tgz',workdir)
    f+=myglob('*.png',workdir)
    f+=myglob('DDS*smoothed*.npz',workdir)
    f+=images('image_full_ampphase_di_m.NS')
    f+=images('image_full_low_m')
    f+=shiftimages('image_full_ampphase_di_m.NS')
    for i in range(3):
        f+=shiftimages('image_full_ampphase_di_m.NS_Band%i' %i)
    f+=myglob('image_full_low_stokesV.dirty.*',workdir)
    f+=myglob('image_full_low_QU.cube.*',workdir)
    f+=myglob('image_full_vlow_QU.cube.*',workdir)

    while True:
        s='cd '+workdir+'; rsync -avz --progress --inplace --append --partial --timeout=20 '+' '.join(f)+' '+target+'/disks/paradata/shimwell/LoTSS-DR2/archive/'+name
        print 'Running command:',s
        retval=call(s,shell=True)
        if retval==0:
            break
        print 'Non-zero return value',retval
        if retval!=30:
            raise RuntimeError('rsync failed unexpectedly')
        sleep(10)

    update_status(name,'Archived',workdir=workdir)
        
if __name__=='__main__':
    import sys
    do_upload(sys.argv[1],sys.argv[2])