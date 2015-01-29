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
masterlist=r'C:\Users\rbanderson\Documents\MSL\ChemCam\ChemCam\ops_ccam_misc\MASTERLIST.csv'
name_subs=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Input\target_name_subs.csv'
which_elem='MgO'
nc_full=5
nc_low=5
nc_high=6

fullnorm=3
lownorm=3
highnorm=3
low_cutoff=3.0

data,wvl,filelist=ccam.read_ccs(searchdir)
data,wvl=ccam.mask(data,wvl,maskfile)
data_norm3=ccam.normalize(data,wvl,normtype=3)
data_norm1=ccam.normalize(data,wvl,normtype=1)

targetlist=ccam.target_lookup(filelist,masterlist,name_subs)

coeff_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_0-100_mlpy_nc20_norm3_beta_coeffs.csv'
means_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_0-100_mlpy_nc20_norm3_meancenters.csv'
y_full=ccam.pls_unk(data_norm3,nc_full,coeff_file=coeff_file,means_file=means_file)

coeff_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_0-3.5_mlpy_nc20_norm3_beta_coeffs.csv'
means_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_0-3.5_mlpy_nc20_norm3_meancenters.csv'
y_low=ccam.pls_unk(data_norm3,nc_full,coeff_file=coeff_file,means_file=means_file)

coeff_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_2.5-100_mlpy_nc20_norm3_beta_coeffs.csv'
means_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Working\Output\MgO_2.5-100_mlpy_nc20_norm3_meancenters.csv'
y_high=ccam.pls_unk(data_norm3,nc_full,coeff_file=coeff_file,means_file=means_file)

y_combined=numpy.zeros_like(y_high)

combined_description='If Low>'+str(low_cutoff)+' use High, if Low <'+str(low_cutoff)+' use Low'
for i in range(len(y_combined)):
    if y_low[i]<low_cutoff:
        y_combined[i]=y_low[i]
    if y_low[i]>low_cutoff:
        y_combined[i]=y_high[i]
        
with open(outpath+'\\'+which_elem+'_predictions.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['','','Full (0-100)','Low (0-'+str(low_cutoff)+')','High ('+str(low_cutoff)+'-100)','Combined']
        writer.writerow(row)
        row=['','Norm=',fullnorm,lownorm,highnorm,combined_description]
        writer.writerow(row)
        row=['','nc=',str(nc_full),str(nc_low),str(nc_high)]
        writer.writerow(row)
        row=['File','Target',which_elem,which_elem,which_elem,which_elem]
        writer.writerow(row)
        
        for i in range(0,len(y_combined)):
            row=[filelist[i],targetlist[i],y_full[i],y_low[i],y_high[i],y_combined[i]]
            writer.writerow(row)        
        
        
