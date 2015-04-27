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

searchdir=r'M:\ChemCam MSL Data\ops_ccam_team'
searchdir_cal=r'D:\Ryan\20150401_Python_RLS_A\CCCT'
searchdir_apxs=r'D:\Ryan\20150401_Python_RLS_A\Best APXS Comparisons'
searchdir_val=r'D:\Ryan\20150401_Python_RLS_A\Validation Targets'
maskfile=r'D:\Ryan\20150401_Python_RLS_A\Input\mask_minors_noise.csv'
outpath=r'D:\Ryan\20150401_Python_RLS_A\Output\MgO'
masterlist=r'D:\Ryan\20150401_Python_RLS_A\Input\MASTERLIST.csv'
name_subs=r'D:\Ryan\20150401_Python_RLS_A\Input\target_name_subs.csv'
dbfile='D:\\Ryan\\20150401_Python_RLS_A\\Input\\full_db_mars_corrected.csv'
keepfile=None
removefile='D:\\Ryan\\20150401_Python_RLS_A\\Input\\removelist.csv'


#ica_db_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\ICA_1500mm_db.csv'
#uni_db_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Univariate_1500mm_db.csv'


which_elem='MgO'
plstype='sklearn'
mincomp=0
maxcomp=100

#set plot range
xminmax=[0,50]
yminmax=xminmax

maxnc=20
fullmin=0
fullmax=100
lowmin=0
lowmax=3.5
midmin=0
midmax=20
highmin=8
highmax=100

fullnorm=3
lownorm=1
midnorm=1
highnorm=3

#specify the number of components to use for each submodel
nc_full=7
nc_low=5
nc_mid=7
nc_high=7

#specify the files that hold the mean centering info
means_file_full=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(fullnorm)+'_'+str(fullmin)+'-'+str(fullmax)+'_meancenters.csv'
means_file_low=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(lownorm)+'_'+str(lowmin)+'-'+str(lowmax)+'_meancenters.csv'
means_file_mid=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(midnorm)+'_'+str(midmin)+'-'+str(midmax)+'_meancenters.csv'
means_file_high=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(highnorm)+'_'+str(highmin)+'-'+str(highmax)+'_meancenters.csv'

#specify the files that store the regression models (these are the python equivalent of IDL .SAV files)
loadfile_full=outpath+'\\'+which_elem+'_'+plstype+'_norm'+str(fullnorm)+'_'+str(fullmin)+'-'+str(fullmax)+'.pkl'
loadfile_low=outpath+'\\'+which_elem+'_'+plstype+'_norm'+str(lownorm)+'_'+str(lowmin)+'-'+str(lowmax)+'.pkl'
loadfile_mid=outpath+'\\'+which_elem+'_'+plstype+'_norm'+str(midnorm)+'_'+str(midmin)+'-'+str(midmax)+'.pkl'
loadfile_high=outpath+'\\'+which_elem+'_'+plstype+'_norm'+str(highnorm)+'_'+str(highmin)+'-'+str(highmax)+'.pkl'

#specify where to save csv files with predictions
outputfile=outpath+'\\'+which_elem+'_predictions.csv'
db_outputfile=outpath+'\\'+which_elem+'_db_predictions.csv'

#specify files containing cross validation results
full_cv_file=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(fullnorm)+'_'+str(fullmin)+'-'+str(fullmax)+'_cv_predict.csv'
low_cv_file=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(lownorm)+'_'+str(lowmin)+'-'+str(lowmax)+'_cv_predict.csv'
mid_cv_file=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(midnorm)+'_'+str(midmin)+'-'+str(midmax)+'_cv_predict.csv'
high_cv_file=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(highnorm)+'_'+str(highmin)+'-'+str(highmax)+'_cv_predict.csv'

#specify files containing outlier evaluation results
full_Qres_file=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(fullnorm)+'_'+str(fullmin)+'-'+str(fullmax)+'_Q_res.csv'
low_Qres_file=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(lownorm)+'_'+str(lowmin)+'-'+str(lowmax)+'_Q_res.csv'
mid_Qres_file=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(midnorm)+'_'+str(midmin)+'-'+str(midmax)+'_Q_res.csv'
high_Qres_file=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(highnorm)+'_'+str(highmin)+'-'+str(highmax)+'_Q_res.csv'

full_T2_file=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(fullnorm)+'_'+str(fullmin)+'-'+str(fullmax)+'_HotellingT2.csv'
low_T2_file=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(lownorm)+'_'+str(lowmin)+'-'+str(lowmax)+'_HotellingT2.csv'
mid_T2_file=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(midnorm)+'_'+str(midmin)+'-'+str(midmax)+'_HotellingT2.csv'
high_T2_file=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(highnorm)+'_'+str(highmin)+'-'+str(highmax)+'_HotellingT2.csv'

#specify file names for Q vs T2 plots
outfile_Q_T2=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(fullnorm)+'_'+str(fullmin)+'-'+str(fullmax)+'_QvsT2_full.png'
outfile_Q_T2_low=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(lownorm)+'_'+str(lowmin)+'-'+str(lowmax)+'_QvsT2_low.png'
outfile_Q_T2_mid=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(midnorm)+'_'+str(midmin)+'-'+str(midmax)+'_QvsT2_mid.png'
outfile_Q_T2_high=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(highnorm)+'_'+str(highmin)+'-'+str(highmax)+'_QvsT2_high.png'

#specify where to save csv files with predictions
outputfile=outpath+'\\'+which_elem+'_all_predictions_low ('+str(lowmin)+'-'+str(lowmax)+')_mid ('+str(midmin)+'-'+str(midmax)+')_high ('+str(highmin)+'-'+str(highmax)+').csv'
outputfile_apxs=outpath+'\\'+which_elem+'_apxs_predictions_low ('+str(lowmin)+'-'+str(lowmax)+')_mid ('+str(midmin)+'-'+str(midmax)+')_high ('+str(highmin)+'-'+str(highmax)+').csv'
outputfile_cal=outpath+'\\'+which_elem+'_cal_predictions_low ('+str(lowmin)+'-'+str(lowmax)+')_mid ('+str(midmin)+'-'+str(midmax)+')_high ('+str(highmin)+'-'+str(highmax)+').csv'
db_outputfile=outpath+'\\'+which_elem+'_db_predictions_low ('+str(lowmin)+'-'+str(lowmax)+')_mid ('+str(midmin)+'-'+str(midmax)+')_high ('+str(highmin)+'-'+str(highmax)+').csv'
outputfile_val=outpath+'\\'+which_elem+'_val_predictions_low ('+str(lowmin)+'-'+str(lowmax)+')_mid ('+str(midmin)+'-'+str(midmax)+')_high ('+str(highmin)+'-'+str(highmax)+').csv'

#specify files containing cross validation results
full_cv_file=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(fullnorm)+'_'+str(fullmin)+'-'+str(fullmax)+'_cv_predict.csv'
low_cv_file=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(lownorm)+'_'+str(lowmin)+'-'+str(lowmax)+'_cv_predict.csv'
mid_cv_file=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(midnorm)+'_'+str(midmin)+'-'+str(midmax)+'_cv_predict.csv'
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

print 'Making outlier check plots'
Q_res_full,Q_labels_full=ccam.read_csv_cols(full_Qres_file,0,labelrow=True)
Q_res_low,Q_labels_low=ccam.read_csv_cols(low_Qres_file,0,labelrow=True)
Q_res_mid,Q_labels_mid=ccam.read_csv_cols(mid_Qres_file,0,labelrow=True)
Q_res_high,Q_labels_high=ccam.read_csv_cols(high_Qres_file,0,labelrow=True)
Q_res_full=numpy.array(Q_res_full[4:],dtype='float')
Q_res_low=numpy.array(Q_res_low[4:],dtype='float')
Q_res_mid=numpy.array(Q_res_mid[4:],dtype='float')
Q_res_high=numpy.array(Q_res_high[4:],dtype='float')

T2_res_full,T2_labels_full=ccam.read_csv_cols(full_T2_file,0,labelrow=True)
T2_res_low,T2_labels_low=ccam.read_csv_cols(low_T2_file,0,labelrow=True)
T2_res_mid,T2_labels_mid=ccam.read_csv_cols(mid_T2_file,0,labelrow=True)
T2_res_high,T2_labels_high=ccam.read_csv_cols(high_T2_file,0,labelrow=True)
T2_res_full=numpy.array(T2_res_full[4:],dtype='float')
T2_res_low=numpy.array(T2_res_low[4:],dtype='float')
T2_res_mid=numpy.array(T2_res_mid[4:],dtype='float')
T2_res_high=numpy.array(T2_res_high[4:],dtype='float')

colors=['r']
markers=['o']
labels=['Full','Low','Mid','High','Blended']
plot_title=['Outlier check for '+which_elem]
ccam.plots.Plot1to1(T2_res_full[nc_full-1],Q_res_full[nc_full-1],plot_title,labels[0],colors[0],markers[0],outfile_Q_T2,xminmax=[0,1.1*numpy.max(T2_res_full[nc_full-1])],yminmax=[0,1.1*numpy.max(Q_res_full[nc_full-1])],ylabel='Q Residual',xlabel='Hotelling T2',one_to_one=False)
ccam.plots.Plot1to1(T2_res_low[nc_low-1],Q_res_low[nc_low-1],plot_title,labels[1],colors[0],markers[0],outfile_Q_T2_low,xminmax=[0,1.1*numpy.max(T2_res_low[nc_low-1])],yminmax=[0,1.1*numpy.max(Q_res_low[nc_low-1])],ylabel='Q Residual',xlabel='Hotelling T2',one_to_one=False)
ccam.plots.Plot1to1(T2_res_mid[nc_mid-1],Q_res_mid[nc_mid-1],plot_title,labels[2],colors[0],markers[0],outfile_Q_T2_mid,xminmax=[0,1.1*numpy.max(T2_res_mid[nc_mid-1])],yminmax=[0,1.1*numpy.max(Q_res_mid[nc_mid-1])],ylabel='Q Residual',xlabel='Hotelling T2',one_to_one=False)
ccam.plots.Plot1to1(T2_res_high[nc_high-1],Q_res_high[nc_high-1],plot_title,labels[3],colors[0],markers[0],outfile_Q_T2_high,xminmax=[0,1.1*numpy.max(T2_res_high[nc_high-1])],yminmax=[0,1.1*numpy.max(Q_res_high[nc_high-1])],ylabel='Q Residual',xlabel='Hotelling T2',one_to_one=False)

  
#make 1 to 1 plots using CV results

full_cv_predict,full_cv_samples,full_cv_truecomps,full_cv_folds,full_cv_spect=ccam.plots.readpredicts(full_cv_file,nc_full)
low_cv_predict,low_cv_samples,low_cv_truecomps,low_cv_folds,low_cv_spect=ccam.plots.readpredicts(low_cv_file,nc_low)
high_cv_predict,high_cv_samples,high_cv_truecomps,high_cv_folds,high_cv_spect=ccam.plots.readpredicts(high_cv_file,nc_high)
mid_cv_predict,mid_cv_samples,mid_cv_truecomps,mid_cv_folds,mid_cv_spect=ccam.plots.readpredicts(mid_cv_file,nc_mid)


      
RMSECV_full=numpy.sqrt(numpy.mean((full_cv_predict-full_cv_truecomps)**2))
RMSECV_low=numpy.sqrt(numpy.mean((low_cv_predict-low_cv_truecomps)**2))
RMSECV_mid=numpy.sqrt(numpy.mean((mid_cv_predict-mid_cv_truecomps)**2))
RMSECV_high=numpy.sqrt(numpy.mean((high_cv_predict-high_cv_truecomps)**2))



#RMSECV_combined=numpy.sqrt(numpy.mean((combined_cv_predict[(combined_cv_predict!=9999)]-full_cv_truecomps[(combined_cv_predict!=9999)])**2))

truecomps=[full_cv_truecomps,low_cv_truecomps,mid_cv_truecomps,high_cv_truecomps]
predicts=[full_cv_predict,low_cv_predict,mid_cv_predict,high_cv_predict]
labels=['Full (nc='+str(nc_full)+', norm='+str(fullnorm)+', RMSECV='+str(RMSECV_full)+')','Low (nc='+str(nc_low)+',norm='+str(lownorm)+', RMSECV='+str(RMSECV_low)+')','Low (nc='+str(nc_mid)+',norm='+str(midnorm)+', RMSECV='+str(RMSECV_mid)+')','High (nc='+str(nc_high)+',norm='+str(highnorm)+', RMSECV='+str(RMSECV_high)+')']
colors=['c','r','g','b']
markers=['o','<','v','^']
plot_title=which_elem+' Cross Validation'
ccam.Plot1to1(truecomps,predicts,plot_title,labels,colors,markers,outfile1to1,xminmax=xminmax,yminmax=yminmax)
ccam.Plot1to1(truecomps[0],predicts[0],plot_title,labels[0],colors[0],markers[0],outfile1to1_full,xminmax=xminmax,yminmax=yminmax)
ccam.Plot1to1(truecomps[1],predicts[1],plot_title,labels[1],colors[1],markers[1],outfile1to1_low,xminmax=xminmax,yminmax=yminmax)
ccam.Plot1to1(truecomps[2],predicts[2],plot_title,labels[2],colors[2],markers[2],outfile1to1_mid,xminmax=xminmax,yminmax=yminmax)
ccam.Plot1to1(truecomps[3],predicts[3],plot_title,labels[3],colors[3],markers[3],outfile1to1_high,xminmax=xminmax,yminmax=yminmax)




print 'Reading database'
sys.stdout.flush()
spectra,comps,spect_index,names,labels,wvl=ccam.read_db(dbfile,compcheck=True)
oxides=labels[2:]
compindex=numpy.where(oxides==which_elem)[0]

print 'Choosing spectra'


spectra,names,spect_index,comps=ccam.choose_spectra(spectra,spect_index,names,comps,compindex,mincomp=0,maxcomp=100,keepfile=keepfile,removefile=removefile,which_removed=None)
y_db_full,fullnorm=ccam.pls_predict(spectra,nc_full,wvl,maskfile,loadfile=loadfile_full,mean_file=means_file_full)
y_db_low,lownorm=ccam.pls_predict(spectra,nc_low,wvl,maskfile,loadfile=loadfile_low,mean_file=means_file_low)
y_db_mid,midnorm=ccam.pls_predict(spectra,nc_mid,wvl,maskfile,loadfile=loadfile_mid,mean_file=means_file_mid)
y_db_high,highnorm=ccam.pls_predict(spectra,nc_high,wvl,maskfile,loadfile=loadfile_high,mean_file=means_file_high)


"""
If full model <10, use the low model
if full is 10 to 20, blend the low and mid model using full as reference
If full model is 20 to 25 blend mid and high using full as reference
if full model is >25 use high
Use full for all others
Do not overwrite predictions that have already been set in a previous round of logic.
"""

predicts=[y_db_full,y_db_low,y_db_mid,y_db_high]
ranges=[[-10,1],[1,2],[2,6],[6,12],[12,100],[0,100]]
inrange=[0,0,0,0,0,0]
refpredict=[0,0,0,0,0,0]
toblend=[[1,1],[1,2],[2,2],[2,3],[3,0],[0,0]]

blended2=ccam.submodels_blend(predicts,ranges,inrange,refpredict,toblend,overwrite=False)

truecomps=[comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex]]
predicts=[y_db_full,y_db_low,y_db_mid,y_db_high,blended2]
plot_title='Final Model '+which_elem+' Predictions of Full Database'
labels=['Full','Low','Mid','High','Blended']
colors=['c','r','g','b','k']
markers=['o','<','v','^','*']

ccam.plots.Plot1to1(truecomps,predicts,plot_title,labels,colors,markers,imgfile,xminmax=xminmax,yminmax=yminmax)
ccam.plots.Plot1to1([truecomps[4]],[predicts[4]],plot_title,[labels[4]],[colors[4]],[markers[4]],imgfile_blended,xminmax=xminmax,yminmax=yminmax)
ccam.plots.Plot1to1([truecomps[0]],[predicts[0]],plot_title,[labels[0]],[colors[0]],[markers[0]],imgfile_full,xminmax=xminmax,yminmax=yminmax)
ccam.plots.Plot1to1([truecomps[1]],[predicts[1]],plot_title,[labels[1]],[colors[1]],[markers[1]],imgfile_low,xminmax=xminmax,yminmax=yminmax)
ccam.plots.Plot1to1([truecomps[2]],[predicts[2]],plot_title,[labels[2]],[colors[2]],[markers[2]],imgfile_mid,xminmax=xminmax,yminmax=yminmax)
ccam.plots.Plot1to1([truecomps[3]],[predicts[3]],plot_title,[labels[3]],[colors[3]],[markers[3]],imgfile_high,xminmax=xminmax,yminmax=yminmax)

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




#get apxs CCS results
data,wvl,filelist=ccam.read_ccs(searchdir_apxs)

y_full,fullnorm=ccam.pls_predict(data,nc_full,wvl,maskfile,loadfile=loadfile_full,mean_file=means_file_full)
y_low,lownorm=ccam.pls_predict(data,nc_low,wvl,maskfile,loadfile=loadfile_low,mean_file=means_file_low)
y_mid,midnorm=ccam.pls_predict(data,nc_mid,wvl,maskfile,loadfile=loadfile_mid,mean_file=means_file_mid)
y_high,highnorm=ccam.pls_predict(data,nc_high,wvl,maskfile,loadfile=loadfile_high,mean_file=means_file_high)

predicts=[y_full,y_low,y_mid,y_high]
blended=ccam.submodels_blend(predicts,ranges,inrange,refpredict,toblend,overwrite=False)

targetlist,targetdists,targetamps=ccam.target_lookup(filelist,masterlist,name_subs)

y_combined=numpy.zeros_like(y_high)
print 'Writing results'
with open(outputfile_apxs,'wb') as writefile:
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

#get validation CCS results
data,wvl,filelist=ccam.read_ccs(searchdir_val)

y_full,fullnorm=ccam.pls_predict(data,nc_full,wvl,maskfile,loadfile=loadfile_full,mean_file=means_file_full)
y_low,lownorm=ccam.pls_predict(data,nc_low,wvl,maskfile,loadfile=loadfile_low,mean_file=means_file_low)
y_mid,midnorm=ccam.pls_predict(data,nc_mid,wvl,maskfile,loadfile=loadfile_mid,mean_file=means_file_mid)
y_high,highnorm=ccam.pls_predict(data,nc_high,wvl,maskfile,loadfile=loadfile_high,mean_file=means_file_high)

predicts=[y_full,y_low,y_mid,y_high]
blended=ccam.submodels_blend(predicts,ranges,inrange,refpredict,toblend,overwrite=False)

targetlist,targetdists,targetamps=ccam.target_lookup(filelist,masterlist,name_subs)

y_combined=numpy.zeros_like(y_high)
print 'Writing results'
with open(outputfile_val,'wb') as writefile:
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

#get cal target CCS results
data,wvl,filelist=ccam.read_ccs(searchdir_cal)

y_full,fullnorm=ccam.pls_predict(data,nc_full,wvl,maskfile,loadfile=loadfile_full,mean_file=means_file_full)
y_low,lownorm=ccam.pls_predict(data,nc_low,wvl,maskfile,loadfile=loadfile_low,mean_file=means_file_low)
y_mid,midnorm=ccam.pls_predict(data,nc_mid,wvl,maskfile,loadfile=loadfile_mid,mean_file=means_file_mid)
y_high,highnorm=ccam.pls_predict(data,nc_high,wvl,maskfile,loadfile=loadfile_high,mean_file=means_file_high)

predicts=[y_full,y_low,y_mid,y_high]
blended=ccam.submodels_blend(predicts,ranges,inrange,refpredict,toblend,overwrite=False)

targetlist,targetdists,targetamps=ccam.target_lookup(filelist,masterlist,name_subs)

y_combined=numpy.zeros_like(y_high)
print 'Writing results'
with open(outputfile_cal,'wb') as writefile:
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


#get CCS results
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
        
  


