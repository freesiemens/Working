FUNCTION Chemcam_continuum,l,sp,lvmin=lvmin

  n=N_ELEMENTS(sp)
  
  
  lv=FIX(ALOG(n-1)/ALOG(2))
  
  
  ;; sp(0:20)=f_med(sp(0:20),10)
  ;; sp(n-20:*)=f_med(sp(n-20:*),10)
  sp1=sp
  sp1=MEDIAN(sp1,10)
  w=Watrous(sp1,lv)
  lvmn=lv-2
  IF (KEYWORD_SET(lvmin)) THEN BEGIN
    IF (lvmin LT lv) THEN lvmn=lvmin ELSE lvmn=lv-2
  END
  IF lvmn LE 2 THEN lvmn=2
  PRINT,lvmn
  si=TOTAL(w(*,lvmn:*),2)
  ii=FLTARR(n)
  FOR i=1,n-2 DO BEGIN IF( si(i) LT si(i+1) AND si(i) LT si(i-1)) THEN ii(i)=1 & END
  ;for i=1,n-2 do begin if( si(i) gt si(i+1) and si(i) gt si(i-1)) then ii(i)=1 & end
  ii(0)=1
  ii(n-1)=1
  i0=WHERE(ii EQ 1,n0)
  
  yi=FLTARR(n0)
  yi(0)=sp(0)
  yi(n0-1)=sp(n-1)
  FOR i=0,n0-1 DO BEGIN
    dx1=i0(i)-2^(lvmn-1)
    ;     dx1=i0(i)-20
    IF dx1 LT 0 THEN dx1=0
    dx2=i0(i)+2^(lvmn-1)
    ;    dx2=i0(i)+20
    IF dx2 GE n THEN dx2=n-1
    yi(i)=MIN(sp(dx1:dx2))
  END
  
  ;stop
  y=SPL_INIT(l(i0),yi)
  yf=SPL_INTERP(l(i0),yi,y,l)
 
  
  ;yf=interpol(yi,l(i0),l,/spline)
  RETURN,yf
  
END
