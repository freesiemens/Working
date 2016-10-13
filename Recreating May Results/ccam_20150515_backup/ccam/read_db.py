# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 16:14:13 2015

@author: rbanderson
This function reads a comma separated text file containing
LIBS compositional and spectral database entries. 

Input: dbfile = string specifying the path to the database file
The file should be formatted as follows:

First row: column labels
Column 0: Target name
Columns 1 through 9: Major oxide composition 
                    (SiO2, TiO2, Al2O3, FeOT, MnO, MgO, CaO, Na2O, K2O)
Columns 10 through 6153: LIBS spectrum

Optional input:
compcheck = Option to have the script remove any spectra that don't have a 
            corresponding composition (i.e. all oxides are listed as zero)
            (defaults to True)

Output: 
spectra = float array of spectra
comps = float array of compositions
names = string list of sample names for each spectrum
labels = string array of column labels
wvl = array of wavelength values for the LIBS spectra
"""
import numpy
import ccam


def read_db(dbfile,n_elems=9,compcheck=True):
    
    data,labels=ccam.read_csv(dbfile,0,labelrow=True)
  
    names=numpy.array(data[:,0],dtype='string')
    spect_index=numpy.array(data[:,1],dtype='int')
    comps=numpy.array(data[:,2:2+n_elems],dtype='float32')
    spectra=numpy.array(data[:,2+n_elems:len(data[0,:])],dtype='float64')
   
    wvl=numpy.array(labels[2+n_elems:],dtype='float32')
    labels=labels[0:2+n_elems]
    
    if compcheck:
        index=(numpy.sum(comps,axis=1)!=0)
        spectra=spectra[index]
        comps=comps[index]
        names=names[index]
        spect_index=spect_index[index]
    
    return spectra,comps,spect_index,names,labels,wvl
        
        
        
        