# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 12:31:34 2015

@author: rbanderson
"""
import numpy
import ccam
import sys
import sklearn.cluster as cluster
#def kmeans_db(k,dbfile,maskfile,normtype,mincomp=0,maxcomp=100,clustertype='spectra',which_elem=None,keepfile=None,removefile=None):
dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\full_db_mars_corrected.csv'
removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\removelist.csv'
maskfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\mask_minors_noise.csv'
clustertype='spectra'
which_elem='MgO'
mincomp=0
maxcomp=100
k=3
keepfile=None
normtype=3

print 'Reading database'
sys.stdout.flush()
spectra,comps,spect_index,names,labels,wvl=ccam.read_db(dbfile,compcheck=True)
oxides=labels[2:]
compindex=numpy.where(oxides==which_elem)[0]

print 'Choosing spectra'
which_removed='kmeans_removed.csv'
spectra,names,spect_index,comps=ccam.choose_spectra(spectra,spect_index,names,comps,compindex,mincomp=mincomp,maxcomp=maxcomp,keepfile=keepfile,removefile=removefile,which_removed=which_removed)

print 'Masking spectra'
spectra,wvl=ccam.mask(spectra,wvl,maskfile)

print 'Normalizing spectra'
spectra=ccam.normalize(spectra,wvl,normtype=normtype)

kmeans=cluster.KMeans(k,n_init=10)
if clustertype=='spectra':
    kmeans.fit(spectra)
    k_inds=kmeans.predict(spectra)
#        return k_inds
if clustertype=='comp':
    kmeans.fit(comps[:,(oxides!='MnO')])
    k_inds=kmeans.predict(comps[:,(oxides!='MnO')])
 #       return k_inds
print blah