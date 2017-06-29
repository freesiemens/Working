function gauss_mpfit, a, XVAL=x, YVAL=y, ERRVAL=err, model_out=model_out

;-----------------------------------------
;
; GAUSS_MPFIT.PRO
;
; fonction gaussienne avec 3 composantes utilisable par MPFIT
;
; MAMD 18/05/1999
;
;------------------------------------------

if not keyword_set(err) then begin
    err = x
    err(*) = 1.
endif

model = mgauss(x, a)
;model = 1.d*(a(0)*exp(-((x-a(1))/a(2))^2/2.) + a(3)*exp(-((x-a(4))/a(5))^2/2.) + $
;             a(6)*exp(-((x-a(7))/a(8))^2/2.)+a(9)*exp(-((x-a(10))/a(11))^2/2.))+a(12)

if keyword_set(model_out) then return, model else begin
    res = (y-model)/err
    return, res
endelse

end
