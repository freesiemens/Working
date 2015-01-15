# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 10:24:05 2015

@author: rbanderson
"""
import ccam_read_db as read_db
import ccam_mask as mask
import ccam_normalize as normalize
import ccam_choose_spectra as choose_spectra
import ccam_folds as folds
import sys
import csv
import numpy
nooutliers='C:\\Users\\rbanderson\\IDLWorkspace82\\PLS1_fold\\database_input\\goodcomps_20130328_noduplicates_indexed Outliers.csv'
f=open(nooutliers,'rb')
nooutlier_data=zip(*csv.reader(f))
nooutlier_names=numpy.hstack((numpy.array(nooutlier_data[0]),numpy.array(nooutlier_data[2]),numpy.array(nooutlier_data[4]),numpy.array(nooutlier_data[6]),numpy.array(nooutlier_data[8]),numpy.array(nooutlier_data[10]),numpy.array(nooutlier_data[12]),numpy.array(nooutlier_data[14]),numpy.array(nooutlier_data[16])))
nooutlier_indices=numpy.hstack((numpy.array(nooutlier_data[1]),numpy.array(nooutlier_data[3]),numpy.array(nooutlier_data[5]),numpy.array(nooutlier_data[7]),numpy.array(nooutlier_data[9]),numpy.array(nooutlier_data[11]),numpy.array(nooutlier_data[13]),numpy.array(nooutlier_data[15]),numpy.array(nooutlier_data[17])))
nooutlier_combined=numpy.core.defchararray.add(nooutlier_names,nooutlier_indices)

yesoutliers='C:\\Users\\rbanderson\\IDLWorkspace82\\PLS1_fold\\database_input\\goodcomps_20130328_noduplicates_indexed.csv'
f=open(yesoutliers,'rb')
yesoutlier_data=zip(*csv.reader(f))
yesoutlier_names=numpy.hstack((numpy.array(yesoutlier_data[0]),numpy.array(yesoutlier_data[2]),numpy.array(yesoutlier_data[4]),numpy.array(yesoutlier_data[6]),numpy.array(yesoutlier_data[8]),numpy.array(yesoutlier_data[10]),numpy.array(yesoutlier_data[12]),numpy.array(yesoutlier_data[14]),numpy.array(yesoutlier_data[16])))
yesoutlier_indices=numpy.hstack((numpy.array(yesoutlier_data[1]),numpy.array(yesoutlier_data[3]),numpy.array(yesoutlier_data[5]),numpy.array(yesoutlier_data[7]),numpy.array(yesoutlier_data[9]),numpy.array(yesoutlier_data[11]),numpy.array(yesoutlier_data[13]),numpy.array(yesoutlier_data[15]),numpy.array(yesoutlier_data[17])))
yesoutlier_combined=numpy.core.defchararray.add(yesoutlier_names,yesoutlier_indices)

yesoutlier_names_uniq=numpy.unique(yesoutlier_names)
nooutlier_names_uniq=numpy.unique(nooutlier_names)

dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\full_db.csv'
removelist='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\removelist.csv'
foldfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\folds.csv'
maskfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\mask_minors_noise.csv'

print 'Reading database'
sys.stdout.flush()
spectra,comps,spect_index,names,labels,wvl=read_db.ccam_read_db(dbfile,compcheck=True)

print 'Masking spectra'
spectra_masked,wvl_masked=mask.ccam_mask(spectra,wvl,maskfile)

print 'Normalizing spectra'
spectra_norm=normalize.ccam_normalize(spectra_masked,wvl_masked,normtype=3)

print 'Choosing spectra'
compindex=0
spectra_keep,names_keep,spect_index_keep,comps_keep=choose_spectra.ccam_choose_spectra(spectra_norm,spect_index,names,comps,compindex,mincomp=0,maxcomp=100,removelist=removelist)

print 'Assigning Folds'
folds=folds.ccam_folds(foldfile,names_keep)

print 'Stop'

