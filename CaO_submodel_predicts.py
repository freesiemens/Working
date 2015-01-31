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
searchdir=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_team'
maskfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Input\mask_minors_noise.csv'
outpath=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output'
masterlist=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_misc\MASTERLIST.csv'
name_subs=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Input\target_name_subs.csv'

coeff_file_full=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_mlpy_nc20_norm3_0-100_beta_coeffs.csv'
means_file_full=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_mlpy_nc20_norm3_0-100_meancenters.csv'
coeff_file_low=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_mlpy_nc20_norm3_0-7_beta_coeffs.csv'
means_file_low=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_mlpy_nc20_norm3_0-7_meancenters.csv'
coeff_file_mid=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_mlpy_nc20_norm3_5-20_beta_coeffs.csv'
means_file_mid=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_mlpy_nc20_norm3_5-20_meancenters.csv'
coeff_file_high=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_mlpy_nc20_norm3_10-100_beta_coeffs.csv'
means_file_high=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_mlpy_nc20_norm3_10-100_meancenters.csv'


which_elem='CaO'
nc_full=9
nc_low=10
nc_mid=6
nc_high=9

fullnorm=3
lownorm=3
midnorm=3
highnorm=1

low_cutoff=6
high_cutoff=15

data,wvl,filelist=ccam.read_ccs(searchdir)
data,wvl=ccam.mask(data,wvl,maskfile)
data_norm3=ccam_normalize.ccam_normalize(data,wvl,normtype=3)
data_norm1=ccam_normalize.ccam_normalize(data,wvl,normtype=1)

targetlist=ccam.target_lookup(filelist,masterlist,name_subs)

y_full=ccam.pls_unk(data_norm3,nc_full,coeff_file=coeff_file_full,means_file=means_file_full)
y_low=ccam.pls_unk(data_norm3,nc_low,coeff_file=coeff_file_low,means_file=means_file_low)
y_mid=ccam.pls_unk(data_norm3,nc_mid,coeff_file=coeff_file_mid,means_file=means_file_mid)
y_high=ccam.pls_unk(data_norm3,nc_high,coeff_file=coeff_file_high,means_file=means_file_high)

y_combined=numpy.zeros_like(y_high)

combined_description='If Full<'+str(low_cutoff)+'and >'+str(high_cutoff)+' use Mid, if Full <'+str(low_cutoff)+' use Low, if Full >'+str(high_cutoff)+' use high'
#combined_description='If Full<'+str(low_cutoff)+' use low, else use high'
for i in range(len(y_combined)):
    if y_full[i]<low_cutoff:
        y_combined[i]=y_low[i]
    if y_full[i]>low_cutoff and y_full[i]<high_cutoff:
        y_combined[i]=y_mid[i]
    if y_full[i]>high_cutoff:
        y_combined[i]=y_high[i]
        
with open(outpath+'\\'+which_elem+'_predictions.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['','','Full (0-100)','Low (0-7)','Mid (5-20)','High (10-100)','Combined']
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
        
        
