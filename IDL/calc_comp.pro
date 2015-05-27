  
function dynamic_rmsep,predicts,test_predicts,elems,calctest=calctest
rmseps=predicts*0.0+9999
window,0
window,1
for i=0,n_elements(elems)-1 do begin
  if elems[i] eq 'SiO2' then temp_test_predicts=test_predicts.SiO2
  if elems[i] eq 'TiO2' then temp_test_predicts=test_predicts.TiO2
  if elems[i] eq 'Al2O3' then temp_test_predicts=test_predicts.Al2O3
  if elems[i] eq 'FeOT' then temp_test_predicts=test_predicts.FeOT
  if elems[i] eq 'MgO' then temp_test_predicts=test_predicts.MgO
  if elems[i] eq 'CaO' then temp_test_predicts=test_predicts.CaO
  if elems[i] eq 'Na2O' then temp_test_predicts=test_predicts.Na2O
  if elems[i] eq 'K2O' then temp_test_predicts=test_predicts.K2O
  
  
  test_sq_errs=(temp_test_predicts[0,*]-temp_test_predicts[1,*])^2.0
  
  ;Get the RMSEP window size, based on the range of compositions in the test set
  windowsize=0.1
  min_rmsep_num=fix(0.1*n_elements(temp_test_predicts[0,*]))
  rmsep_window=max(temp_test_predicts)*windowsize
  print,elems[i]+': '+strtrim(rmsep_window)
  if keyword_set(calctest) then whichpredicts=findgen(100)/100*max(temp_test_predicts) else whichpredicts=predicts[i,*]
  temp_rmseps=whichpredicts*0.0
  for j=0,n_elements(whichpredicts)-1 do begin
    rmsep_index=where(abs(temp_test_predicts[1,*]-whichpredicts[j]) lt rmsep_window)
    ;help,rmsep_index
    ;by default, calculate the RMSEP using test samples with true compositions that are within +/- 10% of the maximum range of the test set
    if n_elements(rmsep_index) ge min_rmsep_num then begin
      if rmsep_index[0] ne -1 then temp_rmseps[j]=sqrt(mean(test_sq_errs[rmsep_index]))
      ;loadct,0
      ;plot,temp_test_predicts[0,*],temp_Test_predicts[1,*],psym=2
      ;loadct,13
      ;oplot,temp_test_predicts[0,rmsep_index],temp_test_predicts[1,rmsep_index],color=200,psym=4
      ;print,temp_test_predicts[*,j]
      ;print,temp_rmseps[j]
      ;stop
    endif else begin
    ;If there are fewer samples that meet the above criteria than 5% of the total number of test spectra, then use the nearest 5% of spectra to calculate RMSEP
      rmsep_index=(sort(abs(temp_test_predicts[1,*]-whichpredicts[j])))[0:min_rmsep_num-1]
      temp_rmseps[j]=sqrt(mean(test_sq_errs[rmsep_index]))
;      loadct,0
;      plot,temp_test_predicts[0,*],temp_Test_predicts[1,*],psym=2
;      loadct,13
;      oplot,temp_test_predicts[0,rmsep_index],temp_test_predicts[1,rmsep_index],color=200,psym=4
;      stop
;      print,temp_test_predicts[*,j]
;      print,temp_rmseps[j]
      ;stop
    endelse
    
  endfor
  wset,0
  plot,whichpredicts,temp_rmseps,psym=2,xtitle='Predicted '+elems[i],ytitle='Local RMSEP'
  write_gif,elems[i]+'_RMSEPvsPredict.gif',tvrd()
 ; wset,1
 ; ploterror,temp_test_predicts[0,*],temp_Test_predicts[1,*],temp_rmseps*0,temp_rmseps,psym=3
   
  stop
  if keyword_set(calctest) then begin
     if elems[i] eq 'SiO2' then test_predicts.SiO2_rmsep=temp_rmseps
     if elems[i] eq 'TiO2' then test_predicts.TiO2_rmsep=temp_rmseps
     if elems[i] eq 'Al2O3' then test_predicts.Al2O3_rmsep=temp_rmseps
     if elems[i] eq 'FeOT' then test_predicts.FeOT_rmsep=temp_rmseps
     if elems[i] eq 'MgO' then test_predicts.MgO_rmsep=temp_rmseps
     if elems[i] eq 'CaO' then test_predicts.CaO_rmsep=temp_rmseps
     if elems[i] eq 'Na2O' then test_predicts.Na2O_rmsep=temp_rmseps
     if elems[i] eq 'K2O' then test_predicts.K2O_rmsep=temp_rmseps
     
  endif else begin
    rmseps[i,*]=temp_rmseps
  endelse
  
  
endfor
stop

return,rmseps
end   
    
function pls_comp,currentelem,nshots,which_submodel,ymeancenters,meancenters,pls_settings_labels,pls_norms,pls_coeffs,spectra_norm1,spectra_norm3
        ;get full results
        labelindex=where(pls_settings_labels eq currentelem+'_'+which_submodel)
        y_mean=rebin([ymeancenters[labelindex]],1,nshots)
        fullnorm=pls_norms[labelindex]
        full_coeff=pls_coeffs[labelindex,*]
        full_meancenter=rebin(reform(meancenters[labelindex,*]),n_elements(meancenters[labelindex,*]),nshots)
        if fullnorm eq 1 then begin
            calc_comp=matrix_multiply(full_coeff,spectra_norm1-full_meancenter)+y_mean
            
        endif
        if fullnorm eq 3 then begin
            calc_comp=matrix_multiply(full_coeff,spectra_norm3-full_meancenter)+y_mean
        endif     
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
            blendarray=rd_tfile(blend_array_dir+'\\'+elems[k]+'_blend_array.csv',/autocol,delim=',')
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
      blended[where(blended lt 0)]=0
      return,blended
end

pro write_results,blended_all,targets_all,filelist_all,amps_all,dists_all,elems,shots,shotnum_all,ica_comps_all,ica_pls_combined
        caldat,systime(/jul),mm,dd,yy
        yy=strtrim(yy,2)
        mm=strtrim(mm,2)
        if strlen(mm) eq 1 then mm='0'+mm
        dd=strtrim(dd,2)
        if strlen(dd) eq 1 then dd='0'+dd
        today=yy+mm+dd
        if shots eq 1 then begin
            labelrow=['File','Target','Shot Number','Distance (m)','Laser Power',elems,'Total']
            output=transpose([[filelist_all],[targets_all],[strtrim(shotnum_all+1,2)],[strtrim(dists_all,2)],[amps_all]])
            plsoutfile='ccam_comps_singleshots_pls_'+today+'.csv'
            icaoutfile='ccam_comps_singleshots_ica_'+today+'.csv'
            outfile='ccam_comps_singleshots_'+today+'.csv'
            
        endif
        if shots eq 0 then begin
            labelrow=['File','Target','Distance (m)','Laser Power',elems,'Total']
            output=transpose([[filelist_all],[targets_all],[strtrim(dists_all,2)],[amps_all]])
            plsoutfile='ccam_comps_pls_'+today+'.csv'
            icaoutfile='ccam_comps_ica_'+today+'.csv'
            outfile='ccam_comps_'+today+'.csv'
        endif
        plstotals=total(blended_all,1)
        icatotals=total(ica_comps_all,1)
        totals=total(ica_pls_combined,1)
        
        plsoutput=[output,strtrim(blended_all,2),strtrim(transpose(totals),2)]
        icaoutput=[output,strtrim(ica_comps_all,2),strtrim(transpose(totals),2)]
        alloutput=[output,strtrim(ica_pls_combined,2),strtrim(transpose(totals),2)]
        
        plsoutput=[[labelrow],[plsoutput]]
        icaoutput=[[labelrow],[icaoutput]]
        alloutput=[[labelrow],[alloutput]]
        
        write_csv,plsoutfile,plsoutput
        write_csv,icaoutfile,icaoutput
        write_csv,outfile,alloutput
end
            


function calc_comp,searchdir,shots,maskfile,masterfile,recursive,pls_settings_labels,pls_norms,pls_ncs,pls_coeffs,meancenter_labels,ymeancenters,meancenters,blend_array_dir,pls_testresult_dir
        elems=['SiO2','TiO2','Al2O3','FeOT','MgO','CaO','Na2O','K2O']

        SiO2_pls_testresult=rd_tfile(pls_testresult_dir+'\'+elems[0]+'_testset_blended.csv',3,delim=',');[1:*,*]
        TiO2_pls_testresult=rd_tfile(pls_testresult_dir+'\'+elems[1]+'_testset_blended.csv',3,delim=',');[1:*,*]
        Al2O3_pls_testresult=rd_tfile(pls_testresult_dir+'\'+elems[2]+'_testset_blended.csv',3,delim=',');[1:*,*]
        FeOT_pls_testresult=rd_tfile(pls_testresult_dir+'\'+elems[3]+'_testset_blended.csv',3,delim=',');[1:*,*]
        MgO_pls_testresult=rd_tfile(pls_testresult_dir+'\'+elems[4]+'_testset_blended.csv',3,delim=',');[1:*,*]
        CaO_pls_testresult=rd_tfile(pls_testresult_dir+'\'+elems[5]+'_testset_blended.csv',3,delim=',');[1:*,*]
        Na2O_pls_testresult=rd_tfile(pls_testresult_dir+'\'+elems[6]+'_testset_blended.csv',3,delim=',');[1:*,*]
        K2O_pls_testresult=rd_tfile(pls_testresult_dir+'\'+elems[7]+'_testset_blended.csv',3,delim=',');[1:*,*]
        
        pls_testresult={SiO2:float(SiO2_pls_testresult[1:*,1:*]),TiO2:float(TiO2_pls_testresult[1:*,1:*]),$
          Al2O3:float(Al2O3_pls_testresult[1:*,1:*]),FeOT:float(FeOT_pls_testresult[1:*,1:*]),MgO:float(MgO_pls_testresult[1:*,1:*]),$
          CaO:float(CaO_pls_testresult[1:*,1:*]),Na2O:float(Na2O_pls_testresult[1:*,1:*]),K2O:float(K2O_pls_testresult[1:*,1:*]),$
          SiO2_RMSEP:float(SiO2_pls_testresult[1:*,1:*])*0,TiO2_RMSEP:float(TiO2_pls_testresult[1:*,1:*])*0,Al2O3_RMSEP:float(Al2O3_pls_testresult[1:*,1:*])*0,$
          FeOT_RMSEP:float(FeOT_pls_testresult[1:*,1:*])*0,MgO_RMSEP:float(MgO_pls_testresult[1:*,1:*])*0,CaO_RMSEP:float(CaO_pls_testresult[1:*,1:*])*0,$
          Na2O_RMSEP:float(Na2O_pls_testresult[1:*,1:*])*0,K2O_RMSEP:float(K2O_pls_testresult[1:*,1:*])*0}
        print,'Getting CCS files...'
        filelist=ccam_filelist(searchdir,pathlist=pathlist,filelist_sols=filelist_sols,minsol=0,maxsol=999999,recursive=recursive,filelist_sclock=filelist_sclock)
        
        ;Run Olivier's ICA code
        ica_comps_all = transpose(ICR(pathlist+filelist,shot=shots,fn_good_index=fn_good_index))
        stop
        filelist=filelist(fn_good_index)
        pathlist=pathlist(fn_good_index)
        filelist_sols=filelist_sols(fn_good_index)
        filelist_sclock=filelist_sclock(fn_good_index)
        stop
        ;stop
        


        ;self.myWidget.progressBar.setMaximum(len(filelist))
        
        ;Look up target info
        targets=ccam_filelist_targets(masterfile,filelist,filelist_sclock,filelist_nshots=filelist_nshots,filelist_dists=filelist_dists,filelist_amps=filelist_amps)
        

        ;Loop through each file in the file list, apply norm and mask, and run PLS calculations
        for i=0,n_elements(filelist)-1 do begin
            ;app.processEvents()          
            ;self.myWidget.progressBar.setValue(i)
            ;print,pathlist[i]+'\'+filelist[i]
            restore,pathlist[i]+'\'+filelist[i]
            if shots eq 1 then begin
                singleshots=[transpose(uv),transpose(vis),transpose(vnir)]
                wvl=[defuv,defvis,defvnir]
                shotnum=indgen(nshots)
                
                singleshots_masked=ccam_mask(singleshots,wvl,maskfile,masked_wvl=masked_wvl)
                
                
                spectra_masked_norm1=ccam_norm(singleshots_masked,masked_wvl,1)
                spectra_masked_norm3=ccam_norm(singleshots_masked,masked_wvl,3)
                
                
            endif 
               
            if shots eq 0 then begin
                nshots=1
                shotnum=filelist_nshots[i]
                meanspect=[auv,avis,avnir]
                wvl=[defuv,defvis,defvnir]
                
                meanspect_masked=ccam_mask(meanspect,wvl,maskfile,masked_wvl=masked_wvl)
                
                spectra_masked_norm1=ccam_norm(meanspect_masked,masked_wvl,1)
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
                    
            endif else begin
                comps_all={full:[[comps_all.full],[comps_temp.full]],low:[[comps_all.low],[comps_temp.low]],mid:[[comps_all.mid],[comps_temp.mid]],high:[[comps_all.high],[comps_temp.high]]}
                
                filelist_all=[filelist_all,replicate(filelist[i],nshots)]
                shotnum_all=[shotnum_all,shotnum]
                targets_all=[targets_all,replicate(targets[i],nshots)]
                dists_all=[dists_all,replicate(filelist_dists[i],nshots)]
                amps_all=[amps_all,replicate(filelist_amps[i],nshots)]

            endelse
        endfor
        
        ;Blend the PLS submodels  
        blended_all=pls_blend(comps_all,blend_array_dir,elems,filelist_all)
        ;foo=[pls_testresult.SiO2[0,*],pls_testresult.TiO2[0,*],pls_testresult.Al2O3[0,*],pls_testresult.FeOT[0,*],pls_testresult.MgO[0,*],pls_testresult.CaO[0,*],pls_testresult.Na2O[0,*],pls_testresult.K2O[0,*]]
        ;stop
        pls_rmseps=dynamic_rmsep(blended_all,pls_testresult,elems,calctest=1)
        
        ica_pls_combined=$
          [0.5*blended_all[0,*]+0.5*ica_comps_all[0,*],0.5*blended_all[1,*]+0.5*ica_comps_all[1,*],$
          0.75*blended_all[2,*]+0.25*ica_comps_all[2,*],0.75*blended_all[3,*]+0.25*ica_comps_all[3,*],$
          0.5*blended_all[4,*]+0.5*ica_comps_all[4,*],0.5*blended_all[5,*]+0.5*ica_comps_all[5,*],$
          0.4*blended_all[6,*]+0.6*ica_comps_all[6,*],0.4*blended_all[7,*]+0.6*ica_comps_all[7,*]]
        
        write_results,blended_all,targets_all,filelist_all,amps_all,dists_all,elems,shots,shotnum_all,ica_comps_all,ica_pls_combined
  
end
 