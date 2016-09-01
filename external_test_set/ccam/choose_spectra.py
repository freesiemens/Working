# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 14:12:02 2015

@author: rbanderson

This function allows spectra to be restricted to a specified composition range for a given element. 
Optionally, a file can be provided specifying individual spectra that should be removed, regardless of composition

Inputs:
spectra = float array of spectra
spect_index = int array of spectrum indices for each target
comps = float array of target compositions
compindex = the index of comps that corresponds to the element of interest
mincomp = the lower limit of compositions to keep
maxcomp = the upper limit of compositions to keep
removelist = string specifying the path to an optional .csv file that lists individual spectra to remove.
File should have two columns. The first column should have target names, the second column should have the index of the spectrum to remove.
So, to remove the first and third spectrum of AGV2, the file would look like:
AGV2,1
AGV2,3

keepfile = string specifying the path to an optional .csv file that lists the spectra to keep (ALL others are removed)
File should have two columns. The first column should have the index of the spectrum to keep,
(NOTE: For this file, the index should be the index into the full array of spectra, starting at 1, not the 1-5 index for each target)
the second column should have the target names.



Outputs:
spectra_keep = array of spectra that satisfy the constraints on composition and are not listed in the file
names_keep = names of spectra that satisfy the constraints on composition and are not listed in the file
spect_index_keep = indices of spectra that satisfy the constraints on composition and are not listed in the file
comps_keep = = compositions of spectra that satisfy the constraints on composition and are not listed in the file

"""
import numpy
import csv
def choose_spectra(spectra,spect_index,names,comps,compindex,mincomp=0,maxcomp=100,removefile=None,keepfile=None,which_removed=None,linewvl=None,linestrength=None,wvl=None,clustermask=None):

    
   
    #optionally, remove spectra listed in an external file
    if removefile != None:
        #read the list of sample names and spectrum indices from the file
        f=open(removefile,'r')
        data=list(zip(*csv.reader(f)))
        removenames=numpy.array(data[0],dtype='str')
        removeinds=numpy.array(data[1],dtype='int')
        #define an array to hold the indices for each row in the file        
        index=numpy.empty([len(names),len(removenames)])
        for i in range(len(removenames)):
            #for each row, find the indices that correspond to the matching 
            #name AND spectral index
            index[:,i]=(names==removenames[i])&(spect_index==removeinds[i])
        
        names_removed=names[numpy.any(index,axis=1)]
        spect_index_removed=spect_index[numpy.any(index,axis=1)]
        if which_removed:
            with open(which_removed,'w',newline='') as writefile:
                writer=csv.writer(writefile,delimiter=',')
                for i in range(len(names_removed)):
                    writer.writerow([names_removed[i],spect_index_removed[i],'From File'])
            #combine the indices for each row to a single array that indicates which
        #spectra to remove, then invert it to indicate which spectra to keep
        index=numpy.invert(numpy.any(index,axis=1))
       
    
#    if keepfile != None:
#       #read the list of sample names and spectrum indices from the file
#        f=open(keepfile,'r')
#        f.readline()
#        f.readline()
#        data=list(zip(*csv.reader(f)))
#        keepinds=numpy.array(data[0],dtype='int')
#        keepinds=keepinds-1.0
#        index3=numpy.in1d(range(0,len(names)),keepinds)
#        index=numpy.vstack((index,index3))
#        index=numpy.all(index,axis=0)
#        
#    if linewvl!=None:
#
#        bins=numpy.squeeze((wvl>linewvl[0])&(wvl<linewvl[1]))
#        linesums=numpy.sum(spectra[:,bins],axis=1)
#        print(numpy.max(linesums))
#
#        index4=(linesums>linestrength[0])&(linesums<linestrength[1])
#        index=numpy.vstack((index,index4))
#        index=numpy.all(index,axis=0)
        
      #fill the new variables with the data to keep
    spectra_keep=spectra[index]
    names_keep=names[index]
    spect_index_keep=spect_index[index]
    comps_keep=comps[index,:]        
  
   #define index where composition is within the specified range
    index2=numpy.squeeze((comps_keep[:,compindex]>mincomp)&(comps_keep[:,compindex]<maxcomp) )
        
    
    names_removed=names_keep[numpy.invert(index2)]
    spect_index_removed=spect_index_keep[numpy.invert(index2)]
    if which_removed:
        with open(which_removed,'a',newline='') as writefile:
            writer=csv.writer(writefile,delimiter=',')
            for i in range(len(names_removed)):
                writer.writerow([names_removed[i],spect_index_removed[i],'Out of Range'])    
    spectra_keep=spectra_keep[index2]
    names_keep=names_keep[index2]
    spect_index_keep=spect_index_keep[index2]
    comps_keep=comps_keep[index2,:]        
  
#    names_removed=names[numpy.invert(index)]
#    spect_index_removed=spect_index[numpy.invert(index)]
#    
#    if which_removed != None:
#        with open(which_removed,'w',newline='') as writefile:
#            writer=csv.writer(writefile,delimiter=',',)
#            for i in range(len(names_removed)):
#                writer.writerow([names_removed[i],spect_index_removed[i]])
    
             
    return spectra_keep,names_keep,spect_index_keep,comps_keep
    