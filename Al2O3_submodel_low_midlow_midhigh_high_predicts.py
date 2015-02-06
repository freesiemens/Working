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
import ccam_normalize
import copy
import cPickle as pickle

searchdir=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_team'
maskfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Input\mask_minors_noise.csv'
outpath=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output'
masterlist=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_misc\MASTERLIST.csv'
name_subs=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Input\target_name_subs.csv'

coeff_file_full=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\Al2O3_mlpy_nc20_norm1_0-100_beta_coeffs.csv'
means_file_full=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\Al2O3_mlpy_nc20_norm1_0-100_meancenters.csv'
coeff_file_low=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\Al2O3_mlpy_nc20_norm1_0-12_beta_coeffs.csv'
means_file_low=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\Al2O3_mlpy_nc20_norm1_0-12_meancenters.csv'
coeff_file_midlow=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\Al2O3_mlpy_nc20_norm1_10-18_beta_coeffs.csv'
means_file_midlow=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\Al2O3_mlpy_nc20_norm1_10-18_meancenters.csv'
coeff_file_midhigh=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\Al2O3_mlpy_nc20_norm1_16-25_beta_coeffs.csv'
means_file_midhigh=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\Al2O3_mlpy_nc20_norm1_16-25_meancenters.csv'
coeff_file_high=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\Al2O3_mlpy_nc20_norm1_20-100_beta_coeffs.csv'
means_file_high=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\Al2O3_mlpy_nc20_norm1_20-100_meancenters.csv'

fullfiles=[coeff_file_full,means_file_full]
lowfiles=[coeff_file_low,means_file_low]
midlowfiles=[coeff_file_midlow,means_file_midlow]
midhighfiles=[coeff_file_midhigh,means_file_midhigh]
highfiles=[coeff_file_high,means_file_high]

which_elem='Al2O3'
nc_full=5
nc_low=5
nc_midlow=5
nc_midhigh=4
nc_high=6

fullnorm=1
lownorm=1
midlownorm=1
midhighnorm=1
highnorm=1


low_cutoff=11
mid_cutoff=17
high_cutoff=22.5

outputfile=outpath+'\\'+which_elem+'_predictions_low_midlow_midhigh_high.csv'
datafile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\ccam\ccamdata.pkl'
print 'Loading data'
f=open(datafile,'rb')
data=pickle.load(f)
wvl=pickle.load(f)
filelist=pickle.load(f)
#data,wvl,filelist=ccam.read_ccs(searchdir)
#data,wvl=ccam.mask(data,wvl,maskfile)
#data_norm3=ccam_normalize.ccam_normalize(data,wvl,normtype=3)
#data_norm1=ccam_normalize.ccam_normalize(data,wvl,normtype=1)

targetlist=ccam.target_lookup(filelist,masterlist,name_subs)

#y_full=ccam.pls_unk(data_norm1,nc_full,coeff_file=coeff_file_full,means_file=means_file_full)
#y_low=ccam.pls_unk(data_norm1,nc_low,coeff_file=coeff_file_low,means_file=means_file_low)
#y_midlow=ccam.pls_unk(data_norm1,nc_midlow,coeff_file=coeff_file_midlow,means_file=means_file_midlow)
#y_midhigh=ccam.pls_unk(data_norm1,nc_midhigh,coeff_file=coeff_file_midhigh,means_file=means_file_midhigh)
#y_high=ccam.pls_unk(data_norm1,nc_high,coeff_file=coeff_file_high,means_file=means_file_high)

#print 'Full model prediction'
#
y_full,fullnorm=ccam.pls_predict(which_elem,nc_full,copy.copy(data),copy.copy(wvl),maskfile,fullfiles)
y_low,lownorm=ccam.pls_predict(which_elem,nc_low,copy.copy(data),copy.copy(wvl),maskfile,lowfiles)
y_midlow,midlownorm=ccam.pls_predict(which_elem,nc_midlow,copy.copy(data),copy.copy(wvl),maskfile,midlowfiles)
y_midhigh,midhighnorm=ccam.pls_predict(which_elem,nc_midhigh,copy.copy(data),copy.copy(wvl),maskfile,midhighfiles)
y_high,highnorm=ccam.pls_predict(which_elem,nc_high,copy.copy(data),copy.copy(wvl),maskfile,highfiles)

y_combined=numpy.zeros_like(y_high)

combined_description='If Full<'+str(low_cutoff)+'use low, else if Full <'+str(mid_cutoff)+' use midlow, else if Full <'+str(high_cutoff)+' use midhigh, else use high'

for i in range(len(y_combined)):
    if y_full[i]<low_cutoff:
        y_combined[i]=y_low[i]
    else:
        if y_full[i]<mid_cutoff:
            y_combined[i]=y_midlow[i]
        else:
            if y_full[i]<high_cutoff:
                y_combined[i]=y_midhigh[i]
            else:
                y_combined[i]=y_high[i]
        
with open(outputfile,'wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['','','Full (0-100)','Low (0-12)','Midlow (10-18)','Midhigh (16-25)','High (20-100)','Combined']
        writer.writerow(row)
        row=['','Norm=',fullnorm,lownorm,midlownorm,midhighnorm,highnorm,combined_description]
        writer.writerow(row)
        row=['','nc=',str(nc_full),str(nc_low),str(nc_midlow),str(nc_midhigh),str(nc_high)]
        writer.writerow(row)
        row=['File','Target',which_elem,which_elem,which_elem,which_elem,which_elem]
        writer.writerow(row)
        
        for i in range(0,len(y_combined)):
            row=[filelist[i],targetlist[i],y_full[i],y_low[i],y_midlow[i],y_midhigh[i],y_high[i],y_combined[i]]
            writer.writerow(row)        
        
        
