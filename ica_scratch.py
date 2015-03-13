# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 10:31:21 2015

@author: rbanderson
"""
import ccam
import numpy
ica_db_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\ICA_1500mm_db.csv'
uni_db_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Univariate_1500mm_db.csv'

dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\DataProcessing\\Working\\Input\\full_db_mars_corrected.csv'

which_elem='K2O'


ica_db=ccam.read_csv_cols(ica_db_file,0,labelrow=False)

targetnames=numpy.array(ica_db[0],dtype='string')
Si_scores=numpy.array(ica_db[1],dtype='float')
Ti_scores=numpy.array(ica_db[2],dtype='float')
Al_scores=numpy.array(ica_db[3],dtype='float')
Fe_scores=numpy.array(ica_db[4],dtype='float')
Mg_scores=numpy.array(ica_db[5],dtype='float')
Ca_scores=numpy.array(ica_db[6],dtype='float')
Na_scores=numpy.array(ica_db[7],dtype='float')
K_scores=numpy.array(ica_db[8],dtype='float')

ICA_MgO=0.2943*numpy.exp(8.5948*Mg_scores)

uni_db=ccam.read_csv_cols(uni_db_file,1,labelrow=False)
uni_targetnames=numpy.array(uni_db[0],dtype='string')

Na589_areas=numpy.array(uni_db[1],dtype='float')
Na818_areas=numpy.array(uni_db[2],dtype='float')
Na819_areas=numpy.array(uni_db[3],dtype='float')
Casum_areas=numpy.array(uni_db[4],dtype='float')
Si288_areas=numpy.array(uni_db[5],dtype='float')
Sisum_areas=numpy.array(uni_db[6],dtype='float')
K766_areas=numpy.array(uni_db[7],dtype='float')
Mg285_areas=numpy.array(uni_db[8],dtype='float')
Mg448_areas=numpy.array(uni_db[9],dtype='float')
Alsum_areas=numpy.array(uni_db[10],dtype='float')
Ti335_areas=numpy.array(uni_db[11],dtype='float')
Fesum_areas=numpy.array(uni_db[12],dtype='float')

Uni_MgO=4080.43*Mg448_areas+0.35


#print 'Reading database'
#sys.stdout.flush()
#spectra,comps,spect_index,names,labels,wvl=ccam.read_db(dbfile,compcheck=True)
#oxides=labels[2:]
#compindex=numpy.where(oxides=='K2O')[0]

complist=ccam.target_comp_lookup(targetnames,dbfile,which_elem)

uni_complist=ccam.target_comp_lookup(uni_targetnames,dbfile,which_elem)

ccam.Plot1to1([complist],[K_scores],'',['K ICA Score'],['r'],['o'],r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\K_ICA_scores_vs_comp.png',yminmax=[0,numpy.max(K_scores)],xminmax=[0,20],ylabel='ICA Score',xlabel='wt.%',one_to_one=False)
ccam.Plot1to1([uni_complist],[K766_areas],'',['K 766 nm Peak Area'],['r'],['o'],r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\K_766nm_uni_areas_vs_comp.png',yminmax=[0,numpy.max(K766_areas)],xminmax=[0,20],ylabel='766 nm Peak Area',xlabel='wt.%',one_to_one=False)
#ccam.Plot1to1([uni_complist],[Uni_K2O],'',['K2O wt.%'],['r'],['o'],r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\K2O_uni_vs_comp.png',yminmax=[0,20],xminmax=[0,20],ylabel='Wt.%',xlabel='wt.%',one_to_one=True)

ccam.Plot1to1([complist],[Ti_scores],'',['Ti ICA Score'],['r'],['o'],r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Ti_ICA_scores_vs_comp.png',yminmax=[0,numpy.max(Ti_scores)],xminmax=[0,20],ylabel='ICA Score',xlabel='wt.%',one_to_one=False)
ccam.Plot1to1([uni_complist],[Ti335_areas],'',['Ti 335 nm Peak Area'],['r'],['o'],r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\Ti_335nm_uni_areas_vs_comp.png',yminmax=[0,numpy.max(Ti335_areas)],xminmax=[0,20],ylabel='335 nm Peak Area',xlabel='wt.%',one_to_one=False)

print 'stop'