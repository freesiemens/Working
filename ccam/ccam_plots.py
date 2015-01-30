# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 16:14:20 2015

@author: rbanderson
"""
import matplotlib.pyplot as plot
import numpy
import csv

def ccam_plot_RMSE(RMSECV,RMSEP,RMSEC,plot_title,outfile):
    plot.plot(range(1,len(RMSECV)+1),RMSECV,color='r',linewidth=2.0,label='RMSECV (folds)')
    plot.plot(range(1,len(RMSEC)+1),RMSEC,color='b',linewidth=2.0,label='RMSEC (training set)')
    plot.plot(range(1,len(RMSEP)+1),RMSEP,color='g',linewidth=2.0,label='RMSEP (test set)')
    plot.legend()
    plot.title(plot_title)
    plot.xlabel('# of Components')
    plot.ylabel('wt.%')
    plot.xticks(range(1,len(RMSEC)+1))
    fig=plot.gcf()
    fig.set_dpi(600)      
    fig.set_size_inches(11,8.5)
    fig.savefig(outfile)
    fig.clf()

def ccam_plot_1to1(truecomps,predicts,plot_title,labels,colors,markers,outfile,comprange=[0,100]):
    plot.plot([0,100],[0,100],color='k',linewidth=2.0,label='1:1 line')
    for i in range(len(truecomps)):
        plot.plot(truecomps[i],predicts[i],color=colors[i],label=labels[i],marker=markers[i],linewidth=0)
    plot.xlabel('wt.%')
    plot.ylabel('Prediction (wt.%)')
    plot.xlim(comprange)
    plot.ylim(comprange)
    plot.legend(loc=2)
    plot.title(plot_title)
    fig=plot.gcf()
    fig.set_dpi(600)
    fig.set_size_inches(11,8.5)
    fig.savefig(outfile)
    plot.close()

    
def readpredicts(filename,nc):
    f=open(filename,'rb')  #open the file
    cols=f.readline() #read the first line
    cols=numpy.array(cols.split(',')[1:]) 
    
    data=zip(*csv.reader(f))
    samples=numpy.array(data[0],dtype='string')
    spect_indexes=numpy.array(data[1],dtype='int')
    folds=numpy.array(data[2],dtype='int')
    truecomps=numpy.array(data[3],dtype='float')
    predicts=numpy.array(data[numpy.array(numpy.where(cols==str(nc)))],dtype='float')
    
    return predicts,samples,truecomps,folds,spect_indexes