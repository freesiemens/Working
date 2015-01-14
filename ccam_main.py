# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 16:24:05 2014
This is the main program for CCAM data processing. 
@author: rbanderson
"""

#This function reads the correct temperature information from the label info of a spectum
def get_temp(label_info):
    temp=label_info[298]
    temp=temp.split(',')[1]
    temp=float(temp.translate(None,' <degC>'))
    return temp

def ccam_main(searchstring,mars='False',singleshots='False'):
    
    import glob
    import numpy
    import scipy
    import ccam_remove_continuum as cont_remove
    import ccam_denoise as denoise
    import ccam_wave_temp_correction as wave_correct
    import ccam_inst_response
    from scipy.io.idl import readsav
    import matplotlib.pyplot as plot

    #Load the default wavelengths from their respective text files
    defuv=numpy.loadtxt(r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\CCAM\default_wl\Ti_default_UV.dat')
    defvis=numpy.loadtxt(r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\CCAM\default_wl\Ti_default_VIS.dat')
    defvnir=numpy.loadtxt(r'C:\Users\rbanderson\Documents\MSL\ChemCam\Data Processing\CCAM\default_wl\Ti_default_VNIR.dat')
    
    #Search for IDL .SAV files    
    filelist=glob.glob(searchstring)
    #initialize the list that will hold all the data
    alldata=[]
    
    for i in range(len(filelist)):
        tempdata=readsav(filelist[i],python_dict=True)
        tempdata['filename']=filelist[i]
        tempdata['muvdata']=numpy.transpose(tempdata['calibspecmuv'])   
        tempdata['mvisdata']=numpy.transpose(tempdata['calibspecmvis'])    
        tempdata['mvnirdata']=numpy.transpose(tempdata['calibspecmvnir'])   
        tempdata['auvdata']=numpy.transpose(tempdata['calibspecuv']) 
        tempdata['avisdata']=numpy.transpose(tempdata['calibspecvis'])   
        tempdata['avnirdata']=numpy.transpose(tempdata['calibspecvnir'])   
        tempdata['uvdata']=numpy.transpose(tempdata['caliballspecuv']) 
        tempdata['visdata']=numpy.transpose(tempdata['caliballspecvis'])   
        tempdata['vnirdata']=numpy.transpose(tempdata['caliballspecvnir'])
        tempdata['nshots']=tempdata['vnirdata'].shape[1]
        if mars=='True':
            print "Trimming the leading and trailing empty values"
            tempdata['auvdata']=tempdata['auvdata'][50:2098]
            tempdata['avisdata']=tempdata['avisdata'][50:2098]
            tempdata['avnirdata']=tempdata['avnirdata'][50:2098]
            tempdata['muvdata']=tempdata['muvdata'][50:2098]
            tempdata['mvisdata']=tempdata['mvisdata'][50:2098]
            tempdata['mvnirdata']=tempdata['mvnirdata'][50:2098]
            tempdata['uvdata']=tempdata['uvdata'][50:2098,:]
            tempdata['visdata']=tempdata['visdata'][50:2098,:]
            tempdata['vnirdata']=tempdata['vnirdata'][50:2098,:]
        
            print "Applying the wavelength correction"
            tempdata['temp']=get_temp(tempdata['label_info']) #get the temperature from the label
            tempdata['uvdata'],tempdata['visdata'],tempdata['vnirdata']=wave_correct.ccam_wave_temp_correction(numpy.array([tempdata['uvdata'],tempdata['visdata'],tempdata['vnirdata']]),tempdata['temp'],split=True)   
            tempdata['auvdata'],tempdata['avisdata'],tempdata['avnirdata']=wave_correct.ccam_wave_temp_correction(numpy.array([tempdata['auvdata'],tempdata['avisdata'],tempdata['avnirdata']]),tempdata['temp'],split=True)   
            tempdata['muvdata'],tempdata['mvisdata'],tempdata['mvnirdata']=wave_correct.ccam_wave_temp_correction(numpy.array([tempdata['muvdata'],tempdata['mvisdata'],tempdata['mvnirdata']]),tempdata['temp'],split=True)   
             
            print "Denoising the average and median spectra"
            tempdata['auvdata'],tempdata['auvdata_noise']=denoise.ccam_denoise(tempdata['auvdata'])
            tempdata['avisdata'],tempdata['avisdata_noise']=denoise.ccam_denoise(tempdata['avisdata'])
            tempdata['avnirdata'],tempdata['avnirdata_noise']=denoise.ccam_denoise(tempdata['avnirdata'])
            tempdata['muvdata'],tempdata['muvdata_noise']=denoise.ccam_denoise(tempdata['muvdata'])
            tempdata['mvisdata'],tempdata['mvisdata_noise']=denoise.ccam_denoise(tempdata['mvisdata'])
            tempdata['mvnirdata'],tempdata['mvnirdata_noise']=denoise.ccam_denoise(tempdata['mvnirdata'])
        
        #Define continuum removal settings
        int_flag=2
        lvuvmin=6  
        lvvismin=6
        lvvnirtopmin=5
        lvvnirbottommin=3
        
        nuv=2048#tempdata['uvdata'].size/tempdata['uvdata'].shape[0]
        nvis=2048#tempdata['visdata'].size/tempdata['visdata'].shape[0]
        nvnirtop=1800
        nvnirbottom=173+75
        
        lvuv=int(numpy.log(nuv-1)/numpy.log(2))
        lvvis=int(numpy.log(nvis-1)/numpy.log(2))
        lvvnirtop=int(numpy.log(nvnirtop-1)/numpy.log(2))
        lvvnirbottom=int(numpy.log(nvnirbottom-1)/numpy.log(2))
        
        if lvuvmin >= lvuv: lvuvmin=lvuv-2
        if lvvismin >= lvvis: lvvismin=lvvis-2
        if lvvnirtopmin >= lvvnirtop: lvvnirtopmin=lvvnirtop-2   
        if lvvnirbottommin >= lvvnirbottom: lvvnirbottommin=lvvnirbottom-2
        
        #Initialize the dictionary entries to hold the noise and contjnuum for each shot
          
        tempdata['uvdata_noise']=tempdata['uvdata']*0.0
        tempdata['visdata_noise']=tempdata['visdata']*0.0
        tempdata['vnirdata_noise']=tempdata['visdata']*0.0
        
        tempdata['uvdata_cont']=tempdata['uvdata']*0.0
        tempdata['visdata_cont']=tempdata['visdata']*0.0
        tempdata['vnirdata_cont']=tempdata['visdata']*0.0
        
        
        if singleshots=='True':
            print "Denoising, removing continuum, and applying instrument response for the individual shots"        
            for j in range(tempdata['nshots']):
                print "Denoising shot ",j                
                if mars=='True':
                    tempdata['uvdata'][j,:],tempdata['uvdata_noise'][j,:]=denoise.ccam_denoise(tempdata['uvdata'][j,:])
                    tempdata['visdata'][j,:],tempdata['visdata_noise'][j,:]=denoise.ccam_denoise(tempdata['visdata'][j,:])
                    tempdata['vnirdata'][j,:],tempdata['vnirdata_noise'][j,:]=denoise.ccam_denoise(tempdata['vnirdata'][j,:])
                print "Removing continuum from shot ",j
                tempdata['uvdata'][j,:],tempdata['uvdata_cont'][j,:]=cont_remove.ccam_remove_continuum(defuv,tempdata['uvdata'][j,:],lvuv,lvuvmin,int_flag)
                tempdata['visdata'][j,:],tempdata['visdata_cont'][j,:]=cont_remove.ccam_remove_continuum(defvis,tempdata['visdata'][j,:],lvvis,lvvismin,int_flag)
                tempdata['vnirdata'][j,:],tempdata['vnirdata_cont'][j,:]=cont_remove.ccam_remove_continuum(defvnir,tempdata['vnirdata'][j,:],lvvnirtop,lvvnirtopmin,int_flag)
                tempdata['vnirdata'][j,1801:2048],tempdata['vnirdata_cont'][j,1801:2048]=cont_remove.ccam_remove_continuum(defvnir[1801:2048],tempdata['vnirdata'][j,1801:2048],lvvnirbottom,lvvnirbottommin,int_flag)
                print "Applying instrument response to shot ",j                
                tempdata['uvdata'][j,:],tempdata['visdata'][j,:],tempdata['vnirdata'][j,:]=ccam_inst_response.inst_response(defuv,defvis,defvnir,tempdata['uvdata'][j,:],tempdata['visdata'][j,:],tempdata['vnirdata'][j,:])
                tempdata['uvdata_cont'][j,:],tempdata['visdata_cont'][j,:],tempdata['vnirdata_cont'][j,:]=ccam_inst_response.inst_response(defuv,defvis,defvnir,tempdata['uvdata_cont'][j,:],tempdata['visdata_cont'][j,:],tempdata['vnirdata_cont'][j,:])
            #sum continuum
            tempdata['uvdata_cont_sum']=numpy.sum(tempdata['uvdata_cont'],axis=1)
            tempdata['visdata_cont_sum']=numpy.sum(tempdata['visdata_cont'],axis=1)
            tempdata['vnirdata_cont_sum']=numpy.sum(tempdata['vnirdata_cont'],axis=1)
            
            print tempdata['uvdata_cont_sum']
            
            
        print "Removing continuum from the average and median spectra"
        tempdata['auvdata'],tempdata['auvdata_cont']=cont_remove.ccam_remove_continuum(defuv,tempdata['auvdata'],lvuv,lvuvmin,int_flag)
        tempdata['avisdata'],tempdata['avisdata_cont']=cont_remove.ccam_remove_continuum(defvis,tempdata['avisdata'],lvvis,lvvismin,int_flag)
        tempdata['avnirdata'],tempdata['avnirdata_cont']=cont_remove.ccam_remove_continuum(defvnir,tempdata['avnirdata'],lvvnirtop,lvvnirtopmin,int_flag)
        tempdata['avnirdata'][1801:2048],tempdata['avnirdata_cont'][1801:2048]=cont_remove.ccam_remove_continuum(defvnir[1801:2048],tempdata['avnirdata'][1801:2048],lvvnirbottom,lvvnirbottommin,int_flag)
        
        tempdata['muvdata'],tempdata['muvdata_cont']=cont_remove.ccam_remove_continuum(defuv,tempdata['muvdata'],lvuv,lvuvmin,int_flag)
        tempdata['mvisdata'],tempdata['mvisdata_cont']=cont_remove.ccam_remove_continuum(defvis,tempdata['mvisdata'],lvvis,lvvismin,int_flag)
        tempdata['mvnirdata'],tempdata['mvnirdata_cont']=cont_remove.ccam_remove_continuum(defvnir,tempdata['mvnirdata'],lvvnirtop,lvvnirtopmin,int_flag)
        tempdata['mvnirdata'][1801:2048],tempdata['mvnirdata_cont'][1801:2048]=cont_remove.ccam_remove_continuum(defvnir[1801:2048],tempdata['mvnirdata'][1801:2048],lvvnirbottom,lvvnirbottommin,int_flag)

        print "Applying instrument response to average and median spectra"
        tempdata['auvdata'],tempdata['avisdata'],tempdata['avnirdata']=ccam_inst_response.inst_response(defuv,defvis,defvnir,tempdata['auvdata'],tempdata['avisdata'],tempdata['avnirdata'])
        tempdata['auvdata_cont'],tempdata['avisdata_cont'],tempdata['avnirdata_cont']=ccam_inst_response.inst_response(defuv,defvis,defvnir,tempdata['auvdata_cont'],tempdata['avisdata_cont'],tempdata['avnirdata_cont'])
                
        tempdata['auvdata_cont_sum']=numpy.sum(tempdata['auvdata_cont'])
        tempdata['avisdata_cont_sum']=numpy.sum(tempdata['avisdata_cont'])
        tempdata['avnirdata_cont_sum']=numpy.sum(tempdata['avnirdata_cont'])
        
        tempdata['muvdata'],tempdata['mvisdata'],tempdata['mvnirdata']=ccam_inst_response.inst_response(defuv,defvis,defvnir,tempdata['muvdata'],tempdata['mvisdata'],tempdata['mvnirdata'])
        tempdata['muvdata_cont'],tempdata['mvisdata_cont'],tempdata['mvnirdata_cont']=ccam_inst_response.inst_response(defuv,defvis,defvnir,tempdata['muvdata_cont'],tempdata['mvisdata_cont'],tempdata['mvnirdata_cont'])
                
        tempdata['muvdata_cont_sum']=numpy.sum(tempdata['muvdata_cont'])
        tempdata['mvisdata_cont_sum']=numpy.sum(tempdata['mvisdata_cont'])
        tempdata['mvnirdata_cont_sum']=numpy.sum(tempdata['mvnirdata_cont'])
        
        print tempdata['muvdata_cont_sum']
        
        alldata=alldata.append(tempdata)
    


