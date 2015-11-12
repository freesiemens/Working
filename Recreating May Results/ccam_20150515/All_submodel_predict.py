# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:08:53 2015

@author: rbanderson
"""
import ccam
import numpy
import csv
import sys


def generate_filenames(which_elem,outpath,plstype,maxnc,fullnorm,fullmin,fullmax,lownorm,lowmin,lowmax,midnorm,midmin,midmax,highnorm,highmin,highmax,xminmax,yminmax):
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

    return means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,full_cv_file,low_cv_file,mid_cv_file,high_cv_file,outfile1to1,outfile1to1_full,outfile1to1_low,outfile1to1_mid,outfile1to1_high,imgfile,imgfile_blended,imgfile_full,imgfile_low,imgfile_mid,imgfile_high,full_Qres_file,low_Qres_file,mid_Qres_file,high_Qres_file,full_T2_file,low_T2_file,mid_T2_file,high_T2_file,outfile_Q_T2,outfile_Q_T2_low,outfile_Q_T2_mid,outfile_Q_T2_high,outputfile,outputfile_apxs,outputfile_val,outputfile_cal,db_outputfile
    
    
    
def blend_predict(data,wvl,filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile):
    
    
    y_full,fullnorm=ccam.pls_predict(data,nc_full,wvl,maskfile,loadfile=loadfile_full,mean_file=means_file_full)
    y_low,lownorm=ccam.pls_predict(data,nc_low,wvl,maskfile,loadfile=loadfile_low,mean_file=means_file_low)
    y_mid,midnorm=ccam.pls_predict(data,nc_mid,wvl,maskfile,loadfile=loadfile_mid,mean_file=means_file_mid)
    y_high,highnorm=ccam.pls_predict(data,nc_high,wvl,maskfile,loadfile=loadfile_high,mean_file=means_file_high)
    
    predicts=[y_full,y_low,y_mid,y_high]
    blended=ccam.submodels_blend(predicts,ranges,inrange,refpredict,toblend,overwrite=False)
    
    targetlist,targetdists,targetamps,nshots=ccam.target_lookup(filelist,masterlist,name_subs)
    
    y_combined=numpy.zeros_like(y_high)
    print 'Writing results'
    with open(outputfile,'wb') as writefile:
            writer=csv.writer(writefile,delimiter=',')
            row=['','','','','Full ('+str(fullmin)+'-'+str(fullmax)+')','Low ('+str(lowmin)+'-'+str(lowmax)+')','Mid ('+str(midmin)+'-'+str(midmax)+')','High ('+str(highmin)+'-'+str(highmax)+')','Blended']
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

def outlier_plots(full_Qres_file,low_Qres_file,mid_Qres_file,high_Qres_file,full_T2_file,low_T2_file,mid_T2_file,high_T2_file,fullnorm,nc_full,lownorm,nc_low,midnorm,nc_mid,highnorm,nc_high,which_elem):
 
    Q_res_full,Q_labels_full=ccam.read_csv(full_Qres_file,0,labelrow=True)
    Q_res_low,Q_labels_low=ccam.read_csv(low_Qres_file,0,labelrow=True)
    Q_res_mid,Q_labels_mid=ccam.read_csv(mid_Qres_file,0,labelrow=True)
    Q_res_high,Q_labels_high=ccam.read_csv(high_Qres_file,0,labelrow=True)
    Q_res_full=numpy.array(Q_res_full[:,4:],dtype='float')
    Q_res_low=numpy.array(Q_res_low[:,4:],dtype='float')
    Q_res_mid=numpy.array(Q_res_mid[:,4:],dtype='float')
    Q_res_high=numpy.array(Q_res_high[:,4:],dtype='float')
    
    T2_res_full,T2_labels_full=ccam.read_csv(full_T2_file,0,labelrow=True)
    T2_res_low,T2_labels_low=ccam.read_csv(low_T2_file,0,labelrow=True)
    T2_res_mid,T2_labels_mid=ccam.read_csv(mid_T2_file,0,labelrow=True)
    T2_res_high,T2_labels_high=ccam.read_csv(high_T2_file,0,labelrow=True)
    T2_res_full=numpy.array(T2_res_full[:,4:],dtype='float')
    T2_res_low=numpy.array(T2_res_low[:,4:],dtype='float')
    T2_res_mid=numpy.array(T2_res_mid[:,4:],dtype='float')
    T2_res_high=numpy.array(T2_res_high[:,4:],dtype='float')
    
    colors=['r']
    markers=['o']
    labels=['Full Norm='+str(fullnorm)+' NC='+str(nc_full),'Low Norm='+str(lownorm)+' NC='+str(nc_low),'Mid Norm='+str(midnorm)+' NC='+str(nc_mid),'High Norm='+str(highnorm)+' NC='+str(nc_high),'Blended']
    plot_title=['Outlier check for '+which_elem]
    ccam.plots.Plot1to1(T2_res_full[nc_full-1],Q_res_full[nc_full-1],plot_title,labels[0],colors[0],markers[0],outfile_Q_T2,xminmax=[0,1.1*numpy.max(T2_res_full[nc_full-1])],yminmax=[0,1.1*numpy.max(Q_res_full[nc_full-1])],ylabel='Q Residual',xlabel='Hotelling T2',one_to_one=False)
    ccam.plots.Plot1to1(T2_res_low[nc_low-1],Q_res_low[nc_low-1],plot_title,labels[1],colors[0],markers[0],outfile_Q_T2_low,xminmax=[0,1.1*numpy.max(T2_res_low[nc_low-1])],yminmax=[0,1.1*numpy.max(Q_res_low[nc_low-1])],ylabel='Q Residual',xlabel='Hotelling T2',one_to_one=False)
    ccam.plots.Plot1to1(T2_res_mid[nc_mid-1],Q_res_mid[nc_mid-1],plot_title,labels[2],colors[0],markers[0],outfile_Q_T2_mid,xminmax=[0,1.1*numpy.max(T2_res_mid[nc_mid-1])],yminmax=[0,1.1*numpy.max(Q_res_mid[nc_mid-1])],ylabel='Q Residual',xlabel='Hotelling T2',one_to_one=False)
    ccam.plots.Plot1to1(T2_res_high[nc_high-1],Q_res_high[nc_high-1],plot_title,labels[3],colors[0],markers[0],outfile_Q_T2_high,xminmax=[0,1.1*numpy.max(T2_res_high[nc_high-1])],yminmax=[0,1.1*numpy.max(Q_res_high[nc_high-1])],ylabel='Q Residual',xlabel='Hotelling T2',one_to_one=False)
    
def cv_plots(full_cv_file,nc_full,fullnorm,low_cv_file,nc_low,lownorm,mid_cv_file,nc_mid,midnorm,high_cv_file,nc_high,highnorm,xminmax,yminmax,which_elem):      
    #make 1 to 1 plots using CV results
    
    full_cv_predict,full_cv_samples,full_cv_truecomps,full_cv_folds,full_cv_spect=ccam.plots.readpredicts(full_cv_file,nc_full)
    low_cv_predict,low_cv_samples,low_cv_truecomps,low_cv_folds,low_cv_spect=ccam.plots.readpredicts(low_cv_file,nc_low)
    high_cv_predict,high_cv_samples,high_cv_truecomps,high_cv_folds,high_cv_spect=ccam.plots.readpredicts(high_cv_file,nc_high)
    mid_cv_predict,mid_cv_samples,mid_cv_truecomps,mid_cv_folds,mid_cv_spect=ccam.plots.readpredicts(mid_cv_file,nc_mid)
    
    
          
    RMSECV_full=numpy.sqrt(numpy.mean((full_cv_predict-full_cv_truecomps)**2))
    RMSECV_low=numpy.sqrt(numpy.mean((low_cv_predict-low_cv_truecomps)**2))
    RMSECV_mid=numpy.sqrt(numpy.mean((mid_cv_predict-mid_cv_truecomps)**2))
    RMSECV_high=numpy.sqrt(numpy.mean((high_cv_predict-high_cv_truecomps)**2))
    
    
    truecomps=[full_cv_truecomps,low_cv_truecomps,mid_cv_truecomps,high_cv_truecomps]
    predicts=[full_cv_predict,low_cv_predict,mid_cv_predict,high_cv_predict]
    labels=['Full (nc='+str(nc_full)+', norm='+str(fullnorm)+', RMSECV='+str(RMSECV_full)+')','Low (nc='+str(nc_low)+',norm='+str(lownorm)+', RMSECV='+str(RMSECV_low)+')','Mid (nc='+str(nc_mid)+',norm='+str(midnorm)+', RMSECV='+str(RMSECV_mid)+')','High (nc='+str(nc_high)+',norm='+str(highnorm)+', RMSECV='+str(RMSECV_high)+')']
    colors=['c','r','g','b']
    markers=['o','<','v','^']
    plot_title=which_elem+' Cross Validation'
    ccam.Plot1to1(truecomps,predicts,plot_title,labels,colors,markers,outfile1to1,xminmax=xminmax,yminmax=yminmax)
    ccam.Plot1to1(truecomps[0],predicts[0],plot_title,labels[0],colors[0],markers[0],outfile1to1_full,xminmax=xminmax,yminmax=yminmax)
    ccam.Plot1to1(truecomps[1],predicts[1],plot_title,labels[1],colors[1],markers[1],outfile1to1_low,xminmax=xminmax,yminmax=yminmax)
    ccam.Plot1to1(truecomps[2],predicts[2],plot_title,labels[2],colors[2],markers[2],outfile1to1_mid,xminmax=xminmax,yminmax=yminmax)
    ccam.Plot1to1(truecomps[3],predicts[3],plot_title,labels[3],colors[3],markers[3],outfile1to1_high,xminmax=xminmax,yminmax=yminmax)

def final_model_results(y_db_full,y_db_low,y_db_mid,y_db_high,ranges,inrange,refpredict,toblend,truecomps,xminmax,yminmax,fullmin,fullmax,fullnorm,nc_full,lowmin,lowmax,lownorm,nc_low,midmin,midmax,midnorm,nc_mid,highmin,highmax,highnorm,nc_high,which_elem):
    predicts=[y_db_full,y_db_low,y_db_mid,y_db_high]    
    blended2=ccam.submodels_blend(predicts,ranges,inrange,refpredict,toblend,overwrite=False)
    #Create plots of the full model results (NOTE: these plots will show artificially "optimistic" results
    # within the range where the model was trained. These are meant to be used primarily to visualize how the models will do when extrapolating,
    #NOT for evaluation of model accuracy within its training range)
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
            row=['','','','Full ('+str(fullmin)+'-'+str(fullmax)+')','Low ('+str(lowmin)+'-'+str(lowmax)+')','High ('+str(highmin)+'-'+str(highmax)+')','Blended']
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

##############################  SiO2 #####################################


#The directory to search (recursively) for all chemcam CCS files
searchdir=r'F:\ChemCam\ops_ccam_team\CalTarget 95A'
#The directory to search (recursively) for all chemcam cal target CCS files that you want to use
searchdir_cal=r'F:\ChemCam\ops_ccam_team\CalTarget 95A'
#The directory to search (recursively) for all chemcam "good APXS" CCS files that you want to use
searchdir_apxs=r'F:\ChemCam\ops_ccam_team\Best APXS Comparisons'
#The directory to search (recursively) for a list of CCS files for our list of well-known Mars targets
searchdir_val=r'F:\ChemCam\ops_ccam_team\Validation Targets'

#File specifying what part(s) of the spectrum to mask
maskfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\mask_minors_noise.csv'
#Where to write all results
outpath=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Recreating May Results\ccam_20150515\Output\SiO2'
#Location of the master list file (used to look up target names and other info)
masterlist=r'F:\ChemCam\ops_ccam_misc\MASTERLIST_combined_20150811.csv'
#Location of a file with target name substitutions (this is used primarily to substitute cal target names: Cal Target 1 --> Macusanite)
name_subs=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv'
#location of the database file containing compositions and spectra
dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected.csv'
#Location of a file listing spectra to be removed from the model
removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'

#Which element are you predicting?
which_elem='SiO2'
#outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Only_Caltargets_Removed\\'#
outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Final\\'

#Which algorithm to use? (mlpy or sklearn - they give the same results)
plstype='sklearn'

#set plot range
xminmax=[0,100]
yminmax=xminmax

#set number of components
maxnc=20

#set submodel composition ranges
fullmin=0
fullmax=100
lowmin=0
lowmax=50
midmin=30
midmax=70
highmin=60
highmax=100

#sete submodel normalization settings (3 or 1)
fullnorm=3
lownorm=3
midnorm=3
highnorm=1

#specify the number of components to use for each submodel
nc_full=9
nc_low=13
nc_mid=10
nc_high=6


means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,full_cv_file,low_cv_file,mid_cv_file,high_cv_file,outfile1to1,outfile1to1_full,outfile1to1_low,outfile1to1_mid,outfile1to1_high,imgfile,imgfile_blended,imgfile_full,imgfile_low,imgfile_mid,imgfile_high,full_Qres_file,low_Qres_file,mid_Qres_file,high_Qres_file,full_T2_file,low_T2_file,mid_T2_file,high_T2_file,outfile_Q_T2,outfile_Q_T2_low,outfile_Q_T2_mid,outfile_Q_T2_high,outputfile,outputfile_apxs,outputfile_val,outputfile_cal,db_outputfile=generate_filenames(which_elem,outpath,plstype,maxnc,fullnorm,fullmin,fullmax,lownorm,lowmin,lowmax,midnorm,midmin,midmax,highnorm,highmin,highmax,xminmax,yminmax)

print 'Making outlier check plots'
outlier_plots(full_Qres_file,low_Qres_file,mid_Qres_file,high_Qres_file,full_T2_file,low_T2_file,mid_T2_file,high_T2_file,fullnorm,nc_full,lownorm,nc_low,midnorm,nc_mid,highnorm,nc_high,which_elem)
print "Making 1 to 1 plots using CV results"
cv_plots(full_cv_file,nc_full,fullnorm,low_cv_file,nc_low,lownorm,mid_cv_file,nc_mid,midnorm,high_cv_file,nc_high,highnorm,xminmax,yminmax,which_elem)

print 'Reading database'
sys.stdout.flush()
spectra,comps,spect_index,names,labels,wvl=ccam.read_db(dbfile,compcheck=True)
oxides=labels[2:]
compindex=numpy.where(oxides==which_elem)[0]

print 'Choosing spectra'


spectra,names,spect_index,comps=ccam.choose_spectra(spectra,spect_index,names,comps,compindex,mincomp=0,maxcomp=100,keepfile=None,removefile=removefile,which_removed=None)
y_db_full,fullnorm=ccam.pls_predict(spectra,nc_full,wvl,maskfile,loadfile=loadfile_full,mean_file=means_file_full)
y_db_low,lownorm=ccam.pls_predict(spectra,nc_low,wvl,maskfile,loadfile=loadfile_low,mean_file=means_file_low)
y_db_mid,midnorm=ccam.pls_predict(spectra,nc_mid,wvl,maskfile,loadfile=loadfile_mid,mean_file=means_file_mid)
y_db_high,highnorm=ccam.pls_predict(spectra,nc_high,wvl,maskfile,loadfile=loadfile_high,mean_file=means_file_high)


"""
Define blending settings:
"""

ranges=[[-10,30],[30,40],[40,60],[60,70],[70,100]]
inrange=[0,0,0,0,0]
refpredict=[0,0,0,0,0]
toblend=[[1,1],[1,2],[2,2],[2,3],[3,3]]

truecomps=[comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex]]

final_model_results(y_db_full,y_db_low,y_db_mid,y_db_high,ranges,inrange,refpredict,toblend,truecomps,xminmax,yminmax,fullmin,fullmax,fullnorm,nc_full,lowmin,lowmax,lownorm,nc_low,midmin,midmax,midnorm,nc_mid,highmin,highmax,highnorm,nc_high,which_elem)

#Read CCS data
#apxs_data,apxs_wvl,apxs_filelist,shotnums=ccam.read_ccs(searchdir_apxs,shots=True,masterlist=masterlist,name_sub_file=name_subs)
apxs_data,apxs_wvl,apxs_filelist,=ccam.read_ccs(searchdir_apxs)
val_data,val_wvl,val_filelist=ccam.read_ccs(searchdir_val)
cal_data,cal_wvl,cal_filelist=ccam.read_ccs(searchdir_cal)
all_data,all_wvl,all_filelist=ccam.read_ccs(searchdir)


#get apxs CCS results
blend_predict(apxs_data,apxs_wvl,apxs_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_apxs,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get validation CCS results
blend_predict(val_data,val_wvl,val_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_val,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get cal target CCS results
blend_predict(cal_data,cal_wvl,cal_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_cal,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get CCS results (this step takes a while because it needs to read all the CCS files)
blend_predict(all_data,all_wvl,all_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)


##############################  TiO2 #####################################

searchdir=r'F:\ChemCam\ops_ccam_team\CalTarget 95A'
searchdir_cal=r'F:\ChemCam\ops_ccam_team\CalTarget 95A'
searchdir_apxs=r'F:\ChemCam\ops_ccam_team\Best APXS Comparisons'
searchdir_val=r'F:\ChemCam\ops_ccam_team\Validation Targets'
maskfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\mask_minors_noise.csv'
outpath=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Recreating May Results\ccam_20150515\Output\TiO2'
masterlist=r'F:\ChemCam\ops_ccam_misc\MASTERLIST_combined_20150811.csv'
name_subs=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv'
dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected_dopedTiO2.csv'
keepfile=None
removefile=None#'C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'


which_elem='TiO2'
#outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Only_Caltargets_Removed\\'#
outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Final\\'

plstype='sklearn'
mincomp=0
maxcomp=100

#set plot range
xminmax=[0,15]
yminmax=xminmax

maxnc=30
fullmin=0
fullmax=100
lowmin=0
lowmax=2
midmin=1
midmax=5
highmin=3
highmax=100

fullnorm=3
lownorm=1
midnorm=1
highnorm=1

#specify the number of components to use for each submodel
nc_full=6
nc_low=5
nc_mid=4
nc_high=5
means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,full_cv_file,low_cv_file,mid_cv_file,high_cv_file,outfile1to1,outfile1to1_full,outfile1to1_low,outfile1to1_mid,outfile1to1_high,imgfile,imgfile_blended,imgfile_full,imgfile_low,imgfile_mid,imgfile_high,full_Qres_file,low_Qres_file,mid_Qres_file,high_Qres_file,full_T2_file,low_T2_file,mid_T2_file,high_T2_file,outfile_Q_T2,outfile_Q_T2_low,outfile_Q_T2_mid,outfile_Q_T2_high,outputfile,outputfile_apxs,outputfile_val,outputfile_cal,db_outputfile=generate_filenames(which_elem,outpath,plstype,maxnc,fullnorm,fullmin,fullmax,lownorm,lowmin,lowmax,midnorm,midmin,midmax,highnorm,highmin,highmax,xminmax,yminmax)

print 'Making outlier check plots'
outlier_plots(full_Qres_file,low_Qres_file,mid_Qres_file,high_Qres_file,full_T2_file,low_T2_file,mid_T2_file,high_T2_file,fullnorm,nc_full,lownorm,nc_low,midnorm,nc_mid,highnorm,nc_high,which_elem)
print "Making 1 to 1 plots using CV results"
cv_plots(full_cv_file,nc_full,fullnorm,low_cv_file,nc_low,lownorm,mid_cv_file,nc_mid,midnorm,high_cv_file,nc_high,highnorm,xminmax,yminmax,which_elem)


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
If full model 0 to 1, use the low model
if full model is 1 to 2, blend the low and high model using full as reference
if full model is 2 to 100 use high
Use full for all others
Do not overwrite predictions that have already been set in a previous round of logic.
"""

predicts=[y_db_full,y_db_low,y_db_mid,y_db_high]
ranges=[[0,1],[1,2],[2,4],[4,100],[0,100]]
inrange=[0,0,0,0,0]
refpredict=[0,0,0,0,0]
toblend=[[1,1],[1,2],[2,3],[3,3],[0,0]]


truecomps=[comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex]]
final_model_results(y_db_full,y_db_low,y_db_mid,y_db_high,ranges,inrange,refpredict,toblend,truecomps,xminmax,yminmax,fullmin,fullmax,fullnorm,nc_full,lowmin,lowmax,lownorm,nc_low,midmin,midmax,midnorm,nc_mid,highmin,highmax,highnorm,nc_high,which_elem)



#get apxs CCS results
blend_predict(apxs_data,apxs_wvl,apxs_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_apxs,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get validation CCS results
blend_predict(val_data,val_wvl,val_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_val,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get cal target CCS results
blend_predict(cal_data,cal_wvl,cal_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_cal,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get CCS results (this step takes a while because it needs to read all the CCS files)
blend_predict(all_data,all_wvl,all_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)



##############################  Al2O3 #####################################

searchdir=r'F:\ChemCam\ops_ccam_team\CalTarget 95A'
searchdir_cal=r'F:\ChemCam\ops_ccam_team\CalTarget 95A'
searchdir_apxs=r'F:\ChemCam\ops_ccam_team\Best APXS Comparisons'
searchdir_val=r'F:\ChemCam\ops_ccam_team\Validation Targets'
maskfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\mask_minors_noise.csv'
outpath=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Recreating May Results\ccam_20150515\Output\Al2O3'
masterlist=r'F:\ChemCam\ops_ccam_misc\MASTERLIST_combined_20150811.csv'
name_subs=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv'
dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected.csv'
keepfile=None
removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'



which_elem='Al2O3'
#outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Only_Caltargets_Removed\\'#
outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Final\\'

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
lowmax=12
midmin=10
midmax=25
highmin=20
highmax=100

fullnorm=1
lownorm=1
midnorm=1
highnorm=1

#specify the number of components to use for each submodel
nc_full=7
nc_low=9
nc_mid=8
nc_high=4
means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,full_cv_file,low_cv_file,mid_cv_file,high_cv_file,outfile1to1,outfile1to1_full,outfile1to1_low,outfile1to1_mid,outfile1to1_high,imgfile,imgfile_blended,imgfile_full,imgfile_low,imgfile_mid,imgfile_high,full_Qres_file,low_Qres_file,mid_Qres_file,high_Qres_file,full_T2_file,low_T2_file,mid_T2_file,high_T2_file,outfile_Q_T2,outfile_Q_T2_low,outfile_Q_T2_mid,outfile_Q_T2_high,outputfile,outputfile_apxs,outputfile_val,outputfile_cal,db_outputfile=generate_filenames(which_elem,outpath,plstype,maxnc,fullnorm,fullmin,fullmax,lownorm,lowmin,lowmax,midnorm,midmin,midmax,highnorm,highmin,highmax,xminmax,yminmax)

print 'Making outlier check plots'
outlier_plots(full_Qres_file,low_Qres_file,mid_Qres_file,high_Qres_file,full_T2_file,low_T2_file,mid_T2_file,high_T2_file,fullnorm,nc_full,lownorm,nc_low,midnorm,nc_mid,highnorm,nc_high,which_elem)
print "Making 1 to 1 plots using CV results"
cv_plots(full_cv_file,nc_full,fullnorm,low_cv_file,nc_low,lownorm,mid_cv_file,nc_mid,midnorm,high_cv_file,nc_high,highnorm,xminmax,yminmax,which_elem)

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
If full model <12, use the low model
if full is 12 to 20, blend the low and mid model using full as reference
If full model is 20 to 25 blend mid and high using full as reference
if full model is >25 use high
Use full for all others
Do not overwrite predictions that have already been set in a previous round of logic.
"""

predicts=[y_db_full,y_db_low,y_db_mid,y_db_high]
ranges=[[-10,12],[12,20],[20,25],[25,100],[0,100]]
inrange=[0,0,0,0,0]
refpredict=[0,0,0,0,0]
toblend=[[1,1],[1,2],[2,3],[3,3],[0,0]]


truecomps=[comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex]]
final_model_results(y_db_full,y_db_low,y_db_mid,y_db_high,ranges,inrange,refpredict,toblend,truecomps,xminmax,yminmax,fullmin,fullmax,fullnorm,nc_full,lowmin,lowmax,lownorm,nc_low,midmin,midmax,midnorm,nc_mid,highmin,highmax,highnorm,nc_high,which_elem)




#get apxs CCS results
blend_predict(apxs_data,apxs_wvl,apxs_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_apxs,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get validation CCS results
blend_predict(val_data,val_wvl,val_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_val,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get cal target CCS results
blend_predict(cal_data,cal_wvl,cal_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_cal,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get CCS results (this step takes a while because it needs to read all the CCS files)
blend_predict(all_data,all_wvl,all_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)


  
##############################  FeOT #####################################

searchdir=r'F:\ChemCam\ops_ccam_teamCalTarget 95A'
searchdir_cal=r'F:\ChemCam\ops_ccam_team\CalTarget 95A'
searchdir_apxs=r'F:\ChemCam\ops_ccam_team\Best APXS Comparisons'
searchdir_val=r'F:\ChemCam\ops_ccam_team\Validation Targets'
maskfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\mask_minors_noise.csv'
outpath=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Recreating May Results\ccam_20150515\Output\FeOT'
masterlist=r'F:\ChemCam\ops_ccam_misc\MASTERLIST_combined_20150811.csv'
name_subs=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv'
dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected.csv'
keepfile=None
removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'



which_elem='FeOT'
#outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Only_Caltargets_Removed\\'#
outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Final\\'

plstype='sklearn'
mincomp=0
maxcomp=100

#set plot range
xminmax=[0,100]
yminmax=xminmax

maxnc=30
fullmin=0
fullmax=100
lowmin=0
lowmax=15
midmin=5
midmax=25
highmin=15
highmax=100

fullnorm=1
lownorm=3
midnorm=1
highnorm=1

#specify the number of components to use for each submodel
nc_full=6
nc_low=3
nc_mid=10
nc_high=5
means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,full_cv_file,low_cv_file,mid_cv_file,high_cv_file,outfile1to1,outfile1to1_full,outfile1to1_low,outfile1to1_mid,outfile1to1_high,imgfile,imgfile_blended,imgfile_full,imgfile_low,imgfile_mid,imgfile_high,full_Qres_file,low_Qres_file,mid_Qres_file,high_Qres_file,full_T2_file,low_T2_file,mid_T2_file,high_T2_file,outfile_Q_T2,outfile_Q_T2_low,outfile_Q_T2_mid,outfile_Q_T2_high,outputfile,outputfile_apxs,outputfile_val,outputfile_cal,db_outputfile=generate_filenames(which_elem,outpath,plstype,maxnc,fullnorm,fullmin,fullmax,lownorm,lowmin,lowmax,midnorm,midmin,midmax,highnorm,highmin,highmax,xminmax,yminmax)

print 'Making outlier check plots'
outlier_plots(full_Qres_file,low_Qres_file,mid_Qres_file,high_Qres_file,full_T2_file,low_T2_file,mid_T2_file,high_T2_file,fullnorm,nc_full,lownorm,nc_low,midnorm,nc_mid,highnorm,nc_high,which_elem)
print "Making 1 to 1 plots using CV results"
cv_plots(full_cv_file,nc_full,fullnorm,low_cv_file,nc_low,lownorm,mid_cv_file,nc_mid,midnorm,high_cv_file,nc_high,highnorm,xminmax,yminmax,which_elem)


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
If full model <5, use the low model
if full is 5 to 10, blend the low and mid model using full as reference
If full model is 10 to 20 use mid
if full is 20 to 25, blend mid and high using full as reference
if full model is >25 use high
Use full for all others
Do not overwrite predictions that have already been set in a previous round of logic.
"""

predicts=[y_db_full,y_db_low,y_db_mid,y_db_high]
ranges=[[-10,5],[5,10],[10,20],[20,25],[25,100]]
inrange=[0,0,0,0,0]
refpredict=[0,0,0,0,0]
toblend=[[1,1],[1,2],[2,2],[2,3],[3,3]]

truecomps=[comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex]]
final_model_results(y_db_full,y_db_low,y_db_mid,y_db_high,ranges,inrange,refpredict,toblend,truecomps,xminmax,yminmax,fullmin,fullmax,fullnorm,nc_full,lowmin,lowmax,lownorm,nc_low,midmin,midmax,midnorm,nc_mid,highmin,highmax,highnorm,nc_high,which_elem)

#get apxs CCS results
blend_predict(apxs_data,apxs_wvl,apxs_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_apxs,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get validation CCS results
blend_predict(val_data,val_wvl,val_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_val,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get cal target CCS results
blend_predict(cal_data,cal_wvl,cal_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_cal,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get CCS results (this step takes a while because it needs to read all the CCS files)
blend_predict(all_data,all_wvl,all_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)


##############################  MgO #####################################

searchdir=r'F:\ChemCam\ops_ccam_team\CalTarget 95A'
searchdir_cal=r'F:\ChemCam\ops_ccam_team\CalTarget 95A'
searchdir_apxs=r'F:\ChemCam\ops_ccam_team\Best APXS Comparisons'
searchdir_val=r'F:\ChemCam\ops_ccam_team\Validation Targets'
maskfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\mask_minors_noise.csv'
outpath=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Recreating May Results\ccam_20150515\Output\MgO'
masterlist=r'F:\ChemCam\ops_ccam_misc\MASTERLIST_combined_20150811.csv'
name_subs=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv'
dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected.csv'
keepfile=None
removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'


which_elem='MgO'
#outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Only_Caltargets_Removed\\'#
outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Final\\'

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
means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,full_cv_file,low_cv_file,mid_cv_file,high_cv_file,outfile1to1,outfile1to1_full,outfile1to1_low,outfile1to1_mid,outfile1to1_high,imgfile,imgfile_blended,imgfile_full,imgfile_low,imgfile_mid,imgfile_high,full_Qres_file,low_Qres_file,mid_Qres_file,high_Qres_file,full_T2_file,low_T2_file,mid_T2_file,high_T2_file,outfile_Q_T2,outfile_Q_T2_low,outfile_Q_T2_mid,outfile_Q_T2_high,outputfile,outputfile_apxs,outputfile_val,outputfile_cal,db_outputfile=generate_filenames(which_elem,outpath,plstype,maxnc,fullnorm,fullmin,fullmax,lownorm,lowmin,lowmax,midnorm,midmin,midmax,highnorm,highmin,highmax,xminmax,yminmax)

print 'Making outlier check plots'
outlier_plots(full_Qres_file,low_Qres_file,mid_Qres_file,high_Qres_file,full_T2_file,low_T2_file,mid_T2_file,high_T2_file,fullnorm,nc_full,lownorm,nc_low,midnorm,nc_mid,highnorm,nc_high,which_elem)
print "Making 1 to 1 plots using CV results"
cv_plots(full_cv_file,nc_full,fullnorm,low_cv_file,nc_low,lownorm,mid_cv_file,nc_mid,midnorm,high_cv_file,nc_high,highnorm,xminmax,yminmax,which_elem)

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


truecomps=[comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex]]

final_model_results(y_db_full,y_db_low,y_db_mid,y_db_high,ranges,inrange,refpredict,toblend,truecomps,xminmax,yminmax,fullmin,fullmax,fullnorm,nc_full,lowmin,lowmax,lownorm,nc_low,midmin,midmax,midnorm,nc_mid,highmin,highmax,highnorm,nc_high,which_elem)



#get apxs CCS results
blend_predict(apxs_data,apxs_wvl,apxs_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_apxs,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get validation CCS results
blend_predict(val_data,val_wvl,val_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_val,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get cal target CCS results
blend_predict(cal_data,cal_wvl,cal_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_cal,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get CCS results (this step takes a while because it needs to read all the CCS files)
blend_predict(all_data,all_wvl,all_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)



##############################  CaO #####################################

searchdir=r'F:\ChemCam\ops_ccam_team\CalTarget 95A'
searchdir_cal=r'F:\ChemCam\ops_ccam_team\CalTarget 95A'
searchdir_apxs=r'F:\ChemCam\ops_ccam_team\Best APXS Comparisons'
searchdir_val=r'F:\ChemCam\ops_ccam_team\Validation Targets'
maskfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\mask_minors_noise.csv'
outpath=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Recreating May Results\ccam_20150515\Output\CaO'
masterlist=r'F:\ChemCam\ops_ccam_misc\MASTERLIST_combined_20150811.csv'
name_subs=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv'
dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected.csv'
keepfile=None
removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'

which_elem='CaO'
#outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Only_Caltargets_Removed\\'#
outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Final\\'

plstype='sklearn'
mincomp=0
maxcomp=100

#set plot range
xminmax=[0,60]
yminmax=[-5,60]

maxnc=30
fullmin=0
fullmax=42
lowmin=0
lowmax=7
midmin=0
midmax=15
highmin=30
highmax=100

fullnorm=3
lownorm=3
midnorm=3
highnorm=1

#specify the number of components to use for each submodel
nc_full=8
nc_low=13
nc_mid=11
nc_high=7
means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,full_cv_file,low_cv_file,mid_cv_file,high_cv_file,outfile1to1,outfile1to1_full,outfile1to1_low,outfile1to1_mid,outfile1to1_high,imgfile,imgfile_blended,imgfile_full,imgfile_low,imgfile_mid,imgfile_high,full_Qres_file,low_Qres_file,mid_Qres_file,high_Qres_file,full_T2_file,low_T2_file,mid_T2_file,high_T2_file,outfile_Q_T2,outfile_Q_T2_low,outfile_Q_T2_mid,outfile_Q_T2_high,outputfile,outputfile_apxs,outputfile_val,outputfile_cal,db_outputfile=generate_filenames(which_elem,outpath,plstype,maxnc,fullnorm,fullmin,fullmax,lownorm,lowmin,lowmax,midnorm,midmin,midmax,highnorm,highmin,highmax,xminmax,yminmax)


print 'Making outlier check plots'
outlier_plots(full_Qres_file,low_Qres_file,mid_Qres_file,high_Qres_file,full_T2_file,low_T2_file,mid_T2_file,high_T2_file,fullnorm,nc_full,lownorm,nc_low,midnorm,nc_mid,highnorm,nc_high,which_elem)
print "Making 1 to 1 plots using CV results"
cv_plots(full_cv_file,nc_full,fullnorm,low_cv_file,nc_low,lownorm,mid_cv_file,nc_mid,midnorm,high_cv_file,nc_high,highnorm,xminmax,yminmax,which_elem)


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
If full model <2, use the low model
if full 2 to 4, blend the low and mid model using full as reference
if full 4 to 12, use the mid model
if full model 12 to 15, blend mid and full using full as reference
if full model >15 use the full model
otherwise use full

Do not overwrite predictions that have already been set in a previous round of logic.
"""

predicts=[y_db_full,y_db_low,y_db_mid,y_db_high]
ranges=[[-10,2],[2,4],[4,15],[15,25],[25,100],[0,100]]
inrange=[0,0,0,0,0,0]
refpredict=[0,0,0,0,0,0]
toblend=[[1,1],[1,2],[2,2],[2,0],[3,0],[0,0]]

truecomps=[comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex]]
final_model_results(y_db_full,y_db_low,y_db_mid,y_db_high,ranges,inrange,refpredict,toblend,truecomps,xminmax,yminmax,fullmin,fullmax,fullnorm,nc_full,lowmin,lowmax,lownorm,nc_low,midmin,midmax,midnorm,nc_mid,highmin,highmax,highnorm,nc_high,which_elem)

#make 1 to 1 plots using CV results

full_cv_predict,full_cv_samples,full_cv_truecomps,full_cv_folds,full_cv_spect=ccam.plots.readpredicts(full_cv_file,nc_full)
low_cv_predict,low_cv_samples,low_cv_truecomps,low_cv_folds,low_cv_spect=ccam.plots.readpredicts(low_cv_file,nc_low)
high_cv_predict,high_cv_samples,high_cv_truecomps,high_cv_folds,high_cv_spect=ccam.plots.readpredicts(high_cv_file,nc_high)
mid_cv_predict,mid_cv_samples,mid_cv_truecomps,mid_cv_folds,mid_cv_spect=ccam.plots.readpredicts(mid_cv_file,nc_mid)


      
RMSECV_full=numpy.sqrt(numpy.mean((full_cv_predict-full_cv_truecomps)**2))
RMSECV_low=numpy.sqrt(numpy.mean((low_cv_predict-low_cv_truecomps)**2))
RMSECV_mid=numpy.sqrt(numpy.mean((mid_cv_predict-mid_cv_truecomps)**2))
RMSECV_high=numpy.sqrt(numpy.mean((high_cv_predict-high_cv_truecomps)**2))

#mid_should_low=sum(numpy.all(numpy.vstack([(full_cv_predict>2.5),(full_cv_predict<11),(full_cv_truecomps<2.5)]),axis=0))
#low_should_mid=sum(numpy.all(numpy.vstack([(full_cv_predict<2.5),(full_cv_truecomps>2.5),(full_cv_truecomps<11)]),axis=0))
#mid_should_high=sum(numpy.all(numpy.vstack([(full_cv_predict>2.5),(full_cv_predict<11),(full_cv_truecomps>11)]),axis=0))
#high_should_mid=sum(numpy.all(numpy.vstack([(full_cv_predict>11),(full_cv_truecomps<11),(full_cv_truecomps>2.5)]),axis=0))


#RMSECV_combined=numpy.sqrt(numpy.mean((combined_cv_predict[(combined_cv_predict!=9999)]-full_cv_truecomps[(combined_cv_predict!=9999)])**2))

truecomps=[full_cv_truecomps,low_cv_truecomps,mid_cv_truecomps,high_cv_truecomps]
predicts=[full_cv_predict,low_cv_predict,mid_cv_predict,high_cv_predict]
labels=['Full (nc='+str(nc_full)+', norm='+str(fullnorm)+', RMSECV='+str(RMSECV_full)+')','Low (nc='+str(nc_low)+',norm='+str(lownorm)+', RMSECV='+str(RMSECV_low)+')','Mid (nc='+str(nc_mid)+',norm='+str(midnorm)+', RMSECV='+str(RMSECV_mid)+')','High (nc='+str(nc_high)+',norm='+str(highnorm)+', RMSECV='+str(RMSECV_high)+')']
colors=['c','r','g','b']
markers=['o','<','>','^']
plot_title=which_elem+' Cross Validation'
ccam.Plot1to1(truecomps,predicts,plot_title,labels,colors,markers,outfile1to1,xminmax=xminmax,yminmax=yminmax)
ccam.Plot1to1(truecomps[0],predicts[0],plot_title,labels[0],colors[0],markers[0],outfile1to1_full,xminmax=xminmax,yminmax=yminmax)
ccam.Plot1to1(truecomps[1],predicts[1],plot_title,labels[1],colors[1],markers[1],outfile1to1_low,xminmax=xminmax,yminmax=yminmax)
ccam.Plot1to1(truecomps[2],predicts[2],plot_title,labels[2],colors[2],markers[2],outfile1to1_mid,xminmax=xminmax,yminmax=yminmax)
ccam.Plot1to1(truecomps[3],predicts[3],plot_title,labels[3],colors[3],markers[3],outfile1to1_high,xminmax=xminmax,yminmax=yminmax)

#get apxs CCS results
blend_predict(apxs_data,apxs_wvl,apxs_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_apxs,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get validation CCS results
blend_predict(val_data,val_wvl,val_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_val,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get cal target CCS results
blend_predict(cal_data,cal_wvl,cal_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_cal,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get CCS results (this step takes a while because it needs to read all the CCS files)
blend_predict(all_data,all_wvl,all_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)


  
##############################  Na2O #####################################

searchdir=r'F:\ChemCam\ops_ccam_team\CalTarget 95A'
searchdir_cal=r'F:\ChemCam\ops_ccam_team\CalTarget 95A'
searchdir_apxs=r'F:\ChemCam\ops_ccam_team\Best APXS Comparisons'
searchdir_val=r'F:\ChemCam\ops_ccam_team\Validation Targets'
maskfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\mask_minors_noise.csv'
outpath=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Recreating May Results\ccam_20150515\Output\Na2O'
masterlist=r'F:\ChemCam\ops_ccam_misc\MASTERLIST_combined_20150811.csv'
name_subs=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv'
dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected.csv'
keepfile=None
removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'


which_elem='Na2O'
#outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Only_Caltargets_Removed\\'#
outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Final\\'

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
lowmax=100
midmin=0
midmax=100
highmin=0
highmax=100

fullnorm=1
lownorm=1
midnorm=1
highnorm=1

#specify the number of components to use for each submodel
nc_full=7
nc_low=7
nc_mid=7
nc_high=7
means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,full_cv_file,low_cv_file,mid_cv_file,high_cv_file,outfile1to1,outfile1to1_full,outfile1to1_low,outfile1to1_mid,outfile1to1_high,imgfile,imgfile_blended,imgfile_full,imgfile_low,imgfile_mid,imgfile_high,full_Qres_file,low_Qres_file,mid_Qres_file,high_Qres_file,full_T2_file,low_T2_file,mid_T2_file,high_T2_file,outfile_Q_T2,outfile_Q_T2_low,outfile_Q_T2_mid,outfile_Q_T2_high,outputfile,outputfile_apxs,outputfile_val,outputfile_cal,db_outputfile=generate_filenames(which_elem,outpath,plstype,maxnc,fullnorm,fullmin,fullmax,lownorm,lowmin,lowmax,midnorm,midmin,midmax,highnorm,highmin,highmax,xminmax,yminmax)

print 'Making outlier check plots'
outlier_plots(full_Qres_file,low_Qres_file,mid_Qres_file,high_Qres_file,full_T2_file,low_T2_file,mid_T2_file,high_T2_file,fullnorm,nc_full,lownorm,nc_low,midnorm,nc_mid,highnorm,nc_high,which_elem)
print "Making 1 to 1 plots using CV results"
cv_plots(full_cv_file,nc_full,fullnorm,low_cv_file,nc_low,lownorm,mid_cv_file,nc_mid,midnorm,high_cv_file,nc_high,highnorm,xminmax,yminmax,which_elem)



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
Just use the full model!
Do not overwrite predictions that have already been set in a previous round of logic.
"""

predicts=[y_db_full,y_db_low,y_db_mid,y_db_high]
ranges=[[0,100]]
inrange=[0]
refpredict=[0]
toblend=[[0,0]]


truecomps=[comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex]]
final_model_results(y_db_full,y_db_low,y_db_mid,y_db_high,ranges,inrange,refpredict,toblend,truecomps,xminmax,yminmax,fullmin,fullmax,fullnorm,nc_full,lowmin,lowmax,lownorm,nc_low,midmin,midmax,midnorm,nc_mid,highmin,highmax,highnorm,nc_high,which_elem)



#get apxs CCS results
blend_predict(apxs_data,apxs_wvl,apxs_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_apxs,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get validation CCS results
blend_predict(val_data,val_wvl,val_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_val,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get cal target CCS results
blend_predict(cal_data,cal_wvl,cal_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_cal,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get CCS results (this step takes a while because it needs to read all the CCS files)
blend_predict(all_data,all_wvl,all_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)


##############################  K2O #####################################

searchdir=r'F:\ChemCam\ops_ccam_team\CalTarget 95A'
searchdir_cal=r'F:\ChemCam\ops_ccam_team\CalTarget 95A'
searchdir_apxs=r'F:\ChemCam\ops_ccam_team\Best APXS Comparisons'
searchdir_val=r'F:\ChemCam\ops_ccam_team\Validation Targets'
maskfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\mask_minors_noise.csv'
outpath=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Recreating May Results\ccam_20150515\Output\K2O'
masterlist=r'F:\ChemCam\ops_ccam_misc\MASTERLIST_combined_20150811.csv'
name_subs=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv'
dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected.csv'
keepfile=None
removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv'


which_elem='K2O'
#outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Only_Caltargets_Removed\\'#
outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\'+which_elem+'\\Outlier_Example\\Final\\'

plstype='sklearn'
mincomp=0
maxcomp=100

#set plot range
xminmax=[0,20]
yminmax=xminmax

maxnc=20
fullmin=0
fullmax=100
lowmin=0
lowmax=2
midmin=0
midmax=2
highmin=1.5
highmax=100

fullnorm=3
lownorm=3
midnorm=3
highnorm=1

#specify the number of components to use for each submodel
nc_full=4
nc_low=6
nc_mid=6
nc_high=9
means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,full_cv_file,low_cv_file,mid_cv_file,high_cv_file,outfile1to1,outfile1to1_full,outfile1to1_low,outfile1to1_mid,outfile1to1_high,imgfile,imgfile_blended,imgfile_full,imgfile_low,imgfile_mid,imgfile_high,full_Qres_file,low_Qres_file,mid_Qres_file,high_Qres_file,full_T2_file,low_T2_file,mid_T2_file,high_T2_file,outfile_Q_T2,outfile_Q_T2_low,outfile_Q_T2_mid,outfile_Q_T2_high,outputfile,outputfile_apxs,outputfile_val,outputfile_cal,db_outputfile=generate_filenames(which_elem,outpath,plstype,maxnc,fullnorm,fullmin,fullmax,lownorm,lowmin,lowmax,midnorm,midmin,midmax,highnorm,highmin,highmax,xminmax,yminmax)

print 'Making outlier check plots'
outlier_plots(full_Qres_file,low_Qres_file,mid_Qres_file,high_Qres_file,full_T2_file,low_T2_file,mid_T2_file,high_T2_file,fullnorm,nc_full,lownorm,nc_low,midnorm,nc_mid,highnorm,nc_high,which_elem)
print "Making 1 to 1 plots using CV results"
cv_plots(full_cv_file,nc_full,fullnorm,low_cv_file,nc_low,lownorm,mid_cv_file,nc_mid,midnorm,high_cv_file,nc_high,highnorm,xminmax,yminmax,which_elem)


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




predicts=[y_db_full,y_db_low,y_db_mid,y_db_high]
ranges=[[-10,1],[1,2],[2,4],[4,100]]
inrange=[0,0,0,0]
refpredict=[0,0,0,0]
toblend=[[1,1],[1,0],[0,3],[3,3]]


truecomps=[comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex]]
final_model_results(y_db_full,y_db_low,y_db_mid,y_db_high,ranges,inrange,refpredict,toblend,truecomps,xminmax,yminmax,fullmin,fullmax,fullnorm,nc_full,lowmin,lowmax,lownorm,nc_low,midmin,midmax,midnorm,nc_mid,highmin,highmax,highnorm,nc_high,which_elem)

#get apxs CCS results
blend_predict(apxs_data,apxs_wvl,apxs_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_apxs,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get validation CCS results
blend_predict(val_data,val_wvl,val_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_val,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get cal target CCS results
blend_predict(cal_data,cal_wvl,cal_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile_cal,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)

#get CCS results (this step takes a while because it needs to read all the CCS files)
blend_predict(all_data,all_wvl,all_filelist,ranges,inrange,refpredict,toblend,masterlist,name_subs,fullmin,fullmax,lowmin,lowmax,midmin,midmax,highmin,highmax,outputfile,means_file_full,means_file_low,means_file_mid,means_file_high,loadfile_full,loadfile_low,loadfile_mid,loadfile_high,nc_full,nc_low,nc_mid,nc_high,maskfile)
