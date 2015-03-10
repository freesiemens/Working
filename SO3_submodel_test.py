# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 15:21:25 2015

@author: rbanderson
"""

import os
os.chdir(r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working')

import ccam
dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\RyanSInput\\full_db_mars_corrected_peakarea.csv'
removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'
foldfile=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\folds.csv'
maskfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\mask_minors_noise.csv'
keepfile=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\Si_full_included.csv'
outpath='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Output\\SO3\\'
cal_dir=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_team\CalTarget 95A'
masterlist_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_misc\MASTERLIST.csv'
name_sub_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv'

normtype=3
which_elem='SO3'
mincomp=0
maxcomp=100
nfolds=5
testfold=2
nc=20
seed=100
plstype='sklearn'


#calculate full model
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False,n_elems=10)

normtype=1
ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False,n_elems=10)

#Calculate high model
#mincomp=3.5
#maxcomp=100
#normtype=1
#ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)
#
#normtype=3
#ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)
#
#
##calculate low model
#mincomp=0
#maxcomp=4
#normtype=3
#ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)
#
#normtype=1
#ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)
##
###calculate med model
##maxcomp=70
##mincomp=30
##normtype=1
##ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)
##
##normtype=3
##ccam.pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=normtype,mincomp=mincomp,maxcomp=maxcomp,plstype=plstype,keepfile=keepfile,removefile=removefile,cal_dir=cal_dir,masterlist_file=masterlist_file,compfile=dbfile,name_sub_file=name_sub_file,foldfile=foldfile,nfolds=nfolds,seed=seed,n_bag=None,n_boost=None,skscale=False)
#
