# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 11:18:44 2015

@author: rbanderson
"""
import numpy
import csv

def read_csv_cols(filename,skiprows,labelrow=True):
    f=open(filename,'rb')  #open the file
    for i in range(skiprows):
        f.readline()    
    if labelrow==True:
        labels=f.readline() #read the label row
        labels=numpy.array(labels.split(',')) #split it on commas and convert to a string array
        data=zip(*csv.reader(f))
        f.close()
        return data,labels
    else:
        data=zip(*csv.reader(f)) 
        f.close()
        return data