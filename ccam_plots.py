# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 16:14:20 2015

@author: rbanderson
"""
import matplotlib.pyplot as plot
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
