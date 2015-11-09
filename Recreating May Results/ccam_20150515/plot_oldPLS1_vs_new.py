# -*- coding: utf-8 -*-
"""
Created on Fri Nov 06 14:44:33 2015

@author: rbanderson
"""

import ccam
import numpy
def ingest_oldPLS1(filename_pred,filename_err,nc):
    data_pred=ccam.read_csv(filename_pred,0,labelrow=False,skipsym='#')[:,nc-1]
    data_err=ccam.read_csv(filename_err,0,labelrow=False,skipsym='#')[:,nc-1]
    return data_pred.astype('float'),data_err.astype('float')
    
def ingest_newSM_PLS(filename):
    data,label=ccam.read_csv(filename,3,labelrow=True)
    targetlist=data[0]
    truecomps=data[2].astype('float')
    blended=data[6].astype('float')
    return targetlist,truecomps,blended
    
    print 'foo'
    
#Define all the output files from the old PLS1 script
oldPLS1_root="C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\PDL\\PLS\\PLS1_20130829\\RMSEP_output\\"
oldPLS1_pred=[oldPLS1_root+r'matypred_SiO2.csv',oldPLS1_root+r'matypred_TiO2.csv',oldPLS1_root+r'matypred_Al2O3.csv',
              oldPLS1_root+r'matypred_FeOT.csv',oldPLS1_root+r'matypred_MgO.csv',oldPLS1_root+r'matypred_CaO.csv',
              oldPLS1_root+r'matypred_Na2O.csv',oldPLS1_root+r'matypred_K2O.csv']
              
oldPLS1_err=[oldPLS1_root+r'matypres_SiO2.csv',oldPLS1_root+r'matypres_TiO2.csv',oldPLS1_root+r'matypres_Al2O3.csv',
             oldPLS1_root+r'matypres_FeOT.csv',oldPLS1_root+r'matypres_MgO.csv',oldPLS1_root+r'matypres_CaO.csv',
             oldPLS1_root+r'matypres_Na2O.csv',oldPLS1_root+r'matypres_K2O.csv']

elems=['SiO2','TiO2','Al2O3','FeOT','MgO','CaO','Na2O','K2O']
ncs=[8,10,4,7,8,8,10,4]
predicts_old=[]
errs_old=[]
for i in range(len(elems)):
    temp_pred,temp_err=ingest_oldPLS1(oldPLS1_pred[i],oldPLS1_err[i],ncs[i])
    predicts_old.append(temp_pred)
    errs_old.append(temp_err)


#define the output files for the new blended database results
newSM_PLS_root=r'C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\db_predictions_May_results\\'
newSM_PLS=[newSM_PLS_root+'SiO2_db_predictions_low (0-50)_mid (30-70)_high (60-100).csv',newSM_PLS_root+'TiO2_db_predictions_low (0-2)_mid (1-5)_high (3-100).csv',
           newSM_PLS_root+'Al2O3_db_predictions_low (0-12)_mid (10-25)_high (20-100).csv',newSM_PLS_root+'FeOT_db_predictions_low (0-15)_mid (5-25)_high (15-100).csv',
           newSM_PLS_root+'MgO_db_predictions_low (0-3.5)_mid (0-20)_high (8-100).csv',newSM_PLS_root+'CaO_db_predictions_low (0-7)_mid (0-15)_high (30-100).csv',
           newSM_PLS_root+'Na2O_db_predictions_low (0-100)_mid (0-100)_high (0-100).csv',newSM_PLS_root+'K2O_db_predictions_low (0-2)_mid (0-2)_high (60-100).csv']

for i in range(len(newSM_PLS)):
    foo=ingest_newSM_PLS(newSM_PLS[i])
    
