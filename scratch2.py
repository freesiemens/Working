# -*- coding: utf-8 -*-
"""
Created on Mon Mar 09 13:10:18 2015

@author: rbanderson
"""

import ccam
filename='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\RyanSulfatesPA.csv'
maskfile=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Working\Input\mask_minors_noise.csv'

data,wvl,files=ccam.read_spectra(filename)
data,wvl=ccam.mask(data,wvl,maskfile)
print 'stop'