# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 19:59:25 2015

@author: rbanderson
"""
import os
import fnmatch
from scipy.io.idl import readsav
import numpy

def read_ccs(searchdir):#,minsol=0,maxsol=10000,masterlist=None):
    

     #Recursively search for CCS files in the specified directory
    filelist = []
    for root, dirnames, filenames in os.walk(searchdir):
        for filename in fnmatch.filter(filenames, '*CCS*SAV'):
            filelist.append(os.path.join(root, filename))
    filelist=numpy.array(filelist)
    
    #Remove duplicates
    files=numpy.zeros_like(filelist)
    sclocks=numpy.zeros_like(filelist)
    fileversion=numpy.zeros(len(filelist),dtype='int')    
    for i in range(len(filelist)):
        files[i]=filelist[i][-40:]
        sclocks[i]=filelist[i][-36:-27]
        fileversion[i]=filelist[i][-5:-4]

    keep=numpy.zeros(len(files),dtype='bool')    
    for i in range(len(files)):
        sclock_match=numpy.in1d(sclocks,sclocks[i])
        maxversion=max(fileversion[sclock_match])
        if fileversion[i]==maxversion:
            keep[i]=True
            
    files=files[keep]
    filelist=filelist[keep]
    sclocks=sclocks[keep]
            
        
        
    data=numpy.zeros((len(filelist),6144),dtype='float32')
    print 'Reading '+str(len(filelist))+' files...'
    for i in range(len(filelist)):
        if numpy.mod(i,100)==0:
            print i
        tempdata=readsav(filelist[i],python_dict=True)
        tempspect=numpy.hstack([tempdata['auv'],tempdata['avis'],tempdata['avnir']])
        data[i,:]=tempspect
    wvl=numpy.hstack([tempdata['defuv'],tempdata['defvis'],tempdata['defvnir']])
    return data,wvl,files

