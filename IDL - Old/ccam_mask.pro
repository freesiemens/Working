function ccam_mask,spectra,wvl,maskfile,masked_wvl=masked_wvl
  
    masked_spectra=spectra
    masked_wvl=wvl
    mask=(rd_tfile(maskfile,/autocol,delim=','))[1:*,1:*]
    maskindex=intarr(n_elements(wvl),n_elements(mask[0,*]))+1
    for i=0,n_elements(mask[0,*])-1 do begin
          maskindex[where((masked_wvl ge mask[0,i]) and (masked_wvl le mask[1,i])),i]=0
    endfor
    index=where(total(maskindex,2) eq n_elements(mask[0,*]))

    masked_wvl=wvl[index]
    masked_spectra=spectra[index,*]

    return,masked_spectra
    
end