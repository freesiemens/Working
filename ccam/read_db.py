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
import csv

def read_db(dbfile,compcheck=True):
   
  
    f=open(dbfile,'rb')  #open the file
    labels=f.readline() #read the first line
    labels=numpy.array(labels.split(',')) #split it on commas and convert to a string array
    
    data=zip(*csv.reader(f))    
    names=numpy.array(data[0],dtype='string')
    spect_index=numpy.array(data[1],dtype='int')
    comps=numpy.transpose(numpy.array(data[2:11],dtype='float32'))
    spectra=numpy.transpose(numpy.array(data[11:len(data)],dtype='float32'))
    f.close()

    
    wvl=numpy.array(labels[11:],dtype='float')
    labels=labels[0:11]
    
    if compcheck:
        index=(numpy.sum(comps,axis=1)!=0)
        spectra=spectra[index]
        comps=comps[index]
        names=names[index]
        spect_index=spect_index[index]
    
    return spectra,comps,spect_index,names,labels,wvl
        
        
        
        