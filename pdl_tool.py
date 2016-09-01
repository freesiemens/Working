# -*- coding: utf-8 -*-
"""
Created on Tue May 19 12:19:44 2015

@author: rbanderson
"""

from PyQt4 import QtGui  
from PyQt4 import QtCore
from PyQt4 import QtUiTools
import ccam
import numpy
#need these to help pyinstaller find the correct modules
#from PySide import QtXml
#import sklearn.utils.sparsetools._graph_validation
#import scipy
#import scipy.special._ufuncs


class MyWidget(QtGui.QMainWindow):
    def __init__(self, *args):  
        #apply(QtGui.QMainWindow.__init__, (self,) + args)
        QtGui.QMainWindow.__init__(*args)
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(r'C:\Users\rbanderson\Documents\MSL\ChemCam\DataProcessing\ccam_pdl_ui.ui')
        file.open(QtCore.QFile.ReadOnly)
        self.myWidget = loader.load(file, self)
        file.close()
        self.setCentralWidget(self.myWidget)
        self.myWidget.progressBar.reset()
        #read config file
        config=ccam.read_csv('pdl_tool_config.csv',0,labelrow=False,skipsym='#')        
        self.searchdir=config[config[:,0]=='searchdir',1][0]
        self.myWidget.lineEdit.setText(self.searchdir)
        self.masterlist=config[config[:,0]=='masterlist',1][0]
        self.name_sub_file=config[config[:,0]=='name_sub_file',1][0]
        self.maskfile=config[config[:,0]=='maskfile',1][0]
        self.meancenters_file=config[config[:,0]=='meancenters_file',1][0]
        self.settings_coeffs_file=config[config[:,0]=='settings_coeffs_file',1][0]
        self.blend_array_dir=config[config[:,0]=='blend_array_dir',1][0]
        self.elems=['SiO2','TiO2','Al2O3','FeOT','MgO','CaO','Na2O','K2O']
        #read PLS settings files
        self.meancenters,self.meancenter_labels=ccam.read_csv(self.meancenters_file,0,labelrow=True)
        self.meancenter_labels=self.meancenter_labels[1:]
        self.ymeancenters=numpy.array(self.meancenters[0,1:],dtype='float')
        self.meancenters=numpy.array(self.meancenters[1:,1:],dtype='float')
        
        self.pls_settings,self.pls_settings_labels=ccam.read_csv(self.settings_coeffs_file,0,labelrow=True)
        self.pls_settings_labels=self.pls_settings_labels[1:]
        self.pls_norms=numpy.array(self.pls_settings[0,1:],dtype='int')
        self.pls_ncs=numpy.array(self.pls_settings[1,1:],dtype='int')
        self.pls_coeffs=numpy.array(self.pls_settings[2:,1:],dtype='float')        
        
       #Choose search directory
        self.myWidget.browse_button.clicked.connect(self.choosedir)
        
        #Calculate compositions
        self.myWidget.calc_button.clicked.connect(self.calc_comp)
        

        
    def choosedir(self):
        self.searchdir=QtGui.QFileDialog.getExistingDirectory(self,dir=self.searchdir)
        self.myWidget.lineEdit.setText(self.searchdir)
        
    def calc_comp(self):
        #Choose whether to do single shots
        self.shots=self.myWidget.singleshots_checkbox.isChecked()
        filelist,files=ccam.search_ccs(self.searchdir)
        self.myWidget.progressBar.setMaximum(len(filelist))
        targets,dists,amps,nshots=ccam.target_lookup(filelist,self.masterlist,self.name_sub_file) 
        nshots=numpy.array(nshots,dtype='int')
        #Loop through each file in the file list
        for i in range(0,len(filelist)):
            app.processEvents()          
            self.myWidget.progressBar.setValue(i)
            print(filelist[i])
            
                       
            
            if self.shots is True:
                #print 'Single shots'
                singleshots,wvl,filename,shotnum=ccam.read_ccs(filelist[i],skiprows=0,shots=self.shots,masterlist=self.masterlist,name_sub_file=self.name_sub_file,singlefile=True)
                singleshots_masked,wvl_masked=ccam.mask(singleshots,wvl,self.maskfile)
                self.spectra_masked_norm1=ccam.normalize(singleshots_masked,wvl_masked,normtype=1)
                self.spectra_masked_norm3=ccam.normalize(singleshots_masked,wvl_masked,normtype=3)
                
            if self.shots is False:
                #print 'Means'
                nshots[i]=1
                meanspect,wvl,filename=ccam.read_ccs(filelist[i],skiprows=0,shots=self.shots,masterlist=self.masterlist,name_sub_file=self.name_sub_file,singlefile=True)
                meanspect_masked,wvl_masked=ccam.mask(meanspect,wvl,self.maskfile)
                self.spectra_masked_norm1=ccam.normalize(meanspect_masked,wvl_masked,normtype=1)
                self.spectra_masked_norm3=ccam.normalize(meanspect_masked,wvl_masked,normtype=3)
                
            comps_temp=self.pls_submodels(nshots[i])
            if i==0:
                comps_all=comps_temp
                filename_all=filename
                
                if self.shots is True:
                    shotnum_all=shotnum
                    targets_all=numpy.tile(targets[i],nshots[i])
                    dists_all=numpy.tile(dists[i],nshots[i])
                    amps_all=numpy.tile(amps[i],nshots[i])
                    
            else:
                comps_all=[numpy.vstack([comps_all[0],comps_temp[0]]),numpy.vstack([comps_all[1],comps_temp[1]]),numpy.vstack([comps_all[2],comps_temp[2]]),numpy.vstack([comps_all[3],comps_temp[3]])]
                filename_all=numpy.hstack([filename_all,filename])

                
                if self.shots is True:
                    shotnum_all=numpy.hstack([shotnum_all,shotnum])
                    targets_all=numpy.hstack([targets_all,numpy.tile(targets[i],nshots[i])])
                    dists_all=numpy.hstack([dists_all,numpy.tile(dists[i],nshots[i])])
                    amps_all=numpy.hstack([amps_all,numpy.tile(amps[i],nshots[i])])
        
                
        blended_all=self.pls_blend(comps_all)
        self.myWidget.progressBar.setValue(len(filelist))
        if self.shots is False:
            shotnum_all='placeholder'
            targets_all=targets
            dists_all=dists
            amps_all=amps
        self.write_results(blended_all,shotnum_all,targets_all,dists_all,amps_all,filename_all)
            

    
    def pls_submodels(self,nshots):
        which_submodel='full'
        comps_full=self.pls_comp(self.elems[0],nshots,which_submodel)
        for j in range(1,len(self.elems)):
            comps_full=numpy.hstack([comps_full,self.pls_comp(self.elems[j],nshots,which_submodel)])

        which_submodel='low'
        comps_low=self.pls_comp(self.elems[0],nshots,which_submodel)
        for j in range(1,len(self.elems)):
            comps_low=numpy.hstack([comps_low,self.pls_comp(self.elems[j],nshots,which_submodel)])

        which_submodel='mid'
        comps_mid=self.pls_comp(self.elems[0],nshots,which_submodel)
        for j in range(1,len(self.elems)):
            comps_mid=numpy.hstack([comps_mid,self.pls_comp(self.elems[j],nshots,which_submodel)])

        which_submodel='high'
        comps_high=self.pls_comp(self.elems[0],nshots,which_submodel)
        for j in range(1,len(self.elems)):
            comps_high=numpy.hstack([comps_high,self.pls_comp(self.elems[j],nshots,which_submodel)])

        return comps_full,comps_low,comps_mid,comps_high
            
    def pls_comp(self,currentelem,nshots,which_submodel):
        #get full results
        y_mean=self.ymeancenters[self.pls_settings_labels==currentelem+'_'+which_submodel][0]
        fullnorm=self.pls_norms[self.pls_settings_labels==currentelem+'_'+which_submodel][0]
        full_coeff=self.pls_coeffs[:,self.pls_settings_labels==currentelem+'_'+which_submodel]
        full_meancenter=numpy.tile(numpy.transpose(self.meancenters[:,self.meancenter_labels==currentelem+'_'+which_submodel]),[nshots,1])
        if fullnorm==1:
            calc_comp=numpy.dot(self.spectra_masked_norm1-full_meancenter,full_coeff)+y_mean
        if fullnorm==3:
            calc_comp=numpy.dot(self.spectra_masked_norm3-full_meancenter,full_coeff)+y_mean     
        return calc_comp   

    def pls_blend(self,comps_all):
        blended=numpy.zeros_like(comps_all[0])        
        for i in range(0,len(self.elems)):
            #reconstruct the blend input settings from the blend array file
            blendarray,blend_labels=ccam.read_csv(self.blend_array_dir+'\\'+self.elems[i]+'_blend_array.csv',0,labelrow=True)
            blendarray=numpy.array(numpy.array(blendarray,dtype='float'),dtype='int')            
            ranges=[]
            inrange=[]
            refpredict=[]
            toblend=[]
            predict=[]
            for k in comps_all:
                predict.append(k[:,i])
            for j in range(len(blendarray[:,0])):
                ranges.append(blendarray[j,0:2].tolist())
                inrange.append(blendarray[j,2].tolist())
                refpredict.append(blendarray[j,3].tolist())
                toblend.append(blendarray[j,4:].tolist())
                
            blended[:,i]=ccam.submodels_blend(predict,ranges,inrange,refpredict,toblend)
    
        return blended
        
    def write_results(self,blended_all,shotnum_all,targets_all,dists_all,amps_all,filename_all):
        if self.shots is True:
            labelrow=numpy.array(['File','Target','Shot Number','Distance (m)','Laser Power'])
            labelrow=numpy.hstack([labelrow,self.elems])
            output=numpy.vstack([filename_all,targets_all,shotnum_all+1,dists_all,amps_all])
            outfile='ccam_comps_predict_singleshots.csv'
        if self.shots is False:
            labelrow=numpy.array(['File','Target','Distance (m)','Laser Power'])
            labelrow=numpy.hstack([labelrow,self.elems])
            output=numpy.vstack([filename_all,targets_all,dists_all,amps_all])
            outfile='ccam_comps_predict.csv'
        output=numpy.hstack([numpy.transpose(output),blended_all])

        output=numpy.vstack([labelrow,output])
        numpy.savetxt(outfile,output,delimiter=',',fmt='%s')
    



        
        


if __name__ == '__main__':  
   import sys  
   import os
   print("Running in " + os.getcwd() + " .\n")

   app = QtGui.QApplication(sys.argv)  
   
   win  = MyWidget()  
   win.show()

   app.connect(app, QtCore.SIGNAL("lastWindowClosed()"),
               app, QtCore.SLOT("quit()"))
   app.exec_()

