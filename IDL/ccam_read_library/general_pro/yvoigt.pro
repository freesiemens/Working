; -----------------------------------------------------------------
;
; PROCEDURE: yvoigt

; THIS FUNCTION builds the Voigt function which represents one peak.
; Several (N) peaks can be present in the Region Of Interest.
; Compute the derivative parameters too.
;
; Calculation based on McLean A.B., C.E.J. Mitchell, and
; D.M. Swantson, Implementation of an efficient analytical
; approximation to the Voigt function for photoemission lineshape
; analysis, 2002.
;
; ENTERED PARAMETERS: -> x: values at which the Voigt function
;                     -> a: vector which contains
;                          3 parameters for degree-2 polynomial
;                           a[4] + a[5]*x + a[6]*x^2
;                          4xN coefficients that characterize the N peaks:
;                           a[0] = Lorentzian amplitude
;                           a[1] = Position
;                           a[2] = Lorentzian FWHM
;                           a[3] = Gaussian FWHM
;                           ... this 4-coefficients sequence is
;                               repeated for each peak
; RETURNED PARAMETERS: -> f: the magnitude of the  function for the
;                            input x values
;                      -> pder: list of the partial derivatives
;                               relative to the m parameters in a
;
; Olivier Gasnault 2007-02 CESR
;
; -----------------------------------------------------------------

function yvoigt, x, a

    m = n_elements(a)
    n = n_elements(x)
    ; initialisations
    f = a[m-3] + a[m-2]*x + a[m-1]*x*x    ;continuum

    sqrtln2 = sqrt(alog(2.D0))
    sqrtpi = sqrt(!dpi)
    alpha = dblarr(n,4) & beta = dblarr(n,4)

    aa = [-1.2150D0, -1.3509D0, -1.2150D0, -1.3509D0]
    bb = [1.2359D0, 0.3786D0, -1.2359D0, -0.3786D0]
    cc = [-0.3085D0, 0.5906D0, -0.3085D0, 0.5906D0]
    dd = [0.0210D0, -1.1858D0, -0.0210D0, 1.1858D0]

    v = dblarr(n) & dvdx = dblarr(n) & dvdy = dblarr(n)

    ; calculations
    for i=0, (m-4), 4 do begin
	v=v*0.d
       xx = (x-a[i+1])*2.*sqrtln2/a[i+3]
       yy = a[i+2]*sqrtln2/a[i+3]
       constant = a[i+2]*a[i]*sqrtpi*sqrtln2/a[i+3]
       for j=0,3 do begin
           alpha[*,j] = cc[j]*(yy-aa[j]) + dd[j]*(xx-bb[j])
           beta[*,j] = (yy-aa[j])^2 + (xx-bb[j])^2
           v = v + alpha[*,j]/beta[*,j]
       endfor
       f = f + constant*v
        endfor
	return,f

end
