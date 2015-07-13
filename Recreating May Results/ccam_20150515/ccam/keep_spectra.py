# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 08:39:54 2015

@author: rbanderson
"""
import ccam
import numpy

def keep_spectra(keepfile,spectra,names,spect_index,comps):
    keepdata,keepcols=ccam.read_csv_cols(keepfile,1,labelrow=True)    
    keepindex=numpy.array(keepdata[0],dtype='int')-1
    fullindex=range(len(names))
    matchindex=numpy.in1d(fullindex,keepindex)
    spectra=spectra[matchindex,:]
    comps=comps[matchindex,:]
    names=names[matchindex]
    spect_index=spect_index[matchindex]
    
    return spectra,names,spect_index,comps