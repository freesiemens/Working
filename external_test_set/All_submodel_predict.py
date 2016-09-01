# -*- codinF: utf-8 -*-
"""
Created on Fri Apr 24 16:08:53 2015

@author: rbanderson
"""
import ccam
import numpy
import csv
import sys
import scipy.stats as stats
import scipy.optimize as opt
import operator
import os
import pandas

def generate_filenames(which_elem,outpath,plstype,maxnc,norms,ranges,xminmax,yminmax):#which_elem,outpath,plstype,maxnc,fullnorm,fullmin,fullmax,lownorm,lowmin,lowmax,midnorm,midmin,midmax,highnorm,highmin,highmax,xminmax,yminmax):
    prefix={'full':outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(norms['full'])+'_'+str(ranges['full'][0])+'-'+str(ranges['full'][1]),
            'low':outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(norms['low'])+'_'+str(ranges['low'][0])+'-'+str(ranges['low'][1]),
            'mid':outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(norms['mid'])+'_'+str(ranges['mid'][0])+'-'+str(ranges['mid'][1]),
            'high':outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(norms['high'])+'_'+str(ranges['high'][0])+'-'+str(ranges['high'][1])}    
    print(prefix)
    
    #specify the files that hold the mean centering info
    means_file_full=prefix['full']+'_meancenters.csv'
    means_file_low=prefix['low']+'_meancenters.csv'
    means_file_mid=prefix['mid']+'_meancenters.csv'
    means_file_high=prefix['high']+'_meancenters.csv'
    means_file={'full':means_file_full,'low':means_file_low,'mid':means_file_mid,'high':means_file_high}
    
    #specify the files that store the regression models (these are the python equivalent of IDL .SAV files)
    loadfile_full=outpath+'\\'+which_elem+'_'+plstype+'_norm'+str(norms['full'])+'_'+str(ranges['full'][0])+'-'+str(ranges['full'][1])+'.pkl'
    loadfile_low=outpath+'\\'+which_elem+'_'+plstype+'_norm'+str(norms['low'])+'_'+str(ranges['low'][0])+'-'+str(ranges['low'][1])+'.pkl'
    loadfile_mid=outpath+'\\'+which_elem+'_'+plstype+'_norm'+str(norms['mid'])+'_'+str(ranges['mid'][0])+'-'+str(ranges['mid'][1])+'.pkl'
    loadfile_high=outpath+'\\'+which_elem+'_'+plstype+'_norm'+str(norms['high'])+'_'+str(ranges['high'][0])+'-'+str(ranges['high'][1])+'.pkl'
    loadfile={'full':loadfile_full,'low':loadfile_low,'mid':loadfile_mid,'high':loadfile_high}
    
    #specify files containing cross validation results
    full_cv_file=prefix['full']+'_cv_predict.csv'
    low_cv_file=prefix['low']+'_cv_predict.csv'
    mid_cv_file=prefix['mid']+'_cv_predict.csv'
    high_cv_file=prefix['high']+'_cv_predict.csv'
    cv_file={'full':full_cv_file,'low':low_cv_file,'mid':mid_cv_file,'high':high_cv_file}    

    #specify files containing outlier evaluation results
    full_Qres_file=prefix['full']+'_Q_res.csv'
    low_Qres_file=prefix['low']+'_Q_res.csv'
    mid_Qres_file=prefix['mid']+'_Q_res.csv'
    high_Qres_file=prefix['high']+'_Q_res.csv'
    Qres_file={'full':full_Qres_file,'low':low_Qres_file,'mid':mid_Qres_file,'high':high_Qres_file}    
    
    full_T2_file=prefix['full']+'_HotellingT2.csv'
    low_T2_file=prefix['low']+'_HotellingT2.csv'
    mid_T2_file=prefix['mid']+'_HotellingT2.csv'
    high_T2_file=prefix['high']+'_HotellingT2.csv'
    T2_file={'full':full_T2_file,'low':low_T2_file,'mid':mid_T2_file,'high':high_T2_file}    
    
    #specify file names for Q vs T2 plots
    outfile_Q_T2=prefix['full']+'_QvsT2_full.png'
    outfile_Q_T2_low=prefix['low']+'_QvsT2_low.png'
    outfile_Q_T2_mid=prefix['mid']+'_QvsT2_mid.png'
    outfile_Q_T2_high=prefix['high']+'_QvsT2_high.png'
    Q_T2_out={'full':outfile_Q_T2,'low':outfile_Q_T2_low,'mid':outfile_Q_T2_mid,'high':outfile_Q_T2_high}
    #specify where to save csv files with predictions
    outputfile=outpath+'\\'+which_elem+'_all_predictions_low_('+str(ranges['low'][0])+'-'+str(ranges['low'][1])+')_mid_('+str(ranges['mid'][0])+'-'+str(ranges['mid'][1])+')_high_('+str(ranges['high'][0])+'-'+str(ranges['high'][1])+').csv'
    outputfile_apxs=outpath+'\\'+which_elem+'_apxs_predictions_low_('+str(ranges['low'][0])+'-'+str(ranges['low'][1])+')_mid_('+str(ranges['mid'][0])+'-'+str(ranges['mid'][1])+')_high_('+str(ranges['high'][0])+'-'+str(ranges['high'][1])+').csv'
    outputfile_cal=outpath+'\\'+which_elem+'_cal_predictions_low_('+str(ranges['low'][0])+'-'+str(ranges['low'][1])+')_mid_('+str(ranges['mid'][0])+'-'+str(ranges['mid'][1])+')_high_('+str(ranges['high'][0])+'-'+str(ranges['high'][1])+').csv'
    db_outputfile=outpath+'\\'+which_elem+'_db_predictions_low_('+str(ranges['low'][0])+'-'+str(ranges['low'][1])+')_mid_('+str(ranges['mid'][0])+'-'+str(ranges['mid'][1])+')_high_('+str(ranges['high'][0])+'-'+str(ranges['high'][1])+').csv'
    test_outputfile=outpath+'\\'+which_elem+'_test_predictions_low_('+str(ranges['low'][0])+'-'+str(ranges['low'][1])+')_mid_('+str(ranges['mid'][0])+'-'+str(ranges['mid'][1])+')_high_('+str(ranges['high'][0])+'-'+str(ranges['high'][1])+').csv'
        
    outputfile_val=outpath+'\\'+which_elem+'_val_predictions_low_('+str(ranges['low'][0])+'-'+str(ranges['low'][1])+')_mid_('+str(ranges['mid'][0])+'-'+str(ranges['mid'][1])+')_high_('+str(ranges['high'][0])+'-'+str(ranges['high'][1])+').csv'
    pred_csv_out={'all':outputfile,'apxs':outputfile_apxs,'cal':outputfile_cal,'db':db_outputfile,'val':outputfile_val,'test':test_outputfile}
  
  
    
    #specify file names for  CV 1 to 1 plots
    outfile1to1=outpath+'\\'+which_elem+'_submodels_1to1_plot_'+str(xminmax[0])+'_'+str(xminmax[1])+'.png'
    outfile1to1_full=outpath+'\\'+which_elem+'_submodels_1to1_plot_'+str(xminmax[0])+'_'+str(xminmax[1])+'_full ('+str(ranges['full'][0])+'-'+str(ranges['full'][1])+').png'
    outfile1to1_low=outpath+'\\'+which_elem+'_submodels_1to1_plot_'+str(xminmax[0])+'_'+str(xminmax[1])+'_low ('+str(ranges['low'][0])+'-'+str(ranges['low'][1])+').png'
    outfile1to1_mid=outpath+'\\'+which_elem+'_submodels_1to1_plot_'+str(xminmax[0])+'_'+str(xminmax[1])+'_mid ('+str(ranges['mid'][0])+'-'+str(ranges['mid'][1])+').png'
    outfile1to1_high=outpath+'\\'+which_elem+'_submodels_1to1_plot_'+str(xminmax[0])+'_'+str(xminmax[1])+'_high ('+str(ranges['high'][0])+'-'+str(ranges['high'][1])+').png'
    outfiles1to1={'all':outfile1to1,'full':outfile1to1_full,'low':outfile1to1_low,'mid':outfile1to1_mid,'high':outfile1to1_high}
    #specify file names for full database 1 to 1 plots
    imgfile=outpath+'\\'+which_elem+'_final_model_predictions_1to1_'+str(xminmax[0])+'-'+str(xminmax[1])+'.png'
    imgfile_blended=outpath+'\\'+which_elem+'_final_model_predictions_1to1_'+str(xminmax[0])+'-'+str(xminmax[1])+'_blended.png'
    imgfile_full=outpath+'\\'+which_elem+'_final_model_predictions_1to1_'+str(xminmax[0])+'-'+str(xminmax[1])+'_full ('+str(ranges['full'][0])+'-'+str(ranges['full'][1])+').png'
    imgfile_low=outpath+'\\'+which_elem+'_final_model_predictions_1to1_'+str(xminmax[0])+'-'+str(xminmax[1])+'_low ('+str(ranges['low'][0])+'-'+str(ranges['low'][1])+').png'
    imgfile_mid=outpath+'\\'+which_elem+'_final_model_predictions_1to1_'+str(xminmax[0])+'-'+str(xminmax[1])+'_mid ('+str(ranges['mid'][0])+'-'+str(ranges['mid'][1])+').png'
    imgfile_high=outpath+'\\'+which_elem+'_final_model_predictions_1to1_'+str(xminmax[0])+'-'+str(xminmax[1])+'_high ('+str(ranges['high'][0])+'-'+str(ranges['high'][1])+').png'
    imgfiles={'all':imgfile,'blended':imgfile_blended,'full':imgfile_full,'low':imgfile_low,'mid':imgfile_mid,'high':imgfile_high}
    
    imgfile_test=outpath+'\\'+which_elem+'_final_model_predictions_1to1_'+str(xminmax[0])+'-'+str(xminmax[1])+'_test.png'
    imgfile_blended_test=outpath+'\\'+which_elem+'_final_model_predictions_1to1_'+str(xminmax[0])+'-'+str(xminmax[1])+'_blended_test.png'
    imgfile_full_test=outpath+'\\'+which_elem+'_final_model_predictions_1to1_'+str(xminmax[0])+'-'+str(xminmax[1])+'_full ('+str(ranges['full'][0])+'-'+str(ranges['full'][1])+')_test.png'
    imgfile_low_test=outpath+'\\'+which_elem+'_final_model_predictions_1to1_'+str(xminmax[0])+'-'+str(xminmax[1])+'_low ('+str(ranges['low'][0])+'-'+str(ranges['low'][1])+')_test.png'
    imgfile_mid_test=outpath+'\\'+which_elem+'_final_model_predictions_1to1_'+str(xminmax[0])+'-'+str(xminmax[1])+'_mid ('+str(ranges['mid'][0])+'-'+str(ranges['mid'][1])+')_test.png'
    imgfile_high_test=outpath+'\\'+which_elem+'_final_model_predictions_1to1_'+str(xminmax[0])+'-'+str(xminmax[1])+'_high ('+str(ranges['high'][0])+'-'+str(ranges['high'][1])+')_test.png'
    imgfile_blended_full_test=outpath+'\\'+which_elem+'_final_model_predictions_1to1_blended_full_test.png'

    #specify file to store the blending optimization results
    blend_outfile=outpath+'\\'+which_elem+'blend_opt.csv'
    imgfiles_test={'all':imgfile_test,'blended':imgfile_blended_test,'full':imgfile_full_test,'low':imgfile_low_test,'mid':imgfile_mid_test,'high':imgfile_high_test,'blended_full':imgfile_blended_full_test}
  
    filename={'means_file':means_file,'loadfile':loadfile,'cv_file':cv_file,'Qres_file':Qres_file,'T2_file':T2_file,'Q_T2_out':Q_T2_out,'pred_csv_out':pred_csv_out,'cv_file':cv_file,'outfiles1to1':outfiles1to1,'imgfiles':imgfiles,'imgfiles_test':imgfiles_test,'blend_outfile':blend_outfile}
    return filename
    
    
    
def blend_predict(data,wvl,filelist,blendranges,inrange,refpredict,toblend,masterlist,name_subs,ranges,ncs,maskfile,filenames,outputstr):
    
    
    y_full,fullnorm=ccam.pls_predict(data,ncs['full'],wvl,maskfile,loadfile=filenames['loadfile']['full'],mean_file=filenames['means_file']['full'])
    y_low,lownorm=ccam.pls_predict(data,ncs['low'],wvl,maskfile,loadfile=filenames['loadfile']['low'],mean_file=filenames['means_file']['low'])
    y_mid,midnorm=ccam.pls_predict(data,ncs['mid'],wvl,maskfile,loadfile=filenames['loadfile']['mid'],mean_file=filenames['means_file']['mid'])
    y_high,highnorm=ccam.pls_predict(data,ncs['high'],wvl,maskfile,loadfile=filenames['loadfile']['high'],mean_file=filenames['means_file']['high'])
    
    predicts=[y_full,y_low,y_mid,y_high]
    
    blended=ccam.submodels_blend(predicts,blendranges,inrange,refpredict,toblend,overwrite=False,noneg=False)
    
    targetlist,targetdists,targetamps,nshots=ccam.target_lookup(filelist,masterlist,name_subs)
    
    y_combined=numpy.zeros_like(y_high)
    print('Writing results to'+filenames['pred_csv_out'][outputstr])
    with open(filenames['pred_csv_out'][outputstr],'w',newline='') as writefile:
            writer=csv.writer(writefile,delimiter=',')
            row=['','','','','Full ('+str(ranges['full'][0])+'-'+str(ranges['full'][1])+')','Low ('+str(ranges['low'][0])+'-'+str(ranges['low'][1])+')','Mid ('+str(ranges['mid'][0])+'-'+str(ranges['mid'][1])+')','High ('+str(ranges['high'][0])+'-'+str(ranges['high'][1])+')','Blended']
            writer.writerow(row)
            row=['','','','Norm=',fullnorm,lownorm,midnorm,highnorm]
            writer.writerow(row)
            row=['','','','nc=',str(ncs['full']),str(ncs['low']),str(ncs['mid']),str(ncs['high'])]
            writer.writerow(row)
            row=['File','Target','Distance','Power',which_elem,which_elem,which_elem,which_elem,which_elem]
            writer.writerow(row)
            
            for i in range(0,len(y_combined)):
                row=[filelist[i],targetlist[i],targetdists[i],targetamps[i],y_full[i],y_low[i],y_mid[i],y_high[i],blended[i]]
                writer.writerow(row)        

def outlier_plots(filenames,norms,ncs,which_elem):
 
    Q_res_full,Q_labels_full=ccam.read_csv(filenames['Qres_file']['full'],0,labelrow=True)
    Q_res_low,Q_labels_low=ccam.read_csv(filenames['Qres_file']['low'],0,labelrow=True)
    Q_res_mid,Q_labels_mid=ccam.read_csv(filenames['Qres_file']['mid'],0,labelrow=True)
    Q_res_high,Q_labels_high=ccam.read_csv(filenames['Qres_file']['high'],0,labelrow=True)
    Q_res_full=numpy.array(Q_res_full[:,4:],dtype='float')
    Q_res_low=numpy.array(Q_res_low[:,4:],dtype='float')
    Q_res_mid=numpy.array(Q_res_mid[:,4:],dtype='float')
    Q_res_high=numpy.array(Q_res_high[:,4:],dtype='float')
    
    T2_res_full,T2_labels_full=ccam.read_csv(filenames['T2_file']['full'],0,labelrow=True)
    T2_res_low,T2_labels_low=ccam.read_csv(filenames['T2_file']['low'],0,labelrow=True)
    T2_res_mid,T2_labels_mid=ccam.read_csv(filenames['T2_file']['mid'],0,labelrow=True)
    T2_res_high,T2_labels_high=ccam.read_csv(filenames['T2_file']['high'],0,labelrow=True)
    T2_res_full=numpy.array(T2_res_full[:,4:],dtype='float')
    T2_res_low=numpy.array(T2_res_low[:,4:],dtype='float')
    T2_res_mid=numpy.array(T2_res_mid[:,4:],dtype='float')
    T2_res_high=numpy.array(T2_res_high[:,4:],dtype='float')
    
    colors=['r']
    markers=['o']
    labels=['Full Norm='+str(norms['full'])+' NC='+str(ncs['full']),
            'Low Norm='+str(norms['low'])+' NC='+str(ncs['low']),
            'Mid Norm='+str(norms['mid'])+' NC='+str(ncs['mid']),
            'High Norm='+str(norms['high'])+' NC='+str(ncs['high']),
            'Blended']
    
    
    plot_title=['Outlier check for '+which_elem]
    ccam.plots.Plot1to1(T2_res_full[ncs['full']-1],Q_res_full[ncs['full']-1],plot_title,labels[0],colors[0],markers[0],filenames['Q_T2_out']['full'],xminmax=[0,1.1*numpy.max(T2_res_full[ncs['full']-1])],yminmax=[0,1.1*numpy.max(Q_res_full[ncs['full']-1])],ylabel='Q Residual',xlabel='Hotelling T2',one_to_one=False)
    ccam.plots.Plot1to1(T2_res_low[ncs['low']-1],Q_res_low[-1],plot_title,labels[1],colors[0],markers[0],filenames['Q_T2_out']['low'],xminmax=[0,1.1*numpy.max(T2_res_low[ncs['low']-1])],yminmax=[0,1.1*numpy.max(Q_res_low[ncs['low']-1])],ylabel='Q Residual',xlabel='Hotelling T2',one_to_one=False)
    ccam.plots.Plot1to1(T2_res_mid[ncs['mid']-1],Q_res_mid[ncs['mid']-1],plot_title,labels[2],colors[0],markers[0],filenames['Q_T2_out']['mid'],xminmax=[0,1.1*numpy.max(T2_res_mid[ncs['mid']-1])],yminmax=[0,1.1*numpy.max(Q_res_mid[ncs['mid']-1])],ylabel='Q Residual',xlabel='Hotelling T2',one_to_one=False)
    ccam.plots.Plot1to1(T2_res_high[ncs['high']-1],Q_res_high[ncs['high']-1],plot_title,labels[3],colors[0],markers[0],filenames['Q_T2_out']['high'],xminmax=[0,1.1*numpy.max(T2_res_high[ncs['high']-1])],yminmax=[0,1.1*numpy.max(Q_res_high[ncs['high']-1])],ylabel='Q Residual',xlabel='Hotelling T2',one_to_one=False)
    
def cv_plots(filenames,ncs,norms,xminmax,yminmax,which_elem):      
    #make 1 to 1 plots using CV results
    
    full_cv_predict,full_cv_samples,full_cv_truecomps,full_cv_folds,full_cv_spect=ccam.plots.readpredicts(filenames['cv_file']['full'],ncs['full'])
    low_cv_predict,low_cv_samples,low_cv_truecomps,low_cv_folds,low_cv_spect=ccam.plots.readpredicts(filenames['cv_file']['low'],ncs['low'])
    high_cv_predict,high_cv_samples,high_cv_truecomps,high_cv_folds,high_cv_spect=ccam.plots.readpredicts(filenames['cv_file']['high'],ncs['high'])
    mid_cv_predict,mid_cv_samples,mid_cv_truecomps,mid_cv_folds,mid_cv_spect=ccam.plots.readpredicts(filenames['cv_file']['mid'],ncs['mid'])
    
    
          
    RMSECV_full=round(numpy.sqrt(numpy.mean((full_cv_predict-full_cv_truecomps)**2)),2)
    RMSECV_low=round(numpy.sqrt(numpy.mean((low_cv_predict-low_cv_truecomps)**2)),2)
    RMSECV_mid=round(numpy.sqrt(numpy.mean((mid_cv_predict-mid_cv_truecomps)**2)),2)
    RMSECV_high=round(numpy.sqrt(numpy.mean((high_cv_predict-high_cv_truecomps)**2)),2)
    
    
    truecomps=[full_cv_truecomps,low_cv_truecomps,mid_cv_truecomps,high_cv_truecomps]
    predicts=[full_cv_predict,low_cv_predict,mid_cv_predict,high_cv_predict]
#    labels=['Full (nc='+str(ncs['full'])+', norm='+str(norms['full'])+', RMSECV='+str(RMSECV_full)+')','Low (nc='+str(ncs['low'])+',norm='+str(norms['low'])+', RMSECV='+str(RMSECV_low)+')','Mid (nc='+str(ncs['mid'])+',norm='+str(norms['mid'])+', RMSECV='+str(RMSECV_mid)+')','High (nc='+str(ncs['high'])+',norm='+str(norms['high'])+', RMSECV='+str(RMSECV_high)+')']
    labels=['Full (RMSECV='+str(RMSECV_full)+')','Low (RMSECV='+str(RMSECV_low)+')','Mid (RMSECV='+str(RMSECV_mid)+')','High (RMSECV='+str(RMSECV_high)+')']
    
    colors=['c','r','g','b']
    markers=['o','<','v','^']
    plot_title=which_elem+' Cross Validation'
    ccam.Plot1to1(truecomps,predicts,plot_title,labels,colors,markers,filenames['outfiles1to1']['all'],xminmax=xminmax,yminmax=yminmax)
    ccam.Plot1to1([truecomps[0]],[predicts[0]],plot_title,labels[0],colors[0],markers[0],filenames['outfiles1to1']['full'],xminmax=xminmax,yminmax=yminmax)
    ccam.Plot1to1([truecomps[1]],[predicts[1]],plot_title,labels[1],colors[1],markers[1],filenames['outfiles1to1']['low'],xminmax=xminmax,yminmax=yminmax)
    ccam.Plot1to1([truecomps[2]],[predicts[2]],plot_title,labels[2],colors[2],markers[2],filenames['outfiles1to1']['mid'],xminmax=xminmax,yminmax=yminmax)
    ccam.Plot1to1([truecomps[3]],[predicts[3]],plot_title,labels[3],colors[3],markers[3],filenames['outfiles1to1']['high'],xminmax=xminmax,yminmax=yminmax)

def final_model_results(y,spect_index,namelist,compos,blend_settings,xminmax,yminmax,ranges,ncs,norms,which_elem,filenames,outfilestr):
    imgnames=filenames['imgfiles']    
    predicts=[y['full'],y['low'],y['mid'],y['high']]  
    print(blend_settings)
    blended2=ccam.submodels_blend(predicts,blend_settings['blendranges'],blend_settings['inrange'],blend_settings['refpredict'],blend_settings['toblend'],overwrite=False,noneg=False)
    #Create plots of the full model results (NOTE: these plots will show artificially "optimistic" results
    # within the range where the model was trained. These are meant to be used primarily to visualize how the models will do when extrapolating,
    #NOT for evaluation of model accuracy within its training range)
    predicts=[y['full'],y['low'],y['mid'],y['high'],blended2]
    
    if which_elem=='SiO2':
        which_elem_temp=r'SiO$_2$'
    if which_elem=='TiO2':
        which_elem_temp=r'TiO$_2$'
    if which_elem=='Al2O3':
        which_elem_temp=r'Al$_2$O$_3$'
    if which_elem=='FeOT':
        which_elem_temp=r'FeO$_T$'
    if which_elem=='MgO':
        which_elem_temp=r'MgO'
    if which_elem=='CaO':
        which_elem_temp=r'CaO'
    if which_elem=='Na2O':
        which_elem_temp=r'Na$_2$O'
    if which_elem=='K2O':
        which_elem_temp=r'K$_2$O'
    plot_title='Final Model '+which_elem_temp+' Predictions of Full Database'
    labels=['Full','Low ','Mid ','High ','Blended ']
    colors=['k','c','g','b','r']
    markers=['o','<','v','^','o']
    dpi=300
    if outfilestr=='test':
        #dpi=1000
        
        plot_title=which_elem_temp
        imgnames=filenames['imgfiles_test']
        
        percentiles=[0,20,40,60,80]
        bins=numpy.percentile(compos[0],percentiles)
        #bins=numpy.max(compos[0])/20*numpy.arange(20)
        #bins=numpy.hstack(([0],numpy.logspace(-1,2,num=10)[0:-1]))        
        index_bins=numpy.digitize(compos[0],bins)
        
        index_full=numpy.where((compos[0]>0) & (compos[0]<100))
        index_low=numpy.where((compos[1]>ranges['low'][0]) & (compos[1]<ranges['low'][1]))       
        index_mid=numpy.where((compos[2]>ranges['mid'][0]) & (compos[2]<ranges['mid'][1]))
        index_high=numpy.where((compos[3]>ranges['high'][0]) & (compos[3]<ranges['high'][1]))
        index_blend=numpy.where((compos[4]>0) & (compos[4]<100))
            
        n_full=len(index_full[0])
        n_low=len(index_low[0])
        n_mid=len(index_mid[0])
        n_high=len(index_high[0])
        n_blend=len(index_blend[0])
        n_bins=[]
        
        
        RMSEP_bins=[]
        RMSEP_bins_full=[]
        S2_bins=[]
        S2_bins_full=[]
        t_bins=[]
        f_bins=[]
        p_bins=[]
        for i in range(len(bins)):
            n_bins.append(numpy.sum(index_bins==i+1))
            RMSEP_bins.append(numpy.sqrt(numpy.mean((predicts[4][index_bins==i+1]-compos[4][index_bins==i+1])**2)))
            RMSEP_bins_full.append(numpy.sqrt(numpy.mean((predicts[0][index_bins==i+1]-compos[0][index_bins==i+1])**2)))   
            if RMSEP_bins_full[i]<RMSEP_bins[i]:
                print(i)                
                print(RMSEP_bins[i])
                print(RMSEP_bins_full[i])
                print('stop')
            S2_bins.append((RMSEP_bins[i]/numpy.sqrt(2*(n_bins[i]-1)))**2)
            S2_bins_full.append((RMSEP_bins_full[i]/numpy.sqrt(2*(n_bins[i]-1)))**2)
            t_bins.append((RMSEP_bins_full[i]-RMSEP_bins[i])/numpy.sqrt(S2_bins_full[i]+S2_bins[i]))
            f_bins.append(((S2_bins_full[i]+S2_bins[i])**2)/((S2_bins_full[i]**2)/(n_bins[i]-1)+(S2_bins[i]**2)/(n_bins[i]-1)))
            p_bins.append(stats.t.sf(numpy.abs(t_bins[i]),f_bins[i])*2*100)
        

        RMSEP_full=(numpy.sqrt(numpy.mean((predicts[0][index_full]-compos[0][index_full])**2)))
        RMSEP_full_low=(numpy.sqrt(numpy.mean((predicts[0][index_low]-compos[0][index_low])**2)))
        RMSEP_full_mid=(numpy.sqrt(numpy.mean((predicts[0][index_mid]-compos[0][index_mid])**2)))
        RMSEP_full_high=(numpy.sqrt(numpy.mean((predicts[0][index_high]-compos[0][index_high])**2)))
        
        
        S2_full=(RMSEP_full/numpy.sqrt(2*(n_full-1)))**2
        S2_full_low=(RMSEP_full_low/numpy.sqrt(2*(n_low-1)))**2
        S2_full_mid=(RMSEP_full_mid/numpy.sqrt(2*(n_mid-1)))**2
        S2_full_high=(RMSEP_full_high/numpy.sqrt(2*(n_high-1)))**2
       
        RMSEP_low=(numpy.sqrt(numpy.mean((predicts[1][index_low]-compos[1][index_low])**2)))
        RMSEP_mid=(numpy.sqrt(numpy.mean((predicts[2][index_mid]-compos[2][index_mid])**2)))
        RMSEP_high=(numpy.sqrt(numpy.mean((predicts[3][index_high]-compos[3][index_high])**2)))
        
              
        RMSEP_blend=(numpy.sqrt(numpy.mean((predicts[4][index_blend]-compos[4][index_blend])**2)))
        RMSEP_blend_low=(numpy.sqrt(numpy.mean((predicts[4][index_low]-compos[4][index_low])**2)))
        RMSEP_blend_mid=(numpy.sqrt(numpy.mean((predicts[4][index_mid]-compos[4][index_mid])**2)))
        RMSEP_blend_high=(numpy.sqrt(numpy.mean((predicts[4][index_high]-compos[4][index_high])**2)))
        
        S2_blend=(RMSEP_blend/numpy.sqrt(2*(n_blend-1)))**2
        S2_blend_low=(RMSEP_blend_low/numpy.sqrt(2*(n_low-1)))**2
        S2_blend_mid=(RMSEP_blend_mid/numpy.sqrt(2*(n_mid-1)))**2
        S2_blend_high=(RMSEP_blend_high/numpy.sqrt(2*(n_high-1)))**2
        
        t_full_blend=(RMSEP_full-RMSEP_blend)/numpy.sqrt(S2_full+S2_blend)
        t_fulllow_blendlow=(RMSEP_full_low-RMSEP_blend_low)/numpy.sqrt(S2_full_low+S2_blend_low)
        t_fullmid_blendmid=(RMSEP_full_mid-RMSEP_blend_mid)/numpy.sqrt(S2_full_mid+S2_blend_mid)
        t_fullhigh_blendhigh=(RMSEP_full_high-RMSEP_blend_high)/numpy.sqrt(S2_full_high+S2_blend_high)
        
        f_full_blend=((S2_full+S2_blend)**2)/((S2_full**2)/(n_full-1)+(S2_blend**2)/(n_blend-1))
        f_fulllow_blendlow=((S2_full_low+S2_blend_low)**2)/((S2_full_low**2)/(n_low-1)+(S2_blend_low**2)/(n_low-1))
        f_fullmid_blendmid=((S2_full_mid+S2_blend_mid)**2)/((S2_full_mid**2)/(n_mid-1)+(S2_blend_mid**2)/(n_mid-1))
        f_fullhigh_blendhigh=((S2_full_high+S2_blend_high)**2)/((S2_full_high**2)/(n_high-1)+(S2_blend_high**2)/(n_high-1))        
        
        p_full_blend=stats.t.sf(numpy.abs(t_full_blend),f_full_blend)*2
        p_fulllow_blendlow=stats.t.sf(numpy.abs(t_fulllow_blendlow),f_fulllow_blendlow)*2
        p_fullmid_blendmid=stats.t.sf(numpy.abs(t_fullmid_blendmid),f_fullmid_blendmid)*2
        p_fullhigh_blendhigh=stats.t.sf(numpy.abs(t_fullhigh_blendhigh),f_fullhigh_blendhigh)*2

        labels=['PLS1 (RMSEP='+str(round(RMSEP_full,2))+')','Low (RMSEP='+str(round(RMSEP_low,2))+')','Mid (RMSEP='+str(round(RMSEP_mid,2))+')','High (RMSEP='+str(round(RMSEP_high,2))+')','Blended Submodels (RMSEP='+str(round(RMSEP_blend,2))+')']
        f=operator.itemgetter(0,4)
        yminmax[0]=numpy.min(f(predicts))
    
        ccam.plots.Plot1to1(list(f(compos)),list(f(predicts)),plot_title,list(f(labels)),list(f(colors)),list(f(markers)),imgnames['blended_full'],xminmax=xminmax,yminmax=yminmax,dpi=dpi)
        
        cwd=os.getcwd()
        with open(cwd+'\\Testset_RMSEP_summary.csv','a',newline='') as writefile:
            writer=csv.writer(writefile,delimiter=',')
            writer.writerow([which_elem])   
            row=['Ranges']
            for i in blend_settings['blendranges']:
                for j in i:
                    row.append(j)
            writer.writerow(row)
            row=['To blend:']
            for i in blend_settings['toblend']:
                for j in i:
                    row.append(j)
            writer.writerow(row)
            #row=['Ref predict:']
            #for i in blend_settings['refpredict']:
            #    row.append(i)
            #writer.writerow(row)
            #row=['In range:']
            #for i in blend_settings['inrange']:
            #    row.append(i)
            #writer.writerow(row)
            
            writer.writerow(['Composition Range','# of samples','RMSEP full','RMSEP Blended','p-value','RMSEP Sub-Model'])
            writer.writerow([str(ranges['full'][0])+'-'+str(ranges['full'][1]),str(n_full),str(RMSEP_full),str(RMSEP_blend),str(p_full_blend)])
            writer.writerow([str(ranges['low'][0])+'-'+str(ranges['low'][1]),str(n_low),str(RMSEP_full_low),str(RMSEP_blend_low),str(p_fulllow_blendlow),str(RMSEP_low)])
            writer.writerow([str(ranges['mid'][0])+'-'+str(ranges['mid'][1]),str(n_mid),str(RMSEP_full_mid),str(RMSEP_blend_mid),str(p_fullmid_blendmid),str(RMSEP_mid)])
            writer.writerow([str(ranges['high'][0])+'-'+str(ranges['high'][1]),str(n_high),str(RMSEP_full_high),str(RMSEP_blend_high),str(p_fullhigh_blendhigh),str(RMSEP_high)])
                       
            for i in range(len(p_bins)):
                try:
                    row=[str(round(bins[i],2))+'-'+str(round(bins[i+1],2))]
                except:
                    row=[str(round(bins[i],2))+'-100']
                row.append(n_bins[i])
                row.append(RMSEP_bins_full[i])
                row.append(RMSEP_bins[i])
                row.append(p_bins[i])
                print(i)
                print(row)
                writer.writerow(row)
            
           
        
        
        
    

    
    
    yminmax[0]=numpy.min(predicts)
    
    ccam.plots.Plot1to1(compos,predicts,plot_title,labels,colors,markers,imgnames['all'],xminmax=xminmax,yminmax=yminmax,dpi=dpi)
    yminmax[0]=numpy.min(predicts[4])    
    ccam.plots.Plot1to1([compos[4]],[predicts[4]],plot_title,[labels[4]],[colors[4]],[markers[4]],imgnames['blended'],xminmax=xminmax,yminmax=yminmax,dpi=dpi)
    yminmax[0]=numpy.min(predicts[0])
    ccam.plots.Plot1to1([compos[0]],[predicts[0]],plot_title,[labels[0]],[colors[0]],[markers[0]],imgnames['full'],xminmax=xminmax,yminmax=yminmax,dpi=dpi)
    yminmax[0]=numpy.min(predicts[1])
    ccam.plots.Plot1to1([compos[1]],[predicts[1]],plot_title,[labels[1]],[colors[1]],[markers[1]],imgnames['low'],xminmax=xminmax,yminmax=yminmax,dpi=dpi)
    yminmax[0]=numpy.min(predicts[2])
    ccam.plots.Plot1to1([compos[2]],[predicts[2]],plot_title,[labels[2]],[colors[2]],[markers[2]],imgnames['mid'],xminmax=xminmax,yminmax=yminmax,dpi=dpi)
    yminmax[0]=numpy.min(predicts[3])
    ccam.plots.Plot1to1([compos[3]],[predicts[3]],plot_title,[labels[3]],[colors[3]],[markers[3]],imgnames['high'],xminmax=xminmax,yminmax=yminmax,dpi=dpi)
    
    with open(filenames['pred_csv_out'][outfilestr],'w',newline='') as writefile:
            writer=csv.writer(writefile,delimiter=',')
            row=['','','','Full ('+str(ranges['full'][0])+'-'+str(ranges['full'][1])+')','Low ('+str(ranges['low'][0])+'-'+str(ranges['low'][1])+')','Mid ('+str(ranges['mid'][0])+'-'+str(ranges['mid'][1])+')','High ('+str(ranges['high'][0])+'-'+str(ranges['high'][0])+')','Blended']
            writer.writerow(row)
            row=['','','Norm=',norms['full'],norms['low'],norms['mid'],norms['high']]
            writer.writerow(row)
            row=['','','nc=',str(ncs['full']),str(ncs['low']),str(ncs['mid']),str(ncs['high'])]
            writer.writerow(row)
            row=['Target','Index','True Comp',which_elem,which_elem,which_elem,which_elem]
            writer.writerow(row)
            
            for i in range(0,len(namelist)):
                row=[namelist[i],spect_index[i],str(compos[0][i]),y['full'][i],y['low'][i],y['mid'][i],y['high'][i],blended2[i]]
                writer.writerow(row)   

def RMSE_blend(inputvals,inrange,refpredict,predicts,actual):
    ranges=sorted(inputvals[0:4])
    toblend=[inputvals[4:6].tolist(),inputvals[6:8].tolist(),inputvals[8:10].tolist(),inputvals[10:12].tolist(),inputvals[12:14].tolist()]
    try:
        toblend=numpy.array(toblend,dtype='int')
    except:
        print('something is wrong')
    toblend=toblend.tolist()
    #print toblend
    blendranges=[[-20,ranges[0]],[ranges[0],ranges[1]],[ranges[1],ranges[2]],[ranges[2],ranges[3]],[ranges[3],120]]     
    blended=ccam.submodels_blend(predicts,blendranges,inrange,refpredict,toblend,overwrite=False,noneg=False)
    RMSE=numpy.sqrt(numpy.mean((blended-actual)**2))
    print (RMSE)
    return RMSE
    
    
def blend_optimize(y,blend_settings,refcomps,outfile=None):
    predicts=[y['full'],y['low'],y['mid'],y['high']]
    refcomps=numpy.squeeze(numpy.array(refcomps)[0,:])
    
    blendranges=blend_settings['blendranges']
    inrange=blend_settings['inrange']
    refpredict=blend_settings['refpredict']
    toblend=blend_settings['toblend']
    inputvals=[]
    inputvals.extend([blendranges[0][1]])
    inputvals.extend([blendranges[1][1]])
    inputvals.extend([blendranges[2][1]])    
    inputvals.extend([blendranges[3][1]])
    

    for i in toblend:
        inputvals.extend(i)
    result=opt.minimize(RMSE_blend,inputvals,(inrange,refpredict,predicts,refcomps))
        
    opt_ranges=sorted(result.x[0:4])
    blendranges=[[-20,opt_ranges[0]],[opt_ranges[0],opt_ranges[1]],[opt_ranges[1],opt_ranges[2]],[opt_ranges[2],opt_ranges[3]],[opt_ranges[3],110]]
    print(blendranges )
    if outfile:
        with open(outfile,'w',newline='') as writefile:
            writer=csv.writer(writefile,delimiter=',')
            writer.writerow(numpy.round(blendranges,2))
               
    blend_settings={'blendranges':blendranges,'inrange':inrange,'refpredict':refpredict,'toblend':toblend}
    return blend_settings    
    

def predict_elem(which_elem,maxnc,ranges,norms,ncs,testsetfile,predict,blend_settings,searchdir='F:\\ChemCam\\ops_ccam_team\\',searchdir_cal=r'F:\ChemCam\ops_ccam_team\CalTarget 95A',
                 searchdir_apxs=r'F:\ChemCam\ops_ccam_team\Best APXS Comparisons',
                 searchdir_val=r'F:\ChemCam\ops_ccam_team\Validation Targets',
                 maskfile=r'C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\Input\mask_minors_noise.csv',
                 masterlist=r'F:\ChemCam\ops_ccam_misc\MASTERLIST_SOL_0010_0801.csv',
                 name_subs=r'C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\Input\target_name_subs.csv',
                 dbfile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected.csv',
                 removefile='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\removelist.csv',
                 plstype='sklearn',xminmax=[0,100],yminmax=[0,100],blend_opt=True,blend_outfile=None):
    outpath='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\external_test_set\\Output\\'+which_elem+'\\'
    print('############  '+which_elem+' ##############')
    filenames=generate_filenames(which_elem,outpath,plstype,maxnc,norms,ranges,xminmax,yminmax)

    print('Making outlier check plots')
    outlier_plots(filenames,norms,ncs,which_elem)
    print("Making 1 to 1 plots using CV results")
    cv_plots(filenames,ncs,norms,xminmax,yminmax,which_elem)
    
    print('Reading database')
    sys.stdout.flush()
    spectra,comps,spect_index,names,labels,wvl=ccam.read_db(dbfile,compcheck=True)
    oxides=labels[2:]
    compindex=numpy.where(oxides==which_elem)[0]

    print('Choosing spectra')

    spectra,names,spect_index,comps=ccam.choose_spectra(spectra,spect_index,names,comps,compindex,mincomp=0,maxcomp=100,keepfile=None,removefile=removefile,which_removed=None)
    y_db_full,norms['full']=ccam.pls_predict(spectra,ncs['full'],wvl,maskfile,loadfile=filenames['loadfile']['full'],mean_file=filenames['means_file']['full'])
    y_db_low,norms['low']=ccam.pls_predict(spectra,ncs['low'],wvl,maskfile,loadfile=filenames['loadfile']['low'],mean_file=filenames['means_file']['low'])
    y_db_mid,norms['mid']=ccam.pls_predict(spectra,ncs['mid'],wvl,maskfile,loadfile=filenames['loadfile']['mid'],mean_file=filenames['means_file']['mid'])
    y_db_high,norms['high']=ccam.pls_predict(spectra,ncs['high'],wvl,maskfile,loadfile=filenames['loadfile']['high'],mean_file=filenames['means_file']['high'])
    y_db={'full':y_db_full,'low':y_db_low,'mid':y_db_mid,'high':y_db_high}
    
    #Get the test set spectra
    #f=open(testsetfile,'rb')
    data=pandas.read_csv(testsetfile,header=None)
    #data=zip(*csv.reader(f))
    testnames=data.iloc[:,0]
    #testnames=numpy.array(data[0],dtype='string')
    testind=numpy.in1d(names,testnames)
    trainind=numpy.in1d(names,testnames,invert=True)
    test_spectra=spectra[testind]
    train_spectra=spectra[trainind]
    test_comps=comps[testind,compindex]
    train_comps=comps[trainind,compindex]
    test_spect_index=spect_index[testind]
    train_spect_index=spect_index[trainind]
    testnames=names[testind]
    trainnames=names[trainind]
    y_test_full,norms['full']=ccam.pls_predict(test_spectra,ncs['full'],wvl,maskfile,loadfile=filenames['loadfile']['full'],mean_file=filenames['means_file']['full'])
    y_test_low,norms['low']=ccam.pls_predict(test_spectra,ncs['low'],wvl,maskfile,loadfile=filenames['loadfile']['low'],mean_file=filenames['means_file']['low'])
    y_test_mid,norms['mid']=ccam.pls_predict(test_spectra,ncs['mid'],wvl,maskfile,loadfile=filenames['loadfile']['mid'],mean_file=filenames['means_file']['mid'])
    y_test_high,norms['high']=ccam.pls_predict(test_spectra,ncs['high'],wvl,maskfile,loadfile=filenames['loadfile']['high'],mean_file=filenames['means_file']['high'])
    y_test={'full':y_test_full,'low':y_test_low,'mid':y_test_mid,'high':y_test_high}
    
    y_train_full,norms['full']=ccam.pls_predict(train_spectra,ncs['full'],wvl,maskfile,loadfile=filenames['loadfile']['full'],mean_file=filenames['means_file']['full'])
    y_train_low,norms['low']=ccam.pls_predict(train_spectra,ncs['low'],wvl,maskfile,loadfile=filenames['loadfile']['low'],mean_file=filenames['means_file']['low'])
    y_train_mid,norms['mid']=ccam.pls_predict(train_spectra,ncs['mid'],wvl,maskfile,loadfile=filenames['loadfile']['mid'],mean_file=filenames['means_file']['mid'])
    y_train_high,norms['high']=ccam.pls_predict(train_spectra,ncs['high'],wvl,maskfile,loadfile=filenames['loadfile']['high'],mean_file=filenames['means_file']['high'])
    y_train={'full':y_train_full,'low':y_train_low,'mid':y_train_mid,'high':y_train_high}
    
    #optimize the blending settings
    
   
    truecomps=[comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex]]
    truecomps_test=[test_comps,test_comps,test_comps,test_comps,test_comps]
    truecomps_train=[train_comps,train_comps,train_comps,train_comps,train_comps]
    
    if blend_opt:
        blend_settings=blend_optimize(y_train,blend_settings,truecomps_train,outfile=filenames['blend_outfile'])    
    final_model_results(y_db,spect_index,names,truecomps,blend_settings,xminmax,yminmax,ranges,ncs,norms,which_elem,filenames,'db')
    final_model_results(y_test,test_spect_index,testnames,truecomps_test,blend_settings,xminmax,yminmax,ranges,ncs,norms,which_elem,filenames,'test')
    
    if predict:
        #Read CCS data
        #apxs_data,apxs_wvl,apxs_filelist,shotnums=ccam.read_ccs(searchdir_apxs,shots=True,masterlist=masterlist,name_sub_file=name_subs)
        apxs_data,apxs_wvl,apxs_filelist,=ccam.read_ccs(searchdir_apxs)
        val_data,val_wvl,val_filelist=ccam.read_ccs(searchdir_val)
        cal_data,cal_wvl,cal_filelist=ccam.read_ccs(searchdir_cal)
        all_data,all_wvl,all_filelist=ccam.read_ccs(searchdir)
        
        
        #get apxs CCS results
        blend_predict(apxs_data,apxs_wvl,apxs_filelist,blend_settings['blendranges'],blend_settings['inrange'],blend_settings['refpredict'],blend_settings['toblend'],masterlist,name_subs,ranges,ncs,maskfile,filenames,'apxs')
        
        #get validation CCS results
        blend_predict(val_data,val_wvl,val_filelist,blend_settings['blendranges'],blend_settings['inrange'],blend_settings['refpredict'],blend_settings['toblend'],masterlist,name_subs,ranges,ncs,maskfile,filenames,'val')
        
        #get cal target CCS results
        blend_predict(cal_data,cal_wvl,cal_filelist,blend_settings['blendranges'],blend_settings['inrange'],blend_settings['refpredict'],blend_settings['toblend'],masterlist,name_subs,ranges,ncs,maskfile,filenames,'cal')
        
        #get CCS results (this step takes a while because it needs to read all the CCS files)
        blend_predict(all_data,all_wvl,all_filelist,blend_settings['blendranges'],blend_settings['inrange'],blend_settings['refpredict'],blend_settings['toblend'],masterlist,name_subs,ranges,ncs,maskfile,filenames,'all')
        




predict=False
##############################  SiO2 #####################################
#Which element are you predicting?
which_elem='SiO2'
maxnc=20
ranges={'full':[0,100],'low':[0,50],'mid':[30,70],'high':[60,100]}
norms={'full':1,'low':3,'mid':3,'high':1}
ncs={'full':6,'low':9,'mid':6,'high':5}
testsetfile="C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\SiO2_sortfold_testfold.csv"


blendranges=[[-20,30],[30,50],[50,60],[60,70],[70,120]]
inrange=[0,0,0,0,0]
refpredict=[0,0,0,0,0]
toblend=[[1,1],[1,2],[2,2],[2,3],[3,3]]

blend_settings={'blendranges':blendranges,'inrange':inrange,'refpredict':refpredict,'toblend':toblend}
predict_elem(which_elem,maxnc,ranges,norms,ncs,testsetfile,predict,blend_settings,xminmax=[0,100],yminmax=[0,100],blend_opt=True)


###############################  TiO2 #####################################
which_elem='TiO2'

dbfile_TiO2='C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected_dopedTiO2.csv'
maxnc=30
ranges={'full':[0,100],'low':[0,2],'mid':[1,5],'high':[3,100]}
norms={'full':3,'low':3,'mid':1,'high':3}
ncs={'full':5,'low':7,'mid':5,'high':3}
testsetfile="C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\TiO2_sortfold_testfold.csv"
blendranges=[[-20,1],[1,2],[2,3],[3,5],[5,120]]
inrange=[0,0,0,0,0]
refpredict=[0,0,0,0,0]
toblend=[[1,1],[1,2],[2,2],[2,3],[3,3]]
blend_settings={'blendranges':blendranges,'inrange':inrange,'refpredict':refpredict,'toblend':toblend}
predict_elem(which_elem,maxnc,ranges,norms,ncs,testsetfile,predict,blend_settings,xminmax=[0,12],yminmax=[0,12],blend_opt=True,dbfile=dbfile_TiO2)

###############################  Al2O3 #####################################

which_elem='Al2O3'

maxnc=20
ranges={'full':[0,100],'low':[0,12],'mid':[10,25],'high':[20,100]}
norms={'full':3,'low':1,'mid':1,'high':1}
ncs={'full':6,'low':6,'mid':8,'high':6}
testsetfile="C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\Al2O3_sortfold_testfold.csv"
blendranges=[[-20,10],[10,12],[12,20],[20,25],[25,120]]
inrange=[0,0,0,0,0]
refpredict=[0,0,0,0,0]
toblend=[[1,1],[1,2],[2,2],[2,3],[3,3]]
blend_settings={'blendranges':blendranges,'inrange':inrange,'refpredict':refpredict,'toblend':toblend}
predict_elem(which_elem,maxnc,ranges,norms,ncs,testsetfile,predict,blend_settings,xminmax=[0,30],yminmax=[0,30],blend_opt=True)

###############################  FeOT #####################################

which_elem='FeOT'

maxnc=30
ranges={'full':[0,100],'low':[0,15],'mid':[5,25],'high':[15,100]}
norms={'full':3,'low':3,'mid':1,'high':3}
ncs={'full':8,'low':3,'mid':8,'high':3}
testsetfile="C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\FeOT_sortfold_testfold.csv"
blendranges=[[-20,5],[5,15],[15,15],[15,25],[25,120]]
inrange=[0,0,0,0,0]
refpredict=[0,0,0,0,0]
toblend=[[1,1],[1,2],[2,2],[2,3],[3,3]]
blend_settings={'blendranges':blendranges,'inrange':inrange,'refpredict':refpredict,'toblend':toblend}
predict_elem(which_elem,maxnc,ranges,norms,ncs,testsetfile,predict,blend_settings,xminmax=[0,50],yminmax=[0,50],blend_opt=True)

#
###############################  MgO #####################################
which_elem='MgO'
maxnc=20
ranges={'full':[0,100],'low':[0,3.5],'mid':[0,20],'high':[8,100]}
norms={'full':3,'low':1,'mid':1,'high':1}
ncs={'full':7,'low':6,'mid':9,'high':8}
testsetfile="C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\MgO_sortfold_testfold.csv"
blendranges=[[-20,1],[1,3.5],[3.5,8],[8,20],[20,120]]
inrange=[0,0,0,0,0]
refpredict=[0,0,0,0,0]
toblend=[[1,1],[1,2],[2,2],[2,3],[3,3]]
blend_settings={'blendranges':blendranges,'inrange':inrange,'refpredict':refpredict,'toblend':toblend}
predict_elem(which_elem,maxnc,ranges,norms,ncs,testsetfile,predict,blend_settings,xminmax=[0,50],yminmax=[0,50],blend_opt=True)

###############################  CaO #####################################

which_elem='CaO'
maxnc=30
ranges={'full':[0,42],'low':[0,7],'mid':[0,15],'high':[30,100]}
norms={'full':3,'low':1,'mid':3,'high':3}
ncs={'full':8,'low':9,'mid':9,'high':6}
testsetfile="C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\CaO_sortfold_testfold.csv"
blendranges=[[-20,2],[2,7],[7,15],[15,30],[30,120]]
inrange=[0,0,0,0,0]
refpredict=[0,0,0,0,0]
toblend=[[1,1],[1,2],[2,2],[2,3],[3,3]]
blend_settings={'blendranges':blendranges,'inrange':inrange,'refpredict':refpredict,'toblend':toblend}
predict_elem(which_elem,maxnc,ranges,norms,ncs,testsetfile,predict,blend_settings,xminmax=[0,40],yminmax=[0,40],blend_opt=True)

###############################  Na2O #####################################

which_elem='Na2O'

maxnc=20
ranges={'full':[0,100],'low':[0,4],'mid':[0,4],'high':[3.5,100]}
norms={'full':1,'low':1,'mid':1,'high':1}
ncs={'full':8,'low':7,'mid':7,'high':7}
testsetfile="C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\Na2O_sortfold_testfold.csv"
blendranges=[[-20,1],[1,3.5],[3.5,3.5],[3.5,4],[4,120]]
inrange=[0,0,0,0,0]
refpredict=[0,0,0,0,0]
toblend=[[1,1],[1,2],[2,2],[2,3],[3,3]]
blend_settings={'blendranges':blendranges,'inrange':inrange,'refpredict':refpredict,'toblend':toblend}
predict_elem(which_elem,maxnc,ranges,norms,ncs,testsetfile,predict,blend_settings,xminmax=[0,8],yminmax=[0,8],blend_opt=True)

###############################  K2O #####################################
which_elem='K2O'
maxnc=20
ranges={'full':[0,100],'low':[0,2],'mid':[0,2],'high':[1.5,100]}
norms={'full':3,'low':3,'mid':3,'high':1}
ncs={'full':4,'low':6,'mid':6,'high':9}
testsetfile="C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\K2O_sortfold_testfold.csv"
blendranges=[[-10,1],[1,1.5],[1.5,1.5],[1.5,2],[2,120]]
inrange=[0,0,0,0,0]
refpredict=[0,0,0,0,0]
toblend=[[1,1],[1,2],[2,2],[2,3],[3,3]]
blend_settings={'blendranges':blendranges,'inrange':inrange,'refpredict':refpredict,'toblend':toblend}
predict_elem(which_elem,maxnc,ranges,norms,ncs,testsetfile,predict,blend_settings,xminmax=[0,10],yminmax=[0,10],blend_opt=True)
