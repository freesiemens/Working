;+
; NAME:
;        CALC_COMP
;        Includes also:
;           PLOT_1TO1
;           GET_TESTSET_INFO
;           DYNAMIC_RMSEP
;           PLS_COMP
;           PLS_SUBMODELS
;           PLS_BLEND
;           WRITE_RESULTS
;           pls_and_ica
;
; PURPOSE:
; This program calculates the estimated major oxide composition of target(s)
; based on input ChemCam spectra and writes the results to a csv file. This program includes 
; partial least squares (PLS) and independent component analysis (ICA) quantification, and combines
; the two using empirically-derived weighted averages. Accuracy is estimated as root mean squared error
; of prediction (RMSEP) as a function of predicted composition on the fly, based on ICA and PLS results
; on a test set. See documentation of DYNAMIC_RMSEP for details.
;       
;
; CALLING SEQUENCE:
;        calc_comp,searchdir,shots,recursive,configfile,software_version,quiet=quiet,pls_output=pls_output,ica_output=ica_output,calcstdevs=calcstdevs
;        
; INPUTS:
;        searchdir = The path to search for suitable spectra files
;        shots = If set to 1, calculate single shot results. If set to 0, use the average spectra.
;        recursive = If set to 1, search the searchdir recursively. If set to 0, don't search subfolders.
;        configfile = Full path to a file containing config data.        
;        software_version = String giving the tool name, version, and date, to be written in each output file
;        
; OPTIONAL INPUTS:
;        None
;
; KEYWORD PARAMETERS:
;        Quiet = If set, suppress all pop-up windows
;        pls_output = Set to 1 to output the pls results separately
;        ica_output = Set to 1 to output the ICA results separately
;        calcstdevs = Set to 1 to calculate the single shot stdevs and report them along with the mean results
; OUTPUTS:
;       No values are returned directly. The program produces output file(s) in the search directory.
;       
; OPTIONAL OUTPUTS:
;       
; RESTRICTIONS:
;
; EXAMPLE:
;       searchdir='G:/ChemCam/ops_ccam_team/'
;       shots=0
;       recursive=1
;       software_version='sPDL Tool v2 (July 7, 2015)'
;       calc_comp,searchdir,shots,recursive,configfile,software_version,quiet=0,ica_output=1,pls_output=1,calcstdevs=1
;
; MODIFICATION HISTORY:
; R. Anderson: June 2015 - Write initial code
; O. Gasnault: June 25-26, 2015 - Secure usage of WHERE at different places:
;    In GET_TESTSET_INFO:
;       Introduce NAL, the number of AL2O3INDEX for which Al must be corrected
;          and don't apply it if all Al contents are larger than 15 wt% in the
;          test set (never?)
;       Introduce TEST1, TEST2, and TEST3 to check the validity of the
;          conditions on SIO2_TEST_FEOT_TRUE and SIO2TEMP (test1 was not
;          returning in index, so the last value of SiO2 was erroneously
;          modified - impact on SiO2 RMSEP is TBD).
;    In DYNAMIC_RMSEP:
;       Introduce INDX in the calculation of IND, instead of a comparison of
;          float values (risky).
;       Add a test on the size of IND (should never be 0).
;       Use IMIN rather than a comparison of float values (risky) in
;          RMSEPS[i,j]=YY[IMIN].
;    In PLS_COMP: Check that the submodel exists with NL (should not happen).
;    In PLS_BLEND: Add /NULL to WHERE in case all BLENDED values are positive
;       (otherwise would put K (last element) to 0 for PLS).
;    In WRITE_RESULTS: Force TOTALS to be an array even for a single value
;      (single file analysis) to be compatible with the use of TRANSPOSE.
;    In CALC_COMP:
;       Introduce NAL, as in GET_TESTSET_INFO above for Al; Note that this case
;          may happen, it depends on the input files
;       Introduce TEST1, TEST2, and TEST3 as in GET_TESTSET_INFO above for Si;
;          Note that this case may happen, it depends on the input files.
; R. Anderson: July 7-10, 2015 - Change output to include tool name, version, and date of last edit
;                           - Change output so that predictions and RMSEP for each element are next to each other, separated by plus/minus sign
;                           - Round output to more appropriate number of significant figures
;                           - Modified so that most config info is read inside calc_comp rather than in spdl_tool.pro
;                           - Made software version an input so that it is defined in spdl_tool rather than here
;                           - Modified all structures to hashes, which allows streamlining of some parts of the code (because you can loop through them)
;                           - Added more comments and documentation before each function
;                           - Lots of general reorganization
; R. Anderson June 2, 2016 - Add automatic MOC plotting capability
;                           
;-



;
;This program is used to make nice-looking 1 to 1 plots of the test set results and save them as .tif files.
;It also optionally writes the results to a csv file.
;
;Input:
;       actual = array of certificate values for the element being plotted
;       predict = array of corresponding predicted values for the element being plotted
;       names = array of corresponding target names
;       plottitle = string used to label the plot
;       plotfile = Full name of the .tif file to write
;       xsize = Integer specifying the x size of the output plot, in pixels
;       ysize = Integer specifying the y size of the output plot, in pixels
;       csvfile = Name of the csv file to write (optional)

pro out_1to1,actual,predict,names,plottitle,plotfile,xsize=xsize,ysize=ysize,csvfile=csvfile
    if keyword_Set(csvfile) then write_csv,csvfile,[names,strtrim(actual,2),strtrim(predict,2)]
    prettyplot,actual,predict,psym=0,color=0,thick=0,xtitle='Actual wt.%',ytitle='Predicted wt.%',charsize=2,$
       xthick=2,ythick=2,oplot=0,symsize=0.75,xsize=xsize,ysize=ysize,title=plottitle,xrange=[0,max(actual*1.1)],yrange=[0,max(predict)*1.1],winnum=0
    prettyplot,[0,100],[0,100],linestyle=0,oplot=1
    write_tiff,plotfile,reverse(tvrd(),2),compression=1
        
end

;This function extracts test set results from the test result directory. It returns a structure with the 
;test set results for each element using ICA, PLS, and combined, plus the test set quartiles, and actual compositions
;
;Input:
;      testresult_dir = a directory containing the test set results
;      elems = string array of the major element oxides
;      output1to1 = Optional keyword. If set, this function will produce .tif files of test set 1 to 1 plots
;Output:
;      test_info = Structure containing PLS test set results (structure), ICA test set results (structure),
;                  Combined test set results (structure), test set actual compositions (structure), and test set quartiles (array)

function get_testset_info,testresult_dir,elems,output1to1=output1to1
      ;Read the actual FeOT comps for the SiO2 test set (to be used in combining ICA and PLS SiO2 results) 
      SiO2_test_FeOT_true=float((rd_tfile(testresult_dir+'SiO2_testset_FeOT_comps.csv',2,delim=','))[1,1:*])
      
      ;Using hashes significantly streamlines this function by allowing looping through each element
      test_names=hash()
      actuals=hash()
      quartiles=[]
      pls_test=hash()
      ica_test=hash()
      
      for i=0,n_elements(elems)-1 do begin
        pls_test_temp=rd_tfile(testresult_dir+elems[i]+'_testset_blended.csv',3,delim=',')
        test_names=test_names+hash(elems[i],pls_test_temp[0,1:*]) ;get test set sample names
        actuals=actuals+hash(elems[i],float(pls_test_temp[1,1:*])) ;get test set actual compositions
        quartiles=[[quartiles],[summary(actuals[elems[i]])]] ;get test set quartiles
        
        ;get PLS and ICA test set results and store them in hashes
        pls_test=pls_test+hash(elems[i],float(pls_test_temp[2,1:*]))
        ica_test=ica_test+hash(elems[i],float((rd_tfile(testresult_dir+elems[i]+'_testset_ICA.csv',3,delim=','))[2,1:*]))
        
      endfor
      

      ;combine the PLS and ICA test set results
      TiO2=0.5*pls_test['TiO2']+0.5*ica_test['TiO2']
      Al2O3=0.75*pls_test['Al2O3']+0.25*ica_test['Al2O3']
      Al2O3index=where(Al2O3 lt 15.0, nal)
      if nal gt 0 then Al2O3[Al2O3index]=0.06667*Al2O3[Al2O3index]^2+(1-0.06667*Al2O3[Al2O3index])*(ica_test['Al2O3'])[Al2O3index]
      FeOT=0.75*pls_test['FeOT']+0.25*ica_test['FeOT']
      SiO2temp=0.5*pls_test['SiO2']+0.5*ica_test['SiO2']
      SiO2=SiO2temp
      ;We don't have FeOT test predictions for the SiO2 test set because the FeOT test set was defined separately
      ;Instead use the FeOT actuals to determine SiO2. This is "cheating" somewhat because it doesn't include the 
      ;FeOT uncertainties in the SiO2 results, even though FeOT predictions play a role.
      test1 = where(SiO2_test_FeOT_true gt 30, nt1)
      test2 = where(SiO2_test_FeOT_true le 30 and SiO2temp ge 30, nt2)
      test3 = where(SiO2_test_FeOT_true le 30 and SiO2temp lt 30, nt3)
      if nt1 gt 0 then SiO2[test1]=0.75*(pls_test['SiO2'])[test1]+0.25*(ica_test['SiO2'])[test1]
      if nt2 gt 0 then SiO2[test2]=SiO2temp[test2]
      if nt3 gt 0 then SiO2[test3]=SiO2temp[test3]*SiO2temp[test3]*0.03333+$
                                (1-0.0333*SiO2temp[test3])*(ica_test['SiO2'])[test3]
      MgO=0.5*pls_test['MgO']+0.5*ica_test['MgO']
      CaO=0.5*pls_test['CaO']+0.5*ica_test['CaO']
      Na2O=0.4*pls_test['Na2O']+0.6*ica_test['Na2O']
      K2O=0.25*pls_test['K2O']+0.75*ica_test['K2O']

    ;save to a hash since the test sets are sometimes different lengths (array won't work)
        combined_test=hash('SiO2',SiO2,'TiO2',TiO2,'Al2O3',Al2O3,'FeOT',FeOT,'MgO',MgO,'CaO',CaO,'Na2O',Na2O,'K2O',K2O)
        
    ;Optionally produce 1 to 1 plots for the test set data
        if keyword_Set(output1to1) then begin
            xsize=1200
            ysize=1000
            for n=0,n_elements(elems)-1 do begin
               out_1to1,actuals[elems[n]],combined_test[elems[n]],test_names[elems[n]],elems[n]+' ICA+PLS Combined',elems[n]+'_ica_pls_combined_testset_1to1.tif',csvfile=elems[n]+'_testset_combined.csv',xsize=xsize,ysize=ysize
               out_1to1,actuals[elems[n]],PLS_test[elems[n]],names[elems[n]],elems[n]+' PLS',elems[n]+'_PLS_testset_1to1.tif',xsize=xsize,ysize=ysize
               out_1to1,actuals[elems[n]],ICA_test[elems[n]],names[elems[n]],elems[n]+' ICA',elems[n]+'_ICA_testset_1to1.tif',xsize=xsize,ysize=ysize
            endfor
        endif
        ;put everything into one structure to return
        test_info=hash('combined',combined_test,'ICA',ica_test,'PLS',pls_test,'actuals',actuals,'quartiles',quartiles)   
        return,test_info
end

;+
;This function is used to calculate the RMSEP on-the-fly as a function of predicted composition.
;It uses the test set results to create a plot of RMSEP vs composition. This is then smoothed and extrapolated
;and re-sampled to be used as a look-up table for the predictions of unknown targets.
;
;Inputs:
;       predicts = Array containing the predicted compositions that need RMSEPs
;       test_predicts = Hash containing the predicted compositions for the test set
;       test_actuals = Hash containing the actual compositions for the test set
;       elems = string array containing major oxide names
;       makeplot = Optional keyword that produces plots of RMSEP vs composition
;Outputs:
;       rmseps = Array of RMSEP values calculated for each of the predictions in "predicts"
;-
  
function dynamic_rmsep,predicts,test_predicts,test_actuals,elems,makeplot=makeplot
rmseps=predicts*0.0+9999

;get the predictions and actuals for each element
for i=0,n_elements(elems)-1 do begin
  ;calculate the squared errors
  test_sq_errs=(test_predicts[elems[i]]-test_actuals[elems[i]])^2.0
  
  ;Get the RMSEP window size, based on the range of compositions in the test set
  windowsize=0.1
  min_rmsep_num=fix(0.1*n_elements(test_predicts[elems[i]]))
  rmsep_window=max(test_actuals[elems[i]])*windowsize
  
  ;Create an array of "dummy" predictions
  dummypredicts=findgen(100)/100*max(test_actuals[elems[i]])  
  dummy_rmseps=dummypredicts*0.0
  
  ;Loop through the dummy predictions, calculating "local" RMSEPs
  for j=0,n_elements(dummypredicts)-1 do begin
    rmsep_index=where(abs(test_predicts[elems[i]]-dummypredicts[j]) lt rmsep_window)
    ;by default, calculate the RMSEP using test samples with true compositions that are within +/- 10% of the maximum range of the test set
    if n_elements(rmsep_index) ge min_rmsep_num then begin
      if rmsep_index[0] ne -1 then dummy_rmseps[j]=sqrt(mean(test_sq_errs[rmsep_index]))
    endif else begin
    ;If there are fewer samples that meet the above criteria than 10% of the total number of test spectra, then use the nearest 10% of spectra to calculate RMSEP
      rmsep_index=(sort(abs(test_predicts[elems[i]]-dummypredicts[j])))[0:min_rmsep_num-1]
      dummy_rmseps[j]=sqrt(mean(test_sq_errs[rmsep_index]))
    endelse
  endfor
  
  dummy_rmseps_orig=dummy_rmseps ;save a copy of the original dummy rmseps
  dummypredicts_orig=dummypredicts ;save a copy of the original dummy predicts
  
  ;Remove duplicate dummy RMSEP values
  dummypredicts=dummypredicts(uniq(dummy_rmseps,sort(dummy_rmseps)))
  dummy_rmseps=dummy_rmseps(uniq(dummy_rmseps,sort(dummy_rmseps)))
  
  ;re-sort the dummy predicts and rmseps
  dummy_rmseps=dummy_rmseps(sort(dummypredicts))
  dummypredicts=dummypredicts(sort(dummypredicts))
  
  ;Re-interpolate (linear) to cover the gaps so that blending works ok
  ;Removing the duplicate values and then re-interpolating essentially turns some 
  ;"stair-steps" in the dummy RMSEPs into linear slopes
  ;
 ; stop
  dummy_rmseps=interpol(dummy_rmseps,dummypredicts,findgen(100)/100*max(dummypredicts))
  dummypredicts=findgen(100)/100*max(dummypredicts)
  ;smooth the RMSEPs
  dummy_rmseps=gauss_smooth(dummy_rmseps,8,/edge_truncate)
  
  ;Find the extrema of the smoothed RMSEPs
  extremas=extrema(dummy_rmseps)
  ;Get the maximum RMSEP value after the last extremum
  mx = max(extremas)
  endmax=max(dummy_rmseps(mx:*), indx)
  indx = indx+mx   ; Define index of maximum ENDMAX value after index MX 
  ;Define the index of RMSEP values to keep.
  ;The dummy prediction value must be less than the value where endmax occurs, and the RMSEP must be more than 1% lower than endmax 
  ;This ensures that the last few RMSEP points have at least a slightly positive slope, so that when they are extrapolated, 
  ;the RMSEP increases with predicted composition. (This is very ad-hoc, but allows us to calculate a rough RMSEP outside the test set range)
  ; 
  ind=where(dummypredicts lt (dummypredicts(indx))[0] and abs(dummy_rmseps-dummy_rmseps[n_elements(dummy_rmseps)-1]) gt 0.01*dummy_rmseps[n_elements(dummy_rmseps)-1], nind)
  if nind eq 0 then message,'IND is empty, cannot define a subset for RMSEP.'

  ;keep a subset of the dummy predictions and RMSEPs
  dummypredicts=dummypredicts[ind]
  dummy_rmseps=dummy_rmseps[ind]
  
  ;Densely re-sample and extrapolate the resulting curve to use as a look-up table
  dummypredicts_resamp=findgen(10000)/10000*100.
  dummy_rmseps_resamp=interpol(dummy_rmseps,dummypredicts,dummypredicts_resamp)
  
  ;optionally plot the results
  if keyword_set(makeplot) then begin
    window,0
    wset,0
    device,decomposed=0
    loadct,0
    plot,dummypredicts_orig,dummy_rmseps_orig,psym=2,xtitle='Predicted '+elems[i],ytitle='Local RMSEP',xrange=[0,min([100,max(dummypredicts)*3])],yrange=[0,2*max(dummy_rmseps)]
    loadct,13
    
    oplot,dummypredicts_resamp,dummy_rmseps_resamp,psym=3,color=250
    write_tiff,elems[i]+'_RMSEP_vs_predict'+makeplot+'.tif',reverse(tvrd(true=1),3),planarconfig=1,orientation=1
    
  endif
  
  ;Look up the expected RMSEP for the actual predictions
   for j=0,n_elements(predicts[i,*])-1 do begin
       !null = min(abs(predicts[i,j]-dummypredicts_resamp), imin)   ;Find index of minimum value
       rmseps[i,j]=dummy_rmseps_resamp[imin]
   endfor

endfor


return,rmseps
end   


;+
;This function blends together the PLS submodels, based on the blend settings stored in the specified directory.
;Inputs:
;       comps = Hash containing the submodel results
;       blend_array_dir = directory containing the blend settings
;       elems = string array of major oxide labels
;Outputs:
;        blended = Array of blended results      
;-
function pls_blend,comps,blend_array_dir,elems
        blended=comps['full']*0.0        
        for k=0,n_elements(elems)-1 do begin
            ;#reconstruct the blend input settings from the blend array file
            blendarray=rd_tfile(blend_array_dir+elems[k]+'_blend_array.csv',autocol=1,delim=',')
            blend_labels=blendarray[0,*]
            blendarray=blendarray[*,1:*]
            ranges=float(blendarray[0:1,*])
            inrange=fix(blendarray[2,*])
            refpredict=fix(blendarray[3,*])
            toblend=fix(blendarray[4:5,*])
            predicts=[(comps['full'])[k,*],(comps['low'])[k,*],(comps['mid'])[k,*],(comps['high'])[k,*]]
        
            for i=0,n_elements(ranges(0,*))-1 do begin ;#loop over each composition range
                  inrangecheck=where((predicts[inrange[i],*]) gt ranges[0,i] and (predicts[inrange[i],*]) lt ranges[1,i])
                  if inrangecheck[0] ne -1 then begin
                     weight1=1-((predicts[refpredict[i],inrangecheck])-ranges[0,i])/(ranges[1,i]-ranges[0,i])
                     weight2=((predicts[refpredict[i],inrangecheck])-ranges[0,i])/(ranges[1,i]-ranges[0,i])
                     zeros=where(blended[k,inrangecheck] eq 0)
                     if zeros[0] ne -1 then blended[k,inrangecheck[zeros]]=weight1*(predicts[toblend[0,i],inrangecheck[zeros]])+weight2*(predicts[toblend[1,i],inrangecheck[zeros]])
                  endif
            endfor
         endfor
      blended[where(blended lt 0, /null)]=0 ;Set any negative results to zero
      return,blended
end
    
    
;+
;This function applies the spectrum mask and normalization and does the PLS composition calculation
; for each submodel by multiplying the regression coefficients by the spectrum and adding back the y mean. 
; It also keeps track of the pre-norm spectrum total
;Inputs:
;       elems = string array containing major element oxide labels
;       pls_settings = structure containing the pls settings
;       spectra = spectra from unknown target 
;       wvl = array containing the wavelength definitions for the spectrum (used for masking)
;       totals = This keyword returns the spectrum totals prior to normalizatoin       
;;-    
 
function pls_submodels,elems,pls_settings,spectra,wvl,totals=totals
  which_submodel=['full','low','mid','high']
  comps=hash('full',[],'low',[],'mid',[],'high',[],'spect_total',[])

  ;apply the mask and normalization
  spectra=ccam_mask(spectra,wvl,pls_settings['maskfile'],masked_wvl=masked_wvl)
  spectra_norm1=ccam_norm(spectra,masked_wvl,1,totals=totals)
  spectra_norm3=ccam_norm(spectra,masked_wvl,3)
  nshots=n_elements(spectra_norm1[0,*])
  
  for n=0,n_elements(which_submodel)-1 do begin
    for j=0,n_elements(elems)-1 do begin
        labelindex=where(pls_settings['labels'] eq elems[j]+'_'+which_submodel[n], nl)
        if nl eq 0 then message,'No submodel for: '+elems[j]+'_'+which_submodel[n]
        y_mean=rebin([(pls_settings['ymeancenters'])[labelindex]],1,nshots)
        fullnorm=(pls_settings['norms'])[labelindex]
        full_coeff=(pls_settings['coeffs'])[labelindex,*]
        full_meancenter=rebin(reform((pls_settings['meancenters'])[labelindex,*]),$
          n_elements((pls_settings['meancenters'])[labelindex,*]),nshots)
        ;Explicitly check the length of the vectors used to calculate compositions
        lencheck='Pass'
        if n_elements(spectra_norm1[*,0]) ne n_elements(full_meancenter[*,0]) then lencheck='Fail'
        if n_elements(spectra_norm1[*,0]) ne n_elements(full_coeff) then lencheck='Fail'
        
        if lencheck eq 'Fail' then begin
          xmess ,"Vectors are not the same length! Exiting."
          exit
        endif
   
        if fullnorm eq 1 then comp=matrix_multiply(full_coeff,spectra_norm1-full_meancenter)+y_mean
        if fullnorm eq 3 then comp=matrix_multiply(full_coeff,spectra_norm3-full_meancenter)+y_mean
        comps[which_submodel[n]]=[comps[which_submodel[n]],comp]
    endfor
  endfor
  
  plsvals=pls_blend(comps,pls_settings['blend_array_dir'],elems)
  return,plsvals
end         



;+
;This function does the PLS calculations. It is called by pls_and_ica in a loop, once for each file.  
;
;Inputs:
;       spectra = array containing input spectra
;       wvl = array containing the wavelengths of each bin in spectra
;       pls_results = hash containing the results
;       file_data = hash containing file name and associated metadata
;       pls_settings = structure containing all the required settings to run PLS
;       elems = string array of major element oxide labels
;Outputs:
;       pls_results = hash containing the blended submodel results along with associated metadata
;-
function pls,spectra,wvl,pls_results,file_data,pls_settings,elems
    
    shotnum=indgen(n_elements(spectra[0,*]))
    nshots=file_data['nshots']
    ;Run PLS calculations
       
    pls_results['comps']=[[pls_results['comps']],[pls_submodels(elems,pls_settings,spectra,wvl,totals=totals)]]
    pls_results['files']=[pls_results['files'],replicate(file_data['file'],nshots)]
    pls_results['shotnum']=[pls_results['shotnum'],shotnum]
    pls_results['targets']=[pls_results['targets'],replicate(file_data['target'],nshots)]
    pls_results['dists']=[pls_results['dists'],replicate(file_data['dist'],nshots)]
    pls_results['amps']=[pls_results['amps'],replicate(file_data['amps'],nshots)]
    pls_results['totals']=[pls_results['totals'],totals]
    
    return,pls_results

end

;+
;This program combined the results of the ICA and PLS calculations according to the settings determined by Roger and Sylvestre
;Inputs:
;       plsvals
;Outputs:
;       The specified result files will be written in the search directory
;-
function ica_pls_combine,plsvals,icavals
    ;Combine the PLS and ICA results
    ;Settings for these combinations derived by Roger and Sylvestre
    
    TiO2=0.5*plsvals[1,*]+0.5*icavals[1,*]
    Al2O3=0.75*plsvals[2,*]+0.25*icavals[2,*]
    Al2O3index=where(Al2O3 lt 15.0, nal)
    if nal gt 0 then $ 
        Al2O3[Al2O3index]=0.06667*Al2O3[Al2O3index]^2+(1-0.06667*Al2O3[Al2O3index])*icavals[2,[Al2O3index]]
    FeOT=0.75*plsvals[3,*]+0.25*icavals[3,*]
    SiO2temp=0.5*plsvals[0,*]+0.5*icavals[0,*]
    SiO2=SiO2temp
    test1 = where(FeOT gt 30, nt1)
    test2 = where(FeOT le 30 and SiO2temp ge 30, nt2)
    test3 = where(FeOT le 30 and SiO2temp lt 30, nt3)
    if nt1 gt 0 then SiO2[test1]=0.75*plsvals[0,[test1]]+0.25*icavals[0,[test1]]
    if nt2 gt 0 then SiO2[test2]=SiO2temp[test2]
    if nt3 gt 0 then SiO2[test3]=SiO2temp[test3]*SiO2temp[test3]*0.03333+(1-0.0333*SiO2temp[test3])*icavals[0,[test3]]
    MgO=0.5*plsvals[4,*]+0.5*icavals[4,*]
    CaO=0.5*plsvals[5,*]+0.5*icavals[5,*]
    Na2O=0.4*plsvals[6,*]+0.6*icavals[6,*]
    K2O=0.25*plsvals[7,*]+0.75*icavals[7,*]
      
    ica_pls_combined=[SiO2,TiO2,Al2O3,FeOT,MgO,CaO,Na2O,K2O]
    ;print,ica_pls_combined
    
    return,ica_pls_combined
end

;+
;This program writes the quantitative ChemCam results to an output file.
;Inputs:
;       results = this is a structure containing the quantitative results (ICA, PLS, or combined) and rmseps and stdevs
;       file_data = this hash contains metadata for the results (file name, target, distance, laser power etc)
;       elems = this is a string array containing the major oxide labels
;       searchdir =  The directory that was searched for valid ChemCam files (results are written to this directory)
;       testset_quartiles = quartiles calculated for the test set
;       software_version = Name, version number, and date of the current software
;       ica = Set to 1 (and provide ICA results in 'results') to output ICA results
;       pls = Set to 1 (and provide PLS results in 'results') to output PLS results
;       stdevs = Set to 1 to include single shot standard deviations with the averaged results
;       shots = set to 1 for single shot results
;Outputs:
;       The specified result files will be written in the search directory
;-
pro write_results,results,file_data,elems,searchdir,testset_quartiles,software_version,ica=ica,pls=pls,stdevs=stdevs,shots=shots
    if keyword_set(shots) and keyword_set(stdevs) then begin
      xmess,"Warning: stdevs can't be included for single shot results!"
      return
    endif
    
    if keyword_set(iva) and keyword_set(pls) then begin
      xmess,"Warning: Both ICA and PLS keywords are set. This script only handles results from one method at a time."
      return
    endif
    
    ;Set the appropriate hash key to use to access results
    if keyword_set(shots) then resultkey='shots' else resultkey='means'
    
    ;get the current date
    caldat,systime(/jul),mm,dd,yy
    yy=strtrim(yy,2)
    mm=strtrim(mm,2)
    if strlen(mm) eq 1 then mm='0'+mm
    dd=strtrim(dd,2)
    if strlen(dd) eq 1 then dd='0'+dd
    today=yy+mm+dd
   
    ;Set up the output array
    if keyword_set(shots) then begin
       labelrow=['File','Target','Shot Number'] 
       output=[[file_data['filelist']],[file_data['targets']],[strtrim(file_data['shotnum']+1,2)]]  
    endif else begin
       labelrow=['File','Target']
       output=[[file_data['filelist']],[file_data['targets']]]
    endelse
    output=transpose(output)
    pad=strarr(n_elements(labelrow)-1,6) ;create an empty padding array to use later
    
    ;add columns for RMSEPs and, if needed, stdevs
    if keyword_Set(stdevs) then begin
       for n=0,n_elements(elems)-1 do labelrow=[labelrow,elems[n],'+/-',elems[n]+' RMSEP',elems[n]+'_shots_stdev']
       spacer=3
    endif else begin
       for n=0,n_elements(elems)-1 do labelrow=[labelrow,elems[n],'+/-',elems[n]+' RMSEP']
       spacer=2
       
    endelse
    labelrow=[labelrow,'Sum of Oxides','Distance (m)','Laser Power','Spectrum Total']
    
    ;set up output file name
    outputfile=searchdir+'ccam_comps'
    if keyword_Set(pls) then outputfile=outputfile+'_pls' else if keyword_set(ica) then outputfile=outputfile+'_ica'
    if keyword_set(shots) then outputfile=outputfile+'_singleshots'
    outputfile=outputfile+'_'+today+'.csv'
    
    ;get composition totals
    comptotals=[total(results[resultkey],1)]
    comptotals=string(comptotals,format='(F0.2)') 
    
    ;Set up the quartile info for the top of the file
    testset_quartiles_out=[[elems[0],replicate(' ',spacer)],[transpose(strtrim(testset_quartiles[*,0],2)),replicate(' ',spacer,5)]]
    for n=1,n_elements(elems)-1 do testset_quartiles_out=[testset_quartiles_out,[[elems[n],replicate(' ',spacer)],[transpose(strtrim(testset_quartiles[*,n],2)),replicate(' ',spacer,5)]]]
    quartile_labels=['Testset Quartiles','Min','1st','Med','3rd','Max']
    
    testset_quartiles_out=[transpose(quartile_labels),testset_quartiles_out]
    testset_quartiles_out=[pad,testset_quartiles_out,[strarr(4,6)]]
    labelrow=[[testset_quartiles_out],[labelrow]]
    
    ;Create an array full of plus-minus signs of the same length as the output array
    plusminus=transpose(strarr(n_elements(results[resultkey,0,*]))+'+/-')
    
    ;round the compositions and RMSEPs to an appropriate number of digits
    formats=['(F0.1)','(F0.2)','(F0.1)','(F0.1)','(F0.1)','(F0.1)','(F0.2)','(F0.2)']
    results_rounded=strarr(size(results[resultkey],/dim))
    rmseps_rounded=strarr(size(results[resultkey],/dim))
    for i=0,n_elements(elems)-1 do begin
      results_rounded[i,*]=string(results[resultkey,i,*],format=formats[i])
      rmseps_rounded[i,*]=string(results[resultkey+'_rmseps',i,*],format=formats[i])
    endfor
    
    ;Add the compositions, totals, RMSEPs (and stdevs if specified) to the output array   
    if keyword_set(stdevs) then begin
        ;Round the stdevs
        stdevs_rounded=strarr(size(results[resultkey],/dim))
        for i=0,n_elements(elems)-1 do begin
          stdevs_rounded[i,*]=string(results['stdevs',i,*],format=formats[i])
          output=[output,results_rounded[i,*],plusminus,rmseps_rounded[i,*],stdevs_rounded[i,*]]
        endfor
    endif else begin
        for i=0,n_elements(elems)-1 do begin
          output=[output,results_rounded[i,*],plusminus,rmseps_rounded[i,*]]
        endfor
    endelse
    output=[output,transpose([comptotals]),transpose(strtrim(file_data['dists'],2)),transpose(file_data['amps']),transpose(strtrim(file_data['totals'],2))]
    output=[[labelrow],[output]]
    
    ;Add the software version
    output[0,0]=software_version
        
    ;Label what type of results these are
    output[0,1]='COMBINED PLS+ICA RESULTS'
    if keyword_set(pls) then output[0,1]='PLS RESULTS'
    if keyword_set(ica) then output[0,1]='ICA RESULTS'
    
    write_csv,outputfile,output
end
  
function label_energy,labelx,labely,xdata,ydata
   energy=0
   for i=0,n_elements(labelx)-1 do begin
       d=sqrt((labelx[i]-xdata)^2.+(labely[i]-ydata)^2)
       d=d(where(d ne 0))
       energy=energy+total(d^(-2.0))
       
   endfor
   return,energy
end

;This function tests whether two lines intersect, based on their end points
;Line one goes from A to B, Line 2 goes from C to D
;Line one = [[Ax,Ay],[Bx,By]]
;Line two = [[Cx,Cy],[Dx,Dy]]
function lines_intersect,line1,line2
   Ax=line1[0,0]
   Ay=line1[1,0]
   Bx=line1[0,1]
   By=line1[1,1]
   
   Cx=line2[0,0]
   Cy=line2[1,0]
   Dx=line2[0,1]
   Dy=line2[1,1]

   ;Test whether points A and B are on the same side of line CD
   test1=(Dx-Cx)*(Ay-Dy)-(Dy-Cy)*(Ax-Dx)
   test2=(Dx-Cx)*(By-Dy)-(Dy-Cy)*(Bx-Dx)
   
   ;Test whether points C and D are on the same side of line AB
   test3=(Bx-Ax)*(Cy-By)-(By-Ay)*(Cx-Bx)
   test4=(Bx-Ax)*(Dy-By)-(By-Ay)*(Dx-Bx)

   ;The lines intersect iff A and B are on different sides of CD and C and D are on different sides of AB
   if (total(signum([test1,test2])) eq 0) and (total(signum([test3,test4])) eq 0) then intersect=1 else intersect=0

  return,intersect

end

pro refplots,refdata_file,combined_results,file_data,xel,yel,elems,figfile,xrange=xrange,yrange=yrange
  ;index the data matching the element of interest
  xind=(where(elems eq xel))[0]
  
  ;create axis labels
  yind=(where(elems eq yel))[0]
  xtitle=xel+' wt.%'
  ytitle=yel+' wt.%'
  
  ;Read reference data
  refdata=rd_tfile(refdata_file,delim=',',/autocol)
  refnames=refdata[1:*,0]
  refsyms=refdata[1:*,1]
  ref_aves=float(refdata[1:*,3:11])
  ref_stdevs=float(refdata[1:*,14:*])
  
  ;Get the average comps and the error bars  
  ref_aves_x=ref_aves[*,xind]
  ref_aves_y=ref_aves[*,yind]
  ref_stdevs_x=ref_stdevs[*,xind]
  ref_stdevs_y=ref_stdevs[*,yind]
  
  ;create vectors to store all x and y coordinates, to be used when placing labels to avoid data
  xall=[transpose((combined_results['means'])[xind,*]),ref_aves_x]
  yall=[transpose((combined_results['means'])[yind,*]),ref_aves_y]
  
  
 ;Add error bars to xall yall so they repel labels
;  for a=0,n_elements(ref_stdevs_x)-1 do begin
;    xerr_pts=findgen(10)/10*(2*ref_stdevs_x[a])+ref_aves_x[a]-ref_stdevs_x[a]
;    yerr_pts=fltarr(10)+ref_aves_y[a]
;    
;    yerr_pts=[yerr_pts,findgen(10)/10*(2*ref_stdevs_y[a])+ref_aves_y[a]-ref_stdevs_y[a]]
;    xerr_pts=[xerr_pts,fltarr(10)+ref_aves_x[a]]
;    
;    xall=[xall,xerr_pts]
;    yall=[yall,yerr_pts]
;    
;  endfor
  
  ;set ranges if not already defined
  if not(keyword_set(xrange)) then xrange=[min([0,xall]),1.1*max(xall)]
  if not(keyword_set(yrange)) then yrange=[min([0,yall]),1.1*max(yall)]
  
  ;add plot borders to the xall yall arrays to repel labels
  xall=[xall,findgen(100)/100*(max(xrange)-min(xrange))+min(xrange),findgen(100)/100*(max(xrange)-min(xrange))+min(xrange),fltarr(100)+min(xrange),fltarr(100)+max(xrange)]
  yall=[yall,fltarr(100)+min(yrange),fltarr(100)+max(yrange),findgen(100)/100*(max(yrange)-min(yrange))+min(yrange),findgen(100)/100*(max(yrange)-min(yrange))+min(yrange)]

  
  ;Create a list of colors and symbols to loop through when plotting data
  plotcolors=['Crimson','Forest Green','Royal Blue','Aquamarine','Orchid'] ;using defined colors from coyote library
  plotsyms=[14,16,17,18,19,20,45] ;using filled symbols from the coyote library
  colorind=0
  symind=0

  ;Get a list of unique targets
  unique_targets=(file_data['targets'])(uniq(file_data['targets'],sort(file_data['targets'])))
  
  ;loop through unique targets, plotting each one
  for i=0,n_elements(unique_targets)-1 do begin
    ;get x and y coordinates
    target_index=where(file_data['targets'] eq unique_targets[i])
    x=(combined_results['means'])[xind,target_index]
    y=(combined_results['means'])[yind,target_index]
    
    ;on the first iteration, create the plot
    if i eq 0 then begin
      window,0,xsize=3000,ysize=2400,/pixmap
      DEVICE, SET_FONT='Arial', /TT_FONT  ;use a nice-looking font
      cgplot,x,y,psym=plotsyms[symind],color=plotcolors[colorind],xrange=xrange,yrange=yrange,xthick=5,ythick=5,$
        xtitle=xtitle,ytitle=ytitle,symsize=5,charsize=7,charthick=5,font=1
      ;start collecting info to use when drawing the legend
      legendnames=unique_targets[i]
      legendsyms=plotsyms[symind]
      legendsymcolors=plotcolors[colorind]
      
    endif else begin
      ;on subsequent iterations, overplot the data points and add to the legend info
      cgplot,x,y,psym=plotsyms[symind],color=plotcolors[colorind],/overplot,symsize=5
      legendnames=[legendnames,unique_targets[i]]
      legendsyms=[legendsyms,plotsyms[symind]]
      legendsymcolors=[legendsymcolors,plotcolors[colorind]]
      
    endelse

    ;increment the color and symbol indices. Loop them around if needed so they still point at a valid value
    colorind=colorind+1
    if colorind ge n_elements(plotcolors) then begin
      colorind=0
      symind=symind+1 ;increment to a new symbol once all colors have been used up for the current symbol
    endif
    if symind ge n_elements(plotsyms) then begin
      symind=0
    endif
    

  endfor
  
  ;create empty arrays to hold the label coordinates
  x_labels=fltarr(n_elements(refnames))
  y_labels=fltarr(n_elements(refnames))
  
  ;step through each of the reference values
  for k=0,n_elements(refnames)-1 do begin
    ;plot the reference values with error bars
    cgplot,ref_aves_x[k],ref_aves_y[k],psym=fix(refsyms[k]),/overplot,err_ylow=ref_stdevs_y[k],symsize=4,$
      err_yhigh=ref_stdevs_y[k],err_xlow=ref_stdevs_x[k],err_xhigh=ref_stdevs_x[k],color='black',/err_clip,err_width=0.002,err_thick=2
    
    ;create an array of angles and radii to define possible locations for labels around the reference point
    ;exclude angles too close to verticl or horizontal to avoid conflict with error bars
    t_labels_temp=[findgen(25)/25*70+10,findgen(25)/25*70+100,findgen(25)/25*70+190,findgen(25)/25*70+280]*((2*!pi)/360.)
     
    r_labels_temp=[0.1+fltarr(n_elements(t_labels_temp))]
   
    
    ;convert the angles and radii to x and y
    x_labels_temp=ref_aves_x[k]+r_labels_temp*cos(t_labels_temp)*max(xrange)
    y_labels_temp=ref_aves_y[k]+r_labels_temp*sin(t_labels_temp)*max(yrange)

    ;force the coordinates to be within the plot area
    xtoosmall=where(x_labels_temp lt min(xrange))
    ytoosmall=where(y_labels_temp lt min(yrange))
    xtoobig=where(x_labels_temp gt max(xrange))
    ytoobig=where(y_labels_temp gt max(yrange))
    
    if xtoosmall[0] ne -1 then x_labels_temp[xtoosmall]=min(xrange)
    if ytoosmall[0] ne -1 then y_labels_temp[ytoosmall]=min(yrange)
    if xtoobig[0] ne -1 then x_labels_temp[xtoobig]=max(xrange)
    if ytoobig[0] ne -1 then y_labels_temp[ytoobig]=max(yrange)

    ;remove any label coordinates that would result in the line crossing a previous label line
    intersect_check=fltarr(n_elements(x_labels_temp))  ;create an empty array to hold the results
    for n=0,n_elements(t_labels_temp)-1 do begin
       line1=[[ref_aves_x[k],ref_aves_y[k]],[x_labels_temp[n],y_labels_temp[n]]]  ;define line1 from the label options
       
       for m=0,n_elements(x_labels)-1 do begin
           if x_labels[m] ne 0 then begin
             line2=[[ref_aves_x[m],ref_aves_y[m]],[x_labels[m],y_labels[m]]] ;define line2 from the perviously set labels
          
             check=lines_intersect(line1,line2)  ;check whether they intersect
             if check ne 0 then intersect_check[n]=check  ;if so, record it
           endif
      endfor
    endfor
    
    ;keep only the label placement options that don't intersect (unless all options intersect)
    if (where(intersect_check eq 0))[0] ne -1 then begin
      x_labels_temp=x_labels_temp(where(intersect_check eq 0))
      y_labels_temp=y_labels_temp(where(intersect_check eq 0))
      t_labels_temp=t_labels_temp(where(intersect_check eq 0))
      r_labels_temp=r_labels_temp(where(intersect_check eq 0))

    endif
    
    
    ;calculate the "energy" of each possible label location based on inverse squared distance from plotted data
    ;This is somewhat analogous to the potential energy of a charged particle when placed among other particles of the same charge
    ;In other words, choosing the lowest energy label location effective means the data "repels" the label
    ;making it less likely that it will overlap something interesting on the plot
    energy=fltarr(n_elements(x_labels_temp))
    
    for n=0,n_elements(x_labels_temp)-1 do begin
      ;temporarily add the annotation line to xall,yall to be used in repelling
      dx_temp=x_labels_temp[n]-ref_aves_x[k]
      dy_temp=y_labels_temp[n]-ref_aves_y[k]
      linx=findgen(10)/10*dx_temp+ref_aves_x[k]
      liny=findgen(10)/10*dy_temp+ref_aves_y[k]
      xall_temp=[xall,x_labels_temp[n]]
      yall_temp=[yall,y_labels_temp[n]]
      
      ;calculate the "energy" for this potential annotation line
      energy[n]=label_energy(linx,liny,xall,yall)
    endfor

    ;Choose the label location with the lowest energy
    x_labels[k]=(x_labels_temp(where(energy eq min(energy))))[0]
    y_labels[k]=(y_labels_temp(where(energy eq min(energy))))[0]

    ;add the annotation line to xall, yall to repel other labels
    x=[ref_aves_x[k],x_labels[k]]
    y=[ref_aves_y[k],y_labels[k]]
    
    dx=x[1]-x[0]
    dy=y[1]-y[0]
    linx=findgen(10)/10*dx+x[0]
    liny=findgen(10)/10*dy+y[0]
    xall=[xall,linx]
    yall=[yall,liny]
   
    ;draw the annotation line
    cgplot,x,y,/overplot,linestyle=0,thick=3,font=1,color='Gray'
    
    ;set the text alignment
    alignment=[0.0,0.5]
    if dx gt 0 and abs(dx) ge abs(dy) then alignment=[0.0,0.5]
    if dx gt 0 and abs(dx) lt abs(dy) then alignment=[0.5,1.0]
    if dx lt 0 and abs(dx) ge abs(dy) then alignment=[1.0,0.5]
    if dx lt 0 and abs(dx) lt abs(dy) then alignment=[0.5,0]

    ;write annotation text
    newline='!C'
    cgtext,x[1],y[1],strjoin(strsplit(refnames[k],' ',/extract),newline),alignment=alignment[0],charsize=4,charthick=5,font=1
    
  endfor
  ;write the legend
  al_legend,legendnames,psym=legendsyms,colors=legendsymcolors,symsize=5,charsize=4,charthick=5,font=1
  write_png,figfile,tvrd(true=1)

end    

    
    
;+
;This program runs the ICA and PLS calculations.
;Inputs:
;       file_data = Hash containing the file list and associated metadata
;       pls_settings = Hash containing the settings for PLS
;       elems = String array containing major oxide names
;       test_info = Hash containing the test set results
;       searchdir = String with the path for the search directory
;       software_version = String containing the software version, name, and date
;       shots = Set this to 1 to calculate single shot results
;       quiet = Set this to 1 to suppress pop-ups
;       calcstdevs = If shots = 1 and calcstdevs = 1, calculate the standard deviations of single shot results if shots also equals 1. 
;                    If shots = 0 and calcstdevs = 1, then write the stdevs of single shot results in the means output file
;       ica_output = Set to 1 to write the ICA output
;       pls_output = Set to 1 to write the PLS output
;Outputs:
;      Calculation results are written to .csv files in the search directory
;;-
pro pls_and_ica,file_data,pls_settings,elems,test_info,searchdir,software_version,shots=shots,quiet=quiet,calcstdevs=calcstdevs,ica_output=ica_output,pls_output=pls_output,refdata_files=refdata_files,refdata_names=refdata_names
       
       ;create the hashes to contain the results
        pls_results=hash('means',[],'shots',[])
        combined_results=hash('means',[],'shots',[])
        
        ;if not(keyword_Set(shots)) then shots=1
        if keyword_Set(calcstdevs) then begin
          both=1
        endif
       ;Get the ICA results first
       ica_results = ICR(file_data['pathlist']+file_data['filelist'],shot=shots,fn_good_index=fn_good_index,quiet=quiet,both=both)
       
       ica_shots_ptr=ica_results['shots']
       if keyword_Set(shots) then begin
        
           ica_comps=*(ica_results['shots'])[0]
           for i=1,n_elements(ica_results['shots'])-1 do ica_comps=[ica_comps,*(ica_results['shots'])[i]]
           ica_results['shots']=transpose(ica_comps)
       endif
       
       ica_results['means']=transpose(ica_results['means'])
       ;get RMSEPs and put them in the results hash
       if not(keyword_set(shots)) or keyword_set(calcstdevs) then ica_results=ica_results+hash('means_rmseps',dynamic_rmsep(ica_results['means'],test_info['ICA'],test_info['actuals'],elems))
       if keyword_set(shots) or keyword_set(calcstdevs) then ica_results=ica_results+hash('shots_rmseps',dynamic_rmsep(ica_results['shots'],test_info['ICA'],test_info['actuals'],elems))
       
       ;ICA does not use certain files. Remove these from the list before proceeding to PLS  
       
       file_data_keys=file_data.keys()
       for n=0,n_elements(file_data_keys)-1 do file_data[file_data_keys[n]]=file_data[file_data_keys[n],fn_good_index]
       
      
      ;Loop through each file in the file list, restore it and and run PLS calculations
        shotstext=' '
        if keyword_set(shots) and not(keyword_set(calcstdevs)) then shotstext=' single-shot '
        if keyword_set(calcstdevs) then shotstext=' single-shot and mean ' else shotstext=' '
        if not(quiet) then progbar=Obj_New('cgProgressBar',/start,percent=0,title=$
        'Running'+shotstext+'PLS calculation for '+strtrim(n_elements(file_data['filelist']),2)+' files',xsize=375)
        
        ;Create a new hash to hold the expanded metadata for single shot results
        file_data_shots=hash('sols',[],'filelist',[],'shotnum',[],'targets',[],'dists',[],'amps',[],'totals',[],'sclock',[])
        ;Also add totals to the file data hash
        file_data=file_data+hash('totals',[])
        
        for i=0,n_elements(file_data['filelist'])-1 do begin
           restore,file_data['pathlist',i]+file_data['filelist',i],/relaxed
           wvl=[defuv,defvis,defvnir]
           spectra=[transpose(uv),transpose(vis),transpose(vnir)]
           spectra_mean=[auv,avis,avnir]
           
           shotnum=indgen(n_elements(spectra[0,*]))
           
            nshots=file_data['nshots',i]
           
           ;Calculate single shot results and fill in the single shot metadata
           if keyword_set(shots) or keyword_set(calcstdevs) then begin
              pls_results['shots']=[[pls_results['shots']],[pls_submodels(elems,pls_settings,spectra,wvl,totals=totals)]]
              combined_results['shots']=ica_pls_combine(pls_results['shots'],ica_results['shots'])
              file_data_shots['filelist']=[file_data_shots['filelist'],replicate(file_data['filelist',i],nshots)]
              file_data_shots['shotnum']=[file_data_shots['shotnum'],shotnum]
              file_data_shots['targets']=[file_data_shots['targets'],replicate(file_data['targets',i],nshots)]
              file_data_shots['dists']=[file_data_shots['dists'],replicate(file_data['dists',i],nshots)]
              file_data_shots['amps']=[file_data_shots['amps'],replicate(file_data['amps',i],nshots)]
              file_data_shots['sclock']=[file_data_shots['sclock'],replicate(file_data['sclock',i],nshots)]
              file_data_shots['sols']=[file_data_shots['sols'],replicate(file_data['sols',i],nshots)]
              file_data_shots['totals']=[file_data_shots['totals'],totals]
           endif
           ;calculate mean results
           if not(keyword_set(shots)) or keyword_Set(calcstdevs) then begin
              pls_results['means']=[[pls_results['means']],[pls_submodels(elems,pls_settings,spectra_mean,wvl,totals=totals)]]
              combined_results['means']=ica_pls_combine(pls_results['means'],ica_results['means'])
              file_data['totals']=[file_data['totals'],totals]
           endif
           
           if not(quiet) then  progbar -> Update,float(i+1)/n_elements(file_data['filelist'])*100
        endfor
      if not(quiet) then progbar->Destroy
       
      ;Get RMSEPs 
      if keyword_Set(shots) or keyword_set(calcstdevs) then begin
         pls_results=pls_results+hash('shots_rmseps',dynamic_rmsep(pls_results['shots'],test_info['PLS'],test_info['actuals'],elems))
         combined_results=combined_results+hash('shots_rmseps',dynamic_rmsep(combined_results['shots'],test_info['PLS'],test_info['actuals'],elems))
      endif
      if not(keyword_set(shots)) or keyword_set(calcstdevs) then begin
         pls_results=pls_results+hash('means_rmseps',dynamic_rmsep(pls_results['means'],test_info['PLS'],test_info['actuals'],elems))    
         combined_results=combined_results+hash('means_rmseps',dynamic_rmsep(combined_results['means'],test_info['combined'],test_info['actuals'],elems))
      endif
      
        
       ;If shots and calcstdevs are set, then get the stdev of the single shot results
       if keyword_set(calcstdevs) then begin
           combined_stdev=dblarr(n_elements(elems),n_elements(file_data['filelist']))
           pls_stdev=dblarr(n_elements(elems),n_elements(file_data['filelist']))
           ica_stdev=dblarr(n_elements(elems),n_elements(file_data['filelist']))
           for i=0,n_elements(file_data['filelist'])-1 do begin
              ind=where(file_data_shots['filelist'] eq file_data['filelist',i])
              ind2=where(file_data_shots['shotnum',ind]+1 ge 6) ;calculate stdev of shots 6 and higher
              combined_stdev[*,i]=0
              pls_stdev[*,i]=0
              ica_stdev[*,i]=0
              if ind2[0] ne -1 then begin
                 if n_elements(ind[ind2]) gt 1 then begin
                    combined_stdev[*,i]=stddev(combined_results['shots',*,ind[ind2]],dimension=2)
                    pls_stdev[*,i]=stddev(pls_results['shots',*,ind[ind2]],dimension=2)
                    ica_stdev[*,i]=stddev(ica_results['shots',*,ind[ind2]],dimension=2)
                 endif 
              endif
           endfor
           
           combined_results=combined_results+hash('stdevs',combined_stdev)
           ica_results=ica_results+hash('stdevs',ica_stdev)
           pls_results=pls_results+hash('stdevs',pls_stdev)
        endif
        
;make figures
  if refdata_files ne '' then begin
    if quiet eq 0 then xmess,'Making composition plots...',/nowait,wid=id
    for refn=0,n_elements(refdata_files)-1 do begin
      refplots,refdata_files[refn],combined_results,file_data,'SiO2','FeOT',elems,searchdir+'comp_plot_FeOTvsSiO2_'+refdata_names[refn]+'.png'
      refplots,refdata_files[refn],combined_results,file_data,'SiO2','MgO',elems,searchdir+'comp_plot_MgOvsSiO2_'+refdata_names[refn]+'.png'
      refplots,refdata_files[refn],combined_results,file_data,'Al2O3','CaO',elems,searchdir+'comp_plot_CaOvsAl2O3_'+refdata_names[refn]+'.png'
      refplots,refdata_files[refn],combined_results,file_data,'Na2O','K2O',elems,searchdir+'comp_plot_K2OvsNa2O_'+refdata_names[refn]+'.png'
     endfor
    if quiet eq 0 then widget_control, /dest, id
  endif
        
        ;Write the appropriate output files, given the input options
        if keyword_set(shots) then begin
          if keyword_set(ica_output) then write_results,ica_results,file_data_shots,elems,searchdir,test_info['quartiles'],software_version,ica=1,pls=0,stdevs=0,shots=1
          if keyword_set(pls_output) then write_results,pls_results,file_data_shots,elems,searchdir,test_info['quartiles'],software_version,ica=0,pls=1,stdevs=0,shots=1
          write_results,combined_results,file_data_shots,elems,searchdir,test_info['quartiles'],software_version,ica=0,pls=0,stdevs=0,shots=1
        endif
        if not(keyword_set(shots)) or keyword_set(calcstdevs) then begin
          if keyword_set(ica_output) then write_results,ica_results,file_data,elems,searchdir,test_info['quartiles'],software_version,ica=1,pls=0,stdevs=calcstdevs,shots=0
          if keyword_set(pls_output) then write_results,pls_results,file_data,elems,searchdir,test_info['quartiles'],software_version,ica=0,pls=1,stdevs=calcstdevs,shots=0
          write_results,combined_results,file_data,elems,searchdir,test_info['quartiles'],software_version,ica=0,pls=0,stdevs=calcstdevs,shots=0
        endif
        
end


;This program is the master program for calculating compositions. It calls all the various sub-programs. See documentation at the top of this file.
pro calc_comp,searchdir,shots,recursive,configfile,software_version,quiet=quiet,pls_output=pls_output,ica_output=ica_output,calcstdevs=calcstdevs
    if not(keyword_set(quiet)) then quiet=0 ;default to allow progress bars and other pop-ups
    
    ;get config settings from file
    configdata=rd_tfile(configfile,autocol=1,delim=',')
    configdata=repstr(repstr(configdata,'"',''),'\','/') ;strip out any quotes and make all slashes uniform
    
    ;put the masterlist files into an array to be passed to ccam_filelist_targets
    masterlist1=configdata[1,1]
    masterlist2=configdata[1,2]
    masterlist3=configdata[1,3]
    masterlist=[masterlist1,masterlist2,masterlist3]
    
    ;get the other config info
    maskfile=configdata[1,4]
    meancenters_file=configdata[1,5]
    settings_coeffs_file=configdata[1,6]
    blend_array_dir=configdata[1,7]
    testresult_dir=configdata[1,8]
    searchstring=configdata[1,9]
    refdata_files=strsplit(configdata[1,10],';',/extract)
    refdata_names=strsplit(configdata[1,11],';',/extract)
    
    

    
    ;read the meancenter file and get data
    meancenters=rd_tfile(meancenters_file,autocol=1,delim=',')
    meancenter_labels=meancenters[1:*,0]
    ymeancenters=double(meancenters[1:*,1])
    meancenters=double(meancenters[1:*,2:*])
    
    ;extract pls settings and coefficients from the file and define structure of info for PLS calculations
    pls_settings=rd_tfile(settings_coeffs_file,autocol=1,delim=',')
    pls_settings=hash('labels',pls_settings[1:*,0],'norms',fix(pls_settings[1:*,1]),'ncs',fix(pls_settings[1:*,2]),$
      'coeffs',double(pls_settings[1:*,3:*]),'ymeancenters',ymeancenters,'meancenters',meancenters,$
      'maskfile',maskfile,'blend_array_dir',blend_array_dir)
         
    elems=['SiO2','TiO2','Al2O3','FeOT','MgO','CaO','Na2O','K2O']
          
    test_info=get_testset_info(testresult_dir,elems)
        
    if not(quiet) then xmess,"Reading files matching "+searchstring+" in "+searchdir,/nowait,wid=wid
    file_data=ccam_filelist(searchdir,searchstring=searchstring,minsol=0,maxsol=999999,recursive=recursive)
    if not(quiet) then widget_control,/dest,wid
;     stop
    ;Look up target info
    file_data=ccam_filelist_targets(masterlist,file_data,quiet=quiet)
   ; stop
    pls_and_ica,file_data,pls_settings,elems,test_info,searchdir,software_version,shots=shots,quiet=quiet,calcstdevs=calcstdevs,ica_output=ica_output,pls_output=pls_output,refdata_files=refdata_files,refdata_names=refdata_names
   
  
end
 
