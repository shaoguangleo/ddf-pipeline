#!/usr/bin/python

import matplotlib
matplotlib.use('Agg')
from overlay import show_overlay
from astropy.table import Table
from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
import sys
import os

scale=3600.0 # scaling factor for region sizes

def flatten(f,ra,dec,x,y,size,hduid=0,channel=0,freqaxis=3):
    """ 
    Flatten a fits file so that it becomes a 2D image. Return new header and
    data
    This version also makes a sub-image of specified size.
    """

    naxis=f[hduid].header['NAXIS']
    if naxis<2:
        raise OverlayException('Can\'t make map from this')

    ds=f[hduid].data.shape[-2:]
    by,bx=ds
    xmin=int(x-size)
    if xmin<0:
        xmin=0
    xmax=int(x+size)
    if xmax>bx:
        xmax=bx
    ymin=int(y-size)
    if ymin<0:
        ymin=0
    ymax=int(y+size)
    if ymax>by:
        ymax=by
    
    if ymax<=ymin or xmax<=xmin:
        # this can only happen if the required position is not on the map
        print 'Failed to make subimage!'
        return None

    w = WCS(f[hduid].header)
    wn=WCS(naxis=2)
    
    wn.wcs.crpix[0]=w.wcs.crpix[0]-xmin
    wn.wcs.crpix[1]=w.wcs.crpix[1]-ymin
    wn.wcs.cdelt=w.wcs.cdelt[0:2]
    try:
        wn.wcs.pc=w.wcs.pc[0:2,0:2]
    except AttributeError:
        pass # pc is not present
    wn.wcs.crval=w.wcs.crval[0:2]
    wn.wcs.ctype[0]=w.wcs.ctype[0]
    wn.wcs.ctype[1]=w.wcs.ctype[1]
    
    header = wn.to_header()
    header["NAXIS"]=2

    slice=[]
    for i in range(naxis,0,-1):
        if i==1:
            slice.append(np.s_[xmin:xmax])
        elif i==2:
            slice.append(np.s_[ymin:ymax])
        elif i==freqaxis:
            slice.append(channel)
        else:
            slice.append(0)
    print slice

    hdu=fits.PrimaryHDU(f[hduid].data[slice],header)
    copy=('EQUINOX','EPOCH','BMAJ','BMIN','BPA')
    for k in copy:
        r=f[hduid].header.get(k)
        if r:
            hdu.header[k]=r
    if 'TAN' in hdu.header['CTYPE1']:
        hdu.header['LATPOLE']=f[hduid].header['CRVAL2']
    hdulist=fits.HDUList([hdu])
    return hdulist

def extract_subim(filename,ra,dec,size,hduid=0):
    orighdu=fits.open(filename)
    psize=int(size/orighdu[hduid].header['CDELT2'])
    print 'psize is',psize
    ndims=orighdu[hduid].header['NAXIS']
    pvect=np.zeros((1,ndims))
    lwcs=WCS(orighdu[hduid].header)
    pvect[0][0]=ra
    pvect[0][1]=dec
    imc=lwcs.wcs_world2pix(pvect,0)
    x=imc[0][0]
    y=imc[0][1]
    hdu=flatten(orighdu,ra,dec,x,y,psize,hduid=hduid)
    return hdu

def find_bbox(t):
    # given a table t find the bounding box of the ellipses for the regions

    boxes=[]
    for r in t:
        a=r['Maj']/scale
        b=r['Min']/scale
        th=(r['PA']+90)*np.pi/180.0
        dx=np.sqrt((a*np.cos(th))**2.0+(b*np.sin(th))**2.0)
        dy=np.sqrt((a*np.sin(th))**2.0+(b*np.cos(th))**2.0)
        boxes.append([r['RA']-dx/np.cos(r['DEC']*np.pi/180.0),
                      r['RA']+dx/np.cos(r['DEC']*np.pi/180.0),
                      r['DEC']-dy, r['DEC']+dy])

    boxes=np.array(boxes)
    print boxes
    minra=np.min(boxes[:,0])
    maxra=np.max(boxes[:,1])
    mindec=np.min(boxes[:,2])
    maxdec=np.max(boxes[:,3])
    
    ra=np.mean((minra,maxra))
    dec=np.mean((mindec,maxdec))
    size=1.05*3600.0*np.max((maxdec-mindec,(maxra-minra)*np.cos(dec*np.pi/180.0)))
    print 'returned size is',size
    return ra,dec,size

if __name__=='__main__':

    t=Table.read('subset_with_id.fits')
    ot=Table.read('LOFAR_HBA_T1_DR1_catalog_v0.1.fits')
    gals=Table.read('tier1_ps1_wise_hetdex.fits')
    gals['raMean'].name='ra'
    gals['decMean'].name='dec'

    # read lists

    lofarmaps=[l.rstrip().split()[1] for l in open('lofar-maps.txt').readlines()]
    psmaps=[l.rstrip().split()[1] for l in open('panstarrs-list.txt').readlines()]
    firstmaps=[l.rstrip().split()[1] for l in open('first-list.txt').readlines()]
    wisemaps=[l.rstrip().split()[2] for l in open('panstarrs-list.txt').readlines()]

    i=int(sys.argv[1])
    r=t[i]
    print r
    print lofarmaps[i],psmaps[i],wisemaps[i]
    ra,dec=r['RA'],r['DEC']

    iter=0
    while True:
        startra,startdec=ra,dec
        tcopy=t
        tcopy['dist']=np.sqrt((np.cos(dec*np.pi/180.0)*(tcopy['RA']-ra))**2.0+(tcopy['DEC']-dec)**2.0)*3600.0
        tcopy=tcopy[tcopy['dist']<180]
        print 'Iter',iter,'found',len(tcopy),'neighbours'

        # make sure the original source is in there
        for nr in tcopy:
            if r['Source_id']==nr['Source_id']:
                break
        else:
            tcopy=vstack((tcopy,r))

        ra=np.mean(tcopy['RA'])
        dec=np.mean(tcopy['DEC'])

        if startra==ra and startdec==dec:
            break
        iter+=1
        if iter==10:
            break

    # now find the bounding box of the resulting collection
    ra,dec,size=find_bbox(tcopy)
    if size>300.0:
        # revert just to original
        ra,dec=r['RA'],r['DEC']
        tcopy=Table(r)
        ra,dec,size=find_bbox(tcopy)

    if size>300:
        size=300.0
    if size<60:
        size=60.0
    size=(int(0.5+size/10))*10
    print 'size is',size

    size/=3600.0
    pg=gals[(np.abs(gals['ra']-ra)<size) & (np.abs(gals['dec']-dec)<size)]
    del(gals)
    pshdu=extract_subim(psmaps[i],ra,dec,size,hduid=1)
    lhdu=extract_subim(lofarmaps[i],ra,dec,size)
    firsthdu=extract_subim(firstmaps[i],ra,dec,size)
    show_overlay(lhdu,pshdu,ra,dec,size,firsthdu=firsthdu,overlay_cat=ot,overlay_scale=scale,coords_color='red',coords_ra=r['RA'],coords_dec=r['DEC'],coords_lw=3,lw=2,save_name=r['Source_id']+'_PS.png',no_labels=True)
    show_overlay(lhdu,pshdu,ra,dec,size,overlay_cat=ot,overlay_scale=scale,coords_color='red',coords_ra=r['RA'],coords_dec=r['DEC'],coords_lw=3,lw=2,plotpos=pg,show_lofar=False,save_name=r['Source_id']+'_PSp.png',no_labels=True)
    whdu=extract_subim(wisemaps[i],ra,dec,size)
    show_overlay(lhdu,whdu,ra,dec,size,firsthdu=firsthdu,overlay_cat=ot,overlay_scale=scale,coords_color='red',coords_ra=r['RA'],coords_dec=r['DEC'],coords_lw=3,lw=2,save_name=r['Source_id']+'_W.png',no_labels=True)

    os.system('mogrify -quality 90 -trim '+r['Source_id']+'*.png')