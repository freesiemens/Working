# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 09:03:38 2015

@author: rbanderson
"""
import numpy
import ccam

def remove_spectra(removefile,spectra,names,spect_index,comps):
    #read the list of sample names and spectrum indices from the file
    data=ccam.read_csv_cols(removefile,0,labelrow=False)
    removenames=numpy.array(data[0],dtype='string')
    removeinds=numpy.array(data[1],dtype='int')
    #define an array to hold the indices for each row in the file        
    index=numpy.empty([len(names),len(removenames)])
    for i in range(len(removenames)):
        #for each row, find the indices that correspond to the matching 
        #name AND spectral index
        index[:,i]=(names==removenames[i])&(spect_index==removeinds[i])
    #combine the indices for each row to a single array that indicates which
    #spectra to remove, then invert it to indicate which spectra to keep
    index=numpy.invert(numpy.any(index,axis=1))
    
    spectra=spectra[index,:]
    names=names[index]
    spect_index=spect_index[index]
    comps=comps[index,:]
    
    return spectra,names,spect_index,comps
    
    