# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 11:02:50 2015

@author: rbanderson
"""
import numpy
import ccam

full_cv_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_mlpy_nc20_norm3_0-100_cv_predict.csv'
low_cv_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_mlpy_nc20_norm3_0-15_cv_predict.csv'
#mid_cv_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_mlpy_nc20_norm3_5-20_cv_predict.csv'
high_cv_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_mlpy_nc20_norm3_10-100_cv_predict.csv'


nc_full=9
nc_low=11
#nc_mid=6
nc_high=7

norm_full=3
norm_low=3
#norm_mid=3
norm_high=3

low_cutoff=12.5
high_cutoff=12.5
comprange1=[0,60]
comprange2=[0,15]
outfile1=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_submodels_low_high_1to1_plot.png'
outfile2=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_submodels_low_high_1to1_plot_0-15.png'

full_cv_predict,full_cv_samples,full_cv_truecomps,full_cv_folds,full_cv_spect=ccam.plots.readpredicts(full_cv_file,nc_full)
low_cv_predict,low_cv_samples,low_cv_truecomps,low_cv_folds,low_cv_spect=ccam.plots.readpredicts(low_cv_file,nc_low)
high_cv_predict,high_cv_samples,high_cv_truecomps,high_cv_folds,high_cv_spect=ccam.plots.readpredicts(high_cv_file,nc_high)
#mid_cv_predict,mid_cv_samples,mid_cv_truecomps,mid_cv_folds,mid_cv_spect=ccam.plots.readpredicts(mid_cv_file,nc_mid)

low_cv_predict_big=numpy.zeros_like(full_cv_predict)
high_cv_predict_big=numpy.zeros_like(full_cv_predict)

combined_cv_predict=numpy.zeros_like(full_cv_predict)
for i in range(len(combined_cv_predict)):
    
    if full_cv_truecomps[i]>high_cutoff:
        matchsamp=(high_cv_samples==full_cv_samples[i])
        matchspect=(high_cv_spect==full_cv_spect[i])
        bothmatch=numpy.all(numpy.vstack((matchsamp,matchspect)),axis=0)
        if sum(bothmatch)!=1:
            combined_cv_predict[i]=9999
        if sum(bothmatch)==1:
            combined_cv_predict[i]=high_cv_predict[bothmatch]
            
#    if full_cv_truecomps[i]>low_cutoff and full_cv_truecomps[i]<high_cutoff:
#        matchsamp=(mid_cv_samples==full_cv_samples[i])
#        matchspect=(mid_cv_spect==full_cv_spect[i])
#        bothmatch=numpy.all(numpy.vstack((matchsamp,matchspect)),axis=0)
#        if sum(bothmatch)!=1:
#            combined_cv_predict[i]=9999
#        if sum(bothmatch)==1:
#            combined_cv_predict[i]=mid_cv_predict[bothmatch]
##    
#    
    if full_cv_truecomps[i]<low_cutoff:
        matchsamp=(low_cv_samples==full_cv_samples[i])
        matchspect=(low_cv_spect==full_cv_spect[i])
        bothmatch=numpy.all(numpy.vstack((matchsamp,matchspect)),axis=0)
        if sum(bothmatch)!=1:
            combined_cv_predict[i]=9999
        if sum(bothmatch)==1:
            combined_cv_predict[i]=low_cv_predict[bothmatch]


RMSECV_full=numpy.sqrt(numpy.mean((full_cv_predict-full_cv_truecomps)**2))
RMSECV_low=numpy.sqrt(numpy.mean((low_cv_predict-low_cv_truecomps)**2))
#RMSECV_mid=numpy.sqrt(numpy.mean((mid_cv_predict-mid_cv_truecomps)**2))
RMSECV_high=numpy.sqrt(numpy.mean((high_cv_predict-high_cv_truecomps)**2))
RMSECV_combined=numpy.sqrt(numpy.mean((combined_cv_predict[(combined_cv_predict!=9999)]-full_cv_truecomps[(combined_cv_predict!=9999)])**2))

truecomps=[full_cv_truecomps,low_cv_truecomps,high_cv_truecomps]
predicts=[full_cv_predict,low_cv_predict,high_cv_predict]
labels=['Full (nc='+str(nc_full)+', norm='+str(norm_full)+', RMSECV='+str(RMSECV_full)+')','Low (nc='+str(nc_low)+',norm='+str(norm_low)+', RMSECV='+str(RMSECV_low)+')','High (nc='+str(nc_high)+',norm='+str(norm_high)+', RMSECV='+str(RMSECV_high)+')']
colors=['c','r','b']
markers=['o','v','^']
plot_title='CaO Cross Validation (combined RMSECV = '+str(RMSECV_combined)+')'
ccam.plots.Plot1to1(truecomps,predicts,plot_title,labels,colors,markers,outfile1,comprange=comprange1)
ccam.plots.Plot1to1(truecomps,predicts,plot_title,labels,colors,markers,outfile2,comprange=comprange2)




    