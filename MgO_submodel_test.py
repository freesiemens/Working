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
keepfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\Mg_full_included.csv'
outpath='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Output\\'
cal_dir=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_team\CalTarget 95A'
masterlist_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_misc\MASTERLIST.csv'
name_sub_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Input\target_name_subs.csv'

normtype=3
which_elem='MgO'
mincomp=0.0000001
maxcomp=100
testfold=2
nc=20
plstype='mlpy'

#calculate full model
ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file)

normtype=1
ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file)

#calculate low model
maxcomp=3.5
normtype=1
keeplist='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\Mg_low_included.csv'
ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file)

normtype=3
ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file)

#Calculate high model
mincomp=2.5
maxcomp=100
normtype=1
keeplist='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\Mg_high_included.csv'
ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file)

normtype=3
ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file)