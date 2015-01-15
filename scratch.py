# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 10:24:05 2015

@author: rbanderson
"""
import ccam_read_db as read_db
import ccam_mask as mask
import ccam_normalize as normalize
import ccam_choose_spectra as choose_spectra
import sys

dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\full_db.csv'
removelist='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\removelist_test.csv'
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



