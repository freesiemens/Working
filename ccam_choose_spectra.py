# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 14:12:02 2015

@author: rbanderson

"""
import numpy
def ccam_choose_spectra(spectra,spect_index,names,comps,mincomp,maxcomp,removelist=None):
    #define new variable to hold the chosen data (don't want to overwrite the originals) 
    spectra_keep=numpy.empty_like(spectra)
    names_keep=numpy.empty_like(names)
    spect_index_keep=numpy.empty_like(spect_index)
    comps_keep=numpy.empty_like(comps)
    
    index=(comps>mincomp)&(comps<maxcomp) #define index where composition is within the specified range
    
    #fill the new variables with the data to keep
    spectra_keep[index]=spectra[index]
    names_keep[index]=names[index]
    spect_index_keep[index]=spect_index[index]
    comps_keep[index]=comps[index]
    
    #optionally, remove spectra listed in an external file
    if removelist != None:
        remove=numpy.genfromtxt(removelist,delimiter=',')
    
    