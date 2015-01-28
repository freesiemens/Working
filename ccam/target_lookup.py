# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 10:22:55 2015

@author: rbanderson
"""
import numpy
import ccam
def target_lookup(filelist,masterlist_file,name_sub_file):
    data,labels=ccam.read_csv_cols(masterlist_file,1,labelrow=True)
    
    targets=numpy.array(data[5],dtype='string')
    sclocks=numpy.array(data[2],dtype='string')

    
    file_sclocks=numpy.zeros_like(filelist)
    file_targets=numpy.zeros_like(filelist)    
    for i in range(len(filelist)):
        file_sclocks[i]=filelist[i][-36:-27]
        file_targets[i]=targets[(sclocks==file_sclocks[i])][0]
    
    data=ccam.read_csv_cols(name_sub_file,0,labelrow=False)
    old_name=data[0]
    new_name=data[1]    
    for i in range(len(old_name)):
        file_targets[(file_targets==old_name[i])]=new_name[i]
    
    return file_targets