# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 15:21:25 2015

@author: rbanderson
"""
import ccam

dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\full_db_mars_corrected.csv'
removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\removelist.csv'
foldfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\folds.csv'
maskfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\mask_minors_noise.csv'
keepfile=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\Si_full_included.csv'
outpath='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Output\\'


normtype=3
which_elem='MgO'
mincomp=0
maxcomp=100
testfold=2
nc=20
plstype='mlpy'

#calculate full model
ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp)

normtype=1
ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp)

#calculate low model
maxcomp=3
normtype=1
keeplist=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\Si_low_included.csv'
ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp)

normtype=3
ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp)

#Calculate medium model
mincomp=2
maxcomp=12
normtype=1
keeplist=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\Si_medium_included.csv'
ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp)

normtype=3
ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp)

#Calculate high model
mincomp=10
maxcomp=100
normtype=1
keeplist=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\Si_high_included.csv'
ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp)

normtype=3
ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp)
