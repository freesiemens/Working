;+
; NAME:
;        HYPTAN
;
; PURPOSE:
;        Computes composition from scores given a regressionlaw and
;        its parameters. Default linear regression. 
;
; CALLING SEQUENCE:
;        y = Hyptan(x, regress_coef) 
;
; INPUTS:
;        x: a 1-D array of ICA scores
;        regress_coeff: Regression coeefficients
;
; OPTIONAL INPUTS:
;        None
;
; KEYWORD PARAMETERS:
;        PAR: if set computes a parabolic regression law
;        GEOM: if set computes a parabolic regression law
;        EXP: if set computes an exponential regression law
;        TANH: if set computes a hyperbolic tangent regression law
;        LOG3: if set computes a second order logarithmic law
;        LOG4: if set computes a third order logarithmic regression law

; OUTPUTS:
;       An array of composition havind the same dimension as the ICA scores 
;
; OPTIONAL OUTPUTS:
;       None
;
; SIDE EFFECTS:
;       According to the law a NaN can be returned
;
; PROCEDURE:
;       None
;
; EXAMPLE:
;        nel = 0   
;        coef=(ica_rgr(nel).cf)
;        cfa=hyptan(cft(*,nel),coef[0:2],/exp)
;       
; MODIFICATION HISTORY:
; O. Forni: May 2015
;-
function hyptan, x, a,LOG3=log3,LOG4=log4,GEOM=geom,TANH=tanh,EXP=exp,PAR=par
  
y=a(0)+x*a(1) ;default LINEAR
if keyword_set(geom) then y=a(0)*x^a(1)+a(2)
if keyword_set(log3) then y=a(0)+a(1)*alog10(x)+a(2)*alog10(x)*alog10(x)
if keyword_set(log4) then y=a(0)+a(1)*alog10(x)+a(2)*alog10(x)*alog10(x)+a(3)*alog10(x)*alog10(x)*alog10(x)
if keyword_set(tanh) then y=a(0)*(1.+tanh((x-a(1))/a(2)))
if keyword_set(exp) then y=a(0)*a(1)^x+a(2)
if keyword_set(par) then y=a(0)+x*a(1)+x*x*a(2)

return, y

end

