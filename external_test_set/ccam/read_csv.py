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
        #print temp
    if labelrow==True:
        labels=f.readline() #read the label row
        #print labels
        labels=numpy.array(labels.strip().split(',')) #split it on commas and convert to a string array
        data=[]
        for row in f:
            #print row
            if skipsym!=None:
                if not skipsym in str(row):
                    #print row.split(',')
                    if row.strip():
                        data.append(row.strip().split(','))
            else:
                if row.strip():
                    data.append(row.strip().split(','))
        f.close()
        data=numpy.array(data)
        return data,labels
    else:
           
        data=[]
        for row in f:
            if skipsym!=None:
                if not skipsym in str(row):            
                    if row.strip():
                        data.append(row.strip().split(','))
            else:
                if row.strip():
                    data.append(row.strip().split(','))
        f.close()
        data=numpy.array(data)
        return data