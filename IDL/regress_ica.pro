;+
; NAME:
;       REGRESS_ICA
;
; PURPOSE:
;       Retrieves and returns absolute oxydes wt.% given the ICA scores
;
; CALLING SEQUENCE:
;       Oxy=regress_ica(Scores, Ica_rgr_param)
;
; INPUTS:
;       Scores: Computed ICA scores. Dimension [Nb of spectra, 8] if
;       mean spectra composition is computed; Pointer array of Nb of
;       spectra with dimension [Nb of shots, 8] if shot to shot
;       composition is computed.
;       Ica_rgr_param: Structure of 8 elements containing the element name, the
;       array of regression coefficients and the name of the
;       regression law to apply.    
;
; OPTIONAL INPUTS:
;       None
;
; KEYWORD PARAMETERS:
;       None
;
; OUTPUTS:
;       Array of compositions: Dimension [Nb of spectra, 8] if
;       mean spectra composition is computed; Pointer array of Nb of
;       spectra with dimension [Nb of shots, 8] if shot to shot
;       composition is computed. 
;
; OPTIONAL OUTPUTS:
;       None
;
; SIDE EFFECTS:
;      If the number of parameter is not equal to 2 returns -1

; PROCEDURE:
;      HYPTAN
;
;
; EXAMPLE:
;      cfa=regress_ica(cf,ica_rgr_new)
;
; MODIFICATION HISTORY:
; O. Forni: May 2015
;-

FUNCTION regress_ica,cf,ica_rgr
  
  If N_params() ne 2 then return,-1
  
  t=size(cf,/type)
  if t eq 10 then begin
     nsp=n_elements(cf)
     cfa=ptrarr(nsp,/allocate_heap)
;;     for n=0,nsp-1 do *cfa(n)=*cf(n)
  end else begin
     cfa=cf
     s=size(cfa)
     nsp=s(1)
  end
  
  if t eq 10 then begin
     for n=0,nsp-1 do begin
        cft=*cf(n)
        For nel=0,n_elements(ica_rgr)-1 do begin
          
           coef=(ica_rgr(nel).cf)
           case ica_rgr[nel].func of
              'exp':cft(*,nel)=hyptan(cft(*,nel),coef[0:2],/exp)
              'geom':cft(*,nel)=hyptan(cft(*,nel),coef[0:2],/geom)
              'log3':cft(*,nel)=hyptan(cft(*,nel),coef[0:2],/log3)
              'log4':cft(*,nel)=hyptan(cft(*,nel),coef,/log4)
              'par':cft(*,nel)=hyptan(cft(*,nel),coef[0:2],/par)
              'lin':cft(*,nel)=hyptan(cft(*,nel),coef[0:1])
              'tanh':cft(*,nel)=hyptan(cft(*,nel),coef,/tanh)
              else:cft(*,nel)=cft(*,nel)
           end
        end
        cft(where(cft lt 0.))=0.
        cft(where(finite(cft) eq 0))=0.
        *cfa(n)=cft
        
     end

  end else begin
     for n=0,nsp-1 do begin
        cft=cf(n,*)
        For nel=0,n_elements(ica_rgr)-1 do begin
           coef=(ica_rgr(nel).cf)
           case ica_rgr[nel].func of
              'exp':cft(*,nel)=hyptan(cft(*,nel),coef[0:2],/exp)
              'geom':cft(*,nel)=hyptan(cft(*,nel),coef[0:2],/geom)
              'log3':cft(*,nel)=hyptan(cft(*,nel),coef[0:2],/log3)
              'log4':cft(*,nel)=hyptan(cft(*,nel),coef,/log4)
              'par':cft(*,nel)=hyptan(cft(*,nel),coef[0:2],/par)
              'lin':cft(*,nel)=hyptan(cft(*,nel),coef[0:1])
              'tanh':cft(*,nel)=hyptan(cft(*,nel),coef,/tanh)
              else:cft(*,nel)=cft(*,nel)
           end
        end
  
        i0= where(cft lt 0. or finite(cft) eq 0,n0)
        if (n0 gt 0) then cft(i0)=0.
        
        cfa(n,*)=cft
 
     end
  end

  RETURN,cfa
END
