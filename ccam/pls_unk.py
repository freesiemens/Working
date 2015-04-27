# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 18:43:18 2015

@author: rbanderson
"""
import numpy
import ccam
import cPickle as pickle

def pls_unk(unk_spectra,nc,coeff_file=None,means_file=None,beta=None,X_mean=None,Y_mean=None):

    if coeff_file is not None:
        data,cols=ccam.read_csv(coeff_file,0,labelrow=True)
        cols=numpy.array(cols[1:],dtype='int')
        coeffs=numpy.array(data[:,1:],dtype='float')
        beta=coeffs[numpy.where(cols==nc)]
    if means_file is not None:
        data,temp=ccam.read_csv(means_file,0,labelrow=True)
        Y_mean=numpy.array(temp[1],dtype='float')
        X_mean=numpy.array(data[:,1],dtype='float')
        
       
    unk_spectra_centered=ccam.meancenter(unk_spectra,X_mean=X_mean)[0] 

    predicts=numpy.zeros(len(unk_spectra[:,0]))
    for i in range(len(predicts)):
        predicts[i]=numpy.dot(unk_spectra_centered[i,:],beta[:].T)+Y_mean

    return predicts

def pls_unk_load(unk_spectra,nc,modelfile,means_file=None):
    Y_mean=0
    if means_file is not None:
        data,temp=ccam.read_csv(means_file,0,labelrow=True)
        Y_mean=numpy.array(temp[1],dtype='float')
        X_mean=numpy.array(data[:,1],dtype='float')    
    else:
        X_mean is None
        Y_mean=0
        
        
    #load the model from the appropriate pkl file
    with open(modelfile,'rb') as picklefile:
        model=pickle.load(picklefile)[nc-1][0]
    if X_mean is not None:
        unk_spectra_centered=ccam.meancenter(unk_spectra,X_mean=X_mean)[0]
    else:
        unk_spectra_centered=unk_spectra
        
   
    predicts=numpy.squeeze(model.predict(unk_spectra_centered)+Y_mean)

    return predicts
    