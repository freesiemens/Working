# -*- coding: utf-8 -*-
"""
Created on Tue May 10 12:09:29 2016

@author: rbanderson
"""
import pandas as pd
import numpy as np
from pysat.spectral.spectral_data import spectral_data
from pysat.regression.sm import sm
from sklearn.decomposition import PCA, FastICA
import time
#from autocnet.regression.pls_cv import pls_cv

import matplotlib.pyplot as plot

print('Read training database')
db=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Sample_Data\full_db_mars_corrected_dopedTiO2_pandas_format.csv"
data=pd.read_csv(db,header=[0,1])

######read unknown data (only do this the first time since it's slow)
#unknowndatadir=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\Lab Data"
#unknowndatasearch='CM*.SAV'
#unknowndatacsv=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\Lab Data\lab_data_averages_pandas_format.csv"
#unknown_data=ccs_batch(unknowndatadir,searchstring=unknowndatasearch)
#
##write it to a csv file for future use (much faster than reading individual files each time)
#
##this writes all the data, including single shots, to a file (can get very large!!)
#unknown_data.df.to_csv(unknowndatacsv)
#
##this writes just the average spectra to a file
#unknown_data.df.loc['average'].to_csv(unknowndatacsv)

#put the training data dataframe into a spectral_data object
data=spectral_data(data)


print('read unknown data from the combined csv file (much faster)')
unknowndatacsv=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\Lab Data\lab_data_averages_pandas_format.csv"
unknown_data=pd.read_csv(unknowndatacsv,header=[0,1])
unknown_data=spectral_data(unknown_data)

print('Interpolate unknown data onto the same exact wavelengths as the training data')
unknown_data.interp(data.df['wvl'].columns)

print('Mask out unwanted portions of the data')
maskfile=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Input\mask_minors_noise.csv"
data.mask(maskfile)
unknown_data.mask(maskfile)

print('Normalize spectra by specifying the wavelength ranges over which to normalize')
ranges3=[(0,350),(350,470),(470,1000)] #this is equivalent to "norm3"
ranges1=[(0,1000)] #this is equivalent to "norm1"

print('Norm3 data')
data3=data
data3.norm(ranges3)
unknown_data3=unknown_data
unknown_data3.norm(ranges3)

print('norm1 data')
data1=data
data1.norm(ranges1)
unknown_data1=unknown_data
unknown_data1.norm(ranges1)

print('Testing ratio function')
range1=[250,350]
range2=[800,840]
data3.ratio(range1,range2)
data1.ratio(range1,range2)
unknown_data1.ratio(range1,range2)
unknown_data3.ratio(range1,range2)


print('set up for cross validation')
el='SiO2'
nfolds_test=6 #number of folds to divide data into to extract an overall test set
testfold_test=4 #which fold to use as the overall test set
nfolds_cv=5  #number of folds to use for CV
testfold_cv=3 #which fold to use as test set for the cross validation models

compranges=[[-20,50],[30,70],[60,100],[0,120]] #these are the composition ranges for the submodels
nc=20  #max number of components
outpath=r'C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output'

print('remove a test set to be completely excluded from CV and used to assess the final blended model')
data3.stratified_folds(nfolds=nfolds_test,sortby=('meta',el))
data3_train=data3.rows_match(('meta','Folds'),[testfold_test],invert=True)
data3_test=data3.rows_match(('meta','Folds'),[testfold_test])
 
data1.stratified_folds(nfolds=nfolds_test,sortby=('meta',el))
data1_train=data1.rows_match(('meta','Folds'),[testfold_test],invert=True)
data1_test=data1.rows_match(('meta','Folds'),[testfold_test])
   

#do cross validation for each compositional range
#If you know how many components you want to use for each submodel, you can comment this loop out
#for n in compranges:
#    #First use the norm1 data
#    data1_tmp=within_range(data1_train,n,el)
#    #Split the known data into stratified train/test sets for the element desired
#    data1_tmp=folds.stratified(data1_tmp,nfolds=nfolds_cv,sortby=('meta',el))
#    #Separate out the train and test data
#    train_cv=data1_tmp.loc[-data1_tmp[('meta','Folds')].isin([testfold_cv])]
#    test_cv=data1_tmp.loc[data1_tmp[('meta','Folds')].isin([testfold_cv])]
#
#    figfile='PLS_CV_nc'+str(nc)+'_'+el+'_'+str(n[0])+'-'+str(n[1])+'_norm1.png'
#    norm1_rmses=pls_cv(train_cv,Test=test_cv,nc=nc,nfolds=nfolds_cv,ycol=el,doplot=True,
#           outpath=outpath,plotfile=figfile)
#
#    #next use the norm3 data
#    data3_tmp=within_range(data3_train,n,el)
#    #Split the known data into stratified train/test sets for the element desired
#    data3_tmp=folds.stratified(data3_tmp,nfolds=nfolds_cv,sortby=('meta',el))
#    #Separate out the train and test data
#    train_cv=data3_tmp.loc[-data3_tmp[('meta','Folds')].isin([testfold_cv])]
#    test_cv=data3_tmp.loc[data3_tmp[('meta','Folds')].isin([testfold_cv])]
#
#    figfile='PLS_CV_nc'+str(nc)+'_'+el+'_'+str(n[0])+'-'+str(n[1])+'_norm3.png'
#    norm3_rmses=pls_cv(train_cv,Test=test_cv,nc=nc,nfolds=nfolds_cv,ycol=el,doplot=True,
#           outpath=outpath,plotfile=figfile)
#

#At this point, stop and look at the plots produced by cross validation and 
#use them to choose the number of components for each of the submodels. 

#Eventually I will add options to automatically define the "best" number of components
#but for now it is still human-in-the-loop


#Here the models are in the order: Low, Mid, High, Full
#(The "full" model, which is being used as the reference to determine which submodel is appropriate
#should always be the last one)
ncs=[7,7,5,9] #provide the best # of components for each submodel
traindata=[data3_train.df,data3_train.df,data1_train.df,data3_train.df] #provide training data for each submodel
testdata=[data3_test.df,data3_test.df,data1_test.df,data3_test.df] #provide test data for each submodel
unkdata=[unknown_data3.df,unknown_data3.df,unknown_data1.df,unknown_data3.df] #provide unknown data to be fed to each submodel


#create an instance of the submodel object to do pls
labels=['wvl','ratio']
ycol=('meta',el)
method='PLS'
pls_sm=sm(labels,ycol,compranges,method)

#outpath specifies where to write the outlier check plots
print('Fitting PLS Submodels')
pls_sm.fit(traindata,figpath=outpath,nc=ncs)

print('Doing PLS Submodel Predictions')
predictions_train=pls_sm.predict(traindata)
predictions_test=pls_sm.predict(testdata)
predictions_unk=pls_sm.predict(unkdata)


print('Blending PLS submodels')
t=time.clock()
blended_train=pls_sm.do_blend(predictions_train,traindata[0][ycol])
print(time.clock()-t)
t=time.clock()
blended_test=pls_sm.do_blend(predictions_test)
print(time.clock()-t)
t=time.clock()
blended_unk=pls_sm.do_blend(predictions_unk)
print(time.clock()-t)


#create an instance of the submodel object to do gaussian processes
method='GP'
gp_sm=sm(labels,ycol,compranges,method)

#outpath specifies where to write the outlier check plots
print('Fitting GP model (can take a little while)')
t=time.clock()
gp_sm.fit(traindata,figpath=outpath,nc=10,theta0=1.0,thetaL=0.1,thetaU=100,random_start=10,regr='linear')
print(time.clock()-t)

print('Doing GP Submodel Predictions')
t=time.clock()
predictions_train_gp=gp_sm.predict(traindata)
print(time.clock()-t)
t=time.clock()
predictions_test_gp=gp_sm.predict(testdata)
print(time.clock()-t)
t=time.clock()
predictions_unk_gp=gp_sm.predict(unkdata)
print(time.clock()-t)

print('Blending GP submodels')
t=time.clock()

blended_train_gp=gp_sm.do_blend(predictions_train_gp,traindata[0]['meta'][el])
print(time.clock()-t)
t=time.clock()
blended_test_gp=gp_sm.do_blend(predictions_test_gp)
print(time.clock()-t)
t=time.clock()
blended_unk_gp=gp_sm.do_blend(predictions_unk_gp)
print(time.clock()-t)
t=time.clock()


outpath=r'C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output'
resultsfile='pls_sm_test_output.csv'
resultsfile_gp='pls_sm_test_output_gp.csv'

print('Make a figure showing the test set performance')
plot.figure()
plot.scatter(testdata[0]['meta'][el],blended_test,color='r')
plot.scatter(testdata[0]['meta'][el],blended_test_gp,color='b')
plot.plot([0,100],[0,100])
plot.show()

unk_results=unkdata[0]['meta']
unk_results[el]=blended_unk
unk_results.to_csv(outpath+'\\'+resultsfile)

unk_results_gp=unkdata[0]['meta']
unk_results_gp[el]=blended_unk_gp
unk_results.to_csv(outpath+'\\'+resultsfile_gp)

print(foo)
    





