# -*- coding: utf-8 -*-
"""
Created on Tue Feb 03 21:43:25 2015

@author: rbanderson
"""

import ccam
def pls_predict(data,nc,wvl,maskfile,coeff_file=None,mean_file=None,loadfile=None):
    normtype=0
    
    
    data,wvl=ccam.mask(data,wvl,maskfile)
    #find the norm type from the coeff file
    if coeff_file!=None:    
        if coeff_file.find('norm1')!=-1:
            normtype=1
        if coeff_file.find('norm3')!=-1:
            normtype=3
        if normtype==0:
            print('Error: Cant determine normalization from coeff file name!')
            return
        
    
    if loadfile!=None:
        if loadfile.find('norm1')!=-1:
            normtype=1
        if loadfile.find('norm3')!=-1:
            normtype=3
        if normtype==0:
            print('Error: Cant determine normalization from loadfile name!')
            return
    data_norm=ccam.normalize(data,wvl,normtype=normtype)
    if loadfile==None:
        y=ccam.pls_unk(data_norm,nc,coeff_file=coeff_file,means_file=mean_file)
    if loadfile!=None:
        y=ccam.pls_unk_load(data_norm,nc,loadfile,means_file=mean_file)
    return y,normtype

    