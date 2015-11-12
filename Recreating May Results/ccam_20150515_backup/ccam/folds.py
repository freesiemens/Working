# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 10:03:25 2015

@author: rbanderson
This function reads an input file that specifies a cross validation fold for each sample name. 
It assigns these folds to each of the spectra 
"""
import numpy
import csv
def folds(foldfile,names,testfold=None):
    f=open(foldfile,'rb')
    data=zip(*csv.reader(f))
    foldnames=numpy.array(data[0],dtype='string')
    foldnums=numpy.array(data[1],dtype='int')
   
    folds=numpy.zeros(len(names),dtype='int')
    for i in range(len(names)):
        findfold=(foldnames==names[i])
        if sum(findfold)>0:
            folds[i]=(foldnums[findfold])[0]
        else:
            folds[i]=0
          
        
    
    
    return folds
        