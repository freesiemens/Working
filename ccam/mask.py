# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 14:22:16 2015

@author: rbanderson

This function applies a mask to LIBS spectra to remove unwanted regions of the spectrum

Input:
spectra = Float array of shape (samples, spectral channels) (e.g. 2029x6144)
wvl = float array containing wavelengths for each of the spectral channels
maskfile = string specifying the path to the mask file.
    Mask file should have three comma-separated columns:
    column 0 = name of feature being masked
    column 1 = minimum wavelength to be masked for each feature
    column 2= maximum wavelength to be masked for each feature
    
    The first row of the file should contain column headings
    
Output:
spectra_masked = the spectra array, with the columns corresponding to masked wavelengths removed
wvl_masked = the wavelength array, with the masked wavelengths removed
    
"""
import numpy
def mask(spectra,wvl,maskfile):
    spectra_masked=spectra
    wvl_masked=wvl
    mask=numpy.genfromtxt(maskfile,usecols=(1,2),dtype='float',delimiter=',',skip_header=1) #read the mask file
    for i in range(0,mask.shape[0]):
        #create an index for all elements of wvl between the min and max 
        #wavelengths on each row of the mask file, then invert it so everything
        #in that range is false and everything outside is true
        index=numpy.invert((wvl_masked>=mask[i,0]) & (wvl_masked<=mask[i,1])) 
        spectra_masked=spectra_masked[:,index] #mask the spectra
        wvl_masked=wvl_masked[index] #mask wvl
    
    return spectra_masked,wvl_masked    