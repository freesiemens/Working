# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 11:18:44 2015

@author: rbanderson
"""
import numpy

def read_csv(filename,skiprows,labelrow=True,skipsym='#'):
    
    f=open(filename,'r')  #open the file
    for i in range(skiprows):
        f.readline()    
    if labelrow==True:
        labels=f.readline() #read the label row
        labels=numpy.array(labels.split(',')) #split it on commas and convert to a string array
        data=[]
        for row in f:
            if row[0] is not skipsym:            
                data.append(row.split(','))
            
        f.close()
        data=numpy.array(data)
        return data,labels
    else:
           
        data=[]
        for row in f:
            if row[0] is not skipsym:            
                data.append(row.split(','))
            
        f.close()
        data=numpy.array(data)
        return data