function ccam_norm,spectra,wvl,normtype
   spectra_norm=spectra
   if normtype eq 3 then begin
      uvindex=where(wvl le 340.797)
      visindex=where(wvl ge 382.138 and wvl le 469.090)
      vnirindex=where(wvl gt 473.184)
      uvtotal=total(spectra[uvindex,*],1)
      vistotal=total(spectra[visindex,*],1)
      vnirtotal=total(spectra[vnirindex,*],1)
      for i=0,n_elements(uvtotal)-1 do begin
        spectra_norm[uvindex,i]=spectra[uvindex,i]/uvtotal[i]
        spectra_norm[visindex,i]=spectra[visindex,i]/vistotal[i]
        spectra_norm[vnirindex,i]=spectra[vnirindex,i]/vnirtotal[i]
      endfor
      
   endif
   
   if normtype eq 1 then begin
      totals=total(spectra,1)
      for i=0,n_elements(totals)-1 do begin
         spectra_norm[*,i]=spectra[*,i]/totals[i]
      endfor
   endif
   
   return,spectra_norm
end