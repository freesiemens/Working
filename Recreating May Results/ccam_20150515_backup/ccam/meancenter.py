# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 11:57:57 2015

@author: rbanderson
"""
import numpy
import copy
def meancenter(X,X_mean=None):
    X_copy=copy.copy(X)
 
    if X_mean is None:
        X_mean=numpy.mean(X_copy,axis=0)
    checkshape=X.shape
    if len(checkshape)==2:
        for j in range(0,len(X_copy[:,0])):
            X_copy[j,:]=X_copy[j,:]-X_mean
    if len(checkshape)==1:
        X_copy=X_copy-X_mean
    return X_copy,X_mean