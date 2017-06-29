PRO interpol_chemcam_spectrum,ptr

  n= (*ptr[0]).n

  sp_type=detect_sp_type((*ptr[1]).libs_fn_init)
 
  sp=(*ptr[0]).new_spectrum(0:n-1)
  x0 = (*ptr[0]).wavelength(0:n-1)
 
  x=dindgen(n)
  wave=wvl_basis_order4(sp_type,x)

  IF max(wave) EQ -1 THEN wave=x0
  y1 = interpol(sp, x0, wave,/spline)
  
  imn = where( wave lt min(x0),mn)
  if (mn gt 0) then y1(imn) = 0.
  imx = where( wave gt max(x0),mx)
  if (mx gt 0) then y1(imx) = 0.

;;   (*ptr[1]).libs_fn_clb=Write_spectrum(x,sp,param_list,(*ptr[1]).libs_fn_init,type='calib')
   (*ptr[0]).new_spectrum(0:n-1)=y1
   (*ptr[0]).wavelength(0:n-1)=wave

END 
