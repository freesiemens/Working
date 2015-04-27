# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 15:21:25 2015

@author: rbanderson
"""

import os
os.chdir(r'D:\Ryan\20150401_Python_RLS_A')

import ccam
dbfile='D:\\Ryan\\20150401_Python_RLS_A\\Input\\full_db_mars_corrected.csv'
removefile='D:\\Ryan\\20150401_Python_RLS_A\\Input\\removelist.csv'
foldfile=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\folds.csv'
maskfile='D:\\Ryan\\20150401_Python_RLS_A\\Input\\mask_minors_noise.csv'
keepfile=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\Si_full_included.csv'
outpath='D:\\Ryan\\20150401_Python_RLS_A\\Output\\CaO\\'
cal_dir=r'D:\Ryan\20150401_Python_RLS_A\CCCT'
masterlist_file=r'D:\Ryan\20150401_Python_RLS_A\Input\MASTERLIST.csv'
name_sub_file=r'D:\Ryan\20150401_Python_RLS_A\Input\target_name_subs.csv'

normtype=3
which_elem='CaO'

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

