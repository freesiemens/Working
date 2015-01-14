# -*- coding: utf-8 -*-
"""
Created on Fri Nov 07 12:29:20 2014

@author: rbanderson
"""

import glob
import numpy
import scipy
import ccam_remove_continuum
import ccam_denoise
from scipy.io.idl import readsav
import matplotlib.pyplot as plot

filelist=glob.glob('*.SAV')
data=readsav(filelist[0])
muv=data.muvdata
muv_orig=muv
x=numpy.arange(len(muv))

denoise_test=ccam_denoise.ccam_denoise(muv,sig=3,niter=4)
noise=muv_orig-denoise_test
print noise[10:20]
plot.figure()
plot.plot(noise)

test=ccam_remove_continuum.ccam_remove_continuum(x,muv,5,2,2)
plot.figure()
plot.plot(test)
plot.plot(muv_orig)
cont=muv_orig-test
print cont[0:20]
plot.plot(cont)
print 'foo'

