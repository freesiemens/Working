# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 15:21:25 2015

@author: rbanderson
"""
import os
os.chdir(r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\ccam')
#import ccam
import ccam_pls_cal

dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\full_db_mars_corrected.csv'
removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\removelist.csv'
foldfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\folds.csv'
maskfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\mask_minors_noise.csv'
keepfile=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\Si_full_included.csv'
outpath='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Output\\'
cal_dir=None#r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_team\CalTarget 95A'
masterlist_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_misc\MASTERLIST.csv'
name_sub_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Input\target_name_subs.csv'

normtype=3
which_elem='MgO'
mincomp=0
maxcomp=100
testfold=2
nc=20
plstype='mlpy'

#calculate full model
ccam_pls_cal.ccam_pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile)

#ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file)

normtype=1
#ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file)
ccam_pls_cal.ccam_pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile)

#calculate low model
maxcomp=3
normtype=3
#keepfile=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\Mg_low_included.csv'
#ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file)
ccam_pls_cal.ccam_pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile)

normtype=1
#ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file)
ccam_pls_cal.ccam_pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile)

#calculate med model
maxcomp=12
mincomp=2
normtype=1
#keepfile=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\Mg_full_included.csv'
#ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file)
ccam_pls_cal.ccam_pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile)

normtype=3
#ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file)
ccam_pls_cal.ccam_pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile)



#Calculate high model
mincomp=10
maxcomp=100
normtype=1
#keepfile=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\Mg_high_included.csv'
#ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file)
ccam_pls_cal.ccam_pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile)

normtype=3
#ccam.pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,keepfile=keepfile,removefile=removefile,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file)
ccam_pls_cal.ccam_pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile)
