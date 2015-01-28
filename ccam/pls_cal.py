# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 10:24:05 2015

@author: rbanderson
"""
import ccam
import sys
import csv
import numpy
from sklearn.cross_decomposition import PLSRegression
import mlpy

def pls_cal(dbfile,foldfile,maskfile,outpath,which_elem,testfold,nc,normtype=3,mincomp=0,maxcomp=100,plstype='mlpy',keepfile=None,removefile=None,cal_dir=None,masterlist_file=None,compfile=None,name_sub_file=None):
    
    print 'Reading database'
    sys.stdout.flush()
    spectra,comps,spect_index,names,labels,wvl=ccam.read_db(dbfile,compcheck=True)
    oxides=labels[2:]
    compindex=numpy.where(oxides==which_elem)[0]
    
    print 'Choosing spectra'
    which_removed=outpath+which_elem+'_'+plstype+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_removed.csv'
    spectra,names,spect_index,comps=ccam.choose_spectra(spectra,spect_index,names,comps,compindex,mincomp=mincomp,maxcomp=maxcomp,keepfile=keepfile,removefile=removefile,which_removed=which_removed)
    
    print 'Masking spectra'
    spectra,wvl=ccam.mask(spectra,wvl,maskfile)
    
    print 'Normalizing spectra'
    spectra=ccam.normalize(spectra,wvl,normtype=normtype)
    
    
    print 'Assigning Folds'
    folds=ccam.folds(foldfile,names)
    names_nofold=names[(folds==0)]
    spect_index_nofold=spect_index[(folds==0)]
    #write a file containing the samples not assigned to folds
    with open(which_removed,'ab') as writefile:
        writer=csv.writer(writefile,delimiter=',',)
        for i in range(len(names_nofold)):
            writer.writerow([names_nofold[i],spect_index_nofold[i],'No Fold'])
    
    
    #remove spectra that are not assigned to a fold
    spectra=spectra[(folds!=0),:]
    spect_index=spect_index[(folds!=0)]
    names=names[(folds!=0)]
    comps=comps[(folds!=0),:]
    folds=folds[(folds!=0)]
    
    print 'Defining Training and Test Sets'
    spectra_train=spectra[(folds!=testfold)]
    spect_index_train=spect_index[(folds!=testfold)]
    names_train=names[(folds!=testfold)]
    comps_train=comps[(folds!=testfold),compindex]
    folds_train=folds[(folds!=testfold)]
    folds_train_unique=numpy.unique(folds_train)
    
    spectra_test=spectra[(folds==testfold)]
    spect_index_test=spect_index[(folds==testfold)]
    names_test=names[(folds==testfold)]
    comps_test=comps[(folds==testfold),compindex]
    folds_test=folds[(folds==testfold)]
    
    print 'Do Leave One Label Out (LOLO) cross validation with all folds but the test set'
    #define array to hold cross validation predictions and RMSEs
    train_predict_cv=numpy.zeros((len(names_train),nc))
    RMSECV=numpy.zeros(nc)
    
    for i in folds_train_unique:
        print 'Holding out fold #'+str(i)
        #mean center those spectra left in
        X_cv_in,X_cv_in_mean=ccam.meancenter(spectra_train[(folds_train!=i),:])
        #and those left out
        X_cv_out=ccam.meancenter(spectra_train[(folds_train==i),:],X_mean=X_cv_in_mean)[0]   
         
        #mean center compositions left in
        Y_cv_in,Y_cv_in_mean=ccam.meancenter(comps_train[(folds_train!=i)])
       
        #step through each number of components
        for j in range(1,nc+1):
            print 'Training PLS Model for '+str(j)+' components'
            #train the model
            if plstype=='mlpy':
                PLS1model=mlpy.pls.PLS(j)
                PLS1model.learn(X_cv_in,Y_cv_in)
                
                #predict the samples held out
                train_predict_cv[(folds_train==i),j-1]=PLS1model.pred(X_cv_out)+Y_cv_in_mean
            if plstype=='sklearn':
                PLS1model=PLSRegression(n_components=nc)
                PLS1model.fit(X_cv_in,Y_cv_in)
                train_predict_cv[(folds_train==i),j-1]=PLS1model.predict(X_cv_out)+Y_cv_in_mean
    #calculate RMSECV
    for i in range(0,nc):
        sqerr=(train_predict_cv[:,i]-comps_train)**2.0
        RMSECV[i]=numpy.sqrt(numpy.mean(sqerr))
    
    #mean center full model
    X,X_mean=ccam.meancenter(spectra_train)
    X_test=ccam.meancenter(spectra_test,X_mean=X_mean)[0]
    
    Y,Y_mean=ccam.meancenter(comps_train)
    
    #create arrays for results and RMSEs
    trainset_results=numpy.zeros((len(names_train),nc))
    testset_results=numpy.zeros((len(names_test),nc))
    RMSEP=numpy.zeros(nc)
    RMSEC=numpy.zeros(nc)
    beta=numpy.zeros((len(X_mean),nc))
       
    #Now step through each # of components with the full model
    for j in range(1,nc+1):
        print 'Training full model for '+str(j)+' components'
        if plstype=='mlpy':
            PLS1model=mlpy.pls.PLS(j)
            PLS1model.learn(X,Y)
            beta[:,j-1]=PLS1model.beta()
            trainset_results[:,j-1]=PLS1model.pred(X)+Y_mean
            testset_results[:,j-1]=PLS1model.pred(X_test)+Y_mean
        if plstype=='sklearn':
            PLS1model=PLSRegression(n_components=nc)
            PLS1model.fit(X,Y)
            print 'stop'
            
        RMSEC[j-1]=numpy.sqrt(numpy.mean((trainset_results[:,j-1]-comps_train)**2.0))
        RMSEP[j-1]=numpy.sqrt(numpy.mean((testset_results[:,j-1]-comps_test)**2.0))
    
    #if cal_dir is specified, read cal target data and calculate RMSEs    
    if cal_dir!=None:
        cal_data,cal_wvl,cal_filelist=ccam.read_ccs(cal_dir)
        cal_data,cal_wvl=ccam.mask(cal_data,cal_wvl,maskfile)
        cal_data=ccam.normalize(cal_data,cal_wvl,normtype=normtype)
        RMSEP_cal=numpy.zeros(nc)
        targets=ccam.target_lookup(cal_filelist,masterlist_file,name_sub_file)
        target_comps=ccam.target_comp_lookup(targets,compfile,which_elem)
        cal_results=numpy.zeros((len(targets),nc))
        for i in range(nc):
            cal_results[:,i]=ccam.pls_unk(cal_data,i+1,beta=beta[:,i],X_mean=X_mean,Y_mean=Y_mean)          
            RMSEP_cal[i]=numpy.sqrt(numpy.mean((cal_results[:,i]-target_comps)**2))

    # plot RMSEs
    ccam.plots.RMSE(RMSECV,RMSEP,RMSEC,which_elem+'RMSEs',outpath+which_elem+'_'+plstype+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_RMSE_plot.png',RMSEP_cal=RMSEP_cal)
    
    
   
   #Write output info to files
    
    with open(outpath+which_elem+'_'+plstype+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_RMSECV.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        writer.writerow(['NC','RMSECV (wt.%)'])            
        for i in range(0,nc):
            writer.writerow([i+1,RMSECV[i]])
    
    with open(outpath+which_elem+'_'+plstype+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_RMSEC.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        writer.writerow(['NC','RMSEC (wt.%)'])            
        for i in range(0,nc):
            writer.writerow([i+1,RMSEC[i]])
            
    with open(outpath+which_elem+'_'+plstype+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_RMSEP.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        writer.writerow(['NC','RMSEP (wt.%)'])            
        for i in range(0,nc):
            writer.writerow([i+1,RMSEP[i]])
            
    with open(outpath+which_elem+'_'+plstype+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_cv_predict.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['Sample','Spectrum','Fold','True_Comp']
        row.extend(range(1,nc+1))
        writer.writerow(row)
        for i in range(0,len(names_train)):
            row=[names_train[i],spect_index_train[i],folds_train[i],comps_train[i]]
            row.extend(train_predict_cv[i,:])
            writer.writerow(row)
    
    with open(outpath+which_elem+'_'+plstype+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_train_predict.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['Sample','Spectrum','Fold','True_Comp']
        row.extend(range(1,nc+1))
        writer.writerow(row)
        for i in range(0,len(names_train)):
            row=[names_train[i],spect_index_train[i],folds_train[i],comps_train[i]]
            row.extend(trainset_results[i,:])
            writer.writerow(row)
            
    with open(outpath+which_elem+'_'+plstype+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_test_predict.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['Sample','Spectrum','Fold','True_Comp']
        row.extend(range(1,nc+1))
        writer.writerow(row)
        for i in range(0,len(names_test)):
            row=[names_test[i],spect_index_test[i],folds_test[i],comps_test[i]]
            row.extend(testset_results[i,:])
            writer.writerow(row)
            
    with open(outpath+which_elem+'_'+plstype+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_beta_coeffs.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['wvl']
        row.extend(range(1,nc+1))
        writer.writerow(row)
        for i in range(0,len(wvl)):
            row=[wvl[i]]
            row.extend(beta[i,:])
            writer.writerow(row)        
    
    with open(outpath+which_elem+'_'+plstype+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_meancenters.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')        
        writer.writerow([which_elem+' mean',Y_mean])
        for i in range(0,len(wvl)):
            row=[wvl[i],X_mean[i]]
            writer.writerow(row)
            
    with open(outpath+which_elem+'_'+plstype+'_nc'+str(nc)+'_norm'+str(normtype)+'_'+str(mincomp)+'-'+str(maxcomp)+'_inputinfo.csv','wb') as writefile:
        writer=csv.writer(writefile,delimiter=',')        
        writer.writerow(['Spectral database =',dbfile])
        writer.writerow(['Spectra Kept =',keepfile])
        writer.writerow(['Spectra Removed =',which_removed])
        writer.writerow(['Fold Definition =',foldfile])
        writer.writerow(['Test Fold =',maskfile])
        writer.writerow(['Mask File =',maskfile])
        writer.writerow(['Algorithm =',plstype])
        writer.writerow(['# of components =',nc])
        writer.writerow(['Normalization Type =',normtype])
        writer.writerow(['Composition Min. =',mincomp])
        writer.writerow(['Composition Max. =',maxcomp])

