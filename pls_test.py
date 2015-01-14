
import numpy
from sklearn.metrics import mean_squared_error
from sklearn.cross_decomposition import PLSRegression
from scipy.io.idl import readsav
import csv
import matplotlib.pyplot as plot
import pickle

#db_spectra=genfromtxt(r'C:\Users\rbanderson\Documents\MSL\ChemCam\PDL\PL'
#'S\PLS1_20130829\database_input\cleanroom_3m_recal_newir.csv',delimiter=',')


db=readsav(r'C:\Users\rbanderson\IDLWorkspace82\PLS1_fold\database_input\Spectra_1600mm_LANL_indexed.sav')
db_spectra=db['database_spectra'][0][0]
db_std=db['database_spectra'][0][1]
wave=db['database_spectra'][0][2]
db_spect_index=numpy.array((db['database_spectra'][0][3]),dtype='int')

db_std_index=db_std+numpy.array(db_spect_index,dtype='string')


db_comps=readsav(r'C:\Users\rbanderson\IDLWorkspace82\PLS1_fold\database_input\database_comps_majors_20140304.sav')
db_comp_names=db_comps['ccam_std'][0][0]
db_ox_comp=db_comps['ccam_std'][0][1]
db_ox_list=db_comps['ccam_std'][0][2]


#wave=genfromtxt(r'C:\Users\rbanderson\Documents\MSL\ChemCam\PDL\PLS\PLS1'
#'_20130829\database_input\cleanroom_3m_recal_newir_wave.csv')
#
#db_spectra_names=genfromtxt(r'C:\Users\rbanderson\Documents\MSL\ChemCam'
#'\PDL\PLS\PLS1_20130829\database_input\cleanroom_3m_recal_newir_stds.csv',
#dtype='string')
#
#db_comps=genfromtxt(r'C:\Users\rbanderson\Documents\MSL\ChemCam\PDL\PLS'
#'\PLS1_20130829\database_input\ccam_compo_db_20121026.csv',delimiter=',',
#dtype='string')

goodcomps=numpy.genfromtxt(r'C:\Users\rbanderson\IDLWorkspace82\PLS1_fold\database_input\goodcomps_20130328_noduplicates_indexed Outliers.csv',delimiter=',',
dtype='string')

fold=numpy.genfromtxt(r'C:\Users\rbanderson\IDLWorkspace82\PLS1_fold\database_input\best_outlier_split_apxs_moved.csv',delimiter=',',dtype='string')
fold_labels=filter(None,numpy.reshape(numpy.transpose(fold),fold.size))
fold_labels=numpy.vstack((fold_labels,fold_labels))

for i in range(fold.shape[1]):
    fold_match=numpy.where(numpy.in1d(fold_labels[0,:],fold[:,i]))
    fold_labels[1,fold_match]=str(i)

   

#nc=numpy.genfromtxt(r'C:\Users\rbanderson\Documents\MSL\ChemCam\PDL\PLS\PLS1_2'
#'0130829\database_input\PLS1_nc_20130829.csv',delimiter=',',dtype='string')
#nc=nc[:,1]
#nc=nc.astype(int)
nc=15
#Define the mask
mask=numpy.genfromtxt(r'C:\Users\rbanderson\Documents\MSL\ChemCam\PDL\PLS\PLS1'
'_20130829\database_input\PLSmask_minor_noise.csv',delimiter=',',
dtype='string')
#normval=numpy.genfromtxt(r'C:\Users\rbanderson\Documents\MSL\ChemCam\PDL\PLS\PLS1_20130829\database_input\normfile_20130829.txt',delimiter=' ',dtype='string')
#normval=normval[:,1]
#normval=normval.astype(float)

mask_mins=mask[1:,2]
mask_maxs=mask[1:,3]
mask_mins=mask_mins.astype(float)
mask_maxs=mask_maxs.astype(float)
maskbool=numpy.ones(len(wave))
fullspect_index=numpy.arange(6144)
for i in range(len(mask_mins)):
    #print(i)
    #print(mask_mins[i])
    maskbool[numpy.where((fullspect_index>=mask_mins[i])&(fullspect_index<=
        mask_maxs[i]))]=0
# Apply the mask    
wave_mask=wave[numpy.where(maskbool>0)]
db_spectra_mask=numpy.squeeze(db_spectra[numpy.where(maskbool>0),:])


#normalize masked spectra
fullspect_masked_index=numpy.arange(len(wave_mask))
UVindex=fullspect_masked_index[numpy.where(wave_mask<340)]
VISindex=fullspect_masked_index[numpy.where((wave_mask>380)&(wave_mask<480))]
VNIRindex=fullspect_masked_index[numpy.where(wave_mask>490)]

db_spectra_mask_norm1=numpy.zeros(db_spectra_mask.shape)
#db_spectra_mask_norm3=numpy.zeros(db_spectra_mask.shape)
for i in range(len(db_spectra_mask[0,:])):
    db_spectra_mask_norm1[:,i]=db_spectra_mask[:,i]/sum(db_spectra_mask[:,i])
#    db_spectra_mask_norm3[UVindex,i]=(db_spectra_mask[UVindex,i]/
#        sum(db_spectra_mask[UVindex,i]))
#    db_spectra_mask_norm3[VISindex,i]=(db_spectra_mask[VISindex,i]/
#        sum(db_spectra_mask[VISindex,i]))
#    db_spectra_mask_norm3[VNIRindex,i]=(db_spectra_mask[VNIRindex,i]/
#        sum(db_spectra_mask[VNIRindex,i]))
  
#RMSEP=numpy.zeros((len(nc)))

RMSE_train_file=open('RMSE_train.csv','wb')
RMSE_test_file=open('RMSE_test.csv','wb')
RMSE_train=numpy.zeros([nc,len(db_ox_list)])
RMSE_test=numpy.zeros([nc,len(db_ox_list)])
#loop through each major element
for i in range(len(db_ox_list)):
    print db_ox_list[i]
    ii=i*2

#    
    goodcomps_std=numpy.array(filter(None,goodcomps[1:,ii]))
    goodcomps_index=numpy.array(filter(None,goodcomps[1:,ii+1]))
    
    goodcomps_folds=numpy.empty(len(goodcomps_std),dtype='int')
    for j in range(len(goodcomps_folds)):
     
        #print j
        foldmatch=numpy.where(fold_labels[0,:]==goodcomps_std[j])
        if len(foldmatch[0]) != 0:
            goodcomps_folds[j]=fold_labels[1,(numpy.where(fold_labels[0,:]==goodcomps_std[j]))[0][0]]
        else:
            goodcomps_folds[j]=999
    #goodcomps_folds=fold_labels[,1]
    match=numpy.where(goodcomps_folds!=999)
    goodcomps_std=goodcomps_std[numpy.where(goodcomps_folds!=999)]
    goodcomps_index=goodcomps_index[numpy.where(goodcomps_folds!=999)]
    goodcomps_folds=goodcomps_folds[numpy.where(goodcomps_folds!=999)]
    goodcomps_std_index=numpy.array([goodcomps_std[n]+goodcomps_index[n] for n in range(len(goodcomps_index))])
    
    keepindex=(numpy.where(numpy.in1d(db_std_index,goodcomps_std_index)==True))[0]
       
    db_spectra_keep=db_spectra_mask_norm1[:,keepindex]
          
    db_std_keep=db_std[keepindex]
    db_std_comps_keep=numpy.zeros([9,len(keepindex)])
    db_folds=numpy.empty([len(keepindex)])
    

    for j in range(len(keepindex)):
        matchindex=(numpy.where(numpy.in1d(db_comp_names,db_std_keep[j])==True))[0]
        db_std_comps_keep[:,j]=db_ox_comp[matchindex[0],:]
        db_folds[j]=goodcomps_folds[(numpy.where(goodcomps_std==db_std_keep[j]))[0][0]]
       
    db_std_trainset=db_std_keep[numpy.array(numpy.where(db_folds!=1)[0])]
    db_std_testset=db_std_keep[numpy.array(numpy.where(db_folds==1)[0])]
    db_spectra_trainset=db_spectra_keep[:,numpy.array(numpy.where(db_folds!=1)[0])]    
    db_spectra_testset=db_spectra_keep[:,numpy.array(numpy.where(db_folds==1)[0])]    
    db_comps_trainset=db_std_comps_keep[:,numpy.array(numpy.where(db_folds!=1)[0])]
    db_comps_testset=db_std_comps_keep[:,numpy.array(numpy.where(db_folds==1)[0])]    
    db_folds_trainset=db_folds[numpy.array(numpy.where(db_folds!=1))[0]]
    #lolo=cross_validation.LeaveOneLabelOut(db_folds)   

    train_result=numpy.zeros([nc,len(db_comps_trainset[:]),len(db_comps_trainset[0,:])])    
    test_result=numpy.zeros([nc,len(db_comps_testset[:]),len(db_comps_testset[0,:])])    

    RMSECV=numpy.zeros([nc,len(db_ox_list),len(numpy.unique(db_folds_trainset))])

    #loop through each number of components   

    jj=numpy.array([0,2,3,4,5,6])
    for k in range(1,nc+1):    
        #calculate full training model for the current number of components
        print k
        PLS1=PLSRegression(n_components=k)
        x_train=numpy.transpose(db_spectra_trainset)
        x_train_mean=numpy.mean(x_train,axis=0)
        x_train_meancenter=x_train-numpy.tile(x_train_mean,(x_train.shape[0],1))
        
        y_train=numpy.transpose(db_comps_trainset[i,:])            
        y_train_mean=numpy.mean(y_train)
        y_train_meancenter=y_train-y_train_mean
        
        x_test=numpy.transpose(db_spectra_testset)
        x_test_meancenter=x_test-numpy.tile(x_train_mean,(x_test.shape[0],1))
        
        y_test=numpy.transpose(db_comps_testset[i,:])            


        PLS1.fit(x_train_meancenter,y_train_meancenter)
        train_result[k-1,i,:]=numpy.squeeze(PLS1.predict(x_train_meancenter)+y_train_mean)
        test_result[k-1,i,:]=numpy.squeeze(PLS1.predict(x_test_meancenter)+y_train_mean)
        RMSE_train[k-1,i]=numpy.sqrt(mean_squared_error(y_train,train_result[k-1,i,:]))
        RMSE_test[k-1,i]=numpy.sqrt(mean_squared_error(y_test,test_result[k-1,i,:]))

        #loop through each fold to do cross validation
        for j in range(len(numpy.unique(db_folds_trainset))):

            PLS1_cv=PLSRegression(n_components=k)
            cv_train=numpy.array(numpy.where(db_folds_trainset!=jj[j])[0])
            cv_test=numpy.array(numpy.where(db_folds_trainset==jj[j])[0])  
            x_cv_train=numpy.transpose(db_spectra_trainset[:,cv_train])
            x_cv_train_mean=numpy.mean(x_cv_train,axis=0)
            x_cv_train_meancenter=x_cv_train-numpy.tile(x_cv_train_mean,(x_cv_train.shape[0],1))
            
            x_cv_test=numpy.transpose(db_spectra_trainset[:,cv_test])
            x_cv_test_meancenter=x_cv_test-numpy.tile(x_cv_train_mean,(x_cv_test.shape[0],1))
            
            y_cv_train=numpy.transpose(db_comps_trainset[i,cv_train])
            y_cv_train_mean=numpy.mean(y_cv_train)
            y_cv_train_meancenter=y_cv_train-y_cv_train_mean
            
            y_cv_test=numpy.transpose(db_comps_trainset[i,cv_test])
            
            PLS1_cv.fit(x_cv_train_meancenter,y_cv_train_meancenter)
            cv_test_result=PLS1_cv.predict(x_cv_test_meancenter)+y_cv_train_mean            
            RMSECV[k-1,i,j]=numpy.sqrt(mean_squared_error(y_cv_test,cv_test_result))        
            if db_ox_list[i]=='MgO':
                print 'stop'

    #write results to files
    RMSECV_file=open('RMSECV_'+db_ox_list[i]+'.csv','wb')
    csv.writer(RMSECV_file).writerows(RMSECV[:,i,:])   
    RMSECV_file.close()    
    

csv.writer(RMSE_train_file).writerows(RMSE_train)
RMSE_train_file.close()
    
csv.writer(RMSE_test_file).writerows(RMSE_test)
RMSE_test_file.close()                
                
out=open('train_result.pkl','wb')
pickle.dump(train_result,out)
out.close()

out=open('test_result.pkl','wb')
pickle.dump(test_result,out)
out.close()
  
  
print('stop') 
        

        
  

    
