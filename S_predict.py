# -*- coding: utf-8 -*-
"""
Created on Mon Mar 09 13:30:07 2015

@author: rbanderson
"""

import ccam
import numpy
import csv

spectrafile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\RyanSulfatesPA.csv'
maskfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\mask_minors_noise.csv'
outpath=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Output'
outputfile=r'S_predictions.csv'

which_elem='S'
plstype='sklearn'
maxnc=20
norm=1
fullmin=0
fullmax=100
nc=5
means_file=outpath+'\\'+which_elem+'_'+plstype+'_nc'+str(maxnc)+'_norm'+str(norm)+'_'+str(fullmin)+'-'+str(fullmax)+'_meancenters.csv'
loadfile=outpath+'\\'+which_elem+'_'+plstype+'_norm'+str(norm)+'_'+str(fullmin)+'-'+str(fullmax)+'.pkl'

spectra,wvl,labels=ccam.read_spectra(spectrafile)

y_predict,norm=ccam.pls_predict(spectra,nc,wvl,maskfile,loadfile=loadfile,mean_file=means_file)

with open(outputfile,'wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['Norm=',norm]
        writer.writerow(row)
        row=['nc=',str(nc)]
        writer.writerow(row)
        row=['File',which_elem]
        writer.writerow(row)
        
        for i in range(0,len(y_predict)):
            row=[labels[i],y_predict[i]]
            writer.writerow(row)        
