# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 09:48:23 2016

@author: rbanderson
"""
import pandas as pd
import csv
import numpy as np

def make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='w'):
        removed=pd.read_csv(removedfile,header=None)
        removed=removed.set_index([2])
        from_file=removed.loc['From File']
        out_of_range=removed.loc['Out of Range']
        
        test=pd.read_csv(testfile)
        train=pd.read_csv(trainfile)
        
        if mode=='w':
            with open(summaryfile,'w',newline='') as writefile:
                writer=csv.writer(writefile,delimiter=',')
                writer.writerow([' ','Removed',' ',' ',' ',' ',' ','Test',' ','Train',' '])                
                writer.writerow([' ','Outliers',' ','Out of Range',' ','Cal Targets',' ',' ',' ',' ',' '])
                writer.writerow([' ','Spectra','Unique Samples','Spectra','Unique Samples','Spectra','Unique Samples','Spectra','Unique Samples','Spectra','Unique Samples'])
                
        with open(summaryfile,'a',newline='') as writefile:
            writer=csv.writer(writefile,delimiter=',')
            writer.writerow([modelname,from_file.index.size-40,np.unique(from_file[0]).size-8,
                             out_of_range.index.size,np.unique(out_of_range[0]).size,
                             40,8,
                             test.index.size,np.unique(test['Sample']).size,
                             train.index.size,np.unique(train['Sample']).size])
                             
                             

#############SiO2###############
summaryfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\SiO2\outlier_train_test_summary.csv"

modelname='Full'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\SiO2\SiO2_sklearn_nc20_norm1_0-100_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\SiO2\SiO2_sklearn_nc20_norm1_0-100_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\SiO2\SiO2_sklearn_nc20_norm1_0-100_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='w')

modelname='Low'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\SiO2\SiO2_sklearn_nc20_norm1_0-50_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\SiO2\SiO2_sklearn_nc20_norm1_0-50_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\SiO2\SiO2_sklearn_nc20_norm1_0-50_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')

modelname='Mid'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\SiO2\SiO2_sklearn_nc20_norm1_30-70_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\SiO2\SiO2_sklearn_nc20_norm1_30-70_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\SiO2\SiO2_sklearn_nc20_norm1_30-70_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')

modelname='High'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\SiO2\SiO2_sklearn_nc20_norm1_60-100_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\SiO2\SiO2_sklearn_nc20_norm1_60-100_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\SiO2\SiO2_sklearn_nc20_norm1_60-100_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')

#############TiO2###############
summaryfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\TiO2\outlier_train_test_summary.csv"

modelname='Full'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\TiO2\TiO2_sklearn_nc30_norm1_0-100_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\TiO2\TiO2_sklearn_nc30_norm1_0-100_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\TiO2\TiO2_sklearn_nc30_norm1_0-100_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='w')

modelname='Low'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\TiO2\TiO2_sklearn_nc30_norm1_0-2_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\TiO2\TiO2_sklearn_nc30_norm1_0-2_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\TiO2\TiO2_sklearn_nc30_norm1_0-2_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')

modelname='Mid'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\TiO2\TiO2_sklearn_nc30_norm1_1-5_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\TiO2\TiO2_sklearn_nc30_norm1_1-5_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\TiO2\TiO2_sklearn_nc30_norm1_1-5_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')

modelname='High'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\TiO2\TiO2_sklearn_nc30_norm1_3-100_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\TiO2\TiO2_sklearn_nc30_norm1_3-100_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\TiO2\TiO2_sklearn_nc30_norm1_3-100_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')

#############Al2O3###############
summaryfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Al2O3\outlier_train_test_summary.csv"

modelname='Full'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Al2O3\Al2O3_sklearn_nc20_norm1_0-100_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Al2O3\Al2O3_sklearn_nc20_norm1_0-100_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Al2O3\Al2O3_sklearn_nc20_norm1_0-100_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='w')

modelname='Low'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Al2O3\Al2O3_sklearn_nc20_norm1_0-12_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Al2O3\Al2O3_sklearn_nc20_norm1_0-12_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Al2O3\Al2O3_sklearn_nc20_norm1_0-12_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')

modelname='Mid'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Al2O3\Al2O3_sklearn_nc20_norm1_10-25_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Al2O3\Al2O3_sklearn_nc20_norm1_10-25_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Al2O3\Al2O3_sklearn_nc20_norm1_10-25_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')

modelname='High'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Al2O3\Al2O3_sklearn_nc20_norm1_20-100_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Al2O3\Al2O3_sklearn_nc20_norm1_20-100_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Al2O3\Al2O3_sklearn_nc20_norm1_20-100_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')

#############FeOT###############
summaryfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\FeOT\outlier_train_test_summary.csv"

modelname='Full'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\FeOT\FeOT_sklearn_nc30_norm1_0-100_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\FeOT\FeOT_sklearn_nc30_norm1_0-100_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\FeOT\FeOT_sklearn_nc30_norm1_0-100_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='w')

modelname='Low'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\FeOT\FeOT_sklearn_nc30_norm1_0-15_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\FeOT\FeOT_sklearn_nc30_norm1_0-15_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\FeOT\FeOT_sklearn_nc30_norm1_0-15_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')

modelname='Mid'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\FeOT\FeOT_sklearn_nc30_norm1_5-25_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\FeOT\FeOT_sklearn_nc30_norm1_5-25_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\FeOT\FeOT_sklearn_nc30_norm1_5-25_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')

modelname='High'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\FeOT\FeOT_sklearn_nc30_norm1_15-100_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\FeOT\FeOT_sklearn_nc30_norm1_15-100_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\FeOT\FeOT_sklearn_nc30_norm1_15-100_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')

#############MgO###############
summaryfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\MgO\outlier_train_test_summary.csv"

modelname='Full'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\MgO\MgO_sklearn_nc20_norm1_0-100_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\MgO\MgO_sklearn_nc20_norm1_0-100_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\MgO\MgO_sklearn_nc20_norm1_0-100_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='w')

modelname='Low'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\MgO\MgO_sklearn_nc20_norm1_0-3.5_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\MgO\MgO_sklearn_nc20_norm1_0-3.5_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\MgO\MgO_sklearn_nc20_norm1_0-3.5_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')

modelname='Mid'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\MgO\MgO_sklearn_nc20_norm1_0-20_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\MgO\MgO_sklearn_nc20_norm1_0-20_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\MgO\MgO_sklearn_nc20_norm1_0-20_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')

modelname='High'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\MgO\MgO_sklearn_nc20_norm1_8-100_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\MgO\MgO_sklearn_nc20_norm1_8-100_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\MgO\MgO_sklearn_nc20_norm1_8-100_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')

#############CaO###############
summaryfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\CaO\outlier_train_test_summary.csv"

modelname='Full'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\CaO\CaO_sklearn_nc30_norm1_0-42_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\CaO\CaO_sklearn_nc30_norm1_0-42_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\CaO\CaO_sklearn_nc30_norm1_0-42_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='w')

modelname='Low'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\CaO\CaO_sklearn_nc30_norm1_0-7_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\CaO\CaO_sklearn_nc30_norm1_0-7_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\CaO\CaO_sklearn_nc30_norm1_0-7_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')

modelname='Mid'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\CaO\CaO_sklearn_nc30_norm1_0-15_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\CaO\CaO_sklearn_nc30_norm1_0-15_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\CaO\CaO_sklearn_nc30_norm1_0-15_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')

modelname='High'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\CaO\CaO_sklearn_nc30_norm1_30-100_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\CaO\CaO_sklearn_nc30_norm1_30-100_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\CaO\CaO_sklearn_nc30_norm1_30-100_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')

#############Na2O###############
summaryfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Na2O\outlier_train_test_summary.csv"

modelname='Full'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Na2O\Na2O_sklearn_nc20_norm1_0-100_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Na2O\Na2O_sklearn_nc20_norm1_0-100_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Na2O\Na2O_sklearn_nc20_norm1_0-100_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='w')

modelname='Low'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Na2O\Na2O_sklearn_nc20_norm1_0-4_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Na2O\Na2O_sklearn_nc20_norm1_0-4_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Na2O\Na2O_sklearn_nc20_norm1_0-4_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')

modelname='High'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Na2O\Na2O_sklearn_nc20_norm1_3.5-100_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Na2O\Na2O_sklearn_nc20_norm1_3.5-100_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\Na2O\Na2O_sklearn_nc20_norm1_3.5-100_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')

#############K2O###############
summaryfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\K2O\outlier_train_test_summary.csv"

modelname='Full'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\K2O\K2O_sklearn_nc20_norm1_0-100_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\K2O\K2O_sklearn_nc20_norm1_0-100_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\K2O\K2O_sklearn_nc20_norm1_0-100_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='w')

modelname='Low'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\K2O\K2O_sklearn_nc20_norm1_0-2_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\K2O\K2O_sklearn_nc20_norm1_0-2_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\K2O\K2O_sklearn_nc20_norm1_0-2_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')

modelname='High'
removedfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\K2O\K2O_sklearn_nc20_norm1_1.5-100_removed.csv"
testfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\K2O\K2O_sklearn_nc20_norm1_1.5-100_test_predict.csv"
trainfile=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\external_test_set\Output\K2O\K2O_sklearn_nc20_norm1_1.5-100_train_predict.csv"
make_summary(summaryfile,removedfile,testfile,trainfile,modelname,mode='a')
