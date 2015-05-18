# -*- coding: utf-8 -*-
"""
Created on Fri May 15 15:28:19 2015

@author: rbanderson
This is the splitter developed by Tommy Boucher, with some modifications by Ryan Anderson
"""

#import mars.data as mars_data
import numpy as np
import time
import csv

def mean_loss(X,n_folds):
    loss = 0
    n_samps = X.shape[0]
    per_fold = n_samps // n_folds
    pop_mean = X.mean(0)
    for i in xrange(0, n_samps, per_fold):
        fold_mean = X[i:i+per_fold].mean(0)
        loss += np.linalg.norm(pop_mean - fold_mean)
    return loss


def multitask_stratified_splitter(X,n_folds,names,hours=24,outpath='',fname='best_split.txt',load=False):
    start_time = time.time()
    n_samples = X.shape[0]
    best_error = np.inf
    best_perm = np.arange(X.shape[0])
    per_fold=len(X)/n_folds
    folds=np.zeros_like(best_perm)
    if load is True:
        foldfile=np.genfromtxt(outpath+fname,delimiter=',',dtype='str')
        
        for i in range(len(best_perm)):
            best_perm[i]=np.arange(X.shape[0])[names==foldfile[i,0]]
            folds[i]=foldfile[i,1]
        best_error=mean_loss(X[best_perm],n_folds)
        
    while time.time() - start_time < hours * 3600:
        permutation = np.random.permutation(n_samples)
        perm_error = mean_loss(X[permutation],n_folds)
        
        if best_error - perm_error > 1e-7:
            best_error = perm_error
            best_perm = permutation
            print best_error
            #np.savetxt(fname,best_perm,fmt='%d',newline=',')
        for i in range(n_folds):
            folds[best_perm[i*per_fold:i*per_fold+per_fold]]=i+1 
        names_folds=names[best_perm]
        out=np.vstack([names_folds,folds])

        with open(outpath+fname,'wb') as writefile:
            writer=csv.writer(writefile,delimiter=',')
            for i in range(0,len(names)):
                writer.writerow(out[:,i])

        
    return best_perm,folds


def evaluate_split(X,n_folds):
    samp_mean = X.mean(0)
    per_fold = len(X) / n_folds
    print
    for i in xrange(n_folds):
        print i, np.linalg.norm(samp_mean - X[i*per_fold:i*per_fold+per_fold].mean(0))

