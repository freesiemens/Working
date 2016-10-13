# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 10:22:55 2015

@author: rbanderson
"""
import numpy
import ccam

def target_lookup(filelist,masterlist_file,name_sub_file):
    data,labels=ccam.read_csv(masterlist_file,1,labelrow=True)
    
    targets=numpy.array(data[:,5],dtype='string')
    sclocks=numpy.array(data[:,2],dtype='string')
    dists=numpy.array(data[:,8],dtype='string')
    amps=numpy.array(data[:,17],dtype='string')
    nshots=numpy.array(data[:,11])
    file_sclocks=numpy.zeros_like(filelist)
    file_targets=numpy.zeros_like(filelist)  
    file_amps=numpy.zeros_like(filelist)
    file_dists=numpy.zeros_like(filelist)
    file_nshots=numpy.zeros(len(filelist))
    filelist_unique=numpy.unique(filelist)
    for i in range(len(filelist_unique)):
        filelist_ind=filelist==filelist_unique[i]
        filelist_ind_true=(filelist_ind==True)
        file_sclocks[filelist_ind]=filelist_unique[i][-36:-27]
       # print max(sclocks==file_sclocks[filelist_ind_true][0])
        if max(sclocks==file_sclocks[filelist_ind_true][0]):
            
            file_targets[filelist_ind]=targets[(sclocks==file_sclocks[filelist_ind_true][0])][0]
            file_dists[filelist_ind]=dists[(sclocks==file_sclocks[filelist_ind_true][0])][0]
            file_amps[filelist_ind]=amps[(sclocks==file_sclocks[filelist_ind_true][0])][0]
            file_nshots[filelist_ind]=nshots[(sclocks==file_sclocks[filelist_ind_true][0])][0]
    data=ccam.read_csv(name_sub_file,0,labelrow=False)
    old_name=data[:,0]
    new_name=data[:,1]    
    for i in range(len(old_name)):
        file_targets[(file_targets==old_name[i])]=new_name[i]
    
    return file_targets,file_dists,file_amps,file_nshots