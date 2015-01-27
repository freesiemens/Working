# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 11:02:50 2015

@author: rbanderson
"""

full_cv_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\SiO2_mlpy_nc20_norm3_0-100_cv_predict.csv'
low_cv_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\SiO2_mlpy_nc20_norm3_0-40_cv_predict.csv'
med_cv_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\SiO2_mlpy_nc20_norm3_20-65_cv_predict.csv'
high_cv_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\SiO2_mlpy_nc20_norm1_55-100_cv_predict.csv'
import numpy
import csv
import ccam_plots
nc=4
full_cv_predict,full_cv_samples,full_cv_truecomps=ccam_plots.readpredicts(full_cv_file,nc)
nc=3
low_cv_predict,low_cv_samples,low_cv_truecomps=ccam_plots.readpredicts(low_cv_file,nc)
nc=4
med_cv_predict,med_cv_samples,med_cv_truecomps=ccam_plots.readpredicts(med_cv_file,nc)
nc=5
high_cv_predict,high_cv_samples,high_cv_truecomps=ccam_plots.readpredicts(high_cv_file,nc)

combined_cv_predict=numpy.zeros_like(full_cv_predict)
for i in range(len(combined_cv_predict)):
    if full_cv_predict[i]>60:
        combined_cv_predict[i]=high_cv_predict[(high_cv_samples==]
    if full_cv_predict[i]>30 and full_cv_predict[i]<60:
        combined_cv_predict[i]=med_cv_predict[i]
    if full_cv_predict[i]<30:
        combined_cv_predict[i]=low_cv_predict[i]

RMSECV_full=numpy.sqrt(numpy.mean((full_cv_predict-full_cv_truecomps)**2))
RMSECV_low=numpy.sqrt(numpy.mean((low_cv_predict-low_cv_truecomps)**2))
RMSECV_med=numpy.sqrt(numpy.mean((med_cv_predict-med_cv_truecomps)**2))
RMSECV_high=numpy.sqrt(numpy.mean((high_cv_predict-high_cv_truecomps)**2))
RMSECV_combined=numpy.sqrt(numpy.mean((combined_cv_predict-full_cv_truecomps)**2))

truecomps=[full_cv_truecomps,low_cv_truecomps,med_cv_truecomps,high_cv_truecomps]
predicts=[full_cv_predict,low_cv_predict,med_cv_predict,high_cv_predict]
labels=['Full (nc=4, norm=3'+str(RMSECV_full)+')','Low (nc=3,norm=3'+str(RMSECV_low)+')','Med (nc=4,norm=3'+str(RMSECV_med)+')','High (nc=5,norm=1'+str(RMSECV_high)+')']
colors=['c','r','g','b']
markers=['o','v','s','^']
plot_title='SiO2 Cross Validation (combined RMSECV = '+str(RMSECV_combined)+')'
outfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\submodels_1to1_plot.png'
ccam_plots.ccam_plot_1to1(truecomps,predicts,plot_title,labels,colors,markers,outfile)




    