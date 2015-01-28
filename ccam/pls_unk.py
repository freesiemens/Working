# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 18:43:18 2015

@author: rbanderson
"""
import numpy
import ccam
import copy
def pls_unk(unk_spectra,nc,coeff_file=None,means_file=None,beta=None,X_mean=None,Y_mean=None):

    if coeff_file!=None:
        data,cols=ccam.read_csv_cols(coeff_file,1,labelrow=True)
        cols=numpy.array(cols[1:],dtype='int')
        coeffs=numpy.array(data[1:],dtype='float')
        beta=coeffs[numpy.where(cols==nc)]
    if means_file!=None:
        data,temp=ccam.read_csv_cols(means_file,1,labelrow=False)
        Y_mean=numpy.array(temp[1],dtype='float')
        X_mean=numpy.array(data[1],dtype='float')
        
    #Important! Have to use copy here so that the original spectra in the function calling pls_unk are not changed    
    unk_spectra_centered=ccam.meancenter(copy.copy(unk_spectra),X_mean=X_mean)[0] 

    predicts=numpy.zeros(len(unk_spectra[:,0]))
    for i in range(len(predicts)):
        predicts[i]=numpy.dot(unk_spectra_centered[i,:],beta[:].T)+Y_mean

    return predicts
    