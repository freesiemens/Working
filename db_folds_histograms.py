# -*- coding: utf-8 -*-
"""
Created on Fri May 15 13:22:25 2015

@author: rbanderson
"""
import ccam
import matplotlib.pyplot as plot
import numpy
import csv

outpath='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Output\\'
dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected.csv'
ryans_labels = numpy.genfromtxt('C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Database\\CCAM_database_for_strat_partition_noduplicates.csv', delimiter=',')[1:, 1:]
spectra,comps,spect_index,names,labels,wvl=ccam.read_db(dbfile,compcheck=True,n_elems=9)
comps=numpy.delete(comps,4,axis=1)
labels=numpy.delete(labels,6)
names_unique,uniqueindex=numpy.unique(names,return_index=True)
comps_unique=comps[uniqueindex,:]
seed=2
nfolds=5
folds=ccam.random_folds(names_unique,nfolds,seed=seed)
nhours=.1111

for i in range(0,8):
    
    comps_unique_sorted=comps_unique[comps_unique[:,i].argsort()]
    names_unique_sorted=names_unique[comps_unique[:,i].argsort()]
    folds_sorted=range(1,nfolds+1)
    while len(folds_sorted)<len(names_unique_sorted):
        folds_sorted.extend(range(1,nfolds+1))
    folds_sorted=numpy.array(folds_sorted[:len(names_unique_sorted)-len(folds_sorted)],dtype='int')
    
    print labels[i+2]
    for j in range(1,6):
        print 'Fold '+str(j)
        plot.subplot(2,3,j)        
        plot.hist(comps_unique_sorted[folds_sorted==j,i],bins=20,range=[min(comps_unique[:,i]),max(comps_unique[:,i])])
        plot.xlabel(labels[i+2]+' wt.%')
        plot.ylabel('# of samples')
        plot.title('Sort Fold '+str(j)+' - '+labels[i+2])
    plot.tight_layout()
    fig=plot.gcf()
    fig.savefig(outpath+labels[i+2]+'_sortfold_hist.png')
    fig.clf()    
    with open(outpath+labels[i+2]+'_sortfold.csv','wb') as writefile:
            writer=csv.writer(writefile,delimiter=',')
            for k in range(0,len(names_unique_sorted)):
                writer.writerow([names_unique_sorted[k],folds_sorted[k]])
#splitter_folds=numpy.genfromtxt(outpath+'splitter_folds_'+str(nhours)+'.csv',delimiter=',',dtype='int')[:,1]

#splitter_perm,splitter_folds=ccam.splitter.multitask_stratified_splitter(comps_unique,nfolds,names_unique,hours=nhours,fname=outpath+'splitter_folds_'+str(nhours)+'.csv',load=False)
##ccam.splitter.evaluate_split(comps_unique,nfolds)
##ccam.splitter.evaluate_split(comps_unique[splitter_perm],nfolds)
#
#
#for i in range(0,8):
#    print labels[i+2]
#    for j in range(1,6):
#        print 'Splitter Fold '+str(j)
#        plot.subplot(2,3,j)        
#        plot.hist(comps_unique[splitter_folds==j,i],bins=20,range=[min(comps_unique[:,i]),max(comps_unique[:,i])])
#        plot.xlabel(labels[i+2]+' wt.%')
#        plot.ylabel('# of samples')
#        plot.title('Splitter Fold '+str(j)+' - '+labels[i+2])
#    plot.tight_layout()
#    fig=plot.gcf()
#    fig.savefig(outpath+labels[i+2]+'_splitfold_hist_'+str(nhours)+'_hours.png')
#    fig.clf()
#    
#for i in range(0,8):
#    print labels[i+2]
#    for j in range(1,6):
#        print 'Fold '+str(j)
#        plot.subplot(2,3,j)        
#        plot.hist(comps_unique[folds==j,i],bins=20,range=[min(comps_unique[:,i]),max(comps_unique[:,i])])
#        plot.xlabel(labels[i+2]+' wt.%')
#        plot.ylabel('# of samples')
#        plot.title('Fold '+str(j)+' - '+labels[i+2])
#    plot.tight_layout()
#    fig=plot.gcf()
#    fig.savefig(outpath+labels[i+2]+'_randfold_hist_seed'+str(seed)+'.png')
#    fig.clf()
#      
print 'stop'

