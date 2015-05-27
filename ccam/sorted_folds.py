# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:31:22 2015

@author: rbanderson
"""

import numpy

def sorted_folds(names,comps,nfolds,compindex):
    names_unique,uniqueindex=numpy.unique(names,return_index=True)
    comps_unique=comps[uniqueindex,:]
    
    names_unique_sorted=names_unique[comps_unique[:,compindex].argsort()]

    folds_sorted=range(1,nfolds+1)
    
    while len(folds_sorted)<len(names_unique_sorted):
        folds_sorted.extend(range(1,nfolds+1))
    folds_sorted=numpy.array(folds_sorted[:len(names_unique_sorted)],dtype='int')
    folds=numpy.zeros(len(names),dtype='int')
    for i in range(0,len(names_unique)):
        folds[names==names_unique[i]]=folds_sorted[i]
        
    return folds