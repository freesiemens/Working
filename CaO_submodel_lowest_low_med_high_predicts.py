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
coeff_file_lowest=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_mlpy_nc20_norm1_0-2.5_beta_coeffs.csv'
means_file_lowest=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_mlpy_nc20_norm1_0-2.5_meancenters.csv'
coeff_file_low=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_mlpy_nc20_norm1_2.0-7.0_beta_coeffs.csv'
means_file_low=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_mlpy_nc20_norm1_2.0-7.0_meancenters.csv'
coeff_file_mid=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_mlpy_nc20_norm1_6-20_beta_coeffs.csv'
means_file_mid=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_mlpy_nc20_norm1_6-20_meancenters.csv'
coeff_file_high=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_mlpy_nc20_norm3_10-100_beta_coeffs.csv'
means_file_high=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\CaO_mlpy_nc20_norm3_10-100_meancenters.csv'


which_elem='CaO'
nc_full=9
nc_lowest=3
nc_low=3
nc_mid=5
nc_high=7

fullnorm=3
lowestnorm=1
lownorm=1
midnorm=1
highnorm=3

lowest_cutoff=2.25
low_cutoff=6.5
high_cutoff=15

data,wvl,filelist=ccam.read_ccs(searchdir)
data,wvl=ccam.mask(data,wvl,maskfile)
data_norm3=ccam_normalize.ccam_normalize(data,wvl,normtype=3)
data_norm1=ccam_normalize.ccam_normalize(data,wvl,normtype=1)

targetlist=ccam.target_lookup(filelist,masterlist,name_subs)

y_full=ccam.pls_unk(data_norm3,nc_full,coeff_file=coeff_file_full,means_file=means_file_full)
y_lowest=ccam.pls_unk(data_norm1,nc_lowest,coeff_file=coeff_file_lowest,means_file=means_file_lowest)
y_low=ccam.pls_unk(data_norm1,nc_low,coeff_file=coeff_file_low,means_file=means_file_low)
y_mid=ccam.pls_unk(data_norm1,nc_mid,coeff_file=coeff_file_mid,means_file=means_file_mid)
y_high=ccam.pls_unk(data_norm3,nc_high,coeff_file=coeff_file_high,means_file=means_file_high)

y_combined=numpy.zeros_like(y_high)

combined_description='If Full<'+str(lowest_cutoff)+'use low, if Full >'+str(lowest_cutoff)+' and <'+str(low_cutoff)+' use low, if Full > '+str(low_cutoff)+' and < '+str(high_cutoff)+' use Mid, if Full >'+str(high_cutoff)+' use high'
#combined_description='If Full<'+str(low_cutoff)+' use low, else use high'
for i in range(len(y_combined)):
    if y_full[i]<lowest_cutoff:
        y_combined[i]=y_lowest[i]
    if y_full[i]>lowest_cutoff and y_full[i]<low_cutoff:
        y_combined[i]=y_low[i]
    if y_full[i]>low_cutoff and y_full[i]<high_cutoff:
        y_combined[i]=y_mid[i]
    if y_full[i]>high_cutoff:
        y_combined[i]=y_high[i]
        
with open(outpath+'\\'+which_elem+'_predictions.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['','','Full (0-100)','Lowest (0-2.5)','Low (2-7)','Med (6-20)','High (10-100)','Combined']
        writer.writerow(row)
        row=['','Norm=',fullnorm,lowestnorm,lownorm,midnorm,highnorm,combined_description]
        writer.writerow(row)
        row=['','nc=',str(nc_full),str(nc_lowest),str(nc_low),str(nc_mid),str(nc_high)]
        writer.writerow(row)
        row=['File','Target',which_elem,which_elem,which_elem,which_elem,which_elem]
        writer.writerow(row)
        
        for i in range(0,len(y_combined)):
            row=[filelist[i],targetlist[i],y_full[i],y_lowest[i],y_low[i],y_mid[i],y_high[i],y_combined[i]]
            writer.writerow(row)        
        
        
