# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 11:57:57 2015

@author: rbanderson
"""
import numpy
def ccam_meancenter(X,X_mean=None):
    if X_mean == None:
        X_mean=numpy.mean(X,axis=0)
    checkshape=X.shape
    if len(checkshape)==2:
        for j in range(0,len(X[:,0])):
            X[j,:]=X[j,:]-X_mean
    if len(checkshape)==1:
        X=X-X_mean
    return X,X_mean