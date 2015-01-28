# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 21:08:20 2015

@author: rbanderson
"""
import ccam
import numpy
import csv

searchdir=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_team'
maskfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Input\mask_minors_noise.csv'
outpath=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output'
which_elem='MgO'
nc_full=6
nc_low=10
nc_mid=3
nc_high=5
high_cutoff=11
low_cutoff=2.5

data,wvl,filelist=ccam.read_ccs(searchdir)
data,wvl=ccam.mask(data,wvl,maskfile)

normtype=3
data_norm3=ccam.normalize(data,wvl,normtype=normtype)
coeff_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_mlpy_nc20_norm3_0-100_beta_coeffs.csv'
means_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_mlpy_nc20_norm3_0-100_meancenters.csv'
y_full=ccam.pls_unk(data_norm3,coeff_file,means_file,nc_full)

normtype=3
data_norm3=ccam.normalize(data,wvl,normtype=normtype)
coeff_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_mlpy_nc20_norm3_0-3_beta_coeffs.csv'
means_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_mlpy_nc20_norm3_0-3_meancenters.csv'
y_low=ccam.pls_unk(data_norm3,coeff_file,means_file,nc_low)

normtype=3
data_norm3=ccam.normalize(data,wvl,normtype=normtype)
coeff_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_mlpy_nc20_norm3_2-12_beta_coeffs.csv'
means_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_mlpy_nc20_norm3_2-12_meancenters.csv'
y_mid=ccam.pls_unk(data_norm3,coeff_file,means_file,nc_mid)

normtype=3
data_norm1=ccam.normalize(data,wvl,normtype=normtype)
coeff_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_mlpy_nc20_norm3_10-100_beta_coeffs.csv'
means_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_mlpy_nc20_norm3_10-100_meancenters.csv'
y_high=ccam.pls_unk(data_norm3,coeff_file,means_file,nc_high)

y_combined=numpy.zeros_like(y_high)

for i in range(len(y_combined)):
    if y_full[i]>high_cutoff:
        y_combined[i]=y_high[i]
    if y_full[i]>low_cutoff and y_full[i]<high_cutoff:
        y_combined[i]=y_mid[i]
    if y_full[i]<low_cutoff:
        y_combined[i]=y_low[i]
        
with open(outpath+'\\'+which_elem+'_predictions.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['','Full (0-100)','Low (0-'+str(low_cutoff)+')','Med ('+str(low_cutoff)+'-'+str(high_cutoff)+')','High ('+str(high_cutoff)+'-100)','Combined']
        writer.writerow(row)
        row=['','norm3','norm3','norm3','norm3','If Full>'+str(high_cutoff)+' use High, if Full <'+str(low_cutoff)+' use Low, else use Mid']
        writer.writerow(row)
        row=['','nc='+str(nc_full),'nc='+str(nc_low),'nc='+str(nc_mid),'nc='+str(nc_high),'']
        writer.writerow(row)
        row=['File',which_elem,which_elem,which_elem,which_elem,which_elem]
        writer.writerow(row)
        
        for i in range(0,len(y_combined)):
            row=[filelist[i],y_full[i],y_low[i],y_mid[i],y_high[i],y_combined[i]]
            writer.writerow(row)        
        
        
