# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 21:08:20 2015

@author: rbanderson
"""

import os
os.chdir(r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\ccam')

import ccam

import ccam_mask as mask
import ccam_normalize as normalize
import numpy
import csv

searchdir=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_team'
maskfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Input\mask_minors_noise.csv'
outpath=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output'
which_elem='SiO2'

data,wvl,filelist=ccam.read_ccs(searchdir)
data,wvl=mask.ccam_mask(data,wvl,maskfile)

normtype=3
data_norm3=normalize.ccam_normalize(data,wvl,normtype=normtype)
print data_norm3[0,0]
coeff_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\SiO2_mlpy_nc20_norm3_0-100_beta_coeffs.csv'
means_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\SiO2_mlpy_nc20_norm3_0-100_meancenters.csv'
nc=7
y_full=ccam.pls_unk(data_norm3,coeff_file,means_file,nc)

normtype=1
data_norm1=normalize.ccam_normalize(data,wvl,normtype=normtype)
print data_norm3[0,0]
coeff_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\SiO2_mlpy_nc20_norm3_0-40_beta_coeffs.csv'
means_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\SiO2_mlpy_nc20_norm3_0-40_meancenters.csv'
nc=4
y_low=ccam.pls_unk(data_norm1,coeff_file,means_file,nc)

normtype=3
data_norm3=normalize.ccam_normalize(data,wvl,normtype=normtype)
print data_norm3[0,0]
coeff_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\SiO2_mlpy_nc20_norm3_20-65_beta_coeffs.csv'
means_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\SiO2_mlpy_nc20_norm3_20-65_meancenters.csv'
nc=7
y_mid=ccam.pls_unk(data_norm3,coeff_file,means_file,nc)

normtype=1
data_norm1=normalize.ccam_normalize(data,wvl,normtype=normtype)
coeff_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\SiO2_mlpy_nc20_norm3_55-100_beta_coeffs.csv'
means_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\SiO2_mlpy_nc20_norm3_55-100_meancenters.csv'
nc=5
y_high=ccam.pls_unk(data_norm1,coeff_file,means_file,nc)

y_combined=numpy.zeros_like(y_high)

for i in range(len(y_combined)):
    if y_full[i]>60:
        y_combined[i]=y_high[i]
    if y_full[i]>30 and y_full[i]<60:
        y_combined[i]=y_mid[i]
    if y_full[i]<30:
        y_combined[i]=y_low[i]
        
with open(outpath+'\\'+which_elem+'_predictions.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['','Full (0-100)','Low (0-40)','Med (20-65)','High (55-100)','Combined']
        writer.writerow(row)
        row=['','norm3','norm1','norm3','norm1','If Full>60 use High, if Full <30 use Low, else use Mid']
        writer.writerow(row)
        row=['','nc=7','nc=4','nc=7','nc=5','']
        writer.writerow(row)
        row=['File','SiO2','SiO2','SiO2','SiO2','SiO2']
        writer.writerow(row)
        
        for i in range(0,len(y_combined)):
            row=[filelist[i],y_full[i],y_low[i],y_mid[i],y_high[i],y_combined[i]]
            writer.writerow(row)        
        
        
