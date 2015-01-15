# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 10:03:25 2015

@author: rbanderson
This function reads an input file that specifies a cross validation fold for each sample name. 
It assigns these folds to each of the spectra 
"""
import numpy
def ccam_folds(foldfile,names,spectra,testfold=None):
    foldnames=numpy.genfromtxt(foldfile,usecols=0,delimiter=',',dtype='string')
    foldnums=numpy.genfromtxt(foldfile,usecols=1,delimiter=',',dtype='int')
    
    folds=numpy.zeros(len(names),dtype='int')
    for i in range(len(names)):
        findfold=(foldnames==names[i])
        folds[i]=foldnums(findfold)
    
    
    return folds
        