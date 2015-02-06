# -*- coding: utf-8 -*-
"""
Created on Wed Feb 04 21:49:13 2015

@author: rbanderson
"""
import os
os.chdir(r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\ccam')
import ccam_pls_cal

dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\full_db_mars_corrected.csv'
removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\removelist.csv'
foldfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\folds.csv'
maskfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\mask_minors_noise.csv'
keepfile=None
outpath='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Output\\'
cal_dir=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_team\CalTarget 95A'
masterlist_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_misc\MASTERLIST.csv'
name_sub_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Input\target_name_subs.csv'


which_elem='MgO'

testfold=2
nc=20
plstype='mlpy'

#calculate full model
mincomp=0
maxcomp=100

ccam_pls_cal.ccam_pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,normtype=1,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file)
ccam_pls_cal.ccam_pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,normtype=3,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file)
