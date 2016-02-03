function pls_calc_comp,searchdir,shots,maskfile,masterfile,recursive,pls_settings_labels,pls_norms,pls_ncs,pls_coeffs,meancenter_labels,ymeancenters,meancenters,blend_array_dir
        
        filelist=ccam_filelist(searchdir,pathlist=pathlist,filelist_sols=filelist_sols,minsol=0,maxsol=999999,recursive=recursive,filelist_sclock=filelist_sclock)
        
        
        ;self.myWidget.progressBar.setMaximum(len(filelist))
        targets=ccam_filelist_targets(masterfile,filelist,filelist_sclock,filelist_nshots=filelist_nshots,filelist_dists=filelist_dists,filelist_amps=filelist_amps)
        
        elems=['SiO2','TiO2','Al2O3','FeOT','MgO','CaO','Na2O','K2O']
        
        ;Loop through each file in the file list
        for i=0,n_elements(filelist)-1 do begin
            ;app.processEvents()          
            ;self.myWidget.progressBar.setValue(i)
            print,pathlist[i]+'\'+filelist[i]
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
        
          
        blended_all=pls_blend(comps_all,blend_array_dir,elems,filelist_all)
        write_results,blended_all,targets_all,filelist_all,amps_all,dists_all,elems,shots,shotnum_all
  
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

pro write_results,blended_all,targets_all,filelist_all,amps_all,dists_all,elems,shots,shotnum_all

        if shots eq 1 then begin
            labelrow=['File','Target','Shot Number','Distance (m)','Laser Power',elems,'Total']
            output=transpose([[filelist_all],[targets_all],[strtrim(shotnum_all+1,2)],[strtrim(dists_all,2)],[amps_all]])
            outfile='ccam_comps_predict_singleshots.csv'
        endif
        if shots eq 0 then begin
            labelrow=['File','Target','Distance (m)','Laser Power',elems,'Total']
            output=transpose([[filelist_all],[targets_all],[strtrim(dists_all,2)],[amps_all]])
            outfile='ccam_comps_predict.csv'
        endif
        totals=total(blended_all,1)
        
        output=[output,strtrim(blended_all,2),strtrim(transpose(totals),2)]
        
        output=[[labelrow],[output]]
        write_csv,outfile,output
        
end
            
