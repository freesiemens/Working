# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 15:21:25 2015

@author: rbanderson
"""

import os
os.chdir(r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\ccam')
import numpy
import ccam
import sklearn.cluster as cluster
dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\full_db_mars_corrected.csv'
removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\removelist.csv'
foldfile=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\folds.csv'
maskfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\mask_minors_noise.csv'
keepfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\Mg_full_included.csv'
outpath='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Output\\'
cal_dir=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_team\CalTarget 95A'
masterlist_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_misc\MASTERLIST.csv'
name_sub_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Input\target_name_subs.csv'

normtype=3
which_elem='MgO'
mincomp=0
maxcomp=100
nfolds=5
testfold=2
nc=5
plstype='mlpy'
k=3

#print 'Reading database'
#sys.stdout.flush()
#spectra,comps,spect_index,names,labels,wvl=ccam.read_db(dbfile,compcheck=True)
#oxides=labels[2:]
#compindex=numpy.where(oxides==which_elem)[0]
#
#print 'Choosing spectra'
#which_removed=outpath+which_elem+'_'+plstype+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_removed.csv'
#spectra,names,spect_index,comps=ccam.choose_spectra(spectra,spect_index,names,comps,compindex,mincomp=mincomp,maxcomp=maxcomp,keepfile=keepfile,removefile=removefile,which_removed=which_removed)
#
#print 'Masking spectra'
#spectra,wvl=ccam.mask(spectra,wvl,maskfile)
#
#print 'Normalizing spectra'
#spectra=ccam.normalize(spectra,wvl,normtype=normtype)
# 
#km=cluster.KMeans(n_clusters=k,n_init=100)
#km.fit(spectra)
#clusters=km.predict(spectra)
#
#   

#calculate full model
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds)

#for i in range(k):
#    ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,clusters=(clusters==i))
