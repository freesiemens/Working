# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 21:08:20 2015

@author: rbanderson
"""

import os
os.chdir(r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\ccam')
import copy
import ccam
import numpy
import csv
import ccam_normalize
import cPickle as pickle
searchdir=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_team'
maskfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Input\mask_minors_noise.csv'
outpath=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\Al2O3 nc20 initial submodel'
masterlist=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_misc\MASTERLIST.csv'
name_subs=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Input\target_name_subs.csv'


coeff_file_full=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\Al2O3 nc20 initial submodel\Al2O3_mlpy_nc20_norm1_0-100_beta_coeffs.csv'
means_file_full=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\Al2O3 nc20 initial submodel\Al2O3_mlpy_nc20_norm1_0-100_meancenters.csv'
coeff_file_low=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\Al2O3 nc20 initial submodel\Al2O3_mlpy_nc20_norm1_0-12_beta_coeffs.csv'
means_file_low=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\Al2O3 nc20 initial submodel\Al2O3_mlpy_nc20_norm1_0-12_meancenters.csv'
coeff_file_mid=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\Al2O3 nc20 initial submodel\Al2O3_mlpy_nc20_norm1_10-25_beta_coeffs.csv'
means_file_mid=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\Al2O3 nc20 initial submodel\Al2O3_mlpy_nc20_norm1_10-25_meancenters.csv'
coeff_file_high=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\Al2O3 nc20 initial submodel\Al2O3_mlpy_nc20_norm1_20-100_beta_coeffs.csv'
means_file_high=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\Al2O3 nc20 initial submodel\Al2O3_mlpy_nc20_norm1_20-100_meancenters.csv'

fullfiles=[coeff_file_full,means_file_full]
lowfiles=[coeff_file_low,means_file_low]
midfiles=[coeff_file_mid,means_file_mid]
highfiles=[coeff_file_high,means_file_high]


which_elem='Al2O3'
nc_full=5
nc_low=5
nc_mid=4
nc_high=6

low_cutoff=11
high_cutoff=22.5

outputfile=outpath+'\\'+which_elem+'_predictions_newsettings.csv'
datafile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\ccam\ccamdata.pkl'
print 'Loading data'
f=open(datafile,'rb')
data=pickle.load(f)
wvl=pickle.load(f)
filelist=pickle.load(f)

#data,wvl,filelist=ccam.read_ccs(searchdir)
fullfiles=[coeff_file_full,means_file_full]

print 'Full model prediction'
y_full,fullnorm=ccam.pls_predict(which_elem,nc_full,copy.copy(data),copy.copy(wvl),maskfile,fullfiles)
print 'Low model prediction'
y_low,lownorm=ccam.pls_predict(which_elem,nc_low,copy.copy(data),copy.copy(wvl),maskfile,lowfiles)
print 'Mid model prediction'
y_mid,midnorm=ccam.pls_predict(which_elem,nc_mid,copy.copy(data),copy.copy(wvl),maskfile,midfiles)
print 'High model prediction'
y_high,highnorm=ccam.pls_predict(which_elem,nc_high,copy.copy(data),copy.copy(wvl),maskfile,highfiles)

targetlist=ccam.target_lookup(filelist,masterlist,name_subs)

y_combined=numpy.zeros_like(y_high)
print 'Combining predictions'
combined_description='If Full <'+str(low_cutoff)+' use Low, if Full >'+str(high_cutoff)+' use high, else use mid'
#combined_description='If Full<'+str(low_cutoff)+' use low, else use high'
for i in range(len(y_combined)):
    if y_full[i]<low_cutoff:
        y_combined[i]=y_low[i]
    if y_full[i]>low_cutoff and y_full[i]<high_cutoff:
        y_combined[i]=y_mid[i]
    if y_full[i]>high_cutoff:
        y_combined[i]=y_high[i]
print 'Writing results'
with open(outputfile,'wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['','','Full (0-100)','Low (0-12)','Mid (10-25)','High (20-100)','Combined']
        writer.writerow(row)
        row=['','Norm=',fullnorm,lownorm,midnorm,highnorm,combined_description]
        writer.writerow(row)
        row=['','nc=',str(nc_full),str(nc_low),str(nc_mid),str(nc_high)]
        writer.writerow(row)
        row=['File','Target',which_elem,which_elem,which_elem,which_elem]
        writer.writerow(row)
        
        for i in range(0,len(y_combined)):
            row=[filelist[i],targetlist[i],y_full[i],y_low[i],y_mid[i],y_high[i],y_combined[i]]
            writer.writerow(row)        
        
        
