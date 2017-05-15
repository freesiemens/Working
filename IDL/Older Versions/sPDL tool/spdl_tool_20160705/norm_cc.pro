;+
; NAME: 
;       NORM_CC
;
; PURPOSE:
;       This routine returns normalized CCAM spectrum with its total emission
;
; CALLING SEQUENCE:
;       Norm_Spectrum = Norm_CC( Spectrum, Norm, STD=std)
;
; INPUTS:
;       Spectrum: The CCAM spectrum or array of spectra to
;       normalize. The dimension is [6144, Nb of spectra]
;       Norm: Paramater defining the type of norm to apply
;           Norm = 1: The entire spctrum is normalized
;           Norm = 3: Each spectral range is normalized individually
;
; OPTIONAL INPUTS:
;       None
;
; KEYWORD PARAMETERS:
;       STD: If set normalization is done with the standard deviation
;       instead of total emission
;
; OUTPUTS:
;       Return a normalized CCAM spectrum or array of spectra having
;       the same dimension as the input array
;
; OPTIONAL OUTPUTS:
;       None
;
; SIDE EFFECTS:
;      If the number of input parameters id different from 2, the
;      routine returns -1.
;      If the number of spectral channel is different from 6144, the
;      routine returns -1.
;      If Norm is different from 1 or 3 no normalization is done
;
; EXAMPLE:
;      sp_norm = norm_cc( sp_in, 3,/std)
;
; MODIFICATION HISTORY:
; O. Forni: May 2015
;-
FUNCTION norm_cc,sp_in,norm,std=std

  if n_params() ne 2 then return,-1
  
  nchan=n_elements(sp_in[*,0])
  if nchan ne 6144 then return, -1

  nchan1=0
  nchan2=2047
  
  spnm=sp_in
  s=size(spnm)
  if s(0) eq 1 then nusp=1 else nusp=s(2)
  
  if keyword_set(std) then begin
  CASE norm OF
     1: for n=0,nusp-1 do spnm(*,n)=sp_in(*,n)/stddev(sp_in(*,n))

     3:BEGIN
        for n=0,nusp-1 do begin
           spnm[nchan1:nchan2,n]=sp_in[nchan1:nchan2,n]/stddev(sp_in[nchan1:nchan2,n])
           spnm[2048+nchan1:2048+nchan2,n]=sp_in[2048+nchan1:2048+nchan2,n]/stddev(sp_in[2048+nchan1:2048+nchan2,n])
           spnm[4096+nchan1:4096+nchan2,n]=sp_in[4096+nchan1:4096+nchan2,n]/stddev(sp_in[4096+nchan1:4096+nchan2,n])
        end        
     end
       ELSE:break
   end
end else begin
  CASE norm OF
     1: for n=0,nusp-1 do spnm(*,n)=sp_in(*,n)/total(sp_in(*,n))

     3:BEGIN
        for n=0,nusp-1 do begin
           spnm[nchan1:nchan2,n]=sp_in[nchan1:nchan2,n]/total(sp_in[nchan1:nchan2,n])
           spnm[2048+nchan1:2048+nchan2,n]=sp_in[2048+nchan1:2048+nchan2,n]/total(sp_in[2048+nchan1:2048+nchan2,n])
           spnm[4096+nchan1:4096+nchan2,n]=sp_in[4096+nchan1:4096+nchan2,n]/total(sp_in[4096+nchan1:4096+nchan2,n])
        end        
     end
       ELSE:break
   end
end

return,spnm
end

 
