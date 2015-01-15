# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 10:03:25 2015

@author: rbanderson
This function reads an input file that specifies a cross validation fold for each sample name. 
It assigns these folds to each of the spectra 
"""
import numpy
import csv
def ccam_folds(foldfile,names,testfold=None):
    f=open(foldfile,'rb')
    data=zip(*csv.reader(f))
    foldnames=numpy.array(data[0],dtype='string')
    foldnums=numpy.array(data[1],dtype='int')
   
    #first check if there are any samples in the fold names that are not in the spectra names
    check1=numpy.in1d(foldnames,names)
    check2=numpy.in1d(names,foldnames)
    
   
    folds=numpy.zeros(len(names),dtype='int')
    for i in range(len(names)):
        
        findfold=(foldnames==names[i])
        folds[i]=foldnums(findfold)
    
    
    return folds
        