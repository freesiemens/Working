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

searchdir=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_team\Best APXS Comparisons'
maskfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\mask_minors_noise.csv'
outpath=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Output\K2O'
masterlist=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_misc\MASTERLIST.csv'
name_subs=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv'
dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected.csv'
keepfile=None
removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'
ica_db_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\ICA_1500mm_db.csv'
uni_db_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Univariate_1500mm_db.csv'


which_elem='K2O'
plstype='sklearn'
mincomp=0
maxcomp=100

#set plot range
xminmax=[0,20]
yminmax=[-5,20]

maxnc=30
fullmin=0
fullmax=100
lowmin=0
lowmax=2
midmin=1.5
midmax=5
highmin=3.5
highmax=100

fullnorm=1
lownorm=3
#midnorm=3
highnorm=1

#specify the number of components to use for each submodel
nc_full=10
nc_low=4
#nc_mid=6
nc_high=10

#specify the files that hold the mean centering info
means_file_full=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(fullnorm)+'_'+str(fullmin)+'-'+str(fullmax)+'_meancenters.csv'
means_file_low=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(lownorm)+'_'+str(lowmin)+'-'+str(lowmax)+'_meancenters.csv'
#means_file_mid=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(midnorm)+'_'+str(midmin)+'-'+str(midmax)+'_meancenters.csv'
means_file_high=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(highnorm)+'_'+str(highmin)+'-'+str(highmax)+'_meancenters.csv'

#specify the files that store the regression models (these are the python equivalent of IDL .SAV files)
loadfile_full=outpath+'\\'+which_elem+'_'+plstype+'_norm'+str(fullnorm)+'_'+str(fullmin)+'-'+str(fullmax)+'.pkl'
loadfile_low=outpath+'\\'+which_elem+'_'+plstype+'_norm'+str(lownorm)+'_'+str(lowmin)+'-'+str(lowmax)+'.pkl'
#loadfile_mid=outpath+'\\'+which_elem+'_'+plstype+'_norm'+str(midnorm)+'_'+str(midmin)+'-'+str(midmax)+'.pkl'
loadfile_high=outpath+'\\'+which_elem+'_'+plstype+'_norm'+str(highnorm)+'_'+str(highmin)+'-'+str(highmax)+'.pkl'

#specify where to save csv files with predictions
#outputfile=outpath+'\\'+which_elem+'_predictions_low ('+str(lowmin)+'-'+str(lowmax)+')_high ('+str(highmin)+'-'+str(highmax)+').csv'
#db_outputfile=outpath+'\\'+which_elem+'_db_predictions_low ('+str(lowmin)+'-'+str(lowmax)+')_high ('+str(highmin)+'-'+str(highmax)+').csv'
outputfile=outpath+'\\'+which_elem+'_predictions_low ('+str(lowmin)+'-'+str(lowmax)+')_full ('+str(fullmin)+'-'+str(fullmax)+').csv'
db_outputfile=outpath+'\\'+which_elem+'_db_predictions_low ('+str(lowmin)+'-'+str(lowmax)+')_full ('+str(fullmin)+'-'+str(fullmax)+').csv'


#specify files containing cross validation results
full_cv_file=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(fullnorm)+'_'+str(fullmin)+'-'+str(fullmax)+'_cv_predict.csv'
low_cv_file=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(lownorm)+'_'+str(lowmin)+'-'+str(lowmax)+'_cv_predict.csv'
#mid_cv_file=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(midnorm)+'_'+str(midmin)+'-'+str(midmax)+'_cv_predict.csv'
high_cv_file=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(highnorm)+'_'+str(highmin)+'-'+str(highmax)+'_cv_predict.csv'



#specify file names for  CV 1 to 1 plots
outfile1to1=outpath+'\\'+which_elem+'_submodels_1to1_plot_'+str(xminmax[0])+'_'+str(xminmax[1])+'.png'
outfile1to1_full=outpath+'\\'+which_elem+'_submodels_1to1_plot_'+str(xminmax[0])+'_'+str(xminmax[1])+'_full ('+str(fullmin)+'-'+str(fullmax)+').png'
outfile1to1_low=outpath+'\\'+which_elem+'_submodels_1to1_plot_'+str(xminmax[0])+'_'+str(xminmax[1])+'_low ('+str(lowmin)+'-'+str(lowmax)+').png'
outfile1to1_mid=outpath+'\\'+which_elem+'_submodels_1to1_plot_'+str(xminmax[0])+'_'+str(xminmax[1])+'_mid ('+str(midmin)+'-'+str(midmax)+').png'
outfile1to1_high=outpath+'\\'+which_elem+'_submodels_1to1_plot_'+str(xminmax[0])+'_'+str(xminmax[1])+'_high ('+str(highmin)+'-'+str(highmax)+').png'

#specify file names for full database 1 to 1 plots
imgfile=outpath+'\\'+which_elem+'_final_model_predictions_1to1_'+str(xminmax[0])+'-'+str(xminmax[1])+'.png'
imgfile_blended=outpath+'\\'+which_elem+'_final_model_predictions_1to1_'+str(xminmax[0])+'-'+str(xminmax[1])+'_blended.png'
imgfile_full=outpath+'\\'+which_elem+'_final_model_predictions_1to1_'+str(xminmax[0])+'-'+str(xminmax[1])+'_full ('+str(fullmin)+'-'+str(fullmax)+').png'
imgfile_low=outpath+'\\'+which_elem+'_final_model_predictions_1to1_'+str(xminmax[0])+'-'+str(xminmax[1])+'_low ('+str(lowmin)+'-'+str(lowmax)+').png'
imgfile_mid=outpath+'\\'+which_elem+'_final_model_predictions_1to1_'+str(xminmax[0])+'-'+str(xminmax[1])+'_mid ('+str(midmin)+'-'+str(midmax)+').png'
imgfile_high=outpath+'\\'+which_elem+'_final_model_predictions_1to1_'+str(xminmax[0])+'-'+str(xminmax[1])+'_high ('+str(highmin)+'-'+str(highmax)+').png'

print 'Reading database'
sys.stdout.flush()
spectra,comps,spect_index,names,labels,wvl=ccam.read_db(dbfile,compcheck=True)
oxides=labels[2:]
compindex=numpy.where(oxides==which_elem)[0]

print 'Choosing spectra'


spectra,names,spect_index,comps=ccam.choose_spectra(spectra,spect_index,names,comps,compindex,mincomp=0,maxcomp=100,keepfile=keepfile,removefile=removefile,which_removed=None)
y_db_full,fullnorm=ccam.pls_predict(spectra,nc_full,wvl,maskfile,loadfile=loadfile_full,mean_file=means_file_full)
y_db_low,lownorm=ccam.pls_predict(spectra,nc_low,wvl,maskfile,loadfile=loadfile_low,mean_file=means_file_low)
#y_db_mid,midnorm=ccam.pls_predict(spectra,nc_mid,wvl,maskfile,loadfile=loadfile_mid,mean_file=means_file_mid)
y_db_high,highnorm=ccam.pls_predict(spectra,nc_high,wvl,maskfile,loadfile=loadfile_high,mean_file=means_file_high)


"""
If full model <3, use the low model
if full model is 3 to 4, blend the low and full model using full as reference
if full model >4 use full
otherwise use full

Do not overwrite predictions that have already been set in a previous round of logic.
"""

predicts=[y_db_full,y_db_low,y_db_high]
ranges=[[-5,3],[3,4],[4,100],[0,100]]
inrange=[0,0,0,0]
refpredict=[0,0,0,0]
toblend=[[1,1],[1,0],[0,0],[0,0]]

blended2=ccam.submodels_blend(predicts,ranges,inrange,refpredict,toblend,overwrite=False)

truecomps=[comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex]]
predicts=[y_db_full,y_db_low,y_db_high,blended2]
plot_title='Final Model '+which_elem+' Predictions of Full Database'
labels=['Full','Low','High','Blended']
colors=['c','r','b','k']
markers=['o','<','^','*']

ccam.plots.Plot1to1(truecomps,predicts,plot_title,labels,colors,markers,imgfile,xminmax=xminmax,yminmax=yminmax)
ccam.plots.Plot1to1([truecomps[3]],[predicts[3]],plot_title,[labels[3]],[colors[3]],[markers[3]],imgfile_blended,xminmax=xminmax,yminmax=yminmax)
ccam.plots.Plot1to1([truecomps[0]],[predicts[0]],plot_title,[labels[0]],[colors[0]],[markers[0]],imgfile_full,xminmax=xminmax,yminmax=yminmax)
ccam.plots.Plot1to1([truecomps[1]],[predicts[1]],plot_title,[labels[1]],[colors[1]],[markers[1]],imgfile_low,xminmax=xminmax,yminmax=yminmax)
#ccam.plots.Plot1to1([truecomps[2]],[predicts[2]],plot_title,[labels[2]],[colors[2]],[markers[2]],imgfile_mid,xminmax=xminmax,yminmax=yminmax)
ccam.plots.Plot1to1([truecomps[2]],[predicts[2]],plot_title,[labels[2]],[colors[2]],[markers[2]],imgfile_high,xminmax=xminmax,yminmax=yminmax)

with open(db_outputfile,'wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['','','','Full','Low ('+str(lowmin)+'-'+str(lowmax)+')','High ('+str(highmin)+'-'+str(highmax)+')','Blended']
        writer.writerow(row)
        row=['','','Norm=',fullnorm,lownorm,highnorm]
        writer.writerow(row)
        row=['','','nc=',str(nc_full),str(nc_low),str(nc_high)]
        writer.writerow(row)
        row=['Target','Index','True Comp',which_elem,which_elem,which_elem,which_elem]
        writer.writerow(row)
        
        for i in range(0,len(names)):
            row=[names[i],spect_index[i],str(comps[i,compindex][0]),y_db_full[i],y_db_low[i],y_db_high[i],blended2[i]]
            writer.writerow(row)   

#make 1 to 1 plots using CV results

full_cv_predict,full_cv_samples,full_cv_truecomps,full_cv_folds,full_cv_spect=ccam.plots.readpredicts(full_cv_file,nc_full)
low_cv_predict,low_cv_samples,low_cv_truecomps,low_cv_folds,low_cv_spect=ccam.plots.readpredicts(low_cv_file,nc_low)
high_cv_predict,high_cv_samples,high_cv_truecomps,high_cv_folds,high_cv_spect=ccam.plots.readpredicts(high_cv_file,nc_high)
#mid_cv_predict,mid_cv_samples,mid_cv_truecomps,mid_cv_folds,mid_cv_spect=ccam.plots.readpredicts(mid_cv_file,nc_mid)


      
RMSECV_full=numpy.sqrt(numpy.mean((full_cv_predict-full_cv_truecomps)**2))
RMSECV_low=numpy.sqrt(numpy.mean((low_cv_predict-low_cv_truecomps)**2))
#RMSECV_mid=numpy.sqrt(numpy.mean((mid_cv_predict-mid_cv_truecomps)**2))
RMSECV_high=numpy.sqrt(numpy.mean((high_cv_predict-high_cv_truecomps)**2))

#mid_should_low=sum(numpy.all(numpy.vstack([(full_cv_predict>2.5),(full_cv_predict<11),(full_cv_truecomps<2.5)]),axis=0))
#low_should_mid=sum(numpy.all(numpy.vstack([(full_cv_predict<2.5),(full_cv_truecomps>2.5),(full_cv_truecomps<11)]),axis=0))
#mid_should_high=sum(numpy.all(numpy.vstack([(full_cv_predict>2.5),(full_cv_predict<11),(full_cv_truecomps>11)]),axis=0))
#high_should_mid=sum(numpy.all(numpy.vstack([(full_cv_predict>11),(full_cv_truecomps<11),(full_cv_truecomps>2.5)]),axis=0))


#RMSECV_combined=numpy.sqrt(numpy.mean((combined_cv_predict[(combined_cv_predict!=9999)]-full_cv_truecomps[(combined_cv_predict!=9999)])**2))

truecomps=[full_cv_truecomps,low_cv_truecomps,high_cv_truecomps]
predicts=[full_cv_predict,low_cv_predict,high_cv_predict]
labels=['Full (nc='+str(nc_full)+', norm='+str(fullnorm)+', RMSECV='+str(RMSECV_full)+')','Low (nc='+str(nc_low)+',norm='+str(lownorm)+', RMSECV='+str(RMSECV_low)+')','High (nc='+str(nc_high)+',norm='+str(highnorm)+', RMSECV='+str(RMSECV_high)+')']
colors=['c','r','b']
markers=['o','<','^']
plot_title=which_elem+' Cross Validation'
ccam.Plot1to1(truecomps,predicts,plot_title,labels,colors,markers,outfile1to1,xminmax=xminmax,yminmax=yminmax)
ccam.Plot1to1(truecomps[0],predicts[0],plot_title,labels[0],colors[0],markers[0],outfile1to1_full,xminmax=xminmax,yminmax=yminmax)
ccam.Plot1to1(truecomps[1],predicts[1],plot_title,labels[1],colors[1],markers[1],outfile1to1_low,xminmax=xminmax,yminmax=yminmax)
#ccam.Plot1to1(truecomps[2],predicts[2],plot_title,labels[2],colors[2],markers[2],outfile1to1_mid,xminmax=xminmax,yminmax=yminmax)
ccam.Plot1to1(truecomps[2],predicts[2],plot_title,labels[2],colors[2],markers[2],outfile1to1_high,xminmax=xminmax,yminmax=yminmax)



#get CCS results
data,wvl,filelist=ccam.read_ccs(searchdir)

y_full,fullnorm=ccam.pls_predict(data,nc_full,wvl,maskfile,loadfile=loadfile_full,mean_file=means_file_full)
y_low,lownorm=ccam.pls_predict(data,nc_low,wvl,maskfile,loadfile=loadfile_low,mean_file=means_file_low)
#y_mid,midnorm=ccam.pls_predict(data,nc_mid,wvl,maskfile,loadfile=loadfile_mid,mean_file=means_file_mid)
y_high,highnorm=ccam.pls_predict(data,nc_high,wvl,maskfile,loadfile=loadfile_high,mean_file=means_file_high)

predicts=[y_full,y_low,y_high]
blended=ccam.submodels_blend(predicts,ranges,inrange,refpredict,toblend,overwrite=False)

targetlist,targetdists,targetamps=ccam.target_lookup(filelist,masterlist,name_subs)

y_combined=numpy.zeros_like(y_high)
print 'Writing results'
with open(outputfile,'wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['','','','','Full','Low ('+str(lowmin)+'-'+str(lowmax)+')','High ('+str(highmin)+'-'+str(highmax)+')','Blended']
        writer.writerow(row)
        row=['','','','Norm=',fullnorm,lownorm,highnorm]
        writer.writerow(row)
        row=['','','','nc=',str(nc_full),str(nc_low),str(nc_high)]
        writer.writerow(row)
        row=['File','Target','Distance','Power',which_elem,which_elem,which_elem,which_elem]
        writer.writerow(row)
        
        for i in range(0,len(y_combined)):
            row=[filelist[i],targetlist[i],targetdists[i],targetamps[i],y_full[i],y_low[i],y_high[i],blended[i]]
            writer.writerow(row)        
        
  
