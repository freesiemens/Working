# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 16:08:54 2015

@author: rbanderson
This function normalizes LIBS spectra in one of two ways, depending on the value of the "normtype" keyword.

Inputs:
spectra = float array of spectra to be normalized
wvl = float array of wavelengths for the spectra
normtype = specifies whether to normalize by the sum of the spectrum across all wavelengths (normtype = 1)
or by the sum for each spectrometer (normtype = 3)
"""
import numpy
import copy
def normalize(spectra,wvl,normtype=3):
    spectra_norm=copy.copy(spectra)
    if normtype==3:
        uv_index=(wvl<=340.797)  #create an index for the UV range
        vis_index=(wvl>=382.138)&(wvl<=469.090) #create an index for the VIS range
        vnir_index=(wvl>=473.184) #create an index for the VNIR range
        uvtotals=numpy.sum(spectra[:,uv_index],axis=1)  #calculate the totals of each spectrum in the UV range
        vistotals=numpy.sum(spectra[:,vis_index],axis=1)  #calculate the totals of each spectrum in the VIS range
        vnirtotals=numpy.sum(spectra[:,vnir_index],axis=1)  #calculate the totals of each spectrum in the VNIR range
        for i in range(len(uvtotals)): spectra_norm[i,uv_index]=spectra[i,uv_index]/uvtotals[i]  #normalize each spectrum in the UV range
        for i in range(len(vistotals)): spectra_norm[i,vis_index]=spectra[i,vis_index]/vistotals[i]  #normalize each spectrum in the VIS range  
        for i in range(len(vnirtotals)): spectra_norm[i,vnir_index]=spectra[i,vnir_index]/vnirtotals[i]  #normalize each spectrum in the VNNIR range  
        
    if normtype==1:
        totals=numpy.sum(spectra,axis=1) #calculate the total of each spectrum
        for i in range(len(totals)):
            spectra_norm[i,:]=spectra[i,:]/totals[i] #normalize each spectrum
        
    return spectra_norm
            
