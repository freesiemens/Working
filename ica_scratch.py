# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 10:31:21 2015

@author: rbanderson
"""
import ccam
import numpy
ica_db_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\ICA_1500mm_db.csv'
uni_db_file=r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\Univariate_1500mm_db.csv'

dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\full_db_mars_corrected.csv'

which_elem='MgO'


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
#compindex=numpy.where(oxides=='MgO')[0]

complist=ccam.target_comp_lookup(targetnames,dbfile,which_elem)
uni_complist=ccam.target_comp_lookup(uni_targetnames,dbfile,which_elem)
ccam.Plot1to1([complist],[Mg_scores],'',['MgO ICA Score'],['r'],['o'],r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\MgO_ICA_scores_vs_comp.png',yminmax=[0,numpy.max(Mg_scores)],xminmax=[0,60],ylabel='ICA Score',xlabel='wt.%',one_to_one=False)
ccam.Plot1to1([uni_complist],[Mg448_areas],'',['MgO 448 nm Peak Area'],['r'],['o'],r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\MgO_448nm_uni_areas_vs_comp.png',yminmax=[0,numpy.max(Mg448_areas)],xminmax=[0,60],ylabel='448 nm Peak Area',xlabel='wt.%',one_to_one=False)
ccam.Plot1to1([uni_complist],[Mg285_areas],'',['MgO 285 nm Peak Area'],['r'],['o'],r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\MgO_285nm_uni_areas_vs_comp.png',yminmax=[0,numpy.max(Mg285_areas)],xminmax=[0,60],ylabel='285 nm Peak Area',xlabel='wt.%',one_to_one=False)
ccam.Plot1to1([uni_complist],[Uni_MgO],'',['MgO wt.%'],['r'],['o'],r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\MgO_uni_vs_comp.png',yminmax=[0,60],xminmax=[0,60],ylabel='Wt.%',xlabel='wt.%',one_to_one=True)


print 'stop'