; Modified 27 Jun 2015 (OG): Add tests on WHERE outputs
function ccam_mask,spectra,wvl,pls_settings,masked_wvl=masked_wvl
    maskfile=pls_settings['maskfile']
;    masked_wvl=reform(pls_settings['coeffs_wvl'])
;    
;    
;    masked_spectra=[]
;    for i=0,n_elements(spectra[0,*])-1 do begin
;      masked_spectra=[[masked_spectra],[interpol(spectra[*,i],wvl,masked_Wvl)]]
;    endfor
    ;wvl=round(wvl*1000)/1000.
    masked_wvl=wvl
    mask=(rd_tfile(maskfile,/autocol,delim=','))[1:*,1:*]
   ; mask=(rd_tfile(maskfile,/autocol,delim=','))[1:*,1:*]

    maskindex=intarr(n_elements(wvl),n_elements(mask[0,*]))+1
    index=wvl*0
    for i=0,n_elements(mask[0,*])-1 do begin
          k = where((masked_wvl ge mask[0,i]) and (masked_wvl le mask[1,i]), nk)
          print,i,n_elements(k),masked_wvl[k[0]],masked_wvl[k[-1]]
          if nk eq 0 then message,'This should not happen (1).'
          ;maskindex[k,i]=0
          index[k]=1.0
    endfor
    
    ;index=where(total(maskindex,2) eq n_elements(mask[0,*]), ni)
    index=where(index eq 0)
   ; if ni eq 0 then message,'This should not happen (2).'

    masked_wvl=wvl[index]
    masked_spectra=spectra[index,*]

    return,masked_spectra
    
end