# -*- coding: utf-8 -*-
"""
Created on Tue May 10 12:09:29 2016

@author: rbanderson
"""
import pandas as pd
import numpy as np
import pysat
from pysat.spectral.spectral_data import spectral_data
from pysat.spectral.within_range import within_range
from pysat.spectral.meancenter import meancenter
from pysat.regression.sm import sm
from sklearn.decomposition import PCA, FastICA
from sklearn import linear_model
from sklearn.cross_decomposition.pls_ import PLSRegression
from pysat.plotting import plots
import time
from pysat.regression import cv
from pysat.regression.regression import regression

#import matplotlib.pyplot as plot
import warnings

warnings.filterwarnings('ignore')

print('Read training database with mixtures')
db=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\Database\full_db_mars_corrected_dopedTiO2_mixtures_pandas.csv"
data_mix=pd.read_csv(db,header=[0,1])
data_mix=spectral_data(data_mix)

print('Read training database')
db=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\Database\full_db_mars_corrected_dopedTiO2_pandas_format.csv"
data=pd.read_csv(db,header=[0,1])
data=spectral_data(data)

print('Mask out unwanted portions of the data')
maskfile=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Input\mask_minors_noise.csv"
data.mask(maskfile)
data_mix.mask(maskfile)

print('Normalize spectra by specifying the wavelength ranges over which to normalize')
ranges=[(0,1000)] #this is equivalent to "norm3"

print('Norm1 data')
data.norm(ranges)
data_mix.norm(ranges)


print('Remove data without compositions')
data_mix=spectral_data(data_mix.df.ix[-data_mix.df[('comp','Na2O')].isnull()])
data=spectral_data(data.df.ix[-data.df[('comp','Na2O')].isnull()])

print('set up for cross validation')
el='Na2O'
nfolds=5 #number of folds to divide data into to extract an overall test set
testfold=3 #which fold to use as the overall test set

nc=15  #max number of components
outpath=r'C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output'

print('remove a test set to be completely excluded from CV and used to assess the final model')
data.stratified_folds(nfolds=nfolds,sortby=('comp',el))
data_train=data.rows_match(('meta','Folds'),[testfold],invert=True)
data_test=data.rows_match(('meta','Folds'),[testfold])
 
data_mix.stratified_folds(nfolds=nfolds,sortby=('comp',el))
data_mix_train=data_mix.rows_match(('meta','Folds'),[testfold],invert=True)
data_mix_test=data_mix.rows_match(('meta','Folds'),[testfold])
 
 
# print('Do PLS CV')
# figfile='Na2O_CV_0-100_norm1_v2.png'
# params={'n_components':list(range(1,nc+1)),'scale':[False]}
# params={'n_components':[4,5],'scale':[False]}
#
# cv_obj=cv.cv(params)
# data_train.df,output_pls=cv_obj.do_cv(data_train.df,xcols='wvl',ycol=('comp',el),method='PLS')
# data_mix_train.df,output_pls_mix=cv_obj.do_cv(data_mix_train.df,xcols='wvl',ycol=('comp',el),method='PLS')
#
# #params={'n_components':list(range(1,nc+1)),'reduce_dim':['PCA'],'regr':['linear'],'theta0':[1],'thetaL':[0.1],'thetaU':[100],'random_start':[1]}
# #output_gp=cv(data_train.df,params,xcols='wvl',ycol=('comp',el),method='GP',ransacparams=None)
# #output_gp_mix=cv(data_mix_train.df,params,xcols='wvl',ycol=('comp',el),method='GP',ransacparams=None)
#
#
# x=output_pls['n_components']
# y=output_pls['RMSECV']
# fig1=plots.make_plot(x,y,outpath,figfile=figfile,xtitle='# of components',ytitle='wt.%',title='Na2O',
#                 lbl='RMSECV - PLS',one_to_one=False,dpi=1000,color=[1,0,0,1],loadfig=None,marker='None',linestyle='-')
#
# x=output_pls_mix['n_components']
# y=output_pls_mix['RMSECV']
# fig1=plots.make_plot(x,y,outpath,figfile=figfile,xtitle='# of components',ytitle='wt.%',title='Na2O',
#                 lbl='RMSECV - PLS (with mixtures)',one_to_one=False,dpi=1000,color=[0,1,0,1],loadfig=fig1,marker='None',linestyle='-')


best_pls_model_mix=regression(['PLS'],[{'n_components':4,'scale':[False]}])
best_pls_model_mix.fit(data_mix_train.df['wvl'],data_mix_train.df[('comp','Na2O')])
pls_mix_train=best_pls_model_mix.predict(data_mix_train.df['wvl'])
pls_mix=best_pls_model_mix.predict(data_mix_test.df['wvl'])

best_pls_model=regression(['PLS'],[{'n_components':6,'scale':[False]}])
best_pls_model.fit(data_train.df['wvl'],data_train.df[('comp','Na2O')])
pls_train=best_pls_model.predict(data_train.df['wvl'])
pls=best_pls_model.predict(data_test.df['wvl'])

# best_gp_model_mix=regression(['GP'],[{'n_components':9,'reduce_dim':'PCA','regr':'linear','theta0':1,'thetaL':0.1,'thetaU':100,'random_start':1}])
# best_gp_model_mix.fit(data_train.df['wvl'],data_train.df[('comp','Na2O')])
# gp_mix=best_gp_model_mix.predict(data_mix_test.df['wvl'])

# best_gp_model=regression(['GP'],[{'n_components':13,'reduce_dim':'PCA','regr':'linear','theta0':1,'thetaL':0.1,'thetaU':100,'random_start':1}])
# best_gp_model.fit(data_train.df['wvl'],data_train.df[('comp','Na2O')])
# gp=best_gp_model.predict(data_test.df['wvl'])

x=data_train.df[('comp','Na2O')]
y=pls_train
colors=[1,0,0,1]
lbls=['PLS (nc=5,mixtures)']
figfile='Na2O_1to1_train.png'
fig2=plots.make_plot(x,y,outpath,figfile=figfile,xtitle='# of components',ytitle='wt.%',title='Na2O',
                lbl='RMSECV - PLS',one_to_one=True,dpi=1000,color=colors,loadfig=None,marker='o',linestyle='None')

x=data_mix_train.df[('comp','Na2O')]
y=pls_mix_train
colors=[0,1,0,1]
lbls=['PLS (nc=6)']
fig2=plots.make_plot(x,y,outpath,figfile=figfile,xtitle='# of components',ytitle='wt.%',title='Na2O',
                lbl='RMSECV - PLS (with mixtures)',one_to_one=True,dpi=1000,color=colors,loadfig=fig2,marker='o',linestyle='None')



pass
    





