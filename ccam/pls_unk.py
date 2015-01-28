# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 18:43:18 2015

@author: rbanderson
"""
import numpy
import csv
import ccam_meancenter

def pls_unk(unk_spectra,coeff_file,means_file,nc):
   
    f=open(coeff_file,'rb')  #open the file
    cols=f.readline() #read the first line
    cols=numpy.array(cols.split(',')[1:],dtype='int') 
    
    data=zip(*csv.reader(f))
    coeffs=numpy.array(data[1:],dtype='float')
    beta=coeffs[numpy.where(cols==nc)]
    
    f=open(means_file,'rb')
    temp=f.readline()
    Y_mean=numpy.array(temp.split(',')[1],dtype='float')
    print Y_mean
    data=zip(*csv.reader(f))
    X_mean=numpy.array(data[1],dtype='float')
    
    unk_spectra=ccam_meancenter.ccam_meancenter(unk_spectra,X_mean=X_mean)[0]
    predicts=numpy.zeros(len(unk_spectra[:,0]))
    for i in range(len(predicts)):
        predicts[i]=numpy.dot(unk_spectra[i,:],beta[:].T)+Y_mean
        
    return predicts
    