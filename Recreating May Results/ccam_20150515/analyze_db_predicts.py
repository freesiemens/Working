# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 14:38:27 2015

@author: rbanderson
"""
import numpy
import os
import fnmatch
import csv

def read_csv(filename,skiprows,labelrow=True,skipsym='#'):
    
    f=open(filename,'r')  #open the file
    for i in range(skiprows):
        f.readline()    
    if labelrow==True:
        labels=f.readline() #read the label row
        labels=numpy.array(labels.split(',')) #split it on commas and convert to a string array
        data=[]
        for row in f:
            if row[0] is not skipsym:            
                data.append(row.strip().split(','))
            
        f.close()
        data=numpy.array(data)
        return data,labels
    else:
           
        data=[]
        for row in f:
                        
            if row[0] is not skipsym:            
                data.append(row.strip().split(','))
            
        f.close()
        data=numpy.array(data)
        return data

def ica_pls_combine(plsval,icaval,elem,FeOTval=None):
    #Combine the PLS and ICA results
    #Settings for these combinations derived by Roger and Sylvestre

    if elem=='TiO2':
        combinedval=0.5*plsval+0.5*icaval
    if elem=='Al2O3':
        combinedval=0.75*plsval+0.25*icaval
        if combinedval<15.0:
            combinedval=0.0667*combinedval**2+(1-0.06667*combinedval)*icaval
    if elem=='FeOT':
        combinedval=0.75*plsval+0.25*icaval
    if elem=='SiO2':
        SiO2temp=0.5*plsval+0.5*icaval
        combinedval=SiO2temp
        if FeOTval>30:
            combinedval=0.75*plsval+0.25*icaval
        if (FeOTval<=30)&(SiO2temp>= 30):
            combinedval=SiO2temp            
        if (FeOTval<=30) & (SiO2temp<30):
            combinedval=SiO2temp*SiO2temp*0.03333+(1-0.0333*SiO2temp)*icaval
    if elem=='MgO':
        combinedval=0.5*plsval+0.5*icaval
    if elem=='CaO':
        combinedval=0.5*plsval+0.5*icaval
    if elem=='Na2O':
        combinedval=0.4*plsval+0.6*icaval
    if elem=='K2O':
        combinedval=0.25*plsval+0.75*icaval
       
    return combinedval





##Read in old PLS db results
#ncs=[8,10,4,7,8,8,10,4]
which_elem=['SiO2','TiO2','Al2O3','FeOT','MgO','CaO','Na2O','K2O']
#old_PLS_path="C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\PDL\\PLS\\PLS1_20130829\\RMSEP_output"
#matypred=[]
#matypres=[]
#truecomps=[]
#for i in range(len(ncs)):
#    matypred.append(numpy.array(read_csv(old_PLS_path+"\\matypred_"+which_elem[i]+'.csv',0,labelrow=False,skipsym='#')[:,ncs[i]-1],dtype='float'))
#    matypres.append(numpy.array(read_csv(old_PLS_path+"\\matypres_"+which_elem[i]+'.csv',0,labelrow=False,skipsym='#')[:,ncs[i]-1],dtype='float'))
#    truecomps.append(numpy.add(matypred[i],matypres[i]))
#    


#Read in submodel PLS new db results
new_PLS_path=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\DataProcessing\Working\Recreating May Results\ccam_20150515\Output\db_predictions_May_results"
newPLS_results=[]
newPLS_samples=[]
newPLS_sample_index=[]
newPLS_samples_unique=[]

for i in range(len(which_elem)):
    searchstring=which_elem[i]+'_db_predictions*.csv'    
    filelist = []
    for root, dirnames, filenames in os.walk(new_PLS_path):
        for filename in fnmatch.filter(filenames, searchstring):
            filelist.append(os.path.join(root, filename))
    filelist=filelist[0]
    tmp,labels=read_csv(filelist,3,labelrow=True,skipsym='#')
    newPLS_results.append(numpy.array(tmp[:,6],dtype='float'))
    newPLS_samples.append(tmp[:,0])
    newPLS_sample_index.append(numpy.array(tmp[:,1],dtype='int'))
    newPLS_samples_unique.append(numpy.unique(newPLS_samples[i]))

#read in ICA new db results
ICA_path="C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\db_predictions_May_results\\ICA_db_predicts"
ICA_results=[]
ICA_samples=[]
ICA_samples_unique=[]
for i in range(len(which_elem)):
    tmp=read_csv(ICA_path+'\\'+which_elem[i]+'_ICA.csv',0,labelrow=False,skipsym='#')
    tmp=numpy.core.defchararray.replace(tmp,'"','')
    tmp=numpy.core.defchararray.replace(tmp,' ','')
    tmp=numpy.core.defchararray.replace(tmp,'\r','')
    tmp=numpy.core.defchararray.replace(tmp,'\n','')
    
    ICA_results.append(numpy.array(tmp[:,2],dtype='float'))
    ICA_samples.append(tmp[:,0])
    ICA_samples_unique.append(numpy.unique(ICA_samples[i]))
    

#Combine submodel PLS and ICA results
full_db_file="C:\\Users\\rbanderson\\Documents\\Projects\\MSL\\ChemCam\\DataProcessing\\Working\\Recreating May Results\\ccam_20150515\\Output\\db_predictions_May_results\\full_db_names_comps.csv"
full_db,labels=read_csv(full_db_file,0,labelrow=True,skipsym='#')
foo,ind=numpy.unique(full_db[:,0],return_index=True)    
full_db_unique=full_db[ind,:]
full_db_unique_samples=full_db_unique[:,0]
full_db_unique_comps=numpy.array(full_db_unique[:,1:],dtype='float')

ICA_full=numpy.zeros(full_db[:,1:].shape)+99999
PLS_full=numpy.zeros(full_db[:,1:].shape)+99999
Combined_full=numpy.zeros(full_db[:,1:].shape)+99999
looper=[1,2,3,4,5,6,7,0]

for j in looper:
    for i in range(len(full_db[:,0])):
        spect_ind=int(full_db[i,1])
        ICA_index=ICA_samples[j]==full_db[i,0]
        
        if numpy.max(ICA_index)==True:        
            ICA_full[i,j]=ICA_results[j][ICA_index][spect_ind-1]
        else:
            ICA_full[i,j]=99999
            
        ind=(newPLS_samples[j]==full_db[i,0])&(newPLS_sample_index[j]==spect_ind)
        if numpy.max(ind)==True:
            if numpy.sum(ind)>1:
                print(blah)
            PLS_full[i,j]=newPLS_results[j][ind][0]
        else:
            PLS_full[i,j]=99999
            
        if (ICA_full[i,j]!=99999)&(PLS_full[i,j]!=99999):
            if which_elem[j]!='SiO2':
                Combined_full[i,j]=ica_pls_combine(float(ICA_full[i,j]),float(PLS_full[i,j]),which_elem[j])
            if which_elem[j]=='SiO2':
                Combined_full[i,j]=ica_pls_combine(float(ICA_full[i,j]),float(PLS_full[i,j]),which_elem[j],FeOTval=Combined_full[i,3])

combined_stdevs=numpy.zeros([len(full_db_unique_samples),len(which_elem)])
combined_stdevs_n=numpy.zeros([len(full_db_unique_samples),len(which_elem)])
for i in range (len(which_elem)):
    for j in range(len(full_db_unique_samples)):
        goodindex=(full_db[:,0]==full_db_unique_samples[j])&(Combined_full[:,i]!=99999)
        combined_stdevs_n[j,i]=numpy.sum(goodindex)
        if combined_stdevs_n[j,i]>1: 
            stdtmp=numpy.std(Combined_full[goodindex,i],ddof=1)

            combined_stdevs[j,i]=stdtmp       
        

print('Writing stdev results')
stdevoutputfile=new_PLS_path+'\\combined_stdevs_ddof1.csv'
with open(stdevoutputfile,'w',newline='') as writefile:
    writer=csv.writer(writefile,delimiter=',')
    row=['Target','SiO2 #','SiO2 stdev','TiO2 #','TiO2 stdev','Al2O3 #','Al2O3 stdev','FeOT #','FeOT stdev','MgO #','MgO stdev','CaO #','CaO stdev','Na2O #','Na2O stdev','K2O #','K2O stdev']
    writer.writerow(row)
    for i in range(len(full_db_unique_samples)):
        row=[full_db_unique_samples[i]]
        for j in range(len(which_elem)):
            row.extend([combined_stdevs_n[i,j]])
            row.extend([combined_stdevs[i,j]])
        writer.writerow(row)     
        
print('Writing full results')
for j in range(len(which_elem)):
    fulloutfile=new_PLS_path+'\\'+which_elem[j]+'_full_results.csv'
    with open(fulloutfile,'w',newline='') as writefile:
        writer=csv.writer(writefile,delimiter=',')
        row=['Target','ICA','PLS','Combined']
        writer.writerow(row)
        for i in range(len(Combined_full[:,0])):
            row=[full_db[i,0],ICA_full[i,j],PLS_full[i,j],Combined_full[i,j]]
            writer.writerow(row)
            
    
print('foo')
#plot old pls results vs new combined results (for old db only)

#calculate stdev of combined results for each sample