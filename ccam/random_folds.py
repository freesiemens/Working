# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 14:14:46 2015

@author: rbanderson

This function uses scikit-learn's k-fold cross validation tool to generate a specified number of random folds.
It keeps all spectra from a given sample in the same fold.

"""
import numpy
import sklearn.cross_validation as cv
def random_folds(names,nfolds):
    uniqnames,uniqindex=numpy.unique(names,return_index=True)
    kf=cv.KFold(len(uniqnames),nfolds)
    uniqfolds=numpy.zeros(len(uniqnames))
    folds=numpy.zeros(len(names),dtype='int')    
    i=0
    for train,test in kf:
        i=i+1        
        uniqfolds[test]=i
    
    for j in range(len(uniqfolds)):
        folds[(names==uniqnames[j])]=uniqfolds[j]
        
    return folds