# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 19:59:25 2015

@author: rbanderson
"""
import os
import fnmatch
from scipy.io.idl import readsav
import numpy

def ccam_read_ccs(searchdir):#,minsol=0,maxsol=10000,masterlist=None):
    

    searchdir='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\ChemCam\\ops_ccam_team\\CalTarget 95A\\'
    #Recursively search for CCS files in the specified directory
    filelist = []
    for root, dirnames, filenames in os.walk(searchdir):
        for filename in fnmatch.filter(filenames, '*CCS*SAV'):
            filelist.append(os.path.join(root, filename))
    filelist=numpy.array(filelist)
    
    #Remove duplicates
    files=numpy.zeros_like(filelist)
    for i in range(len(filelist)):
        files[i]=filelist[i][-40:]
    filelist=filelist[numpy.unique(files,return_index=True)[1]]
        
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

