# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 16:14:20 2015

@author: rbanderson
"""
import matplotlib.pyplot as plot
from matplotlib import rcParams
import numpy
import csv


def RMSE(RMSECV,RMSEP,RMSEC,plot_title,outfile,RMSEP_cals=None,RMSEP_good=None):


    plot.plot(range(1,len(RMSECV)+1),RMSECV,color='r',linewidth=2.0,label='RMSECV (folds)')
    plot.plot(range(1,len(RMSEC)+1),RMSEC,color='b',linewidth=2.0,label='RMSEC (training set)')
    plot.plot(range(1,len(RMSEP)+1),RMSEP,color='g',linewidth=2.0,label='RMSEP (test set)')
    if RMSEP_cals!=None:
       
        if numpy.max(RMSEP_cals[0])>0:        
            plot.plot(range(1,len(RMSEP_cals[0])+1),RMSEP_cals[0],color='m',linewidth=2.0,linestyle='-',label='RMSEP (KGa-MedS)')
        if numpy.max(RMSEP_cals[1])>0:        
            plot.plot(range(1,len(RMSEP_cals[1])+1),RMSEP_cals[1],color='m',linewidth=2.0,linestyle='--',label='RMSEP (Macusanite)')
        if numpy.max(RMSEP_cals[2])>0:
            plot.plot(range(1,len(RMSEP_cals[2])+1),RMSEP_cals[2],color='k',linewidth=2.0,linestyle='-',label='RMSEP (NAU2HIS)')
        if numpy.max(RMSEP_cals[3])>0:
            plot.plot(range(1,len(RMSEP_cals[3])+1),RMSEP_cals[3],color='k',linewidth=2.0,linestyle='--',label='RMSEP (NAU2LOS)')
        if numpy.max(RMSEP_cals[4])>0:
            plot.plot(range(1,len(RMSEP_cals[4])+1),RMSEP_cals[4],color='k',linewidth=2.0,linestyle=':',label='RMSEP (NAU2MEDS)')
        if numpy.max(RMSEP_cals[5])>0:
            plot.plot(range(1,len(RMSEP_cals[5])+1),RMSEP_cals[5],color='c',linewidth=2.0,linestyle='-',label='RMSEP (Norite)')
        if numpy.max(RMSEP_cals[6])>0:
            plot.plot(range(1,len(RMSEP_cals[6])+1),RMSEP_cals[6],color='c',linewidth=2.0,linestyle='--',label='RMSEP (Picrite)')
        if numpy.max(RMSEP_cals[7])>0:
            plot.plot(range(1,len(RMSEP_cals[7])+1),RMSEP_cals[7],color='c',linewidth=2.0,linestyle=':',label='RMSEP (Shergottite)')
        plot.plot(range(1,len(RMSEP_cals[8])+1),RMSEP_cals[8],color='k',linewidth=4.0,linestyle='-',label='RMSEP (Cal Targets In Range)')
        plot.plot(range(1,len(RMSEP_cals[8])+1),RMSEP_cals[8],color='y',linewidth=3.5,linestyle='-',label='RMSEP (Cal Targets In Range)')
    if RMSEP_good is not None:

        plot.plot(range(1,len(RMSEP_good)+1),RMSEP_good,color='k',linewidth=4.0,linestyle='-',label='RMSEP (All cal targets but Macusanite and KGA)')
    #plot.ylim(bottom=0)
       
        
        
    plot.legend()
    plot.title(plot_title)
    
    #plot.ylim([numpy.min([RMSECV,RMSEP,RMSEC]),numpy.max([RMSECV,RMSEP,RMSEC])])
    #if RMSEP_cals!=None:
    #    plot.ylim([numpy.min(numpy.vstack((RMSECV,RMSEP,RMSEC,RMSEP_cals))),numpy.max(numpy.vstack((RMSECV,RMSEP,RMSEC,RMSEP_cals)))])
    plot.xlabel('# of Components')
    plot.ylabel('wt.%')
    plot.xticks(range(1,len(RMSEC)+1))
    fig=plot.gcf()
    #fig.set_dpi(600)      
    fig.set_size_inches(11,8.5)
    fig.savefig(outfile)
    fig.clf()

def Plot1to1(truecomps,predicts,plot_title,labels,colors,markers,outfile,xminmax=[0,100],yminmax=[0,100],ylabel='Prediction (wt.%)',xlabel='Actual (wt.%)',one_to_one=True,dpi=300):
    rcParams['mathtext.default'] = 'regular' 
    rcParams['xtick.labelsize'] = 24
    rcParams['ytick.labelsize'] = 24
    
    if one_to_one:
        plot.plot([0,100],[0,100],color='k',linewidth=2.0,label='1:1 line')
    if isinstance(truecomps,list):
        for i in range(len(truecomps)):
            plot.plot(truecomps[i],predicts[i],color=colors[i],label=labels[i],marker=markers[i],linewidth=0)
    else:
        plot.plot(truecomps,predicts,color=colors,label=labels,marker=markers,linewidth=0)
    plot.xlabel(xlabel,fontsize=24)
    plot.ylabel(ylabel,fontsize=24)
    plot.xlim(xminmax)
    plot.ylim(yminmax)
    plot.legend(loc=0,fontsize=20)
    plot.title(plot_title,fontsize=28)
    fig=plot.gcf()
    fig.set_size_inches(11,8.5)
    
    fig.savefig(outfile,dpi=dpi)
    plot.close()

    
def readpredicts(filename,nc):
    f=open(filename,'r')  #open the file
    cols=f.readline() #read the first line
    cols=numpy.array(cols.split(',')[1:]) 
    cols[-1]=cols[-1].replace('\r','')
    cols[-1]=cols[-1].replace('\n','')
    
    data=list(zip(*csv.reader(f)))
    samples=numpy.array(data[0],dtype='str')
    spect_indexes=numpy.array(data[1],dtype='int')
    folds=numpy.array(data[2])
    truecomps=numpy.array(data[3],dtype='float')
    colmatch=numpy.squeeze(numpy.array(numpy.where(cols==str(nc))))
    predicts=numpy.array(data[colmatch+1],dtype='float')
    
    return predicts,samples,truecomps,folds,spect_indexes