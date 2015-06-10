# -*- coding: utf-8 -*-
"""
Created on Tue Jun 02 13:56:17 2015

@author: rbanderson
"""
import ccam
import numpy

which_elem='K2O'
dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected.csv'
testfoldfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\Input\\'+which_elem+r'_sortfold_testfold.csv'
n_elems=9

spectra,comps,spect_index,names,labels,wvl=ccam.read_db(dbfile,compcheck=True,n_elems=n_elems)
oxides=labels[2:]
compindex=numpy.where(oxides==which_elem)[0]

testfold=numpy.genfromtxt(testfoldfile,delimiter=',',dtype='str')[:,0]
testfold_index=names==testfold[0]        
for i in range(1,len(testfold)):
    testfold_index=testfold_index+(names==testfold[i])
spectra_test=spectra[(testfold_index==True)]
spect_index_test=spect_index[(testfold_index==True)]
names_test=names[(testfold_index==True)]
comps_test=comps[(testfold_index==True),compindex]
#folds_test=folds[(testfold_index==True)]    
    
spectra_train=spectra[(testfold_index==False)]
spect_index_train=spect_index[(testfold_index==False)]
names_train=names[(testfold_index==False)]
comps_train=comps[(testfold_index==False),:]

print 'Min: ',numpy.percentile(comps_test,0)
print '1st Quartile: ',numpy.percentile(comps_test,25)
print 'Med: ',numpy.percentile(comps_test,50)
print '3rd Quartile: ',numpy.percentile(comps_test,75)
print 'Max: ',numpy.percentile(comps_test,100)
