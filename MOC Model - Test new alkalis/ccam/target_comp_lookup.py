# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 11:01:34 2015

@author: rbanderson
"""
import ccam
import numpy
def target_comp_lookup(targetlist,compfile,which_elem):
    data,labels=ccam.read_csv(compfile,0,labelrow=True)
    colmatch=numpy.where(labels==which_elem)
    comps=numpy.array(data[:,colmatch[0]],dtype='float32')
    comp_targets=data[:,numpy.where(labels=='Name')[0]]
    comp_targets,uniqueindex=numpy.unique(comp_targets,return_index=True)
    comps=comps[uniqueindex]
    
    complist=numpy.zeros(len(targetlist))
    for i in range(len(complist)):
        matchtarget=(comp_targets==targetlist[i])
        if sum(matchtarget)==0:
            print('No match found for '+targetlist[i])
            complist[i]=numpy.nan
        if sum(matchtarget)==1:
            complist[i]=comps[matchtarget]
    return complist