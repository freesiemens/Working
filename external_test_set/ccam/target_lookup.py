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
    sclocks[numpy.where(sclocks=='')]='0'
    sclocks_temp=[]
    for i in range(len(sclocks)):sclocks_temp.append(int(sclocks[i]))
    sclocks_temp=numpy.array(sclocks_temp)
    sclocks=sclocks_temp
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
        targetmatch=numpy.where(sclocks==int(file_sclocks[filelist_ind_true][0]))
        if max(targetmatch):
            
            file_targets[filelist_ind]=targets[targetmatch][0]
            file_dists[filelist_ind]=dists[targetmatch][0]
            file_amps[filelist_ind]=amps[targetmatch][0]
            file_nshots[filelist_ind]=nshots[targetmatch][0]
    data=ccam.read_csv(name_sub_file,0,labelrow=False)
    old_name=data[:,0]
    new_name=data[:,1]    
    for i in range(len(old_name)):
        file_targets[(file_targets==old_name[i])]=new_name[i]
    file_targets=numpy.array([i.replace('\n','') for i in file_targets])
    return file_targets,file_dists,file_amps,file_nshots