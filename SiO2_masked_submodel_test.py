# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 15:21:25 2015

@author: rbanderson
"""
#Change to the working directory
import os
os.chdir(r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working')

import ccam
#Specify where the database file containing compositions and spectra is
dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected.csv'
#specify where the list of spectra to remove is
removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'
#If you have one, specify where the file defining the cross validation folds is (default is to not use one and generate folds randomly)
foldfile=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\folds.csv'
#specify where the file describing what parts of the spectrum to mask is
maskfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\mask_minors_noise_FeSi_UV.csv'
#If you have one, specify the location of the file listing spectra to keep in the model (default is to not use this and just use the remove list)
keepfile=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\Si_full_included.csv'
#Specify where to write all output files
outpath='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Output\\SiO2\\'
#Specify directory containing cal target spectra
cal_dir=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_team\CalTarget 95A'
#specify where to find the master list file
masterlist_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_misc\MASTERLIST.csv'
#Location of a file with target name substitutions (this is used primarily to substitute cal target names: Cal Target 1 --> Macusanite)
name_sub_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv'

#Which element do you want to build models for?
which_elem='SiO2'

#How many folds do you want to use?
nfolds=5
#which fold do you want to use as the test set?
testfold=2
#How many componenets should be used in each model?
nc=20
#What seed should be used for the random number generater that randomly assigns samples to folds (using a seed allows the folds to be random but reproducible)
seed=100
#What algorithm to use (mlpy or sklearn - results are the same)
plstype='sklearn'



##calculate full model#
#If you have a remove file specific to this submodel, enter it here (e.g. for outlier removal)
#removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist_SiO2_0-100.csv'
#set the range of compositions in the submodel
mincomp=0
maxcomp=100
#Set the normalization  for the submodel
normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

#Set the normalization  for the submodel
normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)


#calculate mid model
#If you have a remove file specific to this submodel, enter it here (e.g. for outlier removal)
#removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist_SiO2_30-70.csv'
#set the range of compositions in the submodel
mincomp=30
maxcomp=70

#Set the normalization  for the submodel
normtype=3
#Run the calibration and generate the model
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

#Set the normalization  for the submodel
normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)


#calculate low model
#If you have a remove file specific to this submodel, enter it here (e.g. for outlier removal)
#removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist_SiO2_0-50.csv'
#set the range of compositions in the submodel
mincomp=0
maxcomp=50

#Set the normalization  for the submodel
normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

#Set the normalization  for the submodel
normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)


#Calculate high model
#If you have a remove file specific to this submodel, enter it here (e.g. for outlier removal)
#removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist_SiO2_60-100.csv'
#set the range of compositions in the submodel
mincomp=60
maxcomp=100

#Set the normalization  for the submodel
normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)


#Set the normalization  for the submodel
normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)


