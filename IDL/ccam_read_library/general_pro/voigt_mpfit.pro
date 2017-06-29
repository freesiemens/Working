function voigt_mpfit, a, XVAL=x, YVAL=y, ERRVAL=err, model_out=model_out

;-----------------------------------------
;
; VOIGT_MPFIT.PRO
;
; fonction voigt avec 4 composantes utilisable par MPFIT
;
; O.F. / 0.G. 02/07
;
;------------------------------------------

if not keyword_set(err) then begin
    err = x
    err(*) = 1.
endif

model=fvoigt(x, a)
if keyword_set(model_out) then return, model else begin
    res = (y-model)/err
    return, res
endelse

end
