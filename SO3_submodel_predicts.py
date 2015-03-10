# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 21:08:20 2015

@author: rbanderson
"""

#import os
#os.chdir(r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\ccam')

import ccam
import numpy
import csv
import sys

searchdir=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_team'
maskfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\mask_minors_noise.csv'
outpath=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Output\SO3'
masterlist=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_misc\MASTERLIST.csv'
name_subs=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv'
dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\RyanSinput\\full_db_mars_corrected_peakarea.csv'
keepfile=None
removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'
spectrafile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\RyanSulfatesPA.csv'

which_elem='SO3'
plstype='sklearn'
skscale=''
mincomp=0
maxcomp=100

#set plot range
xminmax=[0,100]
yminmax=xminmax

maxnc=30
fullmin=5
fullmax=100

fullnorm=3

#specify the number of components to use for each submodel
nc_full=4

#specify the files that hold the mean centering info
means_file_full=None#outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(fullnorm)+'_'+str(fullmin)+'-'+str(fullmax)+'_meancenters.csv'

#specify the files that store the regression models (these are the python equivalent of IDL .SAV files)
loadfile_full=outpath+'\\'+which_elem+'_'+plstype+skscale+'_norm'+str(fullnorm)+'_'+str(fullmin)+'-'+str(fullmax)+'.pkl'

#specify where to save csv files with predictions
outputfile=outpath+'\\'+which_elem+skscale+'_predictions.csv'
db_outputfile=outpath+'\\'+which_elem+skscale+'_db_predictions.csv'

#specify files containing cross validation results
full_cv_file=outpath+'\\'+which_elem+'_'+plstype+skscale+'_nc'+str(maxnc)+'_norm'+str(fullnorm)+'_'+str(fullmin)+'-'+str(fullmax)+'_cv_predict.csv'

#specify file names for  CV 1 to 1 plots
outfile1to1=outpath+'\\'+which_elem+skscale+'_submodels_1to1_plot_'+str(xminmax[0])+'_'+str(xminmax[1])+'.png'

#specify file names for full database 1 to 1 plots
imgfile=outpath+'\\'+which_elem+skscale+'_final_model_predictions_1to1_'+str(xminmax[0])+'-'+str(xminmax[1])+'.png'

print 'Reading database'
sys.stdout.flush()
spectra,comps,spect_index,names,labels,wvl=ccam.read_db(dbfile,compcheck=True,n_elems=10)
oxides=labels[2:]
compindex=numpy.where(oxides==which_elem)[0]

print 'Choosing spectra'
spectra,names,spect_index,comps=ccam.choose_spectra(spectra,spect_index,names,comps,compindex,mincomp=0,maxcomp=100,keepfile=keepfile,removefile=removefile,which_removed=None)
y_db_full,fullnorm=ccam.pls_predict(spectra,nc_full,wvl,maskfile,loadfile=loadfile_full,mean_file=means_file_full)


truecomps=comps[:,compindex]
predicts=y_db_full
plot_title='Final Model '+which_elem+' Predictions of Full Database'
labels='Full'
colors='c'
markers='o'

ccam.plots.Plot1to1(truecomps,predicts,plot_title,labels,colors,markers,imgfile,xminmax=xminmax,yminmax=yminmax)

with open(db_outputfile,'wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['','','','Full']
        writer.writerow(row)
        row=['','','Norm=',fullnorm]
        writer.writerow(row)
        row=['','','nc=',str(nc_full)]
        writer.writerow(row)
        row=['Target','Index','True Comp',which_elem]
        writer.writerow(row)
        
        for i in range(0,len(names)):
            row=[names[i],spect_index[i],str(comps[i,compindex][0]),y_db_full[i]]
            writer.writerow(row)   


data,wvl,filelist=ccam.read_spectra(spectrafile)

y_full,fullnorm=ccam.pls_predict(data,nc_full,wvl,maskfile,loadfile=loadfile_full,mean_file=means_file_full)

predicts=y_full

print 'Writing results'
with open(outputfile,'wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['Full']
        writer.writerow(row)
        row=['Norm=',fullnorm]
        writer.writerow(row)
        row=['nc=',str(nc_full)]
        writer.writerow(row)
        row=['File',which_elem]
        writer.writerow(row)
        
        for i in range(0,len(y_full)):
            row=[filelist[i],y_full[i]]
            writer.writerow(row)        
        
  
#make 1 to 1 plots using CV results

full_cv_predict,full_cv_samples,full_cv_truecomps,full_cv_folds,full_cv_spect=ccam.plots.readpredicts(full_cv_file,nc_full)
      
RMSECV_full=numpy.sqrt(numpy.mean((full_cv_predict-full_cv_truecomps)**2))


truecomps=full_cv_truecomps
predicts=full_cv_predict
labels='Full (nc='+str(nc_full)+', norm='+str(fullnorm)+', RMSECV='+str(RMSECV_full)+')'
colors='c'
markers='o'
plot_title=which_elem+' Cross Validation'
ccam.Plot1to1(truecomps,predicts,plot_title,labels,colors,markers,outfile1to1,xminmax=xminmax,yminmax=yminmax)


