# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 15:24:36 2015

@author: rbanderson
"""
import ccam
import numpy
import sys

def prepare_data(dbfile,maskfile,which_elem,outpath,plstype,nc,normtype,mincomp=0,maxcomp=100,keepfile=None,removefile=None,foldfile=None,nfolds=None):
    print 'Reading database'
    sys.stdout.flush()
    spectra,comps,spect_index,names,labels,wvl=ccam.read_db(dbfile,compcheck=True)
    oxides=labels[2:]
    compindex=numpy.where(oxides==which_elem)[0]
    
    print 'Choosing spectra'
    which_removed=outpath+which_elem+'_'+plstype+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_removed.csv'
    spectra,names,spect_index,comps=ccam.choose_spectra(spectra,spect_index,names,comps,compindex,mincomp=mincomp,maxcomp=maxcomp,keepfile=keepfile,removefile=removefile,which_removed=which_removed)
    
    print 'Masking spectra'
    spectra,wvl=ccam.mask(spectra,wvl,maskfile)
    
    print 'Normalizing spectra'
    spectra=ccam.normalize(spectra,wvl,normtype=normtype)
    
     print 'Assigning Folds'
        if foldfile!=None:
            #if a fold file is specified, use it
            folds=ccam.folds(foldfile,names)
        else:
            #otherwise, define random folds
            folds=ccam.random_folds(names,nfolds)
        names_nofold=names[(folds==0)]
        spect_index_nofold=spect_index[(folds==0)]
        #write a file containing the samples not assigned to folds
        with open(which_removed,'ab') as writefile:
            writer=csv.writer(writefile,delimiter=',',)
            for i in range(len(names_nofold)):
                writer.writerow([names_nofold[i],spect_index_nofold[i],'No Fold'])
            
    
    return spectra,comps,spect_index,names,labels,wvl,compindex,folds
    