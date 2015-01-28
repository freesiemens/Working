# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 15:21:25 2015

@author: rbanderson
"""
import ccam_pls_cal

dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\full_db_mars_corrected.csv'
removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\removelist.csv'
foldfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\folds.csv'
maskfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\mask_minors_noise.csv'
keepfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\Si_full_included.csv'
outpath='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Output\\'


normtype=3
which_elem='SiO2'
mincomp=0
maxcomp=100
testfold=2
nc=20
plstype='mlpy'

#calculate full model
ccam_pls_cal.ccam_pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp)

normtype=1
ccam_pls_cal.ccam_pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp)

#calculate low model
maxcomp=40
normtype=1
keeplist='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\Si_low_included.csv'
ccam_pls_cal.ccam_pls_cal(dbfile,foldfile,maskfile,keeplist,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp)

normtype=3
ccam_pls_cal.ccam_pls_cal(dbfile,foldfile,maskfile,keeplist,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp)

#Calculate medium model
mincomp=20
maxcomp=65
normtype=1
keeplist='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\Si_medium_included.csv'
ccam_pls_cal.ccam_pls_cal(dbfile,foldfile,maskfile,keeplist,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp)

normtype=3
ccam_pls_cal.ccam_pls_cal(dbfile,foldfile,maskfile,keeplist,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp)

#Calculate high model
mincomp=55
maxcomp=100
normtype=1
keeplist='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\Si_high_included.csv'
ccam_pls_cal.ccam_pls_cal(dbfile,foldfile,maskfile,keeplist,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp)

normtype=3
ccam_pls_cal.ccam_pls_cal(dbfile,foldfile,maskfile,keeplist,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp)
