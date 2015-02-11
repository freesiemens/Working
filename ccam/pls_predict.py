# -*- coding: utf-8 -*-
"""
Created on Tue Feb 03 21:43:25 2015

@author: rbanderson
"""

import ccam
def pls_predict(which_elem,nc,data,wvl,maskfile,modelfiles):
    coeff_file=modelfiles[0]
    mean_file=modelfiles[1]
    
    data,wvl=ccam.mask(data,wvl,maskfile)
    #find the norm type from the coeff file
    if coeff_file.find('norm1')!=-1:
        normtype=1
    if coeff_file.find('norm3')!=-1:
        normtype=3
    if coeff_file.find('norm1')==1 and coeff_file.find('norm3')==1:
        print 'Error: Cant determine normalization from coeff file name!'
        return
    data_norm=ccam.normalize(data,wvl,normtype=normtype)
    y=ccam.pls_unk(data_norm,nc,coeff_file=coeff_file,means_file=mean_file)
    return y,normtype

    