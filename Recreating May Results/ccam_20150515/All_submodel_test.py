# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 14:14:36 2015

@author: rbanderson
"""

#Change to the working directory
import os
os.chdir(r'C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\Recreating May Results\ccam_20150515')
import ccam

#Specify where the database file containing compositions and spectra is
dbfile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected.csv'
#specify where the list of spectra to remove is

removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'

#If you have one, specify where the file defining the cross validation folds is (default is to not use one and generate folds randomly)
foldfile=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\folds.csv'
#specify where the file describing what parts of the spectrum to mask is
maskfile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\mask_minors_noise.csv'
#If you have one, specify the location of the file listing spectra to keep in the model (default is to not use this and just use the remove list)
keepfile=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\Si_full_included.csv'

#Specify directory containing cal target spectra
cal_dir=r'E:\ChemCam\ops_ccam_team\CalTarget 95A'
#specify where to find the master list file
masterlist_file=r'E:\ChemCam\ops_ccam_misc\MASTERLIST.csv'
#Location of a file with target name substitutions (this is used primarily to substitute cal target names: Cal Target 1 --> Macusanite)
name_sub_file=r'C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv'



##############################  SiO2 #####################################

#Which element do you want to build models for?
which_elem='SiO2'

#Specify where to write all output files
outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Final\\'#'C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Final\\'

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
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'
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
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'
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

removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist_SiO2_0-50.csv'
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
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'
#set the range of compositions in the submodel
mincomp=60
maxcomp=100

#Set the normalization  for the submodel
normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)


#Set the normalization  for the submodel
normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)


###############################  TiO2 #####################################
dbfile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected_dopedTiO2.csv'
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'
maskfile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\mask_minors_noise.csv'


keepfile=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\Si_full_included.csv'

name_sub_file=r'C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv'


which_elem='TiO2'
outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Final\\'

mincomp=0
maxcomp=100
nfolds=5
testfold=2
nc=30
seed=100
plstype='sklearn'

#Calculate high model
foldfile=None
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist_TiO2_doped_3-100.csv'
mincomp=3
maxcomp=100
normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

##calculate full model
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist_TiO2_doped_0-100.csv'
foldfile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\folds_TiO2_doped_0-100.csv'
mincomp=0
maxcomp=100
normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

#calculate med model

removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist_TiO2_doped_1-5.csv'
foldfile=None
mincomp=1
maxcomp=5
normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

#calculate low model
foldfile=None
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'
mincomp=0
maxcomp=2
normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)
##############################  Al2O3 #####################################
dbfile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected.csv'
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'
foldfile=None#'C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\folds.csv'
maskfile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\mask_minors_noise.csv'

keepfile=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\Si_full_included.csv'

name_sub_file=r'C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv'


which_elem='Al2O3'
outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Final\\'

mincomp=0
maxcomp=100
nfolds=5
testfold=2
nc=20
seed=100
plstype='sklearn'


##calculate full model

removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist_Al2O3_0-100.csv'

normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

#Calculate high model
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist_Al2O3_20-100.csv'
mincomp=20
maxcomp=100
normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)


#calculate low model
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist_Al2O3_0-12.csv'
mincomp=0
maxcomp=12
normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

#calculate med model
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist_Al2O3_10-25.csv'
mincomp=10
maxcomp=25

normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)


##############################  FeOT #####################################
dbfile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected.csv'
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'
foldfile=None#'C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\folds.csv'
maskfile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\mask_minors_noise.csv'


keepfile=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\Si_full_included.csv'
name_sub_file=r'C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv'


which_elem='FeOT'
outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Final\\'

mincomp=0
maxcomp=100
nfolds=5
testfold=2
nc=30
seed=100
plstype='sklearn'


#calculate full model
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist_FeOT_0-100.csv'

normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

#Calculate high model
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist_FeOT_0-15.csv'
mincomp=15
maxcomp=100
normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)


#calculate low model
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist_FeOT_0-15.csv'
mincomp=0
maxcomp=15
normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

#calculate med model
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist_FeOT_5-25.csv'
mincomp=5
maxcomp=25

normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)


##############################  MgO #####################################

dbfile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected.csv'
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'
foldfile=None#'C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\folds.csv'
maskfile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\mask_minors_noise.csv'


keepfile=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\Si_full_included.csv'

name_sub_file=r'C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv'



which_elem='MgO'
outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Final\\'

mincomp=0
maxcomp=100
nfolds=5
testfold=2
nc=20
seed=100
plstype='sklearn'


#calculate full model
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'
normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

#Calculate high model
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'
mincomp=8
maxcomp=100
normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)


#calculate low model
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'
mincomp=0
maxcomp=3.5
normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

#calculate med model
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'
mincomp=0
maxcomp=20

normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)


##############################  CaO #####################################
dbfile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected.csv'
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'
foldfile=None#'C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\folds.csv'
maskfile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\mask_minors_noise.csv'

keepfile=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\Si_full_included.csv'

name_sub_file=r'C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv'

normtype=3
which_elem='CaO'
outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Final\\'

nfolds=5
testfold=2
nc=30
seed=100
plstype='sklearn'

#calculate low model
mincomp=0
maxcomp=7
normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

#calculate full model
mincomp=0
maxcomp=42
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)
#
normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

##Calculate high model
mincomp=30
maxcomp=100
normtype=1
#
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)
#
normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)
#


#calculate med model
mincomp=0
maxcomp=15

normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)


##############################  Na2O #####################################
dbfile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected.csv'
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'
foldfile=None#'C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\folds.csv'
maskfile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\mask_minors_noise.csv'
keepfile=None#'C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\Si_full_included.csv'

name_sub_file=r'C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv'

normtype=3
which_elem='Na2O'
outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Final\\'

mincomp=0
maxcomp=100
nfolds=5
testfold=2
nc=20
seed=101
plstype='sklearn'


#calculate full model
normtype=3
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist_Na2O_0-100.csv'

ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)



##############################  K2O #####################################
dbfile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected.csv'
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'
foldfile=None#'C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\folds.csv'
maskfile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\mask_minors_noise.csv'
keepfile=None#'C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\Si_full_included.csv'

name_sub_file=r'C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv'

normtype=3
which_elem='K2O'
outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Final\\'

mincomp=0
maxcomp=100
nfolds=5
testfold=2
nc=20
seed=100
plstype='sklearn'

#calculate full model
normtype=3

removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist_Na2O_0-100.csv'

ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

#Calculate high model
mincomp=1.5
maxcomp=100
normtype=1

removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist_Na2O_3.5-100.csv'

ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=3
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

#calculate low model
mincomp=0
maxcomp=2
normtype=3
removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist_Na2O_0-4.csv'

ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)

normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)