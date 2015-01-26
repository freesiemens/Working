# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 10:24:05 2015

@author: rbanderson
"""
import ccam_read_db as read_db
import ccam_mask as mask
import ccam_normalize as normalize
import ccam_choose_spectra as choose_spectra
import ccam_folds as folds
import ccam_meancenter as meancenter
import sys
import csv
import numpy
import sklearn
import mlpy

#nooutliers='C:\\Users\\rbanderson\\IDLWorkspace82\\PLS1_fold\\database_input\\goodcomps_20130328_noduplicates_indexed Outliers.csv'
#f=open(nooutliers,'rb')
#labels=f.readline()
#nooutlier_data=zip(*csv.reader(f))
#nooutlier_names_SiO2=numpy.array(nooutlier_data[0])
#nooutlier_names_TiO2=numpy.array(nooutlier_data[2])
#nooutlier_names_Al2O3=numpy.array(nooutlier_data[4])
#nooutlier_names_FeOT=numpy.array(nooutlier_data[6])
#nooutlier_names_MnO=numpy.array(nooutlier_data[8])
#nooutlier_names_MgO=numpy.array(nooutlier_data[10])
#nooutlier_names_CaO=numpy.array(nooutlier_data[12])
#nooutlier_names_Na2O=numpy.array(nooutlier_data[14])
#nooutlier_names_K2O=numpy.array(nooutlier_data[16])
#
#nooutlier_indices_SiO2=numpy.array(nooutlier_data[1])
#nooutlier_indices_TiO2=numpy.array(nooutlier_data[3])
#nooutlier_indices_Al2O3=numpy.array(nooutlier_data[5])
#nooutlier_indices_FeOT=numpy.array(nooutlier_data[7])
#nooutlier_indices_MnO=numpy.array(nooutlier_data[9])
#nooutlier_indices_MgO=numpy.array(nooutlier_data[11])
#nooutlier_indices_CaO=numpy.array(nooutlier_data[13])
#nooutlier_indices_Na2O=numpy.array(nooutlier_data[15])
#nooutlier_indices_K2O=numpy.array(nooutlier_data[17])
#
#nooutlier_indices_SiO2=numpy.array(nooutlier_indices_SiO2[nooutlier_indices_SiO2!=''],dtype='int')
#nooutlier_names_SiO2=nooutlier_names_SiO2[nooutlier_names_SiO2!='']
#
#
#nooutlier_names=numpy.hstack((numpy.array(nooutlier_data[0]),numpy.array(nooutlier_data[2]),numpy.array(nooutlier_data[4]),numpy.array(nooutlier_data[6]),numpy.array(nooutlier_data[8]),numpy.array(nooutlier_data[10]),numpy.array(nooutlier_data[12]),numpy.array(nooutlier_data[14]),numpy.array(nooutlier_data[16])))
#nooutlier_indices=numpy.hstack((numpy.array(nooutlier_data[1]),numpy.array(nooutlier_data[3]),numpy.array(nooutlier_data[5]),numpy.array(nooutlier_data[7]),numpy.array(nooutlier_data[9]),numpy.array(nooutlier_data[11]),numpy.array(nooutlier_data[13]),numpy.array(nooutlier_data[15]),numpy.array(nooutlier_data[17])))
#nooutlier_combined=numpy.core.defchararray.add(nooutlier_names,nooutlier_indices)
#
#yesoutliers='C:\\Users\\rbanderson\\IDLWorkspace82\\PLS1_fold\\database_input\\goodcomps_20130328_noduplicates_indexed.csv'
#f=open(yesoutliers,'rb')
#yesoutlier_data=zip(*csv.reader(f))
#yesoutlier_names=numpy.hstack((numpy.array(yesoutlier_data[0]),numpy.array(yesoutlier_data[2]),numpy.array(yesoutlier_data[4]),numpy.array(yesoutlier_data[6]),numpy.array(yesoutlier_data[8]),numpy.array(yesoutlier_data[10]),numpy.array(yesoutlier_data[12]),numpy.array(yesoutlier_data[14]),numpy.array(yesoutlier_data[16])))
#yesoutlier_indices=numpy.hstack((numpy.array(yesoutlier_data[1]),numpy.array(yesoutlier_data[3]),numpy.array(yesoutlier_data[5]),numpy.array(yesoutlier_data[7]),numpy.array(yesoutlier_data[9]),numpy.array(yesoutlier_data[11]),numpy.array(yesoutlier_data[13]),numpy.array(yesoutlier_data[15]),numpy.array(yesoutlier_data[17])))
#yesoutlier_combined=numpy.core.defchararray.add(yesoutlier_names,yesoutlier_indices)
#
#yesoutlier_names_uniq=numpy.unique(yesoutlier_names)
#nooutlier_names_uniq=numpy.unique(nooutlier_names)

dbfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\full_db_mars_corrected.csv'
#removelist='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\removelist.csv'
#removedfile='removed_test.csv'
foldfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\folds.csv'
maskfile='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\mask_minors_noise.csv'
keeplist='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Input\\Si_full_included.csv'
outpath='C:\\Users\\rbanderson\\Documents\\MSL\\ChemCam\\Data Processing\\Working\\Output\\'


normtype=3
which_elem='SiO2'
testfold=2
nc=5

print 'Reading database'
sys.stdout.flush()
spectra,comps,spect_index,names,labels,wvl=read_db.ccam_read_db(dbfile,compcheck=True)
oxides=labels[2:]
compindex=numpy.where(oxides==which_elem)[0]

#SiO2_keepcheck=numpy.empty(len(names),dtype='bool')
#for i in range(len(names)):
#   
#    
#    matchnames=numpy.in1d(nooutlier_names_SiO2,names[i])  #Is this sample in the goodcomps file?
#    if max(matchnames)==True:
#        matchindex=numpy.in1d(nooutlier_indices_SiO2[matchnames],spect_index[i])
#        if max(matchindex)==True: 
#            SiO2_keepcheck[i]=True
#                        
#            #print names[i],spect_index[i],'Keep'
#
#        if max(matchindex)!=True:
#            print names[i],spect_index[i],'Discard'
#    if max(matchnames)!=True:
#        print names[i],spect_index[i],'Sample not found at all!'
#            
#        
#print 'stop'



print 'Masking spectra'
spectra_masked,wvl_masked=mask.ccam_mask(spectra,wvl,maskfile)

print 'Normalizing spectra'
spectra_norm=normalize.ccam_normalize(spectra_masked,wvl_masked,normtype=normtype)

print 'Choosing spectra'
spectra_keep,names_keep,spect_index_keep,comps_keep=choose_spectra.ccam_choose_spectra(spectra_norm,spect_index,names,comps,compindex,mincomp=0,maxcomp=100,keeplist=keeplist)

print 'Assigning Folds'
folds=folds.ccam_folds(foldfile,names_keep)
#remove spectra that are not assigned to a fold
spectra_keep=spectra_keep[(folds!=0),:]
spect_index_keep=spect_index_keep[(folds!=0)]
names_keep=names_keep[(folds!=0)]
comps_keep=comps_keep[(folds!=0),:]
folds=folds[(folds!=0)]

print 'Defining Training and Test Sets'
spectra_train=spectra_keep[(folds!=testfold)]
spect_index_train=spect_index_keep[(folds!=testfold)]
names_train=names_keep[(folds!=testfold)]
comps_train=comps_keep[(folds!=testfold),compindex]
folds_train=folds[(folds!=testfold)]
folds_train_unique=numpy.unique(folds_train)

spectra_test=spectra_keep[(folds==testfold)]
spect_index_test=spect_index_keep[(folds==testfold)]
names_test=names_keep[(folds==testfold)]
comps_test=comps_keep[(folds==testfold),compindex]


print 'Do Leave One Label Out (LOLO) cross validation with all folds but the test set'
#define array to hold cross validation predictions and RMSEs
train_predict_cv=numpy.zeros((len(names_train),nc))
RMSECV=numpy.zeros(nc)

for i in folds_train_unique:
    print 'Holding out fold #'+str(i)
    #mean center those spectra left in
    X_cv_in,X_cv_in_mean=meancenter.ccam_meancenter(spectra_train[(folds_train!=i),:])
    #and those left out
    X_cv_out=meancenter.ccam_meancenter(spectra_train[(folds_train==i),:],X_mean=X_cv_in_mean)[0]   
     
    #mean center compositions left in
    Y_cv_in,Y_cv_in_mean=meancenter.ccam_meancenter(comps_train[(folds_train!=i)])
   
    #step through each number of components
    for j in range(1,nc+1):
        print 'Training PLS Model for '+str(j)+' components'
        #train the model
        PLS1model=mlpy.pls.PLS(j)
        PLS1model.learn(X_cv_in,Y_cv_in)
        
        #predict the samples held out
        train_predict_cv[(folds_train==i),j-1]=PLS1model.pred(X_cv_out)+Y_cv_in_mean
        
#calculate RMSECV
for i in range(0,nc):
    sqerr=(train_predict_cv[:,i]-comps_train)**2.0
    RMSECV[i]=numpy.sqrt(numpy.mean(sqerr))

#mean center full model
X,X_mean=meancenter.ccam_meancenter(spectra_train)
X_test=meancenter.ccam_meancenter(spectra_keep[(folds==testfold),:],X_mean=X_mean)[0]

Y,Y_mean=meancenter.ccam_meancenter(comps_train)

#create arrays for results and RMSEs
trainset_results=numpy.zeros((len(names_train),nc))
testset_results=numpy.zeros((len(names_test),nc))
RMSEP=numpy.zeros(nc)
RMSEC=numpy.zeros(nc)
beta=numpy.zeros((len(X_mean),nc))
   
#Now step through each # of components with the full model
for j in range(1,nc+1):
    print 'Training full model for '+str(j)+' components'
    PLS1model=mlpy.pls.PLS(j)
    PLS1model.learn(X,Y)
    beta[:,j-1]=PLS1model.beta()
    trainset_results[:,j-1]=PLS1model.pred(X)+Y_mean
    testset_results[:,j-1]=PLS1model.pred(X_test)+Y_mean
    RMSEP[j-1]=numpy.sqrt(numpy.mean((trainset_results[:,j-1]-comps_train)**2.0))
    RMSEC[j-1]=numpy.sqrt(numpy.mean((testset_results[:,j-1]-comps_test)**2.0))

#Write output info to files

with open(outpath+which_elem+'_RMSECV.csv','wb') as writefile:
    writer=csv.writer(writefile,delimiter=',',)
    writer.writerow(['NC','RMSECV (wt.%)'])            
    for i in range(0,nc):
        writer.writerow([i+1,RMSECV[i]])

with open(outpath+which_elem+'_RMSEC.csv','wb') as writefile:
    writer=csv.writer(writefile,delimiter=',',)
    writer.writerow(['NC','RMSEC (wt.%)'])            
    for i in range(0,nc):
        writer.writerow([i+1,RMSEC[i]])
        
with open(outpath+which_elem+'_RMSEP.csv','wb') as writefile:
    writer=csv.writer(writefile,delimiter=',',)
    writer.writerow(['NC','RMSEP (wt.%)'])            
    for i in range(0,nc):
        writer.writerow([i+1,RMSEP[i]])
        
with open(outpath+which_elem+'_cv_predict.csv','wb') as writefile:
    writer=csv.writer(writefile,delimiter=',',)
    row=['Sample','True_Comp']
    row.extend(range(1,nc+1))
    writer.writerow(row)
    for i in range(0,len(names_train)):
        row=[names_train[i],comps_train[i]]
        row.extend(train_predict_cv[i,:])
        writer.writerow(row)

with open(outpath+which_elem+'_train_predict.csv','wb') as writefile:
    writer=csv.writer(writefile,delimiter=',',)
    row=['Sample','True_Comp']
    row.extend(range(1,nc+1))
    writer.writerow(row)
    for i in range(0,len(names_train)):
        row=[names_train[i],comps_train[i]]
        row.extend(trainset_results[i,:])
        writer.writerow(row)
        
with open(outpath+which_elem+'_test_predict.csv','wb') as writefile:
    writer=csv.writer(writefile,delimiter=',',)
    row=['Sample','True_Comp']
    row.extend(range(1,nc+1))
    writer.writerow(row)
    for i in range(0,len(names_keep[(folds==testfold)])):
        row=[names_test[i],comps_test[i]]
        row.extend(testset_results[i,:])
        writer.writerow(row)
        
print 'Stop'

