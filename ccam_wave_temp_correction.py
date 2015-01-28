# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 09:37:29 2014

@author: rbanderson
;+
; NAME:
;   Wavelength Temperature Correction
;   wave_temp_correction.pro
;
; PURPOSE:
;   Read an EDR LIBS file and return the spectra on a default
;   wavelength basis (in channels) after correction for temperature drift.
;
; CATEGORY:
;   Mars Science Laboratory
;   ChemCam - LIBS
;   Level-1 processing
;
; CALLING SEQUENCE:
;   E.g., file = 'CL5_399889564EDR_F0030530CCAM01027M1.DAT'
;   y1 = wave_temp_correction(file)
;   or
;   use another read routine to get the spectra (spec) and the
;   temperature (temp) then:
;   y1 = wave_temp_correction(spec, temp)
;
; INPUTS:
;   file: The filename of an EDR file to read and process
;      Expected filename format: ?????????????EDR*.DAT
;      (if file is provided, it is not necessary to give temp)
;   spec: The spectrum or spectra to correct (temp must also be provided)
;      Expected format: [3, 2048] or [3, ns, 2048], where ns is the
;      number of spectra
;   temp: The Body Unit Spectrometer A temperature in Celsius (BU_SPECT_A)
;
; OTHER LIBRARY FILES:
;   Tlinreg.sav: Matrix of correction factors (IDL save file)
;      returns coef, which include the intercept and the linear
;      regression coefficient that gives the shift in fraction of
;      channels as a function of temperature. There are 6144
;      regressions, i.e. per wavelength channel.
;
; KEYWORD PARAMETERS:
;   split: return a 3D array for the 3 wavelength ranges
;      (default is to return UV, VIS, and VNIR in 1D)
;
; OUTPUTS:
;   y1: corrected spectra in wavelength channel
;      If the input has the default dimension [3, ns, 2048], where
;      ns=number of spectra, then the default output will be [ns,
;      6144]. If the input has a single spectrum, i.e. [3, 2048], then
;      the default output is [6144]. If the /split keyword is used,
;      then the outputs will have the same dimensions as the input.
;
; RESTRICTIONS:
;
;
;
; PROCEDURE:
;   Read the spectra and the temperature.
;   Reform the dimensions over 6144 channels.
;   Restore the matrix of correction factors.
;   Compute the expected channel drift for the temperature read in the
;      file for each of the 6144 channels.
;   Loop on the spectra (if several) and on the spectral ranges
;   Increase in size of the arrays by the maximum shift plus 2 pixels
;      for the spline function, by repeating the first and last
;      intensity of each spectral end and by increasing monitically
;      the pixel index.
;   Resample each spectrum on the regular channel array of reference
;      (spline interpolation), i.e. would be indentical if the drift
;      was null.
;   Optionally reform the output to the original dimensions.
;   Return the corrected spectra.
;
; MODIFICATION HISTORY:
;   2012.12.06: Agnes Cousin, Jeremie Lasue, Olivier Gasnault - IRAP
;   2012.12.10: OlivierG: accept both file and spectrum inputs
;   2012.12.11: OlivierG: process spectral ranges separately
;                         reduce border effects in interpolation
;   2014.11.14 Ryan Anderson - Translated to Python
;
;-
"""
from scipy.io.idl import readsav
import numpy
import scipy
import matplotlib.pyplot as plot

def ccam_wave_temp_correction(in_spect,temp,split,corr_matrix_path='Tlinreg.sav'):
    Tlinreg=readsav(corr_matrix_path,python_dict=True)
    Tlinreg=Tlinreg['coef']
    mfs=Tlinreg[:,0]+Tlinreg[:,1]*temp
    xout=numpy.arange(len(mfs))
    xin=xout+mfs
    sz=in_spect.shape
    if sz[0]!=3: print 'Unexpected # of spectral ranges!'
    if len(sz)==2:
        if 3*sz[1]!=6144: print 'Unexpected # of wavelengths!'
        tmp=numpy.reshape(in_spect,6144)
        y1=numpy.zeros(6144)
        #resample each spectral range and avoid border effects
        for s in range(3):
            v1=tmp[2048*s:(2048*s+2048)]
            v2=xin[2048*s:(2048*s+2048)]
            v3=xout[2048*s:(2048*s+2048)]
            rep=round(max(abs(v3-v2)))+2 #define border margins
            v1=numpy.concatenate([numpy.full(rep,v1[0]),v1,numpy.full(rep,v1[2047])])
            reprange=numpy.arange(int(rep))+1
            v2=numpy.concatenate([v2[0]-reprange[::-1],v2,v2[2047]+reprange])
            v3=numpy.concatenate([v3[0]-reprange[::-1],v3,v3[2047]+reprange])
            interpfunc=scipy.interpolate.InterpolatedUnivariateSpline(v2,v1,k=3)
            y1[2048*s:(2048*s+2048)]=interpfunc(v3)[rep:(-rep)]
            
        if split==True: return y1[0:2048],y1[2048:4096],y1[4096:]
        if split==False: return y1      
    if len(sz)==3:
        if 3*sz[1]!=6144: print 'Unexpected # of wavelengths!'
        tmp=numpy.reshape(in_spect,[sz[2],6144])
        y1=numpy.zeros([sz[2],6144])
        for n in range(sz[2]):
            for s in range(3):
                v1=tmp[n,2048*s:(2048*s+2048)]
                v2=xin[2048*s:(2048*s+2048)]
                v3=xout[2048*s:(2048*s+2048)]
                rep=round(max(abs(v3-v2)))+2
                v1=numpy.concatenate([numpy.full(rep,v1[0]),v1,numpy.full(rep,v1[2047])])
                reprange=numpy.arange(int(rep))+1
                v2=numpy.concatenate([v2[0]-reprange[::-1],v2,v2[2047]+reprange])
                v3=numpy.concatenate([v3[0]-reprange[::-1],v3,v3[2047]+reprange])
                interpfunc=scipy.interpolate.InterpolatedUnivariateSpline(v2,v1,k=3)
                y1[n,2048*s:(2048*s+2048)]=interpfunc(v3)[rep:(-rep)]

        if split==True: return y1[:,0:2048],y1[:,2048:4096],y1[:,4096:]
        if split==False: return y1
        

        
        