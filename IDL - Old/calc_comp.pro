pro plot_1to1,actual,predict,title=title,outfile=outfile
    prettyplot,actual,predict,psym=0,color=0,thick=0,xtitle='Actual wt.%',ytitle='Predicted wt.%',charsize=2,$
       xthick=2,ythick=2,oplot=0,symsize=0.75,xsize=1200,ysize=1000,title=title,xrange=[0,max(actual*1.1)],yrange=[0,max(predict)*1.1],winnum=0
    prettyplot,[0,100],[0,100],linestyle=0,oplot=1
    write_tiff,outfile,reverse(tvrd(),2),compression=1
        
end

function get_testset_info,testresult_dir,elems,quartiles=quartiles,actuals=actuals,ica_test=ica_test,pls_test=pls_test,output1to1=output1to1
      ;Read the actual FeOT comps for the SiO2 test set (to be used in combining ICA and PLS SiO2 results) 
      SiO2_test_FeOT_true=float((rd_tfile(testresult_dir+'SiO2_testset_FeOT_comps.csv',2,delim=','))[1,1:*])
      
      ;Read the PLS test set predictions
      SiO2_pls_test=rd_tfile(testresult_dir+elems[0]+'_testset_blended.csv',3,delim=',');[1:*,*]
      TiO2_pls_test=rd_tfile(testresult_dir+elems[1]+'_testset_blended.csv',3,delim=',');[1:*,*]
      Al2O3_pls_test=rd_tfile(testresult_dir+elems[2]+'_testset_blended.csv',3,delim=',');[1:*,*]
      FeOT_pls_test=rd_tfile(testresult_dir+elems[3]+'_testset_blended.csv',3,delim=',');[1:*,*]
      MgO_pls_test=rd_tfile(testresult_dir+elems[4]+'_testset_blended.csv',3,delim=',');[1:*,*]
      CaO_pls_test=rd_tfile(testresult_dir+elems[5]+'_testset_blended.csv',3,delim=',');[1:*,*]
      Na2O_pls_test=rd_tfile(testresult_dir+elems[6]+'_testset_blended.csv',3,delim=',');[1:*,*]
      K2O_pls_test=rd_tfile(testresult_dir+elems[7]+'_testset_blended.csv',3,delim=',');[1:*,*]
      
      ;get testset names
      SiO2_test_names=SiO2_pls_test[0,1:*]
      TiO2_test_names=TiO2_pls_test[0,1:*]
      Al2O3_test_names=Al2O3_pls_test[0,1:*]
      FeOT_test_names=FeOT_pls_test[0,1:*]
      MgO_test_names=MgO_pls_test[0,1:*]
      CaO_test_names=CaO_pls_test[0,1:*]
      Na2O_test_names=Na2O_pls_test[0,1:*]
      K2O_test_names=K2O_pls_test[0,1:*]
      
      ;Define the actual compositions for each element's test set (to be used for quartiles) 
      SiO2_test_actual=float(SiO2_pls_test[1,1:*])
      TiO2_test_actual=float(TiO2_pls_test[1,1:*])
      Al2O3_test_actual=float(Al2O3_pls_test[1,1:*])
      FeOT_test_actual=float(FeOT_pls_test[1,1:*])
      MgO_test_actual=float(MgO_pls_test[1,1:*])
      CaO_test_actual=float(CaO_pls_test[1,1:*])
      Na2O_test_actual=float(Na2O_pls_test[1,1:*])
      K2O_test_actual=float(K2O_pls_test[1,1:*])
      actuals={SiO2:SiO2_test_actual,TiO2:TiO2_test_actual,$
        Al2O3:Al2O3_test_actual,FeOT:FeOT_test_actual,MgO:MgO_test_actual,$
        CaO:CaO_test_actual,Na2O:Na2O_test_actual,K2O:K2O_test_actual}
      
      ;calculate the quartiles
      quartiles=[[summary(SiO2_test_actual)],$
        [summary(TiO2_test_actual)],$
        [summary(Al2O3_test_actual)],$
        [summary(FeOT_test_actual)],$
        [summary(MgO_test_actual)],$
        [summary(CaO_test_actual)],$
        [summary(Na2O_test_actual)],$
        [summary(K2O_test_actual)]]
        
      
      ;Convert the PLS test set results to floats
      SiO2_pls_test=float(SiO2_pls_test[2,1:*])
      TiO2_pls_test=float(TiO2_pls_test[2,1:*])
      Al2O3_pls_test=float(Al2O3_pls_test[2,1:*])
      FeOT_pls_test=float(FeOT_pls_test[2,1:*])
      MgO_pls_test=float(MgO_pls_test[2,1:*])
      CaO_pls_test=float(CaO_pls_test[2,1:*])
      Na2O_pls_test=float(Na2O_pls_test[2,1:*])
      K2O_pls_test=float(K2O_pls_test[2,1:*])
      
      ;save to a structure since the test sets are sometimes different lengths (array won't work)
       pls_test={SiO2:SiO2_pls_test,TiO2:TiO2_pls_test,$
        Al2O3:Al2O3_pls_test,FeOT:FeOT_pls_test,MgO:MgO_pls_test,$
        CaO:CaO_pls_test,Na2O:Na2O_pls_test,K2O:K2O_pls_test}

      ;read the ICA test set predictions
      SiO2_ica_test=rd_tfile(testresult_dir+elems[0]+'_testset_ICA.csv',3,delim=',');[1:*,*]
      TiO2_ica_test=rd_tfile(testresult_dir+elems[1]+'_testset_ICA.csv',3,delim=',');[1:*,*]
      Al2O3_ica_test=rd_tfile(testresult_dir+elems[2]+'_testset_ICA.csv',3,delim=',');[1:*,*]
      FeOT_ica_test=rd_tfile(testresult_dir+elems[3]+'_testset_ICA.csv',3,delim=',');[1:*,*]
      MgO_ica_test=rd_tfile(testresult_dir+elems[4]+'_testset_ICA.csv',3,delim=',');[1:*,*]
      CaO_ica_test=rd_tfile(testresult_dir+elems[5]+'_testset_ICA.csv',3,delim=',');[1:*,*]
      Na2O_ica_test=rd_tfile(testresult_dir+elems[6]+'_testset_ICA.csv',3,delim=',');[1:*,*]
      K2O_ica_test=rd_tfile(testresult_dir+elems[7]+'_testset_ICA.csv',3,delim=',');[1:*,*]
       
      ;covert the ICA test results to floats
      SiO2_ica_test=float(SiO2_ica_test[2,1:*])
      TiO2_ica_test=float(TiO2_ica_test[2,1:*])
      Al2O3_ica_test=float(Al2O3_ica_test[2,1:*])
      FeOT_ica_test=float(FeOT_ica_test[2,1:*])
      MgO_ica_test=float(MgO_ica_test[2,1:*])
      CaO_ica_test=float(CaO_ica_test[2,1:*])
      Na2O_ica_test=float(Na2O_ica_test[2,1:*])
      K2O_ica_test=float(K2O_ica_test[2,1:*])
      ;save to a structure since the test sets are sometimes different lengths (array won't work)
       ica_test={SiO2:SiO2_ica_test,TiO2:TiO2_ica_test,$
        Al2O3:Al2O3_ica_test,FeOT:FeOT_ica_test,MgO:MgO_ica_test,$
        CaO:CaO_ica_test,Na2O:Na2O_ica_test,K2O:K2O_ica_test}

      ;combine the PLS and ICA test set results
      TiO2=0.5*TiO2_pls_test+0.5*TiO2_ica_test
      Al2O3=0.75*Al2O3_pls_test+0.25*Al2O3_ica_test
      Al2O3index=where(Al2O3 lt 15.0)
      Al2O3[Al2O3index]=0.06667*Al2O3[Al2O3index]^2+(1-0.06667*Al2O3[Al2O3index])*Al2O3_ica_test[Al2O3index]
      FeOT=0.75*FeOT_pls_test+0.25*FeOT_ica_test
      SiO2temp=0.5*SiO2_pls_test+0.5*SiO2_ica_test
      SiO2=SiO2temp
      ;We don't have FeOT test predictions for the SiO2 test set because the FeOT test set was defined separately
      ;Instead use the FeOT actuals to determine SiO2. This is "cheating" somewhat because it doesn't include the 
      ;FeOT uncertainties
      SiO2[where(SiO2_test_FeOT_true gt 30)]=0.75*SiO2_pls_test[where(SiO2_test_FeOT_true gt 30)]+0.25*SiO2_ica_test[where(SiO2_test_FeOT_true gt 30)]
      SiO2[where(SiO2_test_FeOT_true le 30 and SiO2temp ge 30)]=SiO2temp[where(SiO2_test_FeOT_true le 30 and SiO2temp ge 30)]
      SiO2[where(SiO2_test_FeOT_true le 30 and SiO2temp lt 30)]=$
        SiO2temp[where(SiO2_test_FeOT_true le 30 and SiO2temp lt 30)]*$
        SiO2temp[where(SiO2_test_FeOT_true le 30 and SiO2temp lt 30)]*$
        0.03333+(1-0.0333*SiO2temp[where(SiO2_test_FeOT_true le 30 and SiO2temp lt 30)])*$
        SiO2_ica_test[where(SiO2_test_FeOT_true le 30 and SiO2temp lt 30)]
      MgO=0.5*MgO_pls_test+0.5*MgO_ica_test
      CaO=0.5*CaO_pls_test+0.5*CaO_ica_test
      Na2O=0.4*Na2O_pls_test+0.6*Na2O_ica_test
      K2O=0.25*K2O_pls_test+0.75*K2O_ica_test

    ;save to a structure since the test sets are sometimes different lengths (array won't work)
        combined_test={SiO2:SiO2,TiO2:TiO2,Al2O3:Al2O3,FeOT:FeOT,MgO:MgO,CaO:CaO,Na2O:Na2O,K2O:K2O}
        
    ;Optionally produce 1 to 1 plots for the test set data
        if keyword_Set(output1to1) then begin
            write_csv,'SiO2_testset_combined.csv',[sio2_test_names,strtrim(sio2_test_actual,2),strtrim(combined_test.SiO2,2)]
            write_csv,'TiO2_testset_combined.csv',[Tio2_test_names,strtrim(Tio2_test_actual,2),strtrim(combined_test.TiO2,2)]
            write_csv,'Al2O3_testset_combined.csv',[al2o3_test_names,strtrim(Al2O3_test_actual,2),strtrim(combined_test.Al2O3,2)]
            write_csv,'FeOT_testset_combined.csv',[feot_test_names,strtrim(FeOT_test_actual,2),strtrim(combined_test.FeOT,2)]
            write_csv,'MgO_testset_combined.csv',[mgo_test_names,strtrim(MgO_test_actual,2),strtrim(combined_test.MgO,2)]
            write_csv,'CaO_testset_combined.csv',[cao_test_names,strtrim(CaO_test_actual,2),strtrim(combined_test.CaO,2)]
            write_csv,'Na2O_testset_combined.csv',[na2o_test_names,strtrim(Na2O_test_actual,2),strtrim(combined_test.Na2O,2)]
            write_csv,'K2O_testset_combined.csv',[k2o_test_names,strtrim(K2O_test_actual,2),strtrim(combined_test.K2O,2)]
            
            plot_1to1,sio2_test_actual,combined_test.sio2,title='SiO2 ICA+PLS Combined',outfile='SiO2_ica_pls_combined_testset_1to1.tif'
            plot_1to1,Tio2_test_actual,combined_test.Tio2,title='TiO2 ICA+PLS Combined',outfile='TiO2_ica_pls_combined_testset_1to1.tif'
            plot_1to1,Al2O3_test_actual,combined_test.Al2O3,title='Al2O3 ICA+PLS Combined',outfile='Al2O3_ica_pls_combined_testset_1to1.tif'
            plot_1to1,FeOT_test_actual,combined_test.FeOT,title='FeOT ICA+PLS Combined',outfile='FeOT_ica_pls_combined_testset_1to1.tif'
            plot_1to1,MgO_test_actual,combined_test.MgO,title='MgO ICA+PLS Combined',outfile='MgO_ica_pls_combined_testset_1to1.tif'
            plot_1to1,CaO_test_actual,combined_test.CaO,title='CaO ICA+PLS Combined',outfile='CaO_ica_pls_combined_testset_1to1.tif'
            plot_1to1,Na2O_test_actual,combined_test.Na2O,title='Na2O ICA+PLS Combined',outfile='Na2O_ica_pls_combined_testset_1to1.tif'
            plot_1to1,K2O_test_actual,combined_test.K2O,title='K2O ICA+PLS Combined',outfile='K2O_ica_pls_combined_testset_1to1.tif'
            
            plot_1to1,sio2_test_actual,pls_test.sio2,title='SiO2 PLS',outfile='SiO2_pls_testset_1to1.tif'
            plot_1to1,TiO2_test_actual,pls_test.TiO2,title='TiO2 PLS',outfile='TiO2_pls_testset_1to1.tif'
            plot_1to1,Al2O3_test_actual,pls_test.Al2O3,title='Al2O3 PLS',outfile='Al2O3_pls_testset_1to1.tif'
            plot_1to1,FeOT_test_actual,pls_test.FeOT,title='FeOT PLS',outfile='FeOT_pls_testset_1to1.tif'
            plot_1to1,MgO_test_actual,pls_test.MgO,title='MgO PLS',outfile='MgO_pls_testset_1to1.tif'
            plot_1to1,CaO_test_actual,pls_test.CaO,title='CaO PLS',outfile='CaO_pls_testset_1to1.tif'
            plot_1to1,Na2O_test_actual,pls_test.Na2O,title='Na2O PLS',outfile='Na2O_pls_testset_1to1.tif'
            plot_1to1,K2O_test_actual,pls_test.K2O,title='K2O PLS',outfile='K2O_pls_testset_1to1.tif'
            
            plot_1to1,sio2_test_actual,ica_test.sio2,title='SiO2 ICA',outfile='SiO2_ica_testset_1to1.tif'
            plot_1to1,TiO2_test_actual,ica_test.TiO2,title='TiO2 ICA',outfile='TiO2_ica_testset_1to1.tif'
            plot_1to1,Al2O3_test_actual,ica_test.Al2O3,title='Al2O3 ICA',outfile='Al2O3_ica_testset_1to1.tif'
            plot_1to1,FeOT_test_actual,ica_test.FeOT,title='FeOT ICA',outfile='FeOT_ica_testset_1to1.tif'
            plot_1to1,MgO_test_actual,ica_test.MgO,title='MgO ICA',outfile='MgO_ica_testset_1to1.tif'
            plot_1to1,CaO_test_actual,ica_test.CaO,title='CaO ICA',outfile='CaO_ica_testset_1to1.tif'
            plot_1to1,Na2O_test_actual,ica_test.Na2O,title='Na2O ICA',outfile='Na2O_ica_testset_1to1.tif'
            plot_1to1,K2O_test_actual,ica_test.K2O,title='K2O ICA',outfile='K2O_ica_testset_1to1.tif'
        endif     
        return,combined_test
end


  
function dynamic_rmsep,predicts,test_predicts,test_actuals,elems,makeplot=makeplot
rmseps=predicts*0.0+9999

;get the predictions and actuals for each element
for i=0,n_elements(elems)-1 do begin
  if elems[i] eq 'SiO2' then begin
    temp_test_predicts=test_predicts.SiO2
    temp_test_actuals=test_actuals.SiO2
  endif
  if elems[i] eq 'TiO2' then begin
    temp_test_predicts=test_predicts.TiO2
    temp_test_actuals=test_actuals.TiO2
  endif
  if elems[i] eq 'Al2O3' then begin
    temp_test_predicts=test_predicts.Al2O3
    temp_test_actuals=test_actuals.Al2O3
  endif
  if elems[i] eq 'FeOT' then begin
    temp_test_predicts=test_predicts.FeOT
    temp_test_actuals=test_actuals.FeOT
  endif
  if elems[i] eq 'MgO' then begin
    temp_test_predicts=test_predicts.MgO
    temp_test_actuals=test_actuals.MgO
  endif
  if elems[i] eq 'CaO' then begin
    temp_test_predicts=test_predicts.CaO
    temp_test_actuals=test_actuals.CaO
  endif
  if elems[i] eq 'Na2O' then begin
    temp_test_predicts=test_predicts.Na2O
    temp_test_actuals=test_actuals.Na2O
  endif
  if elems[i] eq 'K2O' then begin
    temp_test_predicts=test_predicts.K2O
    temp_test_actuals=test_actuals.K2O
  endif
  ;calcualte the squared errors
  test_sq_errs=(temp_test_predicts-temp_test_actuals)^2.0
  
  ;Get the RMSEP window size, based on the range of compositions in the test set
  windowsize=0.1
  min_rmsep_num=fix(0.1*n_elements(temp_test_predicts))
  rmsep_window=max(temp_test_actuals)*windowsize
  
  ;Create an array of "dummy" predictions
  dummypredicts=findgen(100)/100*max(temp_test_actuals)  
  dummy_rmseps=dummypredicts*0.0
  
  ;Loop through the dummy predictions, calculating RMSEPs
  for j=0,n_elements(dummypredicts)-1 do begin
    rmsep_index=where(abs(temp_test_predicts-dummypredicts[j]) lt rmsep_window)
    ;by default, calculate the RMSEP using test samples with true compositions that are within +/- 10% of the maximum range of the test set
    if n_elements(rmsep_index) ge min_rmsep_num then begin
      if rmsep_index[0] ne -1 then dummy_rmseps[j]=sqrt(mean(test_sq_errs[rmsep_index]))
    endif else begin
    ;If there are fewer samples that meet the above criteria than 10% of the total number of test spectra, then use the nearest 10% of spectra to calculate RMSEP
      rmsep_index=(sort(abs(temp_test_predicts-dummypredicts[j])))[0:min_rmsep_num-1]
      dummy_rmseps[j]=sqrt(mean(test_sq_errs[rmsep_index]))
    endelse
  endfor
  ;Remove duplicate dummy RMSEP values
  dummy_rmseps_orig=dummy_rmseps
  dummypredicts_orig=dummypredicts
  dummypredicts=dummypredicts(uniq(dummy_rmseps,sort(dummy_rmseps)))
  dummy_rmseps=dummy_rmseps(uniq(dummy_rmseps,sort(dummy_rmseps)))
  dummy_rmseps=dummy_rmseps(sort(dummypredicts))
  dummypredicts=dummypredicts(sort(dummypredicts))
  
  ;Re-interpolate (linear) to cover the gaps so that blending works ok
  dummy_rmseps=interpol(dummy_rmseps,dummypredicts,findgen(100)/100*max(dummypredicts))
  dummypredicts=findgen(100)/100*max(dummypredicts)
  ;smooth the RMSEPs
  y=gauss_smooth(dummy_rmseps,8,/edge_truncate)
  
  ;find the extrema of the smoothed RMSEPs
  extremas=extrema(y)
  ;Get the maximum RMSEP value meyond the last extremum
  endmax=max(y(max(extremas):*))
  ;Define the index of RMSEP values to keep.
  ;The dummy prediction value must be less than the value where endmax occurs, and the RMSEP must be more than 1% lower then endmax 
  ;(this ensures that the last few RMSEP points have at least a slightly positive slope)
  ; 
  ind=where(dummypredicts lt (dummypredicts(where(y eq endmax)))[0] and abs(y-y[n_elements(y)-1]) gt 0.01*y[n_elements(y)-1]); and y-endmax gt 0.1*endmax); and dummypredicts gt dummypredicts[max(extremas)]))

  ;keep a subset of the dummy predictions and RMSEPs
  x=dummypredicts[ind]
  y=y[ind]
  
  ;Densely re-sample and extrapolate the resulting curve to use as a look-up table
  xx=findgen(10000)/10000*100.
  yy=interpol(y,x,xx)
  
  ;optionally plot the results
  if keyword_set(makeplot) then begin
    window,0
    wset,0
    device,decomposed=0
    loadct,0
    plot,dummypredicts_orig,dummy_rmseps_orig,psym=2,xtitle='Predicted '+elems[i],ytitle='Local RMSEP',xrange=[0,min([100,max(dummypredicts)*3])],yrange=[0,2*max(dummy_rmseps)]
    loadct,13
    
    oplot,xx,yy,psym=3,color=250
    write_tiff,elems[i]+'_RMSEP_vs_predict'+makeplot+'.tif',reverse(tvrd(true=1),3),planarconfig=1,orientation=1
    stop
  endif
  
  ;Look up the expected RMSEP for the actual predictions
   for j=0,n_elements(predicts[i,*])-1 do begin
       rmseps[i,j]=yy[where(abs(predicts[i,j]-xx) eq min(abs(predicts[i,j]-xx)))]
   endfor
;   
;   ;Get the test set RMSEPs
;   test_rmseps=temp_test_predicts*0+9999
;   for j=0,n_elements(temp_test_predicts)-1 do test_rmseps[j]=yy[where(abs(temp_test_predicts[j]-xx) eq min(abs(temp_test_predicts[j]-xx)))] 
;   write_csv,elems[i]+'_testset_rmseps.csv',[temp_test_actuals,temp_test_predicts,test_rmseps]
;   
 
endfor


return,rmseps
end   
    
function pls_comp,currentelem,nshots,which_submodel,ymeancenters,meancenters,pls_settings_labels,pls_norms,pls_coeffs,spectra_norm1,spectra_norm3
        labelindex=where(pls_settings_labels eq currentelem+'_'+which_submodel)
        y_mean=rebin([ymeancenters[labelindex]],1,nshots)
        fullnorm=pls_norms[labelindex]
        full_coeff=pls_coeffs[labelindex,*]
        full_meancenter=rebin(reform(meancenters[labelindex,*]),n_elements(meancenters[labelindex,*]),nshots)
        if fullnorm eq 1 then calc_comp=matrix_multiply(full_coeff,spectra_norm1-full_meancenter)+y_mean
        if fullnorm eq 3 then calc_comp=matrix_multiply(full_coeff,spectra_norm3-full_meancenter)+y_mean
        return,calc_comp   
end
    
function pls_submodels,nshots,elems,ymeancenters,meancenters,pls_settings_labels,pls_norms,pls_coeffs,spectra_norm1,spectra_norm3
        which_submodel='full'
        comps_full=pls_comp(elems[0],nshots,which_submodel,ymeancenters,meancenters,pls_settings_labels,pls_norms,pls_coeffs,spectra_norm1,spectra_norm3)
        for j=1,n_elements(elems)-1 do begin
            comps_full=[comps_full,pls_comp(elems[j],nshots,which_submodel,ymeancenters,meancenters,pls_settings_labels,pls_norms,pls_coeffs,spectra_norm1,spectra_norm3)]
        endfor
        which_submodel='low'
        comps_low=pls_comp(elems[0],nshots,which_submodel,ymeancenters,meancenters,pls_settings_labels,pls_norms,pls_coeffs,spectra_norm1,spectra_norm3)
        for j=1,n_elements(elems)-1 do begin
            comps_low=[comps_low,pls_comp(elems[j],nshots,which_submodel,ymeancenters,meancenters,pls_settings_labels,pls_norms,pls_coeffs,spectra_norm1,spectra_norm3)]
        endfor
        which_submodel='mid'
        comps_mid=pls_comp(elems[0],nshots,which_submodel,ymeancenters,meancenters,pls_settings_labels,pls_norms,pls_coeffs,spectra_norm1,spectra_norm3)
        for j=1,n_elements(elems)-1 do begin
            comps_mid=[comps_mid,pls_comp(elems[j],nshots,which_submodel,ymeancenters,meancenters,pls_settings_labels,pls_norms,pls_coeffs,spectra_norm1,spectra_norm3)]
        endfor
        which_submodel='high'
        comps_high=pls_comp(elems[0],nshots,which_submodel,ymeancenters,meancenters,pls_settings_labels,pls_norms,pls_coeffs,spectra_norm1,spectra_norm3)
        for j=1,n_elements(elems)-1 do begin
            comps_high=[comps_high,pls_comp(elems[j],nshots,which_submodel,ymeancenters,meancenters,pls_settings_labels,pls_norms,pls_coeffs,spectra_norm1,spectra_norm3)]
        endfor
        
        comps={full:comps_full,low:comps_low,mid:comps_mid,high:comps_high}
        return,comps
end         



function pls_blend,comps,blend_array_dir,elems,filelist
        blended=comps.full*0.0        
        for k=0,n_elements(elems)-1 do begin
            ;#reconstruct the blend input settings from the blend array file
            blendarray=rd_tfile(blend_array_dir+elems[k]+'_blend_array.csv',/autocol,delim=',')
            blend_labels=blendarray[0,*]
            blendarray=blendarray[*,1:*]
            ranges=float(blendarray[0:1,*])
            inrange=fix(blendarray[2,*])
            refpredict=fix(blendarray[3,*])
            toblend=fix(blendarray[4:5,*])
            predicts=[comps.full[k,*],comps.low[k,*],comps.mid[k,*],comps.high[k,*]]
        
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
      blended[where(blended lt 0)]=0 ;Set any negative results to zero
      return,blended
end

pro write_results,comps_all,targets_all,filelist_all,amps_all,dists_all,totals_All,elems,shots,shotnum_all,rmseps,searchdir,testset_quartiles,ica=ica,pls=pls
        ;get the current date
        caldat,systime(/jul),mm,dd,yy
        yy=strtrim(yy,2)
        mm=strtrim(mm,2)
        if strlen(mm) eq 1 then mm='0'+mm
        dd=strtrim(dd,2)
        if strlen(dd) eq 1 then dd='0'+dd
        today=yy+mm+dd
        ;Set up the output array
        if shots eq 1 then begin
            labelrow=['File','Target','Shot Number','Distance (m)','Laser Power','Spectrum Total',elems,'Total',elems+'_RMSEP']
            output=transpose([[filelist_all],[targets_all],[strtrim(shotnum_all+1,2)],[strtrim(dists_all,2)],[amps_all],[strtrim(totals_all,2)]])
            plsoutfile=searchdir+'ccam_comps_singleshots_pls_'+today+'.csv'
            icaoutfile=searchdir+'ccam_comps_singleshots_ica_'+today+'.csv'
            outfile=searchdir+'ccam_comps_singleshots_'+today+'.csv'
            pad=strarr(5,6)
        endif
        if shots eq 0 then begin
            labelrow=['File','Target','Distance (m)','Laser Power','Spectrum Total',elems,'Total',elems+'_RMSEP']
            output=transpose([[filelist_all],[targets_all],[strtrim(dists_all,2)],[amps_all],[strtrim(totals_all,2)]])
            plsoutfile=searchdir+'ccam_comps_pls_'+today+'.csv'
            icaoutfile=searchdir+'ccam_comps_ica_'+today+'.csv'
            outfile=searchdir+'ccam_comps_'+today+'.csv'
            pad=strarr(4,6)
        endif
        
        ;Set up the quartile info for the top of the file
        testset_quartiles_out=[[elems],[transpose(strtrim(testset_quartiles,2))]]
        quartile_labels=['Testset Quartiles','Min','1st','Med','3rd','Max']
        testset_quartiles_out=[transpose(quartile_labels),testset_quartiles_out]
        testset_quartiles_out=[pad,testset_quartiles_out]
        testset_quartiles_out=[testset_quartiles_out,strarr(n_elements(labelrow)-n_elements(testset_quartiles_out[*,0]),6)]
        labelrow=[[testset_quartiles_out],[labelrow]]
        
        ;Calculate the composition totals
        totals=total(comps_all,1)
        
        ;Add the totals and RMSEPs to the output array  
          output=[output,strtrim(comps_all,2),strtrim(transpose(totals),2),strtrim(RMSEPs,2)]
          output=[[labelrow],[output]]
          
          if keyword_set(pls) then begin
            write_csv,plsoutfile,output 
          endif else if keyword_set(ica) then begin
            write_csv,icaoutfile,output
          endif else write_csv,outfile,output
        
end
  
        


function calc_comp,searchdir,shots,maskfile,masterfile,recursive,pls_settings_labels,pls_norms,pls_ncs,pls_coeffs,meancenter_labels,ymeancenters,meancenters,blend_array_dir,testresult_dir,os=os
         
   elems=['SiO2','TiO2','Al2O3','FeOT','MgO','CaO','Na2O','K2O']
        
   combined_test=get_testset_info(testresult_dir,elems,quartiles=testset_quartiles,actuals=test_actuals,ica_test=ica_test,pls_test=pls_test)


   xmess,"Reading CCS files in "+searchdir,/nowait,wid=wid
        
   filelist=ccam_filelist(searchdir,pathlist=pathlist,filelist_sols=filelist_sols,minsol=0,maxsol=999999,recursive=recursive,filelist_sclock=filelist_sclock,os=os)
   widget_control,/dest,wid
   ;Look up target info
   targets=ccam_filelist_targets(masterfile,filelist,filelist_sclock,filelist_nshots=filelist_nshots,filelist_dists=filelist_dists,filelist_amps=filelist_amps)
        
   ;Run ICA code
    icavals = transpose(ICR(pathlist+filelist,shot=shots,fn_good_index=fn_good_index))
    if keyword_set(shots) then begin
       ica_comps=*icavals[0]
       for i=1,n_elements(filelist)-1 do ica_comps=[ica_comps,*icavals[i]]
       icavals=transpose(ica_comps)
    endif
    ica_rmseps=dynamic_rmsep(icavals,ica_test,test_actuals,elems);,makeplot='ICA')
        

    filelist=filelist(fn_good_index)
    pathlist=pathlist(fn_good_index)
    filelist_sols=filelist_sols(fn_good_index)
    filelist_sclock=filelist_sclock(fn_good_index)
    targets=targets(fn_good_index)
    filelist_nshots=filelist_nshots(fn_good_index)
    filelist_dists=filelist_dists(fn_good_index)
    filelist_amps=filelist_amps(fn_good_index)
 
         ;Loop through each file in the file list, apply norm and mask, and run PLS calculations
        progbar=Obj_New('cgProgressBar',/start,percent=0,title='Running PLS calculation for '+strtrim(n_elements(filelist),2)+' files')
        
        for i=0,n_elements(filelist)-1 do begin
           restore,pathlist[i]+filelist[i]
            if shots eq 1 then begin
                singleshots=[transpose(uv),transpose(vis),transpose(vnir)]
                wvl=[defuv,defvis,defvnir]
                shotnum=indgen(nshots)
                singleshots_masked=ccam_mask(singleshots,wvl,maskfile,masked_wvl=masked_wvl)
                spectra_masked_norm1=ccam_norm(singleshots_masked,masked_wvl,1,totals=totals_temp)
                spectra_masked_norm3=ccam_norm(singleshots_masked,masked_wvl,3)
            endif 
            if shots eq 0 then begin
                nshots=1
                shotnum=filelist_nshots[i]
                meanspect=[auv,avis,avnir]
                wvl=[defuv,defvis,defvnir]
                meanspect_masked=ccam_mask(meanspect,wvl,maskfile,masked_wvl=masked_wvl)
                spectra_masked_norm1=ccam_norm(meanspect_masked,masked_wvl,1,totals=totals_temp)
                spectra_masked_norm3=ccam_norm(meanspect_masked,masked_wvl,3)
            endif    
            
            ;Run PLS calculations
            comps_temp=pls_submodels(nshots,elems,ymeancenters,meancenters,pls_settings_labels,pls_norms,pls_coeffs,spectra_masked_norm1,spectra_masked_norm3)
            
            if i eq 0 then begin
                comps_all=comps_temp
                filelist_all=replicate(filelist[i],nshots)
                shotnum_all=shotnum
                targets_all=replicate(targets[i],nshots)
                dists_all=replicate(filelist_dists[i],nshots)
                amps_all=replicate(filelist_amps[i],nshots)
                totals_all=totals_temp
                    
            endif else begin
                comps_all={full:[[comps_all.full],[comps_temp.full]],low:[[comps_all.low],[comps_temp.low]],mid:[[comps_all.mid],[comps_temp.mid]],high:[[comps_all.high],[comps_temp.high]]}
                
                filelist_all=[filelist_all,replicate(filelist[i],nshots)]
                shotnum_all=[shotnum_all,shotnum]
                targets_all=[targets_all,replicate(targets[i],nshots)]
                dists_all=[dists_all,replicate(filelist_dists[i],nshots)]
                amps_all=[amps_all,replicate(filelist_amps[i],nshots)]
                totals_all=[totals_All,totals_temp]
                
            endelse
            progbar -> Update,float(i+1)/n_elements(filelist)*100
        endfor
        progbar->Destroy
        
        ;Blend the PLS submodels  
        plsvals=pls_blend(comps_all,blend_array_dir,elems,filelist_all)
        pls_rmseps=dynamic_rmsep(plsvals,pls_test,test_actuals,elems);,makeplot='PLS')
        
        ;Combine the PLS and ICA results
        TiO2=0.5*plsvals[1,*]+0.5*icavals[1,*]
        Al2O3=0.75*plsvals[2,*]+0.25*icavals[2,*]
        Al2O3[where(Al2O3 lt 15.0)]=0.06667*Al2O3[where(Al2O3 lt 15.0)]^2+(1-0.06667*Al2O3[where(Al2O3 lt 15.0)])*icavals[2,[where(Al2O3 lt 15.0)]]
        FeOT=0.75*plsvals[3,*]+0.25*icavals[3,*]
        SiO2temp=0.5*plsvals[0,*]+0.5*icavals[0,*]
        SiO2=SiO2temp
        SiO2[where(FeOt gt 30)]=0.75*plsvals[0,[where(FeOt gt 30)]]+0.25*icavals[0,[where(FeOt gt 30)]]
        SiO2[where(FeOT le 30 and SiO2temp ge 30)]=SiO2temp[where(FeOT le 30 and SiO2temp ge 30)]
        SiO2[where(FeOT le 30 and SiO2temp lt 30)]=SiO2temp[where(FeOT le 30 and SiO2temp lt 30)]*SiO2temp[where(FeOT le 30 and SiO2temp lt 30)]*0.03333+(1-0.0333*SiO2temp[where(FeOT le 30 and SiO2temp lt 30)])*icavals[0,[where(FeOT le 30 and SiO2temp lt 30)]]
        MgO=0.5*plsvals[4,*]+0.5*icavals[4,*]
        CaO=0.5*plsvals[5,*]+0.5*icavals[5,*]
        Na2O=0.4*plsvals[6,*]+0.6*icavals[6,*]
        K2O=0.25*plsvals[7,*]+0.75*icavals[7,*]
        
        ica_pls_combined=[SiO2,TiO2,Al2O3,FeOT,MgO,CaO,Na2O,K2O]
        rmseps=dynamic_rmsep(ica_pls_combined,combined_test,test_actuals,elems);,makeplot='combined')

        ;Output results
       ; write_results,plsvals,targets_all,filelist_all,amps_all,dists_all,totals_all,elems,shots,shotnum_all,$
       ; pls_rmseps,searchdir,testset_quartiles,ica=0,pls=1
       ; write_results,icavals,targets_all,filelist_all,amps_all,dists_all,totals_all,elems,shots,shotnum_all,$
       ; ica_rmseps,searchdir,testset_quartiles,ica=1,pls=0
        write_results,ica_pls_combined,targets_all,filelist_all,amps_all,dists_all,totals_all,elems,shots,shotnum_all,$
        rmseps,searchdir,testset_quartiles,ica=0,pls=0
        
end
 