;+
; NAME:
;       REMOVE_CONTINUUM
; PURPOSE:
;       This routine removes the continuum from a Libs spectrum
;
; CALLING SEQUENCE: 
;       REMOVE_CONTINUUM, Wavelength, Spectrum, Wavelet_Scale1, Wavelet_Scale2, interpolation_Flaog

; INPUTS: 
;       Wavelength: One dimensional array of wavelengths
;       Spectrum: One dimensional array of libs intensity (same size as wavelength)
;       Wavelet_Scale1: Integer; Largest wavelet scale to start with
;       (2^Wavelet_scale) LT wavelength size)
;       Wavelet_Scale2: Integer; Lowest wavelet scale to look at (must be GE 2)
;       Interpolation_Flag: Integer; Flag to select interpolation method
;       between convex hull points
;         0: linear interpolation    
;         1: quadratic interpolation    
;         2: spline interpolation
    
; OPTIONAL INPUTS:
;
; KEYWORD PARAMETERS:
;
; OUTPUTS:
;
; OPTIONAL OUTPUTS:
;
; COMMON BLOCKS:
;
; SIDE EFFECTS:
;     The input spectrum is replaced by the spectrum - continuum
;
; RESTRICTIONS:
;
; PROCEDURE:
;
; EXAMPLE:
;     Remove_Continuum,wl, sp, 6, 4, 0
; MODIFICATION HISTORY:
;      Olivier Forni IRAP
;      First Version  June 2009
;      Add interpolation Flag October 2009
;      Modify convex hull October 2011
;-

FUNCTION Chemcam_continuum,l,sp,int_flag,lvmin=lvmin

  n=N_ELEMENTS(sp)
  
  lv=FIX(ALOG(n-1)/ALOG(2))
  
  sp1=sp
  sp1=MEDIAN(sp1,10)
  w=Watrous(sp1,lv)
  lvmn=lv-1
  IF (KEYWORD_SET(lvmin)) THEN BEGIN
    IF (lvmin LT lv) THEN lvmn=lvmin ELSE lvmn=lv-1
  END
  IF lvmn LE 1 THEN lvmn=1
  
  si=w(*,lvmn)
  ii=FLTARR(n)
  FOR i=1,n-2 DO BEGIN 
     IF( si(i) LT si(i+1) AND si(i) LT si(i-1)) THEN ii(i)=1
  END
  ii(0)=1
  ii(n-1)=1
  i0=WHERE(ii EQ 1,n0)
  
  yi=FLTARR(n0)
  yi(0)=sp(0)
  yi(n0-1)=sp(n-1)
  FOR i=0,n0-1 DO BEGIN
    dx1=i0(i)-2^(lvmn)
    ;     dx1=i0(i)-20
    IF dx1 LT 0 THEN dx1=0
    dx2=i0(i)+2^(lvmn)
    ;    dx2=i0(i)+20
    IF dx2 GE n THEN dx2=n-1
    yi(i)=MIN(sp(dx1:dx2))
  END

  case int_flag of
    0:yf=interpol(yi,l(i0),l) 
    1:if  n0 ge 3 then yf=interpol(yi,l(i0),l,/quadratic) else yf=interpol(yi,l(i0),l) 
    2: begin
 
    y=SPL_INIT(l(i0),yi)
    yf=SPL_INTERP(l(i0),yi,y,l)
    end
    end

 
  RETURN,yf
  
END

PRO Remove_continuum,x,y,lv,lvmin,int_flag

  IF N_PARAMS() NE 5 THEN BEGIN
     PRINT,'Illegal number of parameters'
     RETURN
  END

  IF size(x,/n_dimension) NE 1 THEN BEGIN
     PRINT,'Wavelength must be a 1D array'
     RETURN
  END

  IF N_ELEMENTS(y) NE N_ELEMENTS(x) THEN BEGIN
     print,'Intensity and Wavelength must have the same size'
     RETURN
  END

  IF lvmin LT 2 THEN BEGIN
     PRINT,'Lowest Wavelet Scale must be greater or equal to 2'
     RETURN
  END

  n=N_ELEMENTS(x)
  lvmax=FIX(ALOG(n-1)/ALOG(2))
  IF lv GT lvmax THEN BEGIN
     PRINT,'Largest Wavelet Scale must be less or equal to: ',lvmax
       RETURN
  END
  
  IF lvmin gt lv THEN BEGIN
      PRINT,'Lowest Wavelet Scale must be less or equal to largest Wavelet Scale'
      RETURN
   END

  IF (int_flag lt 0 OR int_flag GT 2) THEN BEGIN
     PRINT,'Valid values of the Interpolation Flag are 0,1 or 2'
     RETURN
   END

  
  stdb0=STDDEV(y)
  stdb=stdb0
  FOR il=lv,lvmin,-1 DO BEGIN
  
    WHILE stdb GT stdb0*1e-2 DO BEGIN
      sc=Chemcam_continuum(x,y,int_flag,lvmin=il)
     y=y-sc

      stdb=STDDEV(sc)

    END
    stdb0=STDDEV(y)
    stdb=stdb0
    y=y-sc
  END
  RETURN
  
END
