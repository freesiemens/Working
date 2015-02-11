# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 21:08:20 2015

@author: rbanderson
"""

import os
os.chdir(r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\ccam')

import ccam
import numpy
import csv
import sys

searchdir=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_team'
maskfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Input\mask_minors_noise.csv'
outpath=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output'
masterlist=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_misc\MASTERLIST.csv'
name_subs=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Input\target_name_subs.csv'
dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\full_db_mars_corrected.csv'
keepfile=None
removefile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\removelist.csv'


coeff_file_full=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_mlpy_nc20_norm3_0-100_beta_coeffs.csv'
means_file_full=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_mlpy_nc20_norm3_0-100_meancenters.csv'
coeff_file_low=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_mlpy_nc20_norm3_0-3_beta_coeffs.csv'
means_file_low=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_mlpy_nc20_norm3_0-3_meancenters.csv'
coeff_file_mid=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_mlpy_nc20_norm3_2-12_beta_coeffs.csv'
means_file_mid=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_mlpy_nc20_norm3_2-12_meancenters.csv'
coeff_file_high=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_mlpy_nc20_norm1_10-100_beta_coeffs.csv'
means_file_high=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_mlpy_nc20_norm1_10-100_meancenters.csv'
fullfiles=[coeff_file_full,means_file_full]
lowfiles=[coeff_file_low,means_file_low]
midfiles=[coeff_file_mid,means_file_mid]
highfiles=[coeff_file_high,means_file_high]


which_elem='MgO'
nc_full=7
nc_low=3
nc_mid=5
nc_high=9

low_cutoff=2.5
high_cutoff=11
outputfile=outpath+'\\'+which_elem+'_predictions.csv'
db_outputfile=outpath+'\\'+which_elem+'_db_predictions.csv'


print 'Reading database'
sys.stdout.flush()
spectra,comps,spect_index,names,labels,wvl=ccam.read_db(dbfile,compcheck=True)
oxides=labels[2:]
compindex=numpy.where(oxides==which_elem)[0]

print 'Choosing spectra'
mincomp=0
maxcomp=100
spectra,names,spect_index,comps=ccam.choose_spectra(spectra,spect_index,names,comps,compindex,mincomp=mincomp,maxcomp=maxcomp,keepfile=keepfile,removefile=removefile,which_removed=None)

y_db_full,fullnorm=ccam.pls_predict(which_elem,nc_full,spectra,wvl,maskfile,fullfiles)
y_db_low,lownorm=ccam.pls_predict(which_elem,nc_low,spectra,wvl,maskfile,lowfiles)
y_db_mid,midnorm=ccam.pls_predict(which_elem,nc_mid,spectra,wvl,maskfile,midfiles)
y_db_high,highnorm=ccam.pls_predict(which_elem,nc_high,spectra,wvl,maskfile,highfiles)

"""
From low model 0 to 1, use the low model
If low model between 1 and 3, then blend the low and mid models using low as reference
If low model AND mid model are between 3 and 8, use the mid model
If mid is 8 to 12, then blend mid and high using mid as reference
if high >12 then use high
"""

predicts=[y_db_full,y_db_low,y_db_mid,y_db_high]
ranges=[[0,1],[1,3],[3,8],[8,12],[12,100]]
inrange=[1,1,[1,2],2,3]
refpredict=[1,1,2,2,3]
toblend=[[1,1],[1,2],[2,2],[2,3],[3,3]]

blended2=ccam.submodels_blend(predicts,ranges,inrange,refpredict,toblend,overwrite=False)

truecomps=[comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex],comps[:,compindex]]
predicts=[y_db_full,y_db_low,y_db_mid,y_db_high,blended2]
plot_title='Final Model MgO Predictions of Full Database'
labels=['Full','Low','Mid','High','Blended']
colors=['c','r','g','b','k']
markers=['o','<','s','^','*']
imgfile=outpath+'\\'+which_elem+'_final_model_predictions_1to1.png'
xminmax=[0,60]
yminmax=[0,60]
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


imgfile=outpath+'\\'+which_elem+'_final_model_predictions_1to1_0-20.png'
xminmax=[0,20]
yminmax=[0,20]
ccam.plots.Plot1to1(truecomps,predicts,plot_title,labels,colors,markers,imgfile,xminmax=xminmax,yminmax=yminmax)

imgfile=outpath+'\\'+which_elem+'_final_model_predictions_1to1_0-20_full.png'
ccam.plots.Plot1to1([truecomps[0]],[predicts[0]],plot_title,[labels[0]],[colors[0]],[markers[0]],imgfile,xminmax=xminmax,yminmax=yminmax)
imgfile=outpath+'\\'+which_elem+'_final_model_predictions_1to1_0-20_low.png'
ccam.plots.Plot1to1([truecomps[1]],[predicts[1]],plot_title,[labels[1]],[colors[1]],[markers[1]],imgfile,xminmax=xminmax,yminmax=yminmax)
imgfile=outpath+'\\'+which_elem+'_final_model_predictions_1to1_0-20_mid.png'
ccam.plots.Plot1to1([truecomps[2]],[predicts[2]],plot_title,[labels[2]],[colors[2]],[markers[2]],imgfile,xminmax=xminmax,yminmax=yminmax)
imgfile=outpath+'\\'+which_elem+'_final_model_predictions_1to1_0-20_high.png'
ccam.plots.Plot1to1([truecomps[3]],[predicts[3]],plot_title,[labels[3]],[colors[3]],[markers[3]],imgfile,xminmax=xminmax,yminmax=yminmax)
imgfile=outpath+'\\'+which_elem+'_final_model_predictions_1to1_0-20_blended.png'
ccam.plots.Plot1to1([truecomps[4]],[predicts[4]],plot_title,[labels[4]],[colors[4]],[markers[4]],imgfile,xminmax=xminmax,yminmax=yminmax)


with open(db_outputfile,'wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['','','','Full (0-100)','Low (0-3)','Mid (2-12)','High (10-100)','Blended']
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


print 'Full model prediction'
y_full,fullnorm=ccam.pls_predict(which_elem,nc_full,data,wvl,maskfile,fullfiles)
print 'Low model prediction'
y_low,lownorm=ccam.pls_predict(which_elem,nc_low,data,wvl,maskfile,lowfiles)
print 'Mid model prediction'
y_mid,midnorm=ccam.pls_predict(which_elem,nc_mid,data,wvl,maskfile,midfiles)
print 'High model prediction'
y_high,highnorm=ccam.pls_predict(which_elem,nc_high,data,wvl,maskfile,highfiles)

predicts=[y_full,y_low,y_mid,y_high]
ranges=[[0,1.5],[1.5,3],[3,8],[8,10],[10,100]]
inrange=[1,1,[1,2],2,3]
refpredict=[1,1,2,2,3]
toblend=[[1,1],[1,2],[2,2],[2,3],[3,3]]

blended=ccam.submodels_blend(predicts,ranges,inrange,refpredict,toblend,overwrite=False)


targetlist,targetdists,targetamps=ccam.target_lookup(filelist,masterlist,name_subs)

y_combined=numpy.zeros_like(y_high)
#print 'Combining predictions'
#combined_description='If Full <'+str(low_cutoff)+' use Low, if Full >'+str(high_cutoff)+' use high, else use mid'
#
#for i in range(len(y_combined)):
#    if y_full[i]<low_cutoff:
#        y_combined[i]=y_low[i]
#    else:
#        if y_full[i]<high_cutoff:
#            y_combined[i]=y_mid[i]
#        else:
#            if y_full[i]>high_cutoff:
#                y_combined[i]=y_high[i]
#print 'Writing results'
with open(outputfile,'wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['','','','','Full (0-100)','Low (0-3)','Mid (2-12)','High (10-100)','Blended']
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
        
        
