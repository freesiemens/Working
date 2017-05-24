# -*- coding: utf-8 -*-
"""
Created on Mon Mar 09 12:48:23 2015

@author: rbanderson
"""
import csv
import numpy
def read_spectra(filename):
    data=[]
    with open(filename,'rb') as csvfile:

        csvreader=csv.reader(csvfile,delimiter=',')        
        for row in csvreader:
            data.append(row) 
    data=numpy.array(data)
    labels=data[0,1:]
    data=data[1:,:]
    data=numpy.array(data,dtype='float64')
    wvl=data[:,0]
    data=numpy.transpose(data[:,1:])
    
    return data,wvl,labels    