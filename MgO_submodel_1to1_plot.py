# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 11:02:50 2015

@author: rbanderson
"""
import numpy
import ccam

full_cv_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_mlpy_nc20_norm3_0-100_cv_predict.csv'
low_cv_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_mlpy_nc20_norm3_0-3_cv_predict.csv'
mid_cv_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_mlpy_nc20_norm3_2-12_cv_predict.csv'
high_cv_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_mlpy_nc20_norm1_10-100_cv_predict.csv'


nc_full=7
nc_low=3
nc_mid=5
nc_high=9

norm_full=3
norm_low=3
norm_mid=3
norm_high=1

low_cutoff=3
high_cutoff=11
comprange1=[0,60]
comprange2=[0,20]
outfile1=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_submodels_1to1_plot.png'
outfile2=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_submodels_1to1_plot_0-20.png'

full_cv_predict,full_cv_samples,full_cv_truecomps,full_cv_folds,full_cv_spect=ccam.plots.readpredicts(full_cv_file,nc_full)
low_cv_predict,low_cv_samples,low_cv_truecomps,low_cv_folds,low_cv_spect=ccam.plots.readpredicts(low_cv_file,nc_low)
high_cv_predict,high_cv_samples,high_cv_truecomps,high_cv_folds,high_cv_spect=ccam.plots.readpredicts(high_cv_file,nc_high)
mid_cv_predict,mid_cv_samples,mid_cv_truecomps,mid_cv_folds,mid_cv_spect=ccam.plots.readpredicts(mid_cv_file,nc_mid)

low_cv_predict_big=numpy.zeros_like(full_cv_predict)
high_cv_predict_big=numpy.zeros_like(full_cv_predict)

#combined_cv_predict=numpy.zeros_like(full_cv_predict)
#for i in range(len(combined_cv_predict)):
#    
#    if full_cv_predict[i]>high_cutoff:
#        matchsamp=(high_cv_samples==full_cv_samples[i])
#        matchspect=(high_cv_spect==full_cv_spect[i])
#        bothmatch=numpy.all(numpy.vstack((matchsamp,matchspect)),axis=0)
#        if sum(bothmatch)!=1:
#            combined_cv_predict[i]=9999
#        if sum(bothmatch)==1:
#            combined_cv_predict[i]=high_cv_predict[bothmatch]
#            
#    if full_cv_predict[i]>low_cutoff and full_cv_predict[i]<high_cutoff:
#        matchsamp=(mid_cv_samples==full_cv_samples[i])
#        matchspect=(mid_cv_spect==full_cv_spect[i])
#        bothmatch=numpy.all(numpy.vstack((matchsamp,matchspect)),axis=0)
#        if sum(bothmatch)!=1:
#            combined_cv_predict[i]=9999
#        if sum(bothmatch)==1:
#            combined_cv_predict[i]=mid_cv_predict[bothmatch]
##    
#    
#    if full_cv_predict[i]<low_cutoff:
#        matchsamp=(low_cv_samples==full_cv_samples[i])
#        matchspect=(low_cv_spect==full_cv_spect[i])
#        bothmatch=numpy.all(numpy.vstack((matchsamp,matchspect)),axis=0)
#        if sum(bothmatch)!=1:
#            combined_cv_predict[i]=9999
#        if sum(bothmatch)==1:
#            combined_cv_predict[i]=low_cv_predict[bothmatch]


RMSECV_full=numpy.sqrt(numpy.mean((full_cv_predict-full_cv_truecomps)**2))
RMSECV_low=numpy.sqrt(numpy.mean((low_cv_predict-low_cv_truecomps)**2))
RMSECV_mid=numpy.sqrt(numpy.mean((mid_cv_predict-mid_cv_truecomps)**2))
RMSECV_high=numpy.sqrt(numpy.mean((high_cv_predict-high_cv_truecomps)**2))

mid_should_low=sum(numpy.all(numpy.vstack([(full_cv_predict>2.5),(full_cv_predict<11),(full_cv_truecomps<2.5)]),axis=0))
low_should_mid=sum(numpy.all(numpy.vstack([(full_cv_predict<2.5),(full_cv_truecomps>2.5),(full_cv_truecomps<11)]),axis=0))
mid_should_high=sum(numpy.all(numpy.vstack([(full_cv_predict>2.5),(full_cv_predict<11),(full_cv_truecomps>11)]),axis=0))
high_should_mid=sum(numpy.all(numpy.vstack([(full_cv_predict>11),(full_cv_truecomps<11),(full_cv_truecomps>2.5)]),axis=0))


#RMSECV_combined=numpy.sqrt(numpy.mean((combined_cv_predict[(combined_cv_predict!=9999)]-full_cv_truecomps[(combined_cv_predict!=9999)])**2))

truecomps=[full_cv_truecomps,low_cv_truecomps,mid_cv_truecomps,high_cv_truecomps]
predicts=[full_cv_predict,low_cv_predict,mid_cv_predict,high_cv_predict]
labels=['Full (nc='+str(nc_full)+', norm='+str(norm_full)+', RMSECV='+str(RMSECV_full)+')','Low (nc='+str(nc_low)+',norm='+str(norm_low)+', RMSECV='+str(RMSECV_low)+')','Mid (nc='+str(nc_mid)+',norm='+str(norm_mid)+', RMSECV='+str(RMSECV_mid)+')','High (nc='+str(nc_high)+',norm='+str(norm_high)+', RMSECV='+str(RMSECV_high)+')']
colors=['c','r','g','b']
markers=['o','v','s','^']
plot_title='MgO Cross Validation'
ccam.Plot1to1(truecomps,predicts,plot_title,labels,colors,markers,outfile1,xminmax=comprange1,yminmax=comprange1)
outfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_submodels_1to1_plot_full.png'
ccam.Plot1to1(truecomps[0],predicts[0],plot_title,labels[0],colors[0],markers[0],outfile,xminmax=comprange1,yminmax=comprange1)
outfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_submodels_1to1_plot_low.png'
ccam.Plot1to1(truecomps[1],predicts[1],plot_title,labels[1],colors[1],markers[1],outfile,xminmax=comprange1,yminmax=comprange1)
outfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_submodels_1to1_plot_mid.png'
ccam.Plot1to1(truecomps[2],predicts[2],plot_title,labels[2],colors[2],markers[2],outfile,xminmax=comprange1,yminmax=comprange1)
outfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_submodels_1to1_plot_high.png'
ccam.Plot1to1(truecomps[3],predicts[3],plot_title,labels[3],colors[3],markers[3],outfile,xminmax=comprange1,yminmax=comprange1)

ccam.Plot1to1(truecomps,predicts,plot_title,labels,colors,markers,outfile2,xminmax=comprange2,yminmax=comprange2)

outfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_submodels_1to1_plot_0-20_full.png'
ccam.Plot1to1(truecomps[0],predicts[0],plot_title,labels[0],colors[0],markers[0],outfile,xminmax=comprange2,yminmax=comprange2)
outfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_submodels_1to1_plot_0-20_low.png'
ccam.Plot1to1(truecomps[1],predicts[1],plot_title,labels[1],colors[1],markers[1],outfile,xminmax=comprange2,yminmax=comprange2)
outfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_submodels_1to1_plot_0-20_mid.png'
ccam.Plot1to1(truecomps[2],predicts[2],plot_title,labels[2],colors[2],markers[2],outfile,xminmax=comprange2,yminmax=comprange2)
outfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_submodels_1to1_plot_0-20_high.png'
ccam.Plot1to1(truecomps[3],predicts[3],plot_title,labels[3],colors[3],markers[3],outfile,xminmax=comprange2,yminmax=comprange2)





    