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

searchdir=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_team\CalTarget 95A'
maskfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\mask_minors_noise.csv'
outpath=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Output\SiO2'
masterlist=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_misc\MASTERLIST.csv'
name_subs=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv'
dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected.csv'
keepfile=None
removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'


which_elem='SiO2'
maxnc=20
fullmin=0
fullmax=100
lowmin=0
lowmax=40
midmin=30
midmax=70
highmin=60
highmax=100

#!!!!!!!!!!!!!
#NOTE: Normalizations have not been optimized. They were jsut set for testing purposes
#!!!!!!!!!!!!!
fullnorm=1
lownorm=3
midnorm=3
highnorm=1

#specify the number of components to use for each submodel
#!!!!!!!!!!!!!!!!!
#NOTE: These have not been optimized, they are just set to arbitrary values for testing
#!!!!!!!!!!!!!!!!!
nc_full=6
nc_low=3
nc_mid=7
nc_high=6

#specify the files that hold the mean centering info
means_file_full=outpath+'\\'+which_elem+'_sklearn_nc'+str(maxnc)+'_norm'+str(fullnorm)+'_'+str(fullmin)+'-'+str(fullmax)+'_meancenters.csv'
means_file_low=outpath+'\\'+which_elem+'_sklearn_nc'+str(maxnc)+'_norm'+str(lownorm)+'_'+str(lowmin)+'-'+str(lowmax)+'_meancenters.csv'
means_file_mid=outpath+'\\'+which_elem+'_sklearn_nc'+str(maxnc)+'_norm'+str(midnorm)+'_'+str(midmin)+'-'+str(midmax)+'_meancenters.csv'
means_file_high=outpath+'\\'+which_elem+'_sklearn_nc'+str(maxnc)+'_norm'+str(highnorm)+'_'+str(highmin)+'-'+str(highmax)+'_meancenters.csv'

#specify the files that store the regression models (these are the python equivalent of IDL .SAV files)
loadfile_full=outpath+'\\'+which_elem+'_sklearn_norm'+str(fullnorm)+'_'+str(fullmin)+'-'+str(fullmax)+'.pkl'
loadfile_low=outpath+'\\'+which_elem+'_sklearn_norm'+str(lownorm)+'_'+str(lowmin)+'-'+str(lowmax)+'.pkl'
loadfile_mid=outpath+'\\'+which_elem+'_sklearn_norm'+str(midnorm)+'_'+str(midmin)+'-'+str(midmax)+'.pkl'
loadfile_high=outpath+'\\'+which_elem+'_sklearn_norm'+str(highnorm)+'_'+str(highmin)+'-'+str(highmax)+'.pkl'

#specify where to save csv files with predictions
outputfile=outpath+'\\'+which_elem+'_predictions.csv'
db_outputfile=outpath+'\\'+which_elem+'_db_predictions.csv'



#set plot range
xminmax=[0,100]
yminmax=[0,100]

print 'Reading database'
sys.stdout.flush()
spectra,comps,spect_index,names,labels,wvl=ccam.read_db(dbfile,compcheck=True)
oxides=labels[2:]
compindex=numpy.where(oxides==which_elem)[0]

print 'Choosing spectra'
mincomp=0
maxcomp=100
nc=7
spectra,names,spect_index,comps=ccam.choose_spectra(spectra,spect_index,names,comps,compindex,mincomp=mincomp,maxcomp=maxcomp,keepfile=keepfile,removefile=removefile,which_removed=None)
y_db_full,fullnorm=ccam.pls_predict(spectra,nc_full,wvl,maskfile,loadfile=loadfile_full,mean_file=means_file_full)
y_db_low,lownorm=ccam.pls_predict(spectra,nc_low,wvl,maskfile,loadfile=loadfile_low,mean_file=means_file_low)
y_db_mid,midnorm=ccam.pls_predict(spectra,nc_mid,wvl,maskfile,loadfile=loadfile_mid,mean_file=means_file_mid)
y_db_high,highnorm=ccam.pls_predict(spectra,nc_high,wvl,maskfile,loadfile=loadfile_high,mean_file=means_file_high)


"""
From full and low model 0 to 30, use the low model
If full and low model between 30 and 40, then blend the low and mid models using low as reference
If mid model is between 40 and 60, use the mid model
If mid is 60 to 70, then blend mid and high using high as reference
if high 70 then use high
Do not overwrite predictions that have already been set in a previous round of logic.
"""

predicts=[y_db_full,y_db_low,y_db_mid,y_db_high]
ranges=[[0,30],[30,40],[40,60],[60,70],[70,100]]
inrange=[[0,1],[0,1],2,2,3]
refpredict=[1,1,2,3,3]
toblend=[[1,1],[1,2],[2,2],[2,3],[3,3]]

blended2=ccam.submodels_blend(predicts,ranges,inrange,refpredict,toblend,overwrite=False)

truecomps=[comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex]]
predicts=[y_db_full,y_db_low,y_db_mid,y_db_high,blended2]
plot_title='Final Model '+which_elem+' Predictions of Full Database'
labels=['Full','Low','Mid','High','Blended']
colors=['c','r','g','b','k']
markers=['o','<','s','^','*']
imgfile=outpath+'\\'+which_elem+'_final_model_predictions_1to1.png'

ccam.plots.Plot1to1(truecomps,predicts,plot_title,labels,colors,markers,imgfile,xminmax=xminmax,yminmax=yminmax)
imgfile=outpath+'\\'+which_elem+'_final_model_predictions_1to1_blended.png'
ccam.plots.Plot1to1([truecomps[4]],[predicts[4]],plot_title,[labels[4]],[colors[4]],[markers[4]],imgfile,xminmax=xminmax,yminmax=yminmax)
imgfile=outpath+'\\'+which_elem+'_final_model_predictions_1to1_full.png'
ccam.plots.Plot1to1([truecomps[0]],[predicts[0]],plot_title,[labels[0]],[colors[0]],[markers[0]],imgfile,xminmax=xminmax,yminmax=yminmax)
imgfile=outpath+'\\'+which_elem+'_final_model_predictions_1to1_low.png'
ccam.plots.Plot1to1([truecomps[1]],[predicts[1]],plot_title,[labels[1]],[colors[1]],[markers[1]],imgfile,xminmax=xminmax,yminmax=yminmax)
imgfile=outpath+'\\'+which_elem+'_final_model_predictions_1to1_mid.png'
ccam.plots.Plot1to1([truecomps[2]],[predicts[2]],plot_title,[labels[2]],[colors[2]],[markers[2]],imgfile,xminmax=xminmax,yminmax=yminmax)
imgfile=outpath+'\\'+which_elem+'_final_model_predictions_1to1_high.png'
ccam.plots.Plot1to1([truecomps[3]],[predicts[3]],plot_title,[labels[3]],[colors[3]],[markers[3]],imgfile,xminmax=xminmax,yminmax=yminmax)

with open(db_outputfile,'wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['','','','Full','Low ('+str(lowmin)+'-'+str(lowmax)+')','Mid ('+str(midmin)+'-'+str(midmax)+')','High ('+str(highmin)+'-'+str(highmax)+')','Blended']
        writer.writerow(row)
        row=['','','Norm=',fullnorm,lownorm,midnorm,highnorm]
        writer.writerow(row)
        row=['','','nc=',str(nc_full),str(nc_low),str(nc_mid),str(nc_high)]
        writer.writerow(row)
        row=['Target','Index','True Comp',which_elem,which_elem,which_elem,which_elem,which_elem]
        writer.writerow(row)
        
        for i in range(0,len(names)):
            row=[names[i],spect_index[i],str(comps[i,compindex][0]),y_db_full[i],y_db_low[i],y_db_mid[i],y_db_high[i],blended2[i]]
            writer.writerow(row)   


data,wvl,filelist=ccam.read_ccs(searchdir)

y_full,fullnorm=ccam.pls_predict(data,nc_full,wvl,maskfile,loadfile=loadfile_full,mean_file=means_file_full)
y_low,lownorm=ccam.pls_predict(data,nc_low,wvl,maskfile,loadfile=loadfile_low,mean_file=means_file_low)
y_mid,midnorm=ccam.pls_predict(data,nc_mid,wvl,maskfile,loadfile=loadfile_mid,mean_file=means_file_mid)
y_high,highnorm=ccam.pls_predict(data,nc_high,wvl,maskfile,loadfile=loadfile_high,mean_file=means_file_high)

predicts=[y_full,y_low,y_mid,y_high]
blended=ccam.submodels_blend(predicts,ranges,inrange,refpredict,toblend,overwrite=False)

targetlist,targetdists,targetamps=ccam.target_lookup(filelist,masterlist,name_subs)

y_combined=numpy.zeros_like(y_high)
print 'Writing results'
with open(outputfile,'wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['','','','','Full','Low ('+str(lowmin)+'-'+str(lowmax)+')','Mid ('+str(midmin)+'-'+str(midmax)+')','High ('+str(highmin)+'-'+str(highmax)+')','Blended']
        writer.writerow(row)
        row=['','','','Norm=',fullnorm,lownorm,midnorm,highnorm]
        writer.writerow(row)
        row=['','','','nc=',str(nc_full),str(nc_low),str(nc_mid),str(nc_high)]
        writer.writerow(row)
        row=['File','Target','Distance','Power',which_elem,which_elem,which_elem,which_elem,which_elem]
        writer.writerow(row)
        
        for i in range(0,len(y_combined)):
            row=[filelist[i],targetlist[i],targetdists[i],targetamps[i],y_full[i],y_low[i],y_mid[i],y_high[i],blended[i]]
            writer.writerow(row)        
        
        
