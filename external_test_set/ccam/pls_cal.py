# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 10:24:05 2015

@author: rbanderson

This is the PLS calibration function. It handles reading the database, removing specified spectra,
masking and normalizing, splitting into folds, defining training and test sets, and running 
k-fold cross validation. It produces lots of informative output files and plots.

Required Inputs:
dbfile = a csv file containing the combined compositional and spectral database. 
    The file should be formatted as follows:

    First row: column labels
    Column 0: Target name
    Columns 1 through 9: Major oxide composition 
                    (SiO2, TiO2, Al2O3, FeOT, MnO, MgO, CaO, Na2O, K2O)
    Columns 10 through 6153: LIBS spectrum

maskfile = A csv file specifying which parts of the spectrum to mask.
        The first row should contain column names.
        The first column should contain strings with the name of the features being masked (typically an element)
        The second column should contain the minimum wavelengths of the masked regions
        The third column should contain the maximum wavelengths of the masked regions
outpath = the full path where output files should be written.
which_elem = string specifying the name of the major oxideof interest (e.g. 'SiO2')
testfold = which fold to hold out completely and treat as a test set
nc = number of components

Optional inputs:
normtype = Which type of normalization to use. Valid options are 1 or 3. Default value is 1.
mincomp = minimum composition value of database samples to use to generate the PLS model. Default is 0.
maxcomp = maximum composition value of database samples to use to generate the PLS model. Default is 100.
plstype = choose whether to use PLS as implemented in mlpy or scikit-learn by entering 'mlpy' or 'sklearn'. Default is 'mlpy'
keepfile = Optional file listing database samples that should be kept. 
    File should have two columns. The first column should have the index of the spectrum to keep,
    (NOTE: For this file, the index should be the index into the full array of spectra, starting at 1, not the 1-5 index for each target)
    the second column should have the target names.)
removefile = Optional file specifying samples that should be removed from the database. 
    File should have two columns. The first column should have target names, the second column should have the index of the spectrum to remove.
    So, to remove the first and third spectrum of AGV2, the file would look like:
    AGV2,1
    AGV2,3
cal_dir = If you want to generate cal target RMSE curves, use this keyword to specify the directory containing the cal target CCS files.
masterlist_file = If you specify cal_dir, you must also specify a masterlist file to use. This file should be the official master list produced by CCAM
compfile = If you specify cal_dir, this file should contain the compositions of the cal targets in columns labeled with the
     oxide name. The first column should be labeled 'Name' and contain the cal target names.
     NOTE: The database file can be used for this file if it contains the cal targets.
name_sub_file = This file is used when generating cal target results to replace cal target number with the actual target name. 
    The first column should contain the target name as liste din the master list (e.g. 'Cal Target 1') 
    The second column should contain the preferred target name (e.g. 'Macusanite')
foldfile = A file specifying which fold each database sample should be assigned to. 
    The first column should be the list of target names. The second column should be the folds,
    expressed as intergers, starting with 1  
nfolds = number of folds to use if a fold file is not specified
seed = Interger to seed the random number generator used to randomly define folds. This allows random folds to be defined in a reproducible manner    
n_bag = used for bagging ensemble methods. Not fully implemented and tested yet
skscale = whether or not to scale data, used in cases where the algorithm does the scaling for you (the ensemble methods), not used for standard PLS
n_boost = used for boosting ensemble method. Not fully implemented and tested yet
max_samples = used for ensemble methods, not fully implemented and tested yet
n_elems = tells the code how many composition columns to expect before it gets to spectral data in the database file
"""

import ccam
import sys
import csv
import numpy
from sklearn.cross_decomposition import PLSRegression
import sklearn.ensemble as ensemble
import copy
import cPickle as pickle

def pls_cal(dbfile,maskfile,outpath,which_elem,testfold,nc,normtype=1,mincomp=0,maxcomp=100,plstype='mlpy',keepfile=None,removefile=None,cal_dir=None,masterlist_file=None,compfile=None,name_sub_file=None,testsetfile=None,nfolds=7,seed=None,n_bag=None,skscale=False,n_boost=None,max_samples=0.1,n_elems=9):
    plstype_string=plstype    
    if n_bag!=None:
        plstype_string=plstype+'_bag'
    if n_boost!=None:
        plstype_string=plstype+'_boost'
    if skscale==True:
        plstype_string=plstype+'_scale'
    print 'Reading database'
    sys.stdout.flush()
    spectra,comps,spect_index,names,labels,wvl=ccam.read_db(dbfile,compcheck=True,n_elems=n_elems)
    oxides=labels[2:]
    compindex=numpy.where(oxides==which_elem)[0]
    
    print 'Choosing spectra'
    
    which_removed=outpath+which_elem+'_'+plstype_string+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_removed.csv'
    spectra,names,spect_index,comps=ccam.choose_spectra(spectra,spect_index,names,comps,compindex,mincomp=mincomp,maxcomp=maxcomp,keepfile=keepfile,removefile=removefile,which_removed=which_removed)
        
    
    print 'Masking spectra'
    spectra,wvl=ccam.mask(spectra,wvl,maskfile)
    
    print 'Normalizing spectra'
    spectra=ccam.normalize(spectra,wvl,normtype=normtype)
    
    print 'Removing Test Set'
    if testsetfile!=None:
         f=open(testsetfile,'rb')
         data=zip(*csv.reader(f))
         
         testnames=numpy.array(data[0],dtype='string')
         testind=numpy.in1d(names,testnames)
         trainind=numpy.in1d(names,testnames,invert=True)
         names_test=names[testind]
         spectra_test=spectra[testind]
         spect_index_test=spect_index[testind]
         comps_test=comps[testind,compindex]
         
         names_train=names[trainind]
         spectra_train=spectra[trainind]
         spect_index_train=spect_index[trainind]
         names_train=names[trainind]
         comps_train=comps[trainind,compindex]
         
         
    print 'Assigning Folds'
    
        #if a fold file is specified, use it
    #    folds=ccam.folds(foldfile,names)
    #else:
        #otherwise, define random folds
    #    folds=ccam.random_folds(names,nfolds,seed=seed)

    names_unique,uniqueindex=numpy.unique(names_train,return_index=True)
    comps_unique_train=comps_train[uniqueindex]
    nfolds=5

    names_unique_sorted=names_unique[comps_unique_train.argsort()]
    folds=range(1,nfolds+1)
    while len(folds)<len(names_unique_sorted):
        folds.extend(range(1,nfolds+1))
    folds_train=numpy.zeros(len(names_train))
    for i in range(len(names_unique_sorted)):
        print names_unique_sorted[i]
        print folds[i]
        folds_train[numpy.in1d(names_train,names_unique_sorted[i])]=folds[i]

    names_nofold=names[(folds_train==0)]
    spect_index_nofold=spect_index[(folds_train==0)]
    #write a file containing the samples not assigned to folds
    with open(which_removed,'ab') as writefile:
        writer=csv.writer(writefile,delimiter=',',)
        for i in range(len(names_nofold)):
            writer.writerow([names_nofold[i],spect_index_nofold[i],'No Fold'])
    
    
    #remove spectra that are not assigned to any fold
    spectra_train=spectra_train[(folds_train!=0),:]
    spect_index_train=spect_index_train[(folds_train!=0)]
    names_train=names_train[(folds_train!=0)]
    comps_train=comps_train[(folds_train!=0),:]
    folds_train=folds_train[(folds_train!=0)]
    

    
    print 'Do Leave One Label Out (LOLO) cross validation with all folds but the test set'
    #define array to hold cross validation predictions and RMSEs
    train_predict_cv=numpy.zeros((len(names_train),nc))
    RMSECV=numpy.zeros(nc)
    
    for i in range(range(nfolds))+1:
        print 'Holding out fold #'+str(i)
        
        if skscale==False:
        #mean center those spectra left in
            #X_cv_in1,X_cv_in_mean1=meancenter.ccam_meancenter(spectra_train[(folds_train!=i),:])
            X_cv_in,X_cv_in_mean=ccam.meancenter(spectra_train[(folds_train!=i),:])
            
            #and those left out
            X_cv_out=ccam.meancenter(spectra_train[(folds_train==i),:],X_mean=X_cv_in_mean)[0]   
             
            #mean center compositions left in
            Y_cv_in,Y_cv_in_mean=ccam.meancenter(comps_train[(folds_train!=i)])
        if skscale==True:
            X_cv_in=spectra_train[(folds_train!=i),:]
            X_cv_out=spectra_train[(folds_train==i),:]
            Y_cv_in=comps_train[(folds_train!=i)]
            Y_cv_in_mean=0
       
        #step through each number of components
        for j in range(1,nc+1):
            print 'Training Model for '+str(j)+' components'
            #train the model
            if plstype=='mlpy':
                PLS1model=ccam.mlpy_pls.PLS(j)
                PLS1model.learn(X_cv_in,Y_cv_in)
                    #predict the samples held out
                train_predict_cv[(folds_train==i),j-1]=PLS1model.pred(X_cv_out)+Y_cv_in_mean
                
            if plstype=='sklearn':
                PLS1model=PLSRegression(n_components=j,scale=skscale)
                if n_bag==None and n_boost==None:
                    PLS1model.fit(X_cv_in,Y_cv_in)
                    train_predict_cv[(folds_train==i),j-1]=numpy.squeeze(PLS1model.predict(X_cv_out)+Y_cv_in_mean)
                if n_bag!=None:
                    PLS1bagged=ensemble.BaggingRegressor(PLS1model,n_estimators=n_bag,max_samples=max_samples,verbose=1)
                    PLS1bagged.fit(X_cv_in,Y_cv_in)
                    train_predict_cv[(folds_train==i),j-1]=numpy.squeeze(PLS1bagged.predict(X_cv_out)+Y_cv_in_mean)
                if n_boost!=None:
                    PLS1boosted=ensemble.AdaBoostRegressor(PLS1model,n_estimators=n_boost)
                    PLS1boosted.fit(X_cv_in,Y_cv_in)
                    train_predict_cv[(folds_train==i),j-1]=numpy.squeeze(PLS1boosted.predict(X_cv_out)+Y_cv_in_mean)
    #calculate RMSECV
    for i in range(0,nc):
        sqerr=(train_predict_cv[:,i]-comps_train)**2.0
        RMSECV[i]=numpy.sqrt(numpy.mean(sqerr))
    
    #mean center full model
    if skscale==False:
        X,X_mean=ccam.meancenter(spectra_train)
        X_test=ccam.meancenter(spectra_test,X_mean=X_mean)[0]
        X_all=ccam.meancenter(spectra,X_mean=X_mean)[0]
        
        Y,Y_mean=ccam.meancenter(comps_train)
    if skscale==True:
        X=spectra_train
        X_test=spectra_test
        X_all=spectra
        Y=comps_train
        Y_mean=0
    
    #create arrays for results and RMSEs
    trainset_results=numpy.zeros((len(names_train),nc))
    testset_results=numpy.zeros((len(names_test),nc))
    results=numpy.zeros((len(names),nc))    
    
    RMSEP=numpy.zeros(nc)
    RMSEC=numpy.zeros(nc)
    beta=numpy.zeros((len(X[0,:]),nc))
    Q_res=numpy.zeros((len(X[:,0]),nc))
    T2=numpy.zeros((len(X[:,0]),nc))

    [a,evals,b]=numpy.linalg.svd(numpy.cov(numpy.dot(X,X.transpose())))
    evals=numpy.diag(evals**2)
    if cal_dir!=None:
        print 'Reading cal target data'
        cal_data,cal_wvl,cal_filelist=ccam.read_ccs(cal_dir)
        cal_data,cal_wvl=ccam.mask(cal_data,cal_wvl,maskfile)
        cal_data=ccam.normalize(cal_data,cal_wvl,normtype=normtype)
        if skscale==True:
            cal_data_centered=cal_data
        if skscale==False:
            cal_data_centered=ccam.meancenter(cal_data,X_mean=X_mean)[0]

            
        RMSEP_cal=numpy.zeros(nc)
        RMSEP_cal_good=numpy.zeros(nc)        
        RMSEP_KGAMEDS=numpy.zeros(nc)
        RMSEP_MACUSANITE=numpy.zeros(nc)
        RMSEP_NAU2HIS=numpy.zeros(nc)
        RMSEP_NAU2LOS=numpy.zeros(nc)
        RMSEP_NAU2MEDS=numpy.zeros(nc)
        RMSEP_NORITE=numpy.zeros(nc)
        RMSEP_PICRITE=numpy.zeros(nc)
        RMSEP_SHERGOTTITE=numpy.zeros(nc)
        
        targets,dists,amps,nshots=ccam.target_lookup(cal_filelist,masterlist_file,name_sub_file)
        target_comps=ccam.target_comp_lookup(targets,compfile,which_elem)
        cal_results=numpy.zeros((len(targets),nc))
       
    model_list=[]
    #Now step through each # of components with the full model
    for j in range(1,nc+1):
        print 'Training full model for '+str(j)+' components'
        if plstype=='mlpy':
        
            PLS1model=ccam.mlpy_pls.PLS(j)
            PLS1model.learn(X,Y)
            beta[:,j-1]=PLS1model.beta()
            model_list.append([PLS1model])
            trainset_results[:,j-1]=PLS1model.pred(X)+Y_mean
            testset_results[:,j-1]=PLS1model.pred(X_test)+Y_mean
            results[:,j-1]=PLS1model.pred(X_all)+Y_mean
            if cal_dir != None:
                comps_copy=copy.copy(target_comps)
#                if skscale==True:
#                    cal_results[:,j-1]=PLS1model.pred(cal_data)
#                if skscale==False:
                cal_results[:,j-1]=PLS1model.pred(cal_data_centered)+Y_mean
                RMSEP_KGAMEDS[j-1],RMSEP_MACUSANITE[j-1],RMSEP_NAU2HIS[j-1],RMSEP_NAU2LOS[j-1],RMSEP_NAU2MEDS[j-1],RMSEP_NORITE[j-1],RMSEP_PICRITE[j-1],RMSEP_SHERGOTTITE[j-1],RMSEP_cal_good[j-1]=cal_rmses(targets,nc,target_comps,j,cal_data_centered,Y_mean,mincomp,maxcomp,cal_results)
   


        if plstype=='sklearn':
            PLS1model=PLSRegression(n_components=j,scale=skscale)

            if n_bag==None and n_boost==None:
                PLS1model.fit(X,Y)
                T=PLS1model.x_scores_
                #There's probably a more efficient way to calculate T2...
                for k in range(len(X[:,0])):
                    T2[k,j-1]=numpy.dot(T[k,:],numpy.dot(numpy.linalg.inv(numpy.dot(T.transpose(),T)),T[k,:]))
                
                E=X-numpy.dot(PLS1model.x_scores_,PLS1model.x_loadings_.transpose())
                Q_res[:,j-1]=numpy.dot(E,E.transpose()).diagonal()
                
                trainset_results[:,j-1]=numpy.squeeze(PLS1model.predict(X)+Y_mean)
                testset_results[:,j-1]=numpy.squeeze(PLS1model.predict(X_test)+Y_mean)
                results[:,j-1]=numpy.squeeze(PLS1model.predict(X_all)+Y_mean)
                beta[:,j-1]=numpy.squeeze(PLS1model.coefs)
                model_list.append([PLS1model])

                    
                if cal_dir != None:
                    comps_copy=copy.copy(target_comps)
                    cal_results[:,j-1]=numpy.squeeze(PLS1model.predict(cal_data_centered)+Y_mean)
                    RMSEP_KGAMEDS[j-1],RMSEP_MACUSANITE[j-1],RMSEP_NAU2HIS[j-1],RMSEP_NAU2LOS[j-1],RMSEP_NAU2MEDS[j-1],RMSEP_NORITE[j-1],RMSEP_PICRITE[j-1],RMSEP_SHERGOTTITE[j-1],RMSEP_cal_good[j-1]=cal_rmses(targets,nc,target_comps,j,cal_data_centered,Y_mean,mincomp,maxcomp,cal_results)
   
            if n_bag!=None:
                PLS1bagged=ensemble.BaggingRegressor(PLS1model,n_estimators=n_bag,max_samples=max_samples,verbose=1)
                PLS1bagged.fit(X,Y)
                trainset_results[:,j-1]=numpy.squeeze(PLS1bagged.predict(X)+Y_mean)
                testset_results[:,j-1]=numpy.squeeze(PLS1bagged.predict(X_test)+Y_mean)
                results[:,j-1]=numpy.squeeze(PLS1bagged.predict(X_all)+Y_mean)
                beta[:,j-1]=None
                model_list.append([PLS1bagged])
                if cal_dir != None:
                    comps_copy=copy.copy(target_comps)
                    cal_results[:,j-1]=numpy.squeeze(PLS1bagged.predict(cal_data_centered)+Y_mean)
                    RMSEP_KGAMEDS[j-1],RMSEP_MACUSANITE[j-1],RMSEP_NAU2HIS[j-1],RMSEP_NAU2LOS[j-1],RMSEP_NAU2MEDS[j-1],RMSEP_NORITE[j-1],RMSEP_PICRITE[j-1],RMSEP_SHERGOTTITE[j-1],RMSEP_cal_good[j-1]=cal_rmses(targets,nc,target_comps,j,cal_data_centered,Y_mean,mincomp,maxcomp,cal_results)
            if n_boost!=None:
                PLS1boosted=ensemble.AdaBoostRegressor(PLS1model,n_estimators=n_boost)
                PLS1boosted.fit(X,Y)
                trainset_results[:,j-1]=numpy.squeeze(PLS1boosted.predict(X)+Y_mean)
                testset_results[:,j-1]=numpy.squeeze(PLS1boosted.predict(X_test)+Y_mean)
                results[:,j-1]=numpy.squeeze(PLS1boosted.predict(X_all)+Y_mean)
                beta[:,j-1]=None
                model_list.append([PLS1boosted])
                if cal_dir != None:
                    comps_copy=copy.copy(target_comps)
                    cal_results[:,j-1]=numpy.squeeze(PLS1boosted.predict(cal_data_centered)+Y_mean)
                    RMSEP_KGAMEDS[j-1],RMSEP_MACUSANITE[j-1],RMSEP_NAU2HIS[j-1],RMSEP_NAU2LOS[j-1],RMSEP_NAU2MEDS[j-1],RMSEP_NORITE[j-1],RMSEP_PICRITE[j-1],RMSEP_SHERGOTTITE[j-1],RMSEP_cal_good[j-1]=cal_rmses(targets,nc,target_comps,j,cal_data_centered,Y_mean,mincomp,maxcomp,cal_results)
   
        RMSEC[j-1]=numpy.sqrt(numpy.mean((trainset_results[:,j-1]-comps_train)**2.0))
        RMSEP[j-1]=numpy.sqrt(numpy.mean((testset_results[:,j-1]-comps_test)**2.0))
        
   
    with open(outpath+which_elem+'_'+plstype_string+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'.pkl','wb') as picklefile:
            pickle.dump(model_list,picklefile)

 #if cal_dir is specified, read cal target data and calculate RMSEs    
    if cal_dir!=None:

        
        n_good_cal=numpy.sum(numpy.array([RMSEP_KGAMEDS,RMSEP_MACUSANITE,RMSEP_NAU2HIS,RMSEP_NAU2LOS,RMSEP_NAU2MEDS,RMSEP_NORITE,RMSEP_PICRITE,RMSEP_SHERGOTTITE])[:,0]!=0)
        print n_good_cal
        RMSEP_cal=(RMSEP_KGAMEDS+RMSEP_MACUSANITE+RMSEP_NAU2HIS+RMSEP_NAU2LOS+RMSEP_NAU2MEDS+RMSEP_NORITE+RMSEP_PICRITE+RMSEP_SHERGOTTITE)/n_good_cal
        RMSEP_single_cals=[RMSEP_KGAMEDS,RMSEP_MACUSANITE,RMSEP_NAU2HIS,RMSEP_NAU2LOS,RMSEP_NAU2MEDS,RMSEP_NORITE,RMSEP_PICRITE,RMSEP_SHERGOTTITE,RMSEP_cal]            
                       
        with open(outpath+which_elem+'_'+plstype_string+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_caltargets_predict.csv','wb') as writefile:
            writer=csv.writer(writefile,delimiter=',')
            row=['File','Target','Laser Energy','True_Comp']
            row.extend(range(1,nc+1))
            writer.writerow(row)
            for i in range(0,len(targets)):
                row=[cal_filelist[i],targets[i],amps[i],target_comps[i]]
                row.extend(cal_results[i,:])
                writer.writerow(row)
        with open(outpath+which_elem+'_'+plstype_string+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_RMSEP_caltargets.csv','wb') as writefile:
            writer=csv.writer(writefile,delimiter=',')
            writer.writerow(['NC','RMSEP Cal Targets (wt.%)'])            
            for i in range(0,nc):
                writer.writerow([i+1,RMSEP_cal[i]])
        ccam.RMSE(RMSECV,RMSEP,RMSEC,which_elem+' RMSEs',outpath+which_elem+'_'+plstype_string+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_RMSE_plot_cal.png',RMSEP_cals=RMSEP_single_cals)
        ccam.RMSE(RMSECV,RMSEP,RMSEC,which_elem+' RMSEs',outpath+which_elem+'_'+plstype_string+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_RMSE_plot_cal_good.png',RMSEP_good=RMSEP_cal_good)
        
    # plot RMSEs
    ccam.RMSE(RMSECV,RMSEP,RMSEC,which_elem+' RMSEs',outpath+which_elem+'_'+plstype_string+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_RMSE_plot.png')
    
    
   
   #Write output info to files

    with open(outpath+which_elem+'_'+plstype_string+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_Q_res.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=["Sample","Spectrum","Fold","True Comp"]
        row.extend(range(1,nc+1))
        writer.writerow(row)        
        for i in range(0,len(names_train)):
            row=[names_train[i],spect_index_train[i],folds_train[i],comps_train[i]]
            row.extend(Q_res[i,:])
            writer.writerow(row)
    with open(outpath+which_elem+'_'+str(mincomp)+'-'+str(maxcomp)+'_quartiles.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=[which_elem]
        writer.writerow(row)
        row=['Min',numpy.percentile(comps[:,compindex],0)]
        writer.writerow(row)
        row=['1st Quartile',numpy.percentile(comps[:,compindex],25)]
        writer.writerow(row)
        row=['Median',numpy.percentile(comps[:,compindex],50)]
        writer.writerow(row)
        row=['3rd Quartile',numpy.percentile(comps[:,compindex],75)]
        writer.writerow(row)
        row=['Max',numpy.percentile(comps[:,compindex],100)]
        writer.writerow(row)

    with open(outpath+which_elem+'_'+plstype_string+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_HotellingT2.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=["Sample","Spectrum","Fold","True Comp"]
        row.extend(range(1,nc+1))
        writer.writerow(row)        
        for i in range(0,len(names_train)):
            row=[names_train[i],spect_index_train[i],folds_train[i],comps_train[i]]
            row.extend(T2[i,:])
            writer.writerow(row)
            
    with open(outpath+which_elem+'_'+plstype_string+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_RMSECV.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        writer.writerow(['NC','RMSECV (wt.%)'])            
        for i in range(0,nc):
            writer.writerow([i+1,RMSECV[i]])
    
    with open(outpath+which_elem+'_'+plstype_string+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_RMSEC.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        writer.writerow(['NC','RMSEC (wt.%)'])            
        for i in range(0,nc):
            writer.writerow([i+1,RMSEC[i]])
            
    with open(outpath+which_elem+'_'+plstype_string+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_RMSEP.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        writer.writerow(['NC','RMSEP (wt.%)'])            
        for i in range(0,nc):
            writer.writerow([i+1,RMSEP[i]])
            
    with open(outpath+which_elem+'_'+plstype_string+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_cv_predict.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['Sample','Spectrum','Fold','True_Comp']
        row.extend(range(1,nc+1))
        writer.writerow(row)
        for i in range(0,len(names_train)):
            row=[names_train[i],spect_index_train[i],folds_train[i],comps_train[i]]
            row.extend(train_predict_cv[i,:])
            writer.writerow(row)
    
    with open(outpath+which_elem+'_'+plstype_string+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_train_predict.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['Sample','Spectrum','Fold','True_Comp']
        row.extend(range(1,nc+1))
        writer.writerow(row)
        for i in range(0,len(names_train)):
            row=[names_train[i],spect_index_train[i],folds_train[i],comps_train[i]]
            row.extend(trainset_results[i,:])
            writer.writerow(row)
            
    with open(outpath+which_elem+'_'+plstype_string+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_test_predict.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['Sample','Spectrum','Fold','True_Comp']
        row.extend(range(1,nc+1))
        writer.writerow(row)
        for i in range(0,len(names_test)):
            row=[names_test[i],spect_index_test[i],folds_test[i],comps_test[i]]
            row.extend(testset_results[i,:])
            writer.writerow(row)
    
    with open(outpath+which_elem+'_'+plstype_string+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_all_predict.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['Sample','Spectrum','Fold','True_Comp']
        row.extend(range(1,nc+1))
        writer.writerow(row)
        for i in range(0,len(names)):
            row=[names[i],spect_index[i],folds[i],comps[i,compindex]]
            row.extend(results[i,:])
            writer.writerow(row)
            
    with open(outpath+which_elem+'_'+plstype_string+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_beta_coeffs.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['wvl']
        row.extend(range(1,nc+1))
        writer.writerow(row)
        for i in range(0,len(wvl)):
            row=[wvl[i]]
            row.extend(beta[i,:])
            writer.writerow(row)        
    
    if skscale==False:
        with open(outpath+which_elem+'_'+plstype_string+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_meancenters.csv','wb') as writefile:
            writer=csv.writer(writefile,delimiter=',')        
            writer.writerow([which_elem+' mean',Y_mean])
            for i in range(0,len(wvl)):
                row=[wvl[i],X_mean[i]]
                writer.writerow(row)
            
    with open(outpath+which_elem+'_'+plstype_string+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_inputinfo.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')        
        writer.writerow(['Spectral database =',dbfile])
        writer.writerow(['Spectra Kept =',keepfile])
        writer.writerow(['Spectra Removed =',which_removed])
        writer.writerow(['Fold Definition =',foldfile])
        writer.writerow(['Test Fold =',maskfile])
        writer.writerow(['Mask File =',maskfile])
        writer.writerow(['Algorithm =',plstype_string])
        writer.writerow(['# of components =',nc])
        writer.writerow(['Normalization Type =',normtype])
        writer.writerow(['Composition Min. =',mincomp])
        writer.writerow(['Composition Max. =',maxcomp])

def cal_rmses(targets,nc,target_comps,j,cal_data_centered,Y_mean,mincomp,maxcomp,cal_results):

    comps_copy=copy.copy(target_comps)
    RMSEP_KGAMEDS_temp=0
    RMSEP_MACUSANITE_temp=0
    RMSEP_NAU2HIS_temp=0
    RMSEP_NAU2LOS_temp=0
    RMSEP_NAU2MEDS_temp=0
    RMSEP_NORITE_temp=0
    RMSEP_PICRITE_temp=0
    RMSEP_SHERGOTTITE_temp=0
    RMSEP_cal_good_temp=0
    
    if numpy.any(targets=='KGAMEDS'): RMSEP_KGAMEDS_temp=numpy.sqrt(numpy.mean((cal_results[(targets=='KGAMEDS'),j-1]-comps_copy[(targets=='KGAMEDS')])**2))
    if numpy.any(targets=='MACUSANITE'): RMSEP_MACUSANITE_temp=numpy.sqrt(numpy.mean((cal_results[(targets=='MACUSANITE'),j-1]-comps_copy[(targets=='MACUSANITE')])**2))
    if numpy.any(targets=='NAU2HIS'): RMSEP_NAU2HIS_temp=numpy.sqrt(numpy.mean((cal_results[(targets=='NAU2HIS'),j-1]-comps_copy[(targets=='NAU2HIS')])**2))
    if numpy.any(targets=='NAU2LOS'): RMSEP_NAU2LOS_temp=numpy.sqrt(numpy.mean((cal_results[(targets=='NAU2LOS'),j-1]-comps_copy[(targets=='NAU2LOS')])**2))
    if numpy.any(targets=='NAU2MEDS'): RMSEP_NAU2MEDS_temp=numpy.sqrt(numpy.mean((cal_results[(targets=='NAU2MEDS'),j-1]-comps_copy[(targets=='NAU2MEDS')])**2))
    if numpy.any(targets=='NORITE'): RMSEP_NORITE_temp=numpy.sqrt(numpy.mean((cal_results[(targets=='NORITE'),j-1]-comps_copy[(targets=='NORITE')])**2))
    if numpy.any(targets=='PICRITE'): RMSEP_PICRITE_temp=numpy.sqrt(numpy.mean((cal_results[(targets=='PICRITE'),j-1]-comps_copy[(targets=='PICRITE')])**2))
    if numpy.any(targets=='SHERGOTTITE'): RMSEP_SHERGOTTITE_temp=numpy.sqrt(numpy.mean((cal_results[(targets=='SHERGOTTITE'),j-1]-comps_copy[(targets=='SHERGOTTITE')])**2))
    
    if numpy.all([numpy.any(targets=='NAU2HIS'),numpy.any(targets=='NAU2LOS'),numpy.any(targets=='NAU2MEDS'),numpy.any(targets=='NORITE'),numpy.any(targets=='PICRITE'),numpy.any(targets=='SHERGOTTITE')]): 
        RMSEP_cal_good_temp=(RMSEP_NAU2HIS_temp+RMSEP_NAU2LOS_temp+RMSEP_NAU2MEDS_temp+RMSEP_NORITE_temp+RMSEP_PICRITE_temp+RMSEP_SHERGOTTITE_temp)/6.
    else:
        print "Not all 'good' cal targets are present!!! Can't calculate RMSEP_cal_good"
        
    cal_results[(comps_copy<mincomp),j-1]=0
    cal_results[(comps_copy>maxcomp),j-1]=0
    comps_copy[(comps_copy<mincomp)]=0
    comps_copy[(comps_copy>maxcomp)]=0            
    if numpy.any(targets=='KGAMEDS'): RMSEP_KGAMEDS_temp=numpy.sqrt(numpy.mean((cal_results[(targets=='KGAMEDS'),j-1]-comps_copy[(targets=='KGAMEDS')])**2))
    if numpy.any(targets=='MACUSANITE'): RMSEP_MACUSANITE_temp=numpy.sqrt(numpy.mean((cal_results[(targets=='MACUSANITE'),j-1]-comps_copy[(targets=='MACUSANITE')])**2))
    if numpy.any(targets=='NAU2HIS'): RMSEP_NAU2HIS_temp=numpy.sqrt(numpy.mean((cal_results[(targets=='NAU2HIS'),j-1]-comps_copy[(targets=='NAU2HIS')])**2))
    if numpy.any(targets=='NAU2LOS'): RMSEP_NAU2LOS_temp=numpy.sqrt(numpy.mean((cal_results[(targets=='NAU2LOS'),j-1]-comps_copy[(targets=='NAU2LOS')])**2))
    if numpy.any(targets=='NAU2MEDS'): RMSEP_NAU2MEDS_temp=numpy.sqrt(numpy.mean((cal_results[(targets=='NAU2MEDS'),j-1]-comps_copy[(targets=='NAU2MEDS')])**2))
    if numpy.any(targets=='NORITE'): RMSEP_NORITE_temp=numpy.sqrt(numpy.mean((cal_results[(targets=='NORITE'),j-1]-comps_copy[(targets=='NORITE')])**2))
    if numpy.any(targets=='PICRITE'): RMSEP_PICRITE_temp=numpy.sqrt(numpy.mean((cal_results[(targets=='PICRITE'),j-1]-comps_copy[(targets=='PICRITE')])**2))
    if numpy.any(targets=='SHERGOTTITE'): RMSEP_SHERGOTTITE_temp=numpy.sqrt(numpy.mean((cal_results[(targets=='SHERGOTTITE'),j-1]-comps_copy[(targets=='SHERGOTTITE')])**2))
   
    return RMSEP_KGAMEDS_temp,RMSEP_MACUSANITE_temp,RMSEP_NAU2HIS_temp,RMSEP_NAU2LOS_temp,RMSEP_NAU2MEDS_temp,RMSEP_NORITE_temp,RMSEP_PICRITE_temp,RMSEP_SHERGOTTITE_temp,RMSEP_cal_good_temp