# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 19:59:25 2015

@author: rbanderson
"""
import os
import fnmatch
import numpy
import ccam

def search_ccs(searchdir,searchstring='*CCS*csv'):
    
     #Recursively search for CCS files in the specified directory
    filelist = []
    for root, dirnames, filenames in os.walk(searchdir):
        for filename in fnmatch.filter(filenames, searchstring):
            filelist.append(os.path.join(root, filename))
    filelist=numpy.array(filelist)
    
    #Remove duplicates
    files=numpy.zeros_like(filelist)
    sclocks=numpy.zeros_like(filelist)
    fileversion=numpy.zeros(len(filelist),dtype='int')    
    for i in range(len(filelist)):
        files[i]=filelist[i][-40:]
        sclocks[i]=filelist[i][-36:-27]
        fileversion[i]=filelist[i][-5:-4]

    keep=numpy.zeros(len(files),dtype='bool')    
    for i in range(len(files)):
        sclock_match=numpy.in1d(sclocks,sclocks[i])
        maxversion=max(fileversion[sclock_match])
        if fileversion[i]==maxversion:
            keep[i]=True
            
    files=files[keep]
    filelist=filelist[keep]
    sclocks=sclocks[keep]
    
    files,unique_index=numpy.unique(files,return_index=True)
    filelist=filelist[unique_index]
    sclocks=sclocks[unique_index]
    return filelist,files

def read_ccs(searchdir,skiprows=0,shots=False,masterlist=None,name_sub_file=None,singlefile=False):#,minsol=0,maxsol=10000,masterlist=None):
    if singlefile is False:
        filelist,files=search_ccs(searchdir)
    if singlefile is True:
        filelist=numpy.array([searchdir])
        files=[filelist[0][-40:]]

    if shots is True:
        file_targets,file_dists,file_amps,nshots=ccam.target_lookup(filelist,masterlist,name_sub_file)
        nshots=numpy.array(nshots,dtype='int')
        sum_shots=numpy.sum(nshots)
    if singlefile is False:
        print 'Reading '+str(len(filelist))+' files...'
    if shots is not True:
        means=numpy.zeros([len(filelist),6144],dtype='float64')
    if shots is True:
        singleshots=numpy.zeros([6144,sum_shots],dtype='float64')
        files_singleshot=numpy.zeros_like([files[0]]*sum_shots)
        shotnums=numpy.zeros([sum_shots])
        rowcount=0
    for i in range(len(filelist)):
        if singlefile is False:
            if numpy.mod(i+1,100)==0:
                print 'Reading file #'+str(i+1)
        
        tempdata=ccam.read_csv(filelist[i],skiprows,labelrow=False)


        wvl=numpy.array(tempdata[:,0],dtype='float')
        if shots is False:        
            means[i,:]=tempdata[:,-1]
        if shots is True:
            shotnums[rowcount:rowcount+nshots[i]]=range(nshots[i])
            files_singleshot[rowcount:rowcount+nshots[i]]=files[i]            
            singleshots[:,rowcount:rowcount+nshots[i]]=tempdata[:,1:-2]
            rowcount=rowcount+nshots[i]
        
#        if i==0:
#            wvl=numpy.array(tempdata[:,0],dtype='float64')
#            if shots is True:                
#                singleshots=numpy.array(tempdata[:,1:-2],dtype='float64')
#                shotnums=numpy.array(range(len(tempdata[:,1:-2])))
#                files_singleshot=numpy.array([files[i]]*len(tempdata[:,1:-2]))
#            medians=numpy.array(tempdata[:,-2],dtype='float64')
#            means=numpy.array(tempdata[:,-1],dtype='float64')
#            
#        if i>0:
#            if shots is True:                
#                singleshots=numpy.vstack([singleshots,numpy.array(tempdata[:,1:-2],dtype='float64')])
#                shotnums=numpy.hstack([shotnums,numpy.array(range(len(tempdata[:,1:-2])))])
#                files_singleshot=numpy.hstack([files_singleshot,numpy.array([files[i]]*len(tempdata[:,1:-2]))])
#
#            medians=numpy.vstack([medians,numpy.array(tempdata[:,-2],dtype='float64')])
#            means=numpy.vstack([means,numpy.array(tempdata[:,-1],dtype='float64')])

    if shots is True:
        singleshots=numpy.transpose(singleshots)
        return singleshots,wvl,files_singleshot,shotnums
    if shots is False:
        return means,wvl,files

def read_single_ccs(filename,skiprows=0,shots=False,masterlist=None,name_sub_file=None):#,minsol=0,maxsol=10000,masterlist=None):
    filetrim=filename[-40]

    if shots is True:
        file_targets,file_dists,file_amps,nshots=ccam.target_lookup(filename,masterlist,name_sub_file)
        nshots=numpy.array(nshots,dtype='int')
        sum_shots=numpy.sum(nshots)
    
    if shots is not True:
        means=numpy.zeros([6144],dtype='float64')
    if shots is True:
        singleshots=numpy.zeros([6144,sum_shots],dtype='float64')
        files_singleshot=numpy.zeros_like([filetrim[0]]*sum_shots)
        shotnums=numpy.zeros([sum_shots])
        rowcount=0

    tempdata=ccam.read_csv(filename,skiprows,labelrow=False)
    
    wvl=numpy.array(tempdata[:,0],dtype='float')
    if shots is False:        
        means=tempdata[:,-1]
    if shots is True:

        shotnums[rowcount:rowcount+nshots]=range(nshots)
        files_singleshot[rowcount:rowcount+nshots]=filetrim            
        singleshots[:,rowcount:rowcount+nshots]=tempdata[:,1:-2]
        rowcount=rowcount+nshots

    if shots is True:
        singleshots=numpy.transpose(singleshots)
        return singleshots,wvl,files_singleshot,shotnums
    if shots is False:
        return means,wvl,filetrim
