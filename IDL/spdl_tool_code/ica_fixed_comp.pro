;+
; NAME:
;      Ica_Fixed_Comp
;
; PURPOSE:
;      Compute the ICA scores given the spectrum
;      and the ICA components
;
; CALLING SEQUENCE:
;      ICA_Scores = Ica_Fixed_Comp(Spectrum,ICA_Components,
;      NORM=norm, STD=std
;
; INPUTS:
;       Spectrum: The CCAM spectrum or array of spectra to
;       normalize. The dimension is [6144, Nb of spectra]
;       ICA_Components: Structure containing the element name, the
;       relevant ICA component and the the normalizartion parameter
; 
; OPTIONAL INPUTS:
;      None
;
; KEYWORD PARAMETERS:
;     NORM: if set normalize the spectra with the relevant parameter
;     STD: normalize with the standard deviation
;
; OUTPUTS:
;     ICA scores
;
; OPTIONAL OUTPUTS:
;     None
;
; SIDE EFFECTS:
;     Returns an array of pointer if the input is an array of pointer
;     and a floating point array if the input is a floating point
;     array. The type depends on wether the shot to shot analysis is
;     requested or not .
;
; PROCEDURE:
;     NORM_CC
;     ICA_SCORE

; EXAMPLE:
;     cf=Ica_Fixed_Comp(sp_in,cp_ica_new,/norm,/std)
;
; MODIFICATION HISTORY:
; O. Forni; May 2015
;-
Function ica_score,s1,c1,COV=cov

dc=size(c1)

if dc(0) eq  1 then nc=1 else nc=dc(2)
ds=size(s1)
s2=s1

case ds(0) of
    1 :ns=1
    2:NS=DS(2)
    3:ns=ds(3)
end

if ds(0) eq 3 then begin
    s1r=reform(s1,ds(1)*ds(2),ds(3))
end else begin
    s1r=s1
end

cf=fltarr(ns,nc)

if keyword_set(cov) then begin
   ;else cf=compute_ica_score(s1r,c1)
   for l=0,ns-1 do begin
     for n=0,nc-1 do cf(l,n)=correlate(s1r(*,l),c1(*,n),/cov)

   endfor

end else begin
   for l=0,ns-1 do begin
     for n=0,nc-1 do cf(l,n)=correlate(s1r(*,l),c1(*,n))

   endfor
end

return,cf

end

Function Ica_Fixed_Comp,sp_in,cp,norm=norm,std=std

  t=size(sp_in,/type)
  s=size(sp_in)
  inm1=where(cp.norm eq 1,nm1)
  inm3=where(cp.norm eq 3,nm3)
  if t eq 10 then begin
     nusp=n_elements(sp_in)
     cf=ptrarr(nusp,/allocate_heap)
     for n=0,nusp-1 do begin
         if keyword_set(norm) then begin 
            spnm3=norm_cc(*sp_in[n],3)
            spnm1=norm_cc(*sp_in[n],1)
            spnm1=spnm1*3.
         end else begin
            spnm1=*sp_in[n]*3.
            spnm3=*sp_in[n]
         end
         st=size(*sp_in[n])
         if st(0) eq 1 then nsp=1 else nsp=st(2)
         cft=fltarr(nsp,n_elements(cp))
         if keyword_set(std) then begin
            if nm1 gt 0 then  cft(*,inm1)=ica_score(spnm1,cp[inm1].cp)
            if nm3 gt 0 then  cft(*,inm3)=ica_score(spnm3,cp[inm3].cp)
         end else begin
            if nm1 gt 0 then  cft(*,inm1)=ica_score(spnm1,cp[inm1].cp,/cov)
            if nm3 gt 0 then  cft(*,inm3)=ica_score(spnm3,cp[inm3].cp,/cov)
         end
         isi= where(cft(*,0) lt 1e-2,nsi)
         if nsi gt 0 then cft(isi,0)=0.
         *cf[n]=cft
     end

  end else begin
     sr=size(sp)
     if s(0) eq 1 then nusp=1 else nusp=s(2)
     
     if keyword_set(norm) then begin 
        spnm3=norm_cc(sp_in,3)
        spnm1=norm_cc(sp_in,1)
        spnm1=spnm1*3.
     end else begin
        spnm1=sp_in*3.
        spnm3=sp_in
     end
 
 
;; compute Ica scores
     cf=fltarr(nusp,n_elements(cp))
 
     if keyword_set(std) then begin
        if nm1 gt 0 then  cf(*,inm1)=ica_score(spnm1,cp[inm1].cp)
        if nm3 gt 0 then  cf(*,inm3)=ica_score(spnm3,cp[inm3].cp)
     end else begin
        if nm1 gt 0 then  cf(*,inm1)=ica_score(spnm1,cp[inm1].cp,/cov)
        if nm3 gt 0 then  cf(*,inm3)=ica_score(spnm3,cp[inm3].cp,/cov)
     end
     isi= where(cf(*,0) lt 1e-2,nsi)
     if nsi gt 0 then cf(isi,0)=0.
     
  end

  return,cf

END
