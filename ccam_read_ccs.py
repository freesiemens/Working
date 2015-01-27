# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 19:59:25 2015

@author: rbanderson
"""
import os
import fnmatch
from scipy.io.idl import readsav
import numpy

#def ccam_read_ccs(searchdir,minsol=0,maxsol=10000,masterlist=None):
    
    #filelist=glob.glob(searchdir+'*CCS*SAV') 
searchdir=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_team'
filelist = []
for root, dirnames, filenames in os.walk(searchdir):
    for filename in fnmatch.filter(filenames, '*CCS*SAV'):
        filelist.append(os.path.join(root, filename))
filelist=numpy.array(filelist)
data=numpy.zeros((len(filelist),6144),dtype='float32')
print 'Reading '+str(len(filelist))+' files...'
for i in range(len(filelist)):
    tempdata=readsav(filelist[i],python_dict=True)
    tempspect=numpy.hstack([tempdata['auv'],tempdata['avis'],tempdata['avnir']])
    
    
    

    print 'stop'