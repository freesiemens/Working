;+
; NAME:
;       WIDGET_CHEMCAM
;
; PURPOSE:
;       This routine allows read, plot and fit the ChemCam spectra
;
; CALLING SEQUENCE:
;       WIDGET_CHEMCAM
;
; COMMENTS
; v3.0 Common style programming removed. All parameters passed by
; pointers
; v4.0 Added display window in the GUI
; v4.1 Changed Calibration wavelength File and Save Buttons
; v4.2 Added sensitive and insensitive context
; v4.3 Added logfile February 2011   
; v5.0 Added Tag menu October 2011 
; v5.1 Added Zoom November 2011 
; v5.2 Added Matching filter from Jeremie December 2011 
; v5.3 Added Instrument Response function January  2012 
; V6.0 Added EDR and DP reading routine from Dot January  2012 
; V6.1 Added Calibration Status and Concatenatationuary  2012 
;      Added CCS file reading routine
;-O. FORNI IRAP

PRO chemcam_message,message,wait=time

  nm=n_elements(message)
  ms=max(strlen(message))
  base=WIDGET_BASE(/row)
  wLabel=widget_text(base,VALUE=message,FONT="Arial*18",xsize=ms,ysize=nm)
  if not keyword_set(time) then  dbut=WIDGET_BUTTON(base, value='Ok',/align_center,FONT="Arial*18")
 
 WIDGET_CONTROL,base,/REALIZE
 XMANAGER,'chemcam_message',base,/no_block
 if keyword_set(time) then begin
    wait,time
    WIDGET_CONTROL,/destroy,base      
  end
END

PRO chemcam_message_event,ev
 
  WIDGET_CONTROL,ev.id,get_value=v
    
  CASE v OF
     'Ok':Begin
        WIDGET_CONTROL,/destroy,ev.top      
     END
  END

END


PRO Chemcam_Cleanup,Id

  WIDGET_CONTROL,id,get_uvalue=ptr    
  WIDGET_CONTROL,(*ptr[0]).base_id,bad_id=bad_id
  IF bad_id EQ 0 THEN WIDGET_CONTROL, /DESTROY, (*ptr[0]).base_id
  ptr_free,ptr
  close,99
  cd,!chemcam

END

FUNCTION file_remove_ext,fn

  ; remove file extension
  p=STRPOS(fn,'.',/reverse_search)
  IF p NE -1 THEN fn1=STRMID(fn,0,p)
  
  RETURN,fn1
  
END

PRO OpenSpectrum,ev

  for lun=100,128 do free_lun,lun,/force
  WIDGET_CONTROL,ev.id,get_uvalue=ptr
  WIDGET_CONTROL,ev.id,get_value=sp_type
  wPar=WIDGET_INFO(ev.id,/PARENT)
  WIDGET_CONTROL,wPar,get_value=fmt

 ;; print,fmt,sp_type

  dist=(*ptr[5]).dist
  (*ptr(1)).libs_fn_init=Read_spectrum(wl,spectrum,fmt,sp_type,dist)
    ;      PRINT,libs_fn_init
           ; define variables

  n = N_ELEMENTS(spectrum)
  
  printlog,'Opening File: '+(*ptr(1)).libs_fn_init
  if n le 1 then begin
     v=dialog_message('Not a valid ChemCam File',/center)
     (*ptr(0)).n = 0
     printlog,'Open Failed'
    cd,!chemcam
   return
end
  printlog,'Open Succeded'


  (*ptr(0)).n = n
  (*ptr(0)).wavelength = wl
  (*ptr(0)).wavelength0 = wl
  (*ptr(0)).spectrum0 = spectrum
  (*ptr(0)).spectrum = spectrum
  (*ptr(0)).denoised_spectrum = spectrum
  (*ptr(0)).new_spectrum = spectrum
  (*ptr(0)).lmin = wl(0)
  (*ptr(0)).lmax = wl(n-1)
  (*ptr(0)).cmin = 0
  (*ptr(0)).cmax = n-1
  (*ptr(0)).lmin0 = wl(0)
  (*ptr(0)).lmax0 = wl(n-1)
  (*ptr(0)).cmin0 = 0
  (*ptr(0)).cmax0 = n-1
  (*ptr[1]).db_file=!nist+'All_10_vac.dat'
  RoiId= (*ptr(0)).roi_id
 ; print,roiid
  tmp=[ wl(0),wl(n-1)]
  WIDGET_CONTROL,RoiId,set_value=tmp
  Id2id=(*ptr(0)).id2_id
  (*ptr[0]).thresv= (*ptr[0]).thress*stddev(spectrum(0:n-1))
  tmp=[(*ptr[0]).thresv]
  WIDGET_CONTROL,Id2id,set_value=tmp
  for i=100,128 do free_lun,i,/force
  Zero,/nice
          ; define variables
  cmin = (*ptr[0]).cmin
  cmax = (*ptr[0]).cmax
  wl= (*ptr[0]).wavelength
  spectrum = (*ptr[0]).new_spectrum
  x = wl[cmin:cmax]
  y = spectrum[cmin:cmax]
  (*ptr[0]).norm_fact[0]=1.
  (*ptr[0]).norm_fact[1]=total(y)
  (*ptr[0]).norm_fact[2]=stddev(y)
  (*ptr[0]).norm_fact[3]=1.
  dx=mean(ABS(wl(1:*)-wl(0:n-2))) ; resolution

  (*ptr[2]).slit=1.
; Check if the file has already been corrected for Instrument Response
  p=strpos((*ptr(1)).libs_fn_init,'RF')
  (*ptr[5]).dist=dist
  if p GE 0 THEN (*ptr[5]).instresp=1 ELSE (*ptr[5]).instresp=0

          ; plot
  Draw_data,x,y,ptr

end

PRO PlotSpectrum,ev
 WIDGET_CONTROL,ev.id,get_uvalue=ptr
       
;if ~isa(ptr) then return
 
if  (*ptr[0]).n EQ 0 then return 
                               ; plot settings
 Zero,/nice
          ; define variables
 cmin = (*ptr[0]).cmin
 cmax = (*ptr[0]).cmax
 wl= (*ptr[0]).wavelength
 spectrum = (*ptr[0]).new_spectrum
 x = wl[cmin:cmax]
 y = spectrum[cmin:cmax]
          
          ; plot
 Draw_data,x,y,ptr
 old_dev=!d.name
 set_plot,'ps'
    
 device,file='spectrum_plot.ps',/color,bits=8
 !p.font=0 
 device,/helvetica,isolatin1=0
 title=(*ptr[1]).libs_fn_init
 plot,x,y,/xs,title=title,xtitle='Wavelength (nm)',ytitle='Intensity'
 device,/close
 set_plot,old_dev
  
END

PRO dbase,ev

  WIDGET_CONTROL,ev.id,get_uvalue=dbv
  WIDGET_CONTROL,ev.id,get_value=db
 

  CASE db of
     'Nist DB':(*dbv.ptr[1]).db_file=!nist+'All_10_vac.dat'
     'Mars DB':(*dbv.ptr[1]).db_file=!nist+'All_mars.dat'
  END
  printlog,'Selected Line Database: '+db[0]
  WIDGET_CONTROL,dbv.wdbid,SET_VALUE=db[0]

END

PRO Sp_Norm,ev
    
   WIDGET_CONTROL,ev.id,get_uvalue=ptr
   WIDGET_CONTROL,ev.id,get_value=v
   
   n=(*ptr[0]).n
   if  ((*ptr[0]).n EQ 0) then return     
   cmin = (*ptr[0]).cmin
   cmax = (*ptr[0]).cmax
   wl=(*ptr[0]).wavelength(0:n-1)
   sp=(*ptr[0]).new_spectrum(0:n-1)
   
   ; save current normalisation
   (*ptr[0]).norm_st1=(*ptr[0]).norm_st0

   CASE v of
       'None' : BEGIN
          IF (*ptr[0]).norm_st0 NE 0 THEN sp=sp* (*ptr[0]).norm_fact[3]
           (*ptr[0]).norm_st0=0
          (*ptr[0]).norm_fact[3]=1.        
       END
       'Total Emission' : BEGIN
          IF (*ptr[0]).norm_st0 NE 1 THEN sp=sp* (*ptr[0]).norm_fact[3]      
          (*ptr[0]).norm_st0=1
          (*ptr[0]).norm_fact[3]=   (*ptr[0]).norm_fact[1]      
          sp=sp/  (*ptr[0]).norm_fact[1]
       END
      'Std. Dev.': BEGIN
         IF (*ptr[0]).norm_st0 NE 2 THEN sp=sp* (*ptr[0]).norm_fact[3]
         (*ptr[0]).norm_st0=2
         (*ptr[0]).norm_fact[3]=(*ptr[0]).norm_fact[2]   
         sp=sp/(*ptr[0]).norm_fact[2]
     END
   END
   (*ptr[0]).denoised_spectrum(0:n-1)=sp
   (*ptr[0]).new_spectrum(0:n-1)=sp

   printlog,'Normalisation: '+v

   spn=(*ptr[0]).new_spectrum(0:n-1)
   Id2id=(*ptr(0)).id2_id
   (*ptr[0]).thresv=(*ptr[0]).thress*stddev(spn)
   tmp=[(*ptr[0]).thresv]
   WIDGET_CONTROL,Id2id,set_value=tmp
   Draw_data,wl,spn,ptr

END

 
PRO reset,ev

  for lun=100,128 do free_lun,lun,/force
  WIDGET_CONTROL,ev.id,get_uvalue=ptr
     
   (*ptr[0]).n=(*ptr[0]).cmax0-(*ptr[0]).cmin0+1
   (*ptr[0]).cmin=(*ptr[0]).cmin0
   (*ptr[0]).cmax=(*ptr[0]).cmax0
   (*ptr[0]).lmin=(*ptr[0]).lmin0
   (*ptr[0]).lmax=(*ptr[0]).lmax0
   (*ptr[0]).spectrum = (*ptr[0]).spectrum0
   (*ptr[0]).wavelength = (*ptr[0]).wavelength0
   (*ptr[0]).denoised_spectrum = (*ptr[0]).spectrum0
   (*ptr[0]).continuum=0.
   (*ptr[0]).new_spectrum = (*ptr[0]).spectrum0
   (*ptr[0]).norm_st0=0
   (*ptr[0]).norm_st1=0
   (*ptr[0]).norm_fact[3]=1.
  RoiId= (*ptr(0)).roi_id
   tmp=[(*ptr[0]).lmin0,(*ptr[0]).lmax0]
   
   WIDGET_CONTROL,Roiid,set_value=tmp

   sp=(*ptr[0]).new_spectrum(0:(*ptr[0]).cmax-1)
   Id2id=(*ptr(0)).id2_id
   (*ptr[0]).thresv=(*ptr[0]).thress*stddev(sp)
   tmp=[(*ptr[0]).thresv]
   WIDGET_CONTROL,Id2id,set_value=tmp

   fit_files=FILE_SEARCH('*.fit',count=nf)
   if nf gt 0 then FILE_DELETE,fit_files,/quiet
   cd,!work_dir
   printlog,'Reseting to original values'
   
   wl= (*ptr[0]).wavelength
   spectrum = (*ptr[0]).new_spectrum
   cmin = (*ptr[0]).cmin
   cmax = (*ptr[0]).cmax
   x = wl[cmin:cmax]
   y = spectrum[cmin:cmax]
  ; Check if the file has already been corrected for Instrument Response
  p=strpos((*ptr(1)).libs_fn_init,'RF')
  if p GE 0 THEN (*ptr[5]).instresp=1 ELSE (*ptr[5]).instresp=0
      
          ; plot
  Draw_data,x,y,ptr

END

PRO Quit,ev
 
  WIDGET_CONTROL,ev.id,get_uvalue=ptr
  WHILE (!d.window NE -1) DO WDELETE,!d.window
  WIDGET_CONTROL, /DESTROY, (*ptr[0]).base_id
  cd,!chemcam
  close,99

END

PRO Dns_go,ev
 
    WIDGET_CONTROL,ev.id,get_uvalue=ptr    
 
    if  (*ptr[0]).n EQ 0 then return     
    
    cmin = (*ptr[0]).cmin
    cmax = (*ptr[0]).cmax
    sp=(*ptr[0]).new_spectrum
    wl= (*ptr[0]).wavelength
    sig=(*ptr[0]).sigma

    niter=(*ptr[0]).niter
    y=sp(cmin:cmax)
    y=F_med(y,3,sign=-1,thres=.5)
    
    spd=Denoise_spectrum(y,sig=sig,niter=niter)
    (*ptr[0]).denoised_spectrum(cmin:cmax)=spd
    (*ptr[0]).new_spectrum(cmin:cmax)=spd
    x = wl[cmin:cmax]
    y = spd
    noise=sp(cmin:cmax)-spd
   
    Id2id=(*ptr(0)).id2_id
   (*ptr[0]).thresv=(*ptr[0]).thress*stddev(spd)
   tmp=[(*ptr[0]).thresv]
   WIDGET_CONTROL,Id2id,set_value=tmp
     
    Zero,/nice
     Draw_data, x, y, ptr, noise, /denoise
     printlog,'Denoising: Sigma= '+string(sig,format='(f5.1)')

 END

PRO Dns_save,ev 
  
  WIDGET_CONTROL,ev.id,get_uvalue=ptr    
 
  if  (*ptr[0]).n EQ 0 then return     
  
  cmin = (*ptr[0]).cmin
  cmax = (*ptr[0]).cmax

  param_list={infile:' ',wrange:FLTARR(2),sigma:0.0,norm:''}
  param_list.infile=(*ptr[1]).libs_fn_init
  param_list.wrange=Minmax((*ptr[0]).wavelength(cmin:cmax))
  param_list.sigma=(*ptr[0]).Sigma
  norm_st = (*ptr[0]).norm_st0
  CASE norm_st OF
     0:param_list.norm='None'
     1:param_list.norm='Total Emission'       
     2:param_list.norm='Std. Dev.'
  END
  spd=(*ptr[0]).denoised_spectrum(cmin:cmax)
        
  x = (*ptr[0]).wavelength[cmin:cmax]
  (*ptr[1]).libs_fn_dns=Write_spectrum(x,spd,param_list,(*ptr[1]).libs_fn_init,type='denoise')
  printlog,'Save denoised spectrum: '+(*ptr[1]).libs_fn_dns
END

PRO Dns_param,ev

  WIDGET_CONTROL,ev.id,get_uvalue=ptr    
  WIDGET_CONTROL,ev.id,get_value=tmp
 
  if tmp(0) LT 0. then tmp(0)=3.0
   (*ptr[0]).sigma = tmp(0)
 WIDGET_CONTROL,ev.id,set_value=tmp

 END
  
PRO roi,ev   
    
  WIDGET_CONTROL,ev.id,get_uvalue=ptr    
  WIDGET_CONTROL,ev.id,get_value=tmp
      ;tests
      
      ;store values
  n = (*ptr[0]).n
 
  if  (*ptr[0]).n EQ 0 then return  
  wl = (*ptr[0]).wavelength
  wl = wl(0:n-1)
  sp=(*ptr[0]).new_spectrum(0:n-1)

  IF tmp(1) LT tmp(0) THEN BEGIN
     v=dialog_message('Invalid wavelength range',/center)
     tmp(0)=(*ptr[0]).lmin0
     tmp(1)=(*ptr[0]).lmax0
     WIDGET_CONTROL,ev.id,set_value=tmp
     (*ptr[0]).cmin = 0
     (*ptr[0]).cmax = n-1
     Draw_data,wl,sp,ptr
    return
  END

      
  (*ptr[0]).lmin = tmp(0)
  (*ptr[0]).lmax = tmp(1)
  q = WHERE(wl GE tmp(0),nq)
  IF nq GE 1 THEN (*ptr[0]).cmin = q(0) ELSE (*ptr[0]).cmin = 0 
  IF tmp(0) lt (*ptr[0]).lmin0 THEN BEGIN
     (*ptr[0]).cmin = 0
     tmp(0)=(*ptr[0]).lmin0
     (*ptr[0]).lmin = tmp(0)
  END

  q = WHERE(wl LE tmp(1),nq)
  IF nq GT 1 THEN (*ptr[0]).cmax = q(nq-1) ELSE (*ptr[0]).cmax = n-1
  IF tmp(1) gt (*ptr[0]).lmax0 THEN BEGIN
     (*ptr[0]).cmax = n-1
     tmp(1)=(*ptr[0]).lmax0
     (*ptr[0]).lmax = tmp(1)
  END
  printlog,'RoI range changed: '+string(tmp,format='(2f7.1)')

                                ;show stored values
  WIDGET_CONTROL,ev.id,set_value=tmp

  cmin = (*ptr[0]).cmin
  cmax = (*ptr[0]).cmax
  sp=sp(cmin:cmax)
  
  Id2id=(*ptr(0)).id2_id
  (*ptr[0]).thresv=(*ptr[0]).thress*stddev(sp)
  tmp=[(*ptr[0]).thresv]
  WIDGET_CONTROL,Id2id,set_value=tmp

  x = wl[cmin:cmax]
          ; plot
  Draw_data,x,sp,ptr

END
 
PRO bkg_param,ev 

  WIDGET_CONTROL,ev.id,get_uvalue=ptr    
  WIDGET_CONTROL,ev.id,get_value=tmp
  nel=n_elements((*ptr[0]).wavelength)
  lvmax=FIX(ALOG(nel)/ALOG(2))-1
   if tmp(0) LT 2 then tmp(0)=2
   if tmp(0) gt lvmax then tmp(0)=lvmax
   (*ptr[0]).lvmin = tmp(0)
   WIDGET_CONTROL,ev.id,set_value=tmp

END

PRO Bkg_Go,ev
  
    WIDGET_CONTROL,ev.id,get_uvalue=ptr    
    WIDGET_CONTROL,ev.id,get_value=ev2
 
    if  (*ptr[0]).n EQ 0 then return     
  
    cmin = (*ptr[0]).cmin
    cmax = (*ptr[0]).cmax
    sp=(*ptr[0]).denoised_spectrum
    wl= (*ptr[0]).wavelength
    x = wl[cmin:cmax]
    y = sp[cmin:cmax]
    lvmin=(*ptr[0]).lvmin
  
    IF ev2 EQ 'Linear' THEN int_flag = 0
    IF ev2 EQ 'Quadratic' THEN int_flag = 1
    IF ev2 EQ 'Spline' THEN int_flag = 2
    (*ptr[0]).method=ev2
    
    n=N_ELEMENTS(y)
    lv=FIX(ALOG(n-1)/ALOG(2))
    IF lvmin GE lv THEN lvmin=lv-2
    Remove_continuum,x,y,lv,lvmin,int_flag
      
    sc=sp[cmin:cmax]-y
    Zero,/nice
    Draw_data, x, y, ptr, sc, /continuum
    (*ptr[0]).new_spectrum(cmin:cmax)=y
    (*ptr[0]).continuum(cmin:cmax)=sc
    
    Id2id=(*ptr(0)).id2_id
    (*ptr[0]).thresv=(*ptr[0]).thress*stddev(y)
    tmp=[(*ptr[0]).thresv]
    WIDGET_CONTROL,Id2id,set_value=tmp
    
    printlog,'Background substraction: Scale= '+string(lvmin,format='(I3)')+$
             ' Method= '+ev2

END

PRO Bkg_save,ev
    
    WIDGET_CONTROL,ev.id,get_uvalue=ptr    
  
    if  (*ptr[0]).n EQ 0 then return     
   
    cmin = (*ptr[0]).cmin
    cmax = (*ptr[0]).cmax

    param_list={infile:' ',wrange:FLTARR(2),scale:0.0,method:' ',norm:''}
    param_list.infile=(*ptr[1]).libs_fn_init
    print,param_list.infile
    param_list.wrange=Minmax((*ptr[0]).wavelength(cmin:cmax))
    param_list.scale=(*ptr[0]).lvmin
    param_list.method=(*ptr[0]).method
    norm_st=(*ptr[0]).norm_st0
    CASE norm_st OF
       0:param_list.norm='None'
       1:param_list.norm='Total Emission'       
       2:param_list.norm='Std. Dev.'
    END

   x = (*ptr[0]).wavelength[cmin:cmax]
    sp=(*ptr[0]).new_spectrum(cmin:cmax)
    
    (*ptr[1]).libs_fn_bkg=Write_spectrum(x,sp,param_list,(*ptr[1]).libs_fn_init,type='background')
    printlog,'Save background substracted spectrum: '+(*ptr[1]).libs_fn_bkg
 END

PRO Clb_match,ev
  
  WIDGET_CONTROL,ev.id,get_uvalue=ptr    
 
   if  (*ptr[0]).n EQ 0 then return     
   
   cmin = (*ptr[0]).cmin
   cmax = (*ptr[0]).cmax
   wl= (*ptr[0]).wavelength
   spectrum = (*ptr[0]).new_spectrum
   x = wl[cmin:cmax]
   y = spectrum[cmin:cmax]
  
   Draw_calib_match,x,y,ptr
 
END
        
PRO Clb_sel,ev        

   WIDGET_CONTROL,ev.id,get_uvalue=ptr    
  
   if  (*ptr[0]).n EQ 0 then return     

      cmin = (*ptr[0]).cmin
      cmax = (*ptr[0]).cmax
      wl= (*ptr[0]).wavelength
      spectrum = (*ptr[0]).new_spectrum
      x = wl[cmin:cmax]
      y = spectrum[cmin:cmax]

      (*ptr[2]).nclb=0

      Draw_calib_data,x,y,ptr
 
END
        
PRO Clb_file,ev

  WIDGET_CONTROL,ev.id,get_uvalue=ptr    
 
  if  (*ptr[0]).n EQ 0 then return

  filter = ['*.wcb']
  file = DIALOG_PICKFILE(path=!work_dir, filter=filter, /fix_filter,$
                         get_path=sel_path,title='Select Calibrated Wavelength  File', /must_exist)   
  n=(*ptr[0]).n
  printlog,'Opening Calibrated Wavelength File: '+file
  msg1='Not a valid Calibrated Wavelength File'
  IF (file EQ '') THEN BEGIN
     v=dialog_message(msg1,/center)
     printlog, msg1
     return
  END
  wl=fltarr(n)
  lf=file_lines(file)
  IF  lf NE n THEN BEGIN
     v=dialog_message(msg1,/center)
     printlog, msg1
      return
  END ELSE BEGIN
     readcol,file,wl,/silent
     if ~isa(wl) then BEGIN
     v=dialog_message(msg1,/center)
     printlog, msg1
      return
     end
     (*ptr[0]).wavelength(0:n-1)=wl
     y=(*ptr[0]).new_spectrum(0:n-1)
     Draw_data,wl,y,ptr
  END
 
END

PRO Clb_IR,ev

  WIDGET_CONTROL,ev.id,get_uvalue=ptr    
 
  n=(*ptr[0]).n
  if  n EQ 0 then return     
  
  chemcam_instrument_response,ptr

END

PRO Clb_save,ev

  WIDGET_CONTROL,ev.id,get_uvalue=ptr    
 
  n=(*ptr[0]).n
  if  n EQ 0 then return     
 
  interpol_chemcam_spectrum,ptr

  wave=(*ptr[0]).wavelength(0:n-1)
  y1=(*ptr[0]).new_spectrum(0:n-1)

  param_list={infile:' ',wrange:FLTARR(2),norm:'',instresp:0}
   param_list.infile=(*ptr[1]).libs_fn_init
   param_list.wrange=Minmax((*ptr[0]).wavelength(0:n-1))
   norm_st = (*ptr[0]).norm_st0
   CASE norm_st OF
       0:param_list.norm='None'
       1:param_list.norm='Total Emission'       
       2:param_list.norm='Std. Dev.'
    END
   IF   (*ptr[5]).instresp eq 1 THEN BEGIN
      param_list.instresp=1
   END
      
   (*ptr[1]).libs_fn_clb=Write_spectrum(wave,y1,param_list,(*ptr[1]).libs_fn_init,type='calib')
    printlog,'Save resampled and wavelength calibrated spectrum: '+(*ptr[1]).libs_fn_clb
;; Concatenate all wavelength calibrated ranges when available
    Clb_conc,ptr

END

PRO Clb_conc,ptr
;  WIDGET_CONTROL,ev.id,get_uvalue=ptr    

  n=(*ptr[0]).n
  if  n EQ 0 then return  
  
  fn=file_remove_ext((*ptr[1]).libs_fn_init)
  clb_fmt = detect_calib(fn)
  print,clb_fmt
  CASE  clb_fmt.s_clb OF
     0:v=dialog_message('UV, VIS, VNIR calibrated ranges are missing')
     1:v=dialog_message('VIS, VNIR calibrated ranges are missing')
     2:v=dialog_message('UV, VNIR calibrated ranges are missing')
     3:v=dialog_message('VNIR calibrated range is missing')
     4:v=dialog_message('UV, VIS calibrated ranges are missing')
     5:v=dialog_message('VIS calibrated range is missing')
     6:v=dialog_message('UV calibrated ranges is missing')
     7: BEGIN
        fn_uv=clb_fmt.file_clb[1]
        fn_vis=clb_fmt.file_clb[2]
        fn_vnir=clb_fmt.file_clb[3]

        openw,1,clb_fmt.file_clb[0]
        IF (*ptr[5]).instresp eq 0 THEN fmt='(2F10.3)' ELSE fmt='(F10.3,G10.3)'
        readcol,fn_uv,wl,sp,/silent
        for il=0,n_elements(wl)-1 DO printf,1,wl(il),sp(il),FORMAT=fmt
        readcol,fn_vis,wl,sp,/silent
        for il=0,n_elements(wl)-1 DO printf,1,wl(il),sp(il),FORMAT=fmt
        readcol,fn_vnir,wl,sp,/silent
        for il=0,n_elements(wl)-1 DO printf,1,wl(il),sp(il),FORMAT=fmt
        close,1
        msg=strarr(2)
        msg[0]='Wavelength calibration completed'
        msg[1]='Writing to file '+ clb_fmt.file_clb[0]
        v=dialog_message(msg,/information)
     END
  END


END

PRO Id_param1,ev

  WIDGET_CONTROL,ev.id,get_uvalue=ptr    
  WIDGET_CONTROL,ev.id,get_value=tmp
  (*ptr[0]).flt = tmp(0)
  WIDGET_CONTROL,ev.id,set_value=tmp

END

PRO Id_param2,ev

  WIDGET_CONTROL,ev.id,get_uvalue=ptr    
  WIDGET_CONTROL,ev.id,get_value=tmp

  cmin = (*ptr[0]).cmin
  cmax = (*ptr[0]).cmax
  sp=(*ptr[0]).new_spectrum(cmin:cmax)

  (*ptr[0]).thresv = tmp(0)
  (*ptr[0]).thress = tmp(0)/stddev(sp)
  
  tmp=[(*ptr[0]).thresv]

  WIDGET_CONTROL,ev.id,set_value=tmp

END

PRO Id_go,ev

  WIDGET_CONTROL,ev.id,get_uvalue=ptr    
 
  if  (*ptr[0]).n EQ 0 then return     

  cmin = (*ptr[0]).cmin
  cmax = (*ptr[0]).cmax
  wl= (*ptr[0]).wavelength(cmin:cmax)
  sbc=(*ptr[0]).new_spectrum(cmin:cmax)
; take into  account variable resolution
;  dx=abs(mean(wl(1:*)-wl))
  dx=abs(wl(1:*)-wl)
  fsize=(*ptr[0]).flt
  base_id=(*ptr[0]).base_id
  db_file=(*ptr[1]).db_file

  printlog,'Line Identification'
  sl=Chemcam_line_ident1(wl,sbc,fsize,db_file,'All',base_id,/silent,thres=.2,wrange=sqrt(fsize)*dx)  

  v=dialog_message('Line Identification completed',/information)
  printlog,'Line Identification completed'
  nel=N_ELEMENTS(sl)
  (*ptr[3]).nlines=nel
  (*ptr[3]).sp_sel[0:nel-1]=sl
  IF (sl(0).elt NE 'No') THEN BEGIN
     OPENW,LUN,File_remove_ext((*ptr[1]).libs_fn_init)+'_lines.dat',/GET_LUN
 ;    PRINTF,LUN,(*ptr[0]).norm_st
     FOR nl=0,nel-1 DO PRINTF,LUN,sl(nl),(*ptr[0]).norm_st0,format='(2A4,3F10.3,F14.3,2F10.3,2I5)'
  END
  
  ;;        end
  CLOSE,LUN
  FREE_LUN,LUN
END


PRO Id_elt,ev

  WIDGET_CONTROL,ev.id,get_uvalue=ptr    
  
  n=(*ptr[0]).n
  if n EQ 0 then return     
 
 ; define variables
  cmin = (*ptr[0]).cmin
  cmax = (*ptr[0]).cmax
  wl= (*ptr[0]).wavelength
  spectrum = (*ptr[0]).new_spectrum
  thres = (*ptr[0]).thresv
  x = wl[cmin:cmax]
  y = spectrum[cmin:cmax]
  
;  fl_info=FILE_INFO(File_remove_ext((*ptr[1]).libs_fn_init)+'_lines.dat')
 
  nlines=(*ptr[3]).nlines
  IF nlines GT 0 THEN BEGIN
     sl=(*ptr[3]).sp_sel[0:nlines-1]
 
    IF (*ptr[0]).norm_st0 NE (*ptr[0]).norm_st1 THEN $
        sl.intensity=sl.intensity * (*ptr[0]).norm_fact[(*ptr[0]).norm_st1] / (*ptr[0]).norm_fact[(*ptr[0]).norm_st0]^2
 
;  IF (fl_info.exists EQ 1 AND fl_info.size GT 0) THEN BEGIN
 ;   sl=Read_line_file(File_remove_ext((*ptr[1]).libs_fn_init)+'_lines.dat')
    sel_sl=sl(WHERE(sl.wav GE wl(cmin) AND sl.wav LE wl(cmax)))
    is=WHERE(sel_sl.intensity GE thres)
    nel=N_ELEMENTS(sel_sl(is))
    (*ptr[4]).nlines=nel
    (*ptr[4]).sel_sl[0:nel-1]=sel_sl(is)
    name=sel_sl(is).elt
    i_name=SORT(name)
    name=name(i_name)
    name=[name,'All']
    name_list=name(UNIQ(name))
    (*ptr[4]).nelt=n_elements(name_list)
    (*ptr[4]).name_list[0:n_elements(name_list)-1]=name_list
    (*ptr[4]).ind_name[*]=0
   
    Sel_menu,ptr,'ident'

 END

END

PRO Id_Load,ev

 WIDGET_CONTROL,ev.id,get_uvalue=ptr    
 if  (*ptr[0]).n EQ 0 then return 

 norm_st=(*ptr[0]).norm_st0
 line_file=File_remove_ext((*ptr[1]).libs_fn_init)+'_lines.dat'
 fl_info=FILE_INFO(line_file)
 printlog,'Loading Line File: '+line_file

  IF (fl_info.exists EQ 1 AND fl_info.size GT 0) THEN BEGIN
     nrm=-1
    sl=Read_line_file(line_file,nrm)
    if sl[0].elt eq '' then begin
       v=dialog_message('Not a valib line file',/center)  
       printlog,'Not a valib line file'
    return
    end ELSE nlines=n_elements(sl)

;    print,nlines
    v=dialog_message('Loading Line File...',/center,/information)  
    (*ptr[3]).nlines=nlines
    IF nlines GT 0 THEN BEGIN
        (*ptr[3]).sp_sel[0:nlines-1]=sl
        if nrm NE norm_st THEN BEGIN
           sl.intensity=sl.intensity / (*ptr[0]).norm_fact[3]
           msg=strarr(4)
           msg[0]='Different Normalisation'
           CASE norm_st OF
              0:snrm0='None'
              1: snrm0='Total Emission'
              2:snrm0='Std. Dev.'
           END
           sl.intensity=sl.intensity / (*ptr[0]).norm_fact[3] * (*ptr[0]).norm_fact[norm_st]
          CASE nrm OF
              0:snrm1='None'
              1:snrm1='Total Emission'
              2:snrm1='Std. Dev.'
           END
           msg[1]='Spectrum: '+snrm0
           msg[2]='Line File: '+snrm1
           msg[3]='Renormalizing Line Intensities to '+snrm0
           print,(*ptr[0]).norm_fact
           (*ptr[3]).sp_sel[0:nlines-1].intensity=sl.intensity
            (*ptr[0]).norm_st0=nrm
          v=dialog_message(msg,/center)
           printlog,msg
       END

     END
 END ELSE BEGIN
    msg='Line File does not exist or is invalid'
    v=dialog_message(msg,/center)  
 printlog,msg
;     CHEMCAM_MESSAGE,'Not a valib line file'
    return
 END

END


PRO id_plt,ev
    
 WIDGET_CONTROL,ev.id,get_uvalue=ptr    
 
 if  (*ptr[0]).n EQ 0 then return     

 nlines=(*ptr[4]).nlines

 IF nlines GT 0 THEN BEGIN
    cmin = (*ptr[0]).cmin
    cmax = (*ptr[0]).cmax
    wl= (*ptr[0]).wavelength
    spectrum = (*ptr[0]).new_spectrum
    thres = (*ptr[0]).thresv
    x = wl[cmin:cmax]
    y = spectrum[cmin:cmax]
 
    sl=(*ptr[4]).sel_sl[0:nlines-1]
    sel_sl=sl(WHERE(sl.wav GE wl[cmin] AND sl.wav LE wl[cmax]))
    is=WHERE(sel_sl.intensity GE thres)
    sel_sl=sel_sl(is)
    name=sel_sl.elt
    i_name=SORT(name)
    name=name(i_name)
END  ELSE return
 
 nelt=(*ptr[4]).nelt
 p=WHERE((*ptr[4]).ind_name[0:nelt-1] EQ 1,nn)
 
 IF nn GT 0 THEN BEGIN
    name_list=(*ptr[4]).name_list
    p_ind=LONARR(N_ELEMENTS(name))
    IF name_list(p(nn-1)) EQ 'All' THEN p_ind(*)=1 ELSE BEGIN 
       p_ind(*)=0
       
       FOR n=0,nn-1 DO BEGIN
          kn=where(name eq name_list(p(n)))
          p_ind(kn)=1   
       END
        
     END
        
        ;;                print,p_ind
    ip=WHERE(p_ind EQ 1)
    sel_sl=sel_sl(i_name(ip))
    name_list=name_list(p)
    is=sort(sel_sl.wav)
    sel_sl=sel_sl(is)

    (*ptr[4]).nplot=0
    (*ptr[4]).nid=n_elements(sel_sl)
    (*ptr[4]).plot_id(0:n_elements(sel_sl)-1)=sel_sl
    Draw_data, x, y, ptr, sel_sl
        
     Chemcam_plot, x, y, sel_sl,ps=File_remove_ext((*ptr[1]).libs_fn_init)+'_lines',title=File_remove_ext((*ptr[1]).libs_fn_init)+' Identified Lines'
 

  END
END



PRO Fit_elt,ev

 WIDGET_CONTROL,ev.id,get_uvalue=ptr
 WIDGET_CONTROL,ev.id,get_value=v
 
 if  (*ptr[0]).n EQ 0 then return     

CASE v OF
   'Elements':BEGIN
      nlines=(*ptr[4]).nlines
      IF nlines GT 0 THEN  BEGIN
         sl=(*ptr[4]).sel_sl
         (*ptr[4]).type='Elt'
        END ELSE RETURN
   END
   'Selected Lines':BEGIN
      nlines=(*ptr[4]).nplot
      IF nlines GT 0 THEN  BEGIN
         sl=(*ptr[4]).plot_l(0:nlines-1) 
         (*ptr[4]).type='Sel'
         il=sort(sl.lwav)
         sl=sl(il)
         ilu=uniq(sl.lwav)
         sel_sl=sl(ilu)
          nel=n_elements(sel_sl.lwav)
         (*ptr[4]).nplot=nel
         (*ptr[4]).plot_l(0:nel-1)=sel_sl
    END ELSE RETURN
   END
END


cmin = (*ptr[0]).cmin
cmax = (*ptr[0]).cmax
wl= (*ptr[0]).wavelength
spectrum = (*ptr[0]).new_spectrum
thres = (*ptr[0]).thresv
x = wl[cmin:cmax]
y = spectrum[cmin:cmax]
 
sel_sl=sl(WHERE(sl.wav GE wl(cmin) AND sl.wav LE wl(cmax)))
is=WHERE(sel_sl.intensity GE thres)
sel_sl=sel_sl(is)
name=sel_sl.elt+' '+sel_sl.ex_st
i_name=SORT(name)
name=name(i_name)
name=[name,'All']
name_list=name(UNIQ(name))
(*ptr[4]).nelt=n_elements(name_list)
(*ptr[4]).name_list[0:n_elements(name_list)-1]=name_list
(*ptr[4]).ind_name=0
   
Sel_menu,ptr,'fit'
     
END

PRO Fit_go,ev

  WIDGET_CONTROL,ev.id,get_uvalue=ptr
  WIDGET_CONTROL,ev.id,get_value=v
  if  (*ptr[0]).n EQ 0 then return     
  CASE (*ptr[4]).type of
     'Elt':BEGIN
        nlines=(*ptr[4]).nlines
        sel_sl=(*ptr[4]).sel_sl[0: nlines-1]
     END
     'Sel':BEGIN
        nlines=(*ptr[4]).nplot
        sel_sl=(*ptr[4]).plot_l[0: nlines-1]
      END
     ELSE: return
  END
 
  cmin = (*ptr[0]).cmin
  cmax = (*ptr[0]).cmax
  wl= (*ptr[0]).wavelength
  spectrum = (*ptr[0]).new_spectrum
  thres = (*ptr[0]).thresv
  x =	 wl[cmin:cmax]
  y = spectrum[cmin:cmax]

  ind_name=(*ptr[4]).ind_name
;; Take into account eventual zoom
  i_sel=where(sel_sl.lwav GE wl[cmin] AND sel_sl.lwav LE wl[cmax],ns)

;  print,ns,wl[cmin], wl[cmax]
;  help,sel_sl

  IF ns LT 0 THEN RETURN

  sel_sl=sel_sl(i_sel)
;  ind_name=ind_name(i_sel)

  p=WHERE(ind_name EQ 1,nn)
;      print,nn,ind_name
  IF nn GT 0 THEN BEGIN
     name=sel_sl.elt+' '+sel_sl.ex_st
     name_list=(*ptr[4]).name_list
     p_ind=LONARR(nlines)
     IF name_list(p(nn-1)) EQ 'All' THEN p_ind(*)=1 ELSE BEGIN 
        p_ind(*)=0
        FOR n=0,nn-1 DO BEGIN
           kn=where(name eq name_list(p(n)))
           p_ind(kn)=1
        END     
     END

 ;       print,p_ind
     ip=WHERE(p_ind EQ 1)
     sel_slf=sel_sl(ip)

   CASE v OF
        'Gaussian' :BEGIN
           npar=3
           yf=Chemcam_fit(x,y,sel_slf.wav,fp,pf)
        END
        'Lorentz' :BEGIN
           npar=3
           yf=Chemcam_fit(x,y,sel_slf.wav,/lorentz,fp,pf)
        END
        'Voigt' :BEGIN
           npar=4
      yf=Chemcam_fit(x,y,sel_slf.wav,/voigt,fp,pf)
   END
    
     ENDCASE
     p_fit=fp
     fit_func=v
  
     OPENW,lun,(*ptr[1]).libs_fn_init+'.fit',/get_lun,/append
     PRINTF,lun,fit_func
     nsel=n_elements(ip)
     PRINT,nsel
     FOR n=0,nsel-1 DO BEGIN
        PRINTF,lun,sel_slf(n),format='(2A4,3F10.3,F14.3,E13.3,F14.3,I5,2F10.3,I5)'
        line_int=Int_line(p_fit(n*npar:n*npar+npar-1),fit_func)
        PRINTF,lun,p_fit(n*npar:n*npar+npar-1)
        PRINTF,lun,line_int
     END
  
     CLOSE,lun
     free_lun,lun

 ;    stop
     Zero,/nice
     
     (*ptr[0]).fit[cmin:cmax]=yf
     (*ptr[4]).plot_fit[0:n_elements(sel_slf)-1]=sel_slf
     Draw_Data,x,y,ptr,sel_slf,yf=yf
;  Chemcam_plot,x,y,sel_sl,yf=yf
     Chemcam_plot,x,y,sel_slf,yf=yf,ps='chemcam'

  END
END

PRO Sel_Cleanup,Id

  WIDGET_CONTROL,id,get_uvalue=ptr

  sptr=size(ptr)
  ns=n_elements(sptr)

  IF (sptr(ns-2) eq 8) THEN BEGIN
    WIDGET_CONTROL, ptr.base_id ,sensitive=1
  END
END

PRO Sel_menu,ptr,menu_id

  nelt=(*ptr[4]).nelt
  base = (*ptr[0]).base_id
  WIDGET_CONTROL, base ,sensitive=0
  Done_uv={bv:'done',base_id:base}
 IF nelt GE 20 THEN $
    base1=WIDGET_BASE(/COLUMN,/scroll,xsize=150,scr_ysize=800,uvalue=Done_uv) ELSE $
    base1=WIDGET_BASE(/COLUMN, KILL_NOTIFY='Sel_Cleanup',uvalue=Done_uv)

  gr_elt1=CW_BGROUP(base1,(*ptr[4]).name_list[0:nelt-1],/NONEXCLUSIVE,uvalue=ptr,$
                   SET_VALUE=(*ptr[4]).ind_name[0:nelt-1],FONT="Arial*18")
  dbut=WIDGET_BUTTON(base1, value='Done',uvalue=Done_uv,/align_center,FONT="Arial*18")
  WIDGET_CONTROL,base1,/REALIZE
  XMANAGER,'sel_menu',base1,/no_block

END

PRO Sel_menu_event,ev
 
  WIDGET_CONTROL,ev.id,get_value=v
  WIDGET_CONTROL,ev.id,get_uvalue=ptr
  WIDGET_CONTROL,ev.top,get_uvalue=uv
  
  sptr=size(ptr)
  ns=n_elements(sptr)

  IF (sptr(ns-2) eq 8) THEN BEGIN
    WIDGET_CONTROL, ptr.base_id ,sensitive=1
    WIDGET_CONTROL,/destroy,ev.top
  END ELSE (*ptr[4]).ind_name=v  

END

PRO clb_cleanup,ID

WIDGET_CONTROL,Id,get_uvalue=uv1

WIDGET_CONTROL,uv1.base_clb_id,SENSITIVE=1

END


PRO Calib_menu,p,sel_sl,ptr,base_clb_id,menu_id

  v1={but:'sel',sel_sl:sel_sl,ptr:ptr}
  v2={but:'done',sel_sl:sel_sl,ptr:ptr,base_clb_id:base_clb_id}
  IF N_ELEMENTS(p) GE 20 THEN $
    base1=WIDGET_BASE(uvalue=v2,/COLUMN,/scroll,scr_ysize=800,scr_xsize=500,kill_notify='clb_cleanup') ELSE $
    base1=WIDGET_BASE(uvalue=v2,/COLUMN,kill_notify='clb_cleanup')
  gr_elt1=CW_BGROUP(base1,p,/EXCLUSIVE,uvalue=v1,FONT="Arial*18")
  dbut=WIDGET_BUTTON(base1, value='Done',uvalue=v2,/align_center,FONT="Arial*18")
  WIDGET_CONTROL,base1,/REALIZE
  XMANAGER,'calib_menu',base1,/no_block
  
END

PRO Calib_menu_event,ev
  
  WIDGET_CONTROL,ev.id,get_value=v
  WIDGET_CONTROL,ev.id,get_uvalue=uv1
  WIDGET_CONTROL,ev.top,get_uvalue=uv

  ptr=uv1.ptr
  IF (uv1.but eq 'done') THEN BEGIN
     IF (*ptr).x1((*ptr).nclb) gt 0 THEN BEGIN
      (*ptr).nclb += 1
;      PRINT,(*ptr).x1
      WIDGET_CONTROL,/destroy,ev.top
      confirm_calib,ptr
       WIDGET_CONTROL,uv1.base_clb_id,SENSITIVE=1
     
     END
  END ELSE  BEGIN
 ;    PRINT,v
     (*ptr).x1((*ptr).nclb)=uv1.sel_sl(v).wav
  END

END


PRO confirm_calib,ptr

  label=strarr(2)
  label[0]='Calibrate observed line at '+string((*ptr).x0((*ptr).nclb-1),format='(F7.3)')+' nm'
 label[1]='with theoretical line at '+string((*ptr).x1((*ptr).nclb-1),format='(F7.3)')+' nm'

v=dialog_message(label,/question,/center)
CASE v OF
     'No':Begin
       (*ptr).x0((*ptr).nclb) =0.
       (*ptr).x1((*ptr).nclb) =0.
       (*ptr).nclb -=1
    END
    else:break 
END

END

PRO Clb_Quit,ev
 
  WIDGET_CONTROL,ev.id,get_uvalue=ptr
  Draw = (*ptr[0]).text_id
  base = (*ptr[0]).base_id
  WIDGET_CONTROL, base ,sensitive=1
  WIDGET_CONTROL, draw, GET_VALUE=drawID
                                ; Make the draw widget the current IDL drawable area.
  WSET, drawID
;
  tmp=WIDGET_INFO(ev.top,FIND_BY_UNAME='BASE_SYN')
  WIDGET_CONTROL, /DESTROY, tmp


END

PRO Slit_param,ev

  WIDGET_CONTROL,ev.id,get_uvalue=ptr    
  WIDGET_CONTROL,ev.id,get_value=tmp

  n = (*ptr[0]).n
  x = (*ptr[0]).wavelength(0:n-1)
  dx=mean(ABS(x(1:*)-x(0:n-2))) ; resolution

  if tmp(0) LT 0. then tmp(0)= dx
   (*ptr[2]).slit = tmp(0)
 WIDGET_CONTROL,ev.id,set_value=tmp

END

PRO Clb_go_match,ev

  WIDGET_CONTROL,ev.id,get_uvalue=ptr  
  n= (*ptr[0]).n
  n_clb=  (*ptr(0)).n_clb
  
  IF (n EQ 0 OR n_clb EQ 0 )THEN RETURN
 
  cmin=(*ptr[0]).cmin
  cmax=(*ptr[0]).cmax

  wl0=(*ptr[0]).wavelength[cmin:cmax]
  y0=(*ptr[0]).new_spectrum[cmin:cmax]

  wl1=(*ptr[0]).clb_wavelength[cmin:cmax]
  y1=(*ptr[0]).clb_spectrum[cmin:cmax]
  
  optishift=findgen(2048)
  optiarray=y0
  maxshift=6.0
  doplot=0
  spline=1
  MatchFilt1, wl1, y1, y0, optishift, optiarray, MAXSHIFT=maxshift, DOPLOT = doplot, SPLINE=spline
  (*ptr[0]).wavelength=wl1
  (*ptr[0]).new_spectrum=optiarray

  
  wl1=(*ptr[0]).wavelength[0:n-1]
  optiarray= (*ptr[0]).new_spectrum[0:n-1]

  clb_file=file_remove_ext((*ptr[1]).libs_fn_init)+'.wcb'
  (*ptr[1]).libs_fn_wcb=clb_file
  OPENW,lun,clb_file,/get_lun
  FOR i=0,n-1 DO printf,lun,wl1(i)
  CLOSE,lun
  free_lun,lun
 
  PLOT, wl1, optiarray > 0, title=title, xtitle='Wavelength (nm)', ytitle='Intensity', /ynoz, xr=[MIN(wl1),MAX(wl1)],/xs
   col = (*ptr[2]).col
 
 oplot,wl1,y1/max(y1)*max(optiarray),col=col[4]

  Match_draw,ev

RETURN
END

PRO Clb_go_syn,ev

  WIDGET_CONTROL,ev.id,get_uvalue=ptr  
   n= (*ptr[0]).n
  if n EQ 0 then return     
 
  nclb=(*ptr[2]).nclb
 
  IF nclb lt 2 THEN return

  x0=(*ptr[2]).x0
  x1=(*ptr[2]).x1
  wl=(*ptr[0]).wavelength[0:n-1]
  y=(*ptr[0]).new_spectrum[0:n-1]

  print,x0(0:nclb-1),x1(0:nclb-1)
  IF (nclb eq 2) THEN BEGIN
     pl=LINFIT(x0(0:nclb-1),x1(0:nclb-1)) 
     x=wl*pl(1)+pl(0)
  end else begin
     pl=poly_fit(x0(0:nclb-1),x1(0:nclb-1),2)
     x=wl*wl*pl(2)+wl*pl(1)+pl(0)
  end

  (*ptr[0]).wavelength[0:n-1]=x
  (*ptr[2]).nclb=0

 ; interpol_chemcam_spectrum,ptr
  
 ; x=(*ptr[0]).wavelength[0:n-1]

  clb_file=file_remove_ext((*ptr[1]).libs_fn_init)+'.wcb'
  (*ptr[1]).libs_fn_wcb=clb_file
;  print,clb_file
;  clb_exst=FILE_TEST(clb_file)
;  print,clb_exst
   ;    IF clb_exst EQ 0 THEN BEGIN
  OPENW,lun,clb_file,/get_lun
  FOR i=0,n-1 DO printf,lun,x(i)
  CLOSE,lun
  free_lun,lun
 

   syn_but,ev

END

PRO Calib_Cleanup,Id

WIDGET_CONTROL,Id,get_uvalue=ptr

Draw = (*ptr[0]).text_id
base = (*ptr[0]).base_id
WIDGET_CONTROL, base ,sensitive=1
WIDGET_CONTROL, draw, GET_VALUE=drawID
                                ; Make the draw widget the current IDL drawable area.
WSET, drawID

END

PRO Draw_calib_match,x,y,ptr

  base_id=(*ptr[0]).base_id
  WIDGET_CONTROL,base_id,sensitive=0
  zero,/nice

  wBase_clb = WIDGET_BASE(title='Plot Calibrated Spectrum', /COLUMN, uname='BASE_SYN', uvalue=ptr,KILL_NOTIFY='Calib_cleanup')
  (*ptr[0]).base_clb_id=wBase_clb

  base_calib_but= WIDGET_BASE( wbase_clb ,/row)

  open_button=WIDGET_BUTTON(base_calib_but,VALUE='Open',UVALUE=ptr,xsize=50,EVENT_PRO='Match_Open',TOOLTIP='Open Wavelength Calibrated Spectrum')

  go_but=WIDGET_BUTTON(base_calib_but,VALUE='Go',UVALUE=ptr,xsize=50,EVENT_PRO='Clb_go_match',TOOLTIP='Perform Wavelength Calibration and Save Wavelength Calibration File [*.wcb]')
  
  clb_quit= WIDGET_BUTTON(base_calib_but,VALUE='Quit',EVENT_PRO='Clb_quit',uvalue=ptr)
 base_calib_draw = WIDGET_BASE(wBase_clb,/column)

  wdraw=WIDGET_DRAW(base_calib_draw,xsize=2000,ysize=400,x_scroll_size=800,y_scroll_size=400,/button_events,/MOTION_EVENTS,UNAME='DRAW',UVALUE=ptr,EVENT_PRO='Match_Draw')

  label1 = WIDGET_LABEL(base_calib_draw, XSIZE=1000*.9,UNAME='LBL1', $
    VALUE='Wavelength:',FONT="Arial*18")
  label2 = WIDGET_LABEL(base_calib_draw, XSIZE=1000*.9,UNAME='LBL2', $
                        VALUE='Intensity:',FONT="Arial*18")
  
  WIDGET_CONTROL, wBase_clb, /REALIZE

  XMANAGER, '', wBase_clb,/no_block
  
  WIDGET_CONTROL,wDraw,GET_VALUE=fenetre
  WSET,fenetre
  
  cw=!p.clip
; WIDGET_CONTROL,go_but,SET_UVALUE=uv
;  print,wBase_clb,wdraw

  WIDGET_CONTROL,wDraw,SET_UVALUE=ptr

  PLOT, x, y > 0, title=title, xtitle='Wavelength (nm)', ytitle='Intensity', /ynoz, xr=[MIN(x),MAX(x)],/xs

END

PRO Draw_calib_data,x,y,ptr
  
;  if (*ptr[2]).nclb eq n_elements((*ptr[2]).x0)-1 then return
  base_id=(*ptr[0]).base_id
  WIDGET_CONTROL,base_id,sensitive=0
 zero,/nice
 
  wBase_clb = WIDGET_BASE(title='Plot Synthetic Spectrum', /COLUMN, uname='BASE_SYN', uvalue=ptr,KILL_NOTIFY='Calib_cleanup')
  (*ptr[0]).base_clb_id=wBase_clb
  
  base_calib_but= WIDGET_BASE( wbase_clb ,/row)
  sptype=detect_sp_type((*ptr[1]).libs_fn_init)
  case sptype of
     'UV':  name_list=(*ptr[2]).name_list_uv
     'VIS':  name_list=(*ptr[2]).name_list_vis
     'VNIR':  name_list=(*ptr[2]).name_list_vnir
     else:name_list=(*ptr[2]).name_list
  end

  slit=(*ptr[2]).slit

  for nm=0,n_elements(name_list)-1 do but1 =  WIDGET_BUTTON(base_calib_but,VALUE=name_list(nm),UVALUE=ptr,xsize=50,EVENT_PRO='syn_But')
  slit_table = WIDGET_TABLE(base_calib_but,format='(F4.2)',$
    column_labels=['Slit (px)'],/editable,uvalue=ptr, value=[slit],$
    /no_row_headers,/align_center,event_pro='slit_param')
   (*ptr[0]).slit_id=slit_Table

    go_but=WIDGET_BUTTON(base_calib_but,VALUE='Go',UVALUE=ptr,xsize=50,EVENT_PRO='Clb_go_syn',TOOLTIP='Perform Wavelength Calibration and Save Wavelength Calibration File [*.wcb]')
   clb_quit= WIDGET_BUTTON(base_calib_but,VALUE='Quit',EVENT_PRO='Clb_quit',uvalue=ptr)
 base_calib_draw = WIDGET_BASE(wBase_clb,/column)

  wdraw=WIDGET_DRAW(base_calib_draw,xsize=2000,ysize=400,x_scroll_size=800,y_scroll_size=400,/button_events,/MOTION_EVENTS,UNAME='DRAW',UVALUE=uv,EVENT_PRO='syn_Draw')

  label1 = WIDGET_LABEL(base_calib_draw, XSIZE=1000*.9,UNAME='LBL1', $
    VALUE='Wavelength:',FONT="Arial*18")
  label2 = WIDGET_LABEL(base_calib_draw, XSIZE=1000*.9,UNAME='LBL2', $
                        VALUE='Intensity:',FONT="Arial*18")
  label3 = WIDGET_LABEL(base_calib_draw, XSIZE=1000*.9,UNAME='LBL3', $
                        VALUE='Calib Info:',FONT="Arial*18")
 ;
  WIDGET_CONTROL, wBase_clb, /REALIZE

  XMANAGER, '', wBase_clb,/no_block
  
  WIDGET_CONTROL,wDraw,GET_VALUE=fenetre
  WSET,fenetre
  
  cw=!p.clip
  (*ptr[2]).ind_name=0
  uv={ptr:ptr,l_el:0.,cw:cw}
; WIDGET_CONTROL,go_but,SET_UVALUE=uv
  WIDGET_CONTROL,wDraw,SET_UVALUE=uv

  PLOT, x, y > 0, title=title, xtitle='Wavelength (nm)', ytitle='Intensity', /ynoz, xr=[MIN(x),MAX(x)],/xs
 
END

PRO Match_Open,ev

  WIDGET_CONTROL, ev.id, GET_UVALUE=ptr

  n = (*ptr[0]).n
  IF n EQ 0 THEN RETURN
  filter = ['*.txt', '*.dat','*.Scope','*.dns','*.bkg','*.clb','*.edr,','*.dp']
  file = dialog_pickfile(path=!work_dir, filter=filter, /fix_filter,$
                         get_path=sel_path,$
                         title='Select Data Spectrum to Read', /must_exist)

                                ; if the user did not click on the cancel button of the dialog pickfile:
  if ( file ne '' ) then begin
                                ; read ASCII file
     readcol,file,wl,spectrum,/silent,comment=';',format='f,f' 
  end else begin
     wl=0.
     spectrum=0.
  end

  n = N_ELEMENTS(spectrum)
  
  printlog,'Opening Wavelength Calibrated File: '+file
  if n le 1 then begin
     v=dialog_message('Not a valid ChemCam File',/center)
     (*ptr(0)).n_clb = 0
     printlog,'Open Failed'
     cd,!chemcam
     return
  end
  (*ptr(0)).n_clb = n
 printlog,'Open Succeded'
     
  cmin=(*ptr[0]).cmin
  cmax=(*ptr[0]).cmax
  y = (*ptr[0]).new_spectrum(cmin:cmax)
 
  (*ptr[0]).clb_wavelength=wl
  (*ptr[0]).clb_spectrum=spectrum
  
   col = (*ptr[2]).col
   
   wDraw=WIDGET_INFO(ev.top,FIND_BY_UNAME='DRAW')

   plot,wl,y > 0, title=title, xtitle='Wavelength (nm)', ytitle='Intensity', /ynoz, xr=[MIN(wl),MAX(wl)],/xs
   oplot,wl,spectrum/max(spectrum)*max(y),col=col[4]

  Match_Draw,ev

END

PRO Match_Draw,ev

  WIDGET_CONTROL, ev.id, GET_UVALUE=ptr
  wLabel1=WIDGET_INFO(ev.top,FIND_BY_UNAME='LBL1')
  wLabel2=WIDGET_INFO(ev.top,FIND_BY_UNAME='LBL2')


  n = (*ptr[0]).n
  IF n EQ 0 THEN RETURN

  wDraw=WIDGET_INFO(ev.top,FIND_BY_UNAME='DRAW')
;;  print,ev.top,wDraw
  ;; wset,wDraw
  cw=!p.clip

  cmin=(*ptr[0]).cmin
  cmax=(*ptr[0]).cmax
  x = (*ptr[0]).wavelength(cmin:cmax)
  dx=ABS(MEAN(x(1:*)-x))        ; resolution
  y = (*ptr[0]).new_spectrum(cmin:cmax)
 
  ymnx=CONVERT_COORD(cw([0,2]),cw([1,3]),/device,/to_data)
  ymin=ymnx(1,0)
  ymax=ymnx(1,1)

  IF (TAG_NAMES(ev, /STRUCTURE_NAME) EQ 'WIDGET_DRAW') THEN BEGIN
     
     IF ev.release NE 4 THEN BEGIN
        
        xy=CONVERT_COORD(ev.x,ev.y,/device,/to_data)
        iint=WHERE(x GE xy(0)-dx AND x LE xy(0)+dx,nint)
        IF Nint GT 0 THEN its=y(iint(0)) ELSE its=9999
       
        WIDGET_CONTROL, wlabel1, $
                        SET_VALUE='Wavelength: ' + STRING(xy(0),format='(F8.3)')
        WIDGET_CONTROL, wlabel2, $
                        SET_VALUE='Intensity: ' + STRING(its,format='(G11.3)')
     ENDIF
  ENDIF

END

PRO Syn_Draw,ev
  
  WIDGET_CONTROL, ev.id, GET_UVALUE=uv
  ;;  wDraw=WIDGET_INFO(ev.top,FIND_BY_UNAME='DRAW')
;;   WIDGET_CONTROL,wDraw,GET_VALUE=fenetre
;;   WSET,fenetre

  wLabel1=WIDGET_INFO(ev.top,FIND_BY_UNAME='LBL1')
  wLabel2=WIDGET_INFO(ev.top,FIND_BY_UNAME='LBL2')
  wLabel3=WIDGET_INFO(ev.top,FIND_BY_UNAME='LBL3')

  ;stop

  n=(*uv.ptr[0]).n
  if n eq 0 then return 

;  zero,/nice
  cmin=(*uv.ptr[0]).cmin
  cmax=(*uv.ptr[0]).cmax
  x = (*uv.ptr[0]).wavelength(cmin:cmax)
   dx=abs(mean(x(1:*)-x))
  y = (*uv.ptr[0]).new_spectrum(cmin:cmax)
 
  l_el=uv.l_el
  xmin=MIN(x)
  xmax=MAX(x)

  cw=uv.cw
;  !x.s=stash.cx
;  !y.s=stash.cy
  
  ymnx=CONVERT_COORD(cw([0,2]),cw([1,3]),/device,/to_data)
  ymin=ymnx(1,0)
  ymax=ymnx(1,1)

  ind_name=(*uv.ptr[2]).ind_name
  i_ind =where(ind_name eq 1,nelt)
  
  IF (TAG_NAMES(ev, /STRUCTURE_NAME) EQ 'WIDGET_DRAW') THEN BEGIN
     
     IF ev.release NE 4 THEN BEGIN
        
        xy=CONVERT_COORD(ev.x,ev.y,/device,/to_data)
        iint=WHERE(x GE xy(0)-dx AND x LE xy(0)+dx,nint)
        IF Nint GT 0 THEN its=y(iint(0)) ELSE its=9999
        IF nelt gt 0 THEN BEGIN
           cinf=WHERE(uv.l_el.wav GE xy(0)-2*dx AND uv.l_el.wav LE xy(0)+2*dx,nc)
           IF nc GT 0 THEN BEGIN
              nel=cinf(0)
              clab=uv.l_el(nel).elt+' '+ uv.l_el(nel).ex_st+$
                   STRING(uv.l_el(nel).wav,format='(F8.3)')+$
                   STRING(FLOAT(uv.l_el(nel).intensity),format='(F8.3)')
           END ELSE clab=' '
        END ELSE clab=' '
        
        WIDGET_CONTROL, wlabel1, $
                        SET_VALUE='Wavelength: ' + STRING(xy(0),format='(F8.3)')
        WIDGET_CONTROL, wlabel2, $
                        SET_VALUE='Intensity: ' + STRING(its,format='(F8.3)')
        WIDGET_CONTROL, wlabel3, $
                        SET_VALUE='Calib Info: ' + clab
     ENDIF
     IF (ev.press and nelt gt 0) THEN BEGIN
       
    
                                ; Select DB lines that are at a distance
                                ; less than 1 nm from the observed one 
        xmn=xy(0)-1.0
        xmx=xy(0)+1.0        
 ;       PRINT,xy(0),xmn,xmx
;        OPLOT,[xy(0),xy(0)],[ymin,ymax],col=2
        il=WHERE(l_el.wav GE xmn AND  l_el.wav LE xmx,n_l)
        
        IF n_l GT 0 THEN BEGIN

           nt=5
          i1=WHERE(x GE xy(0)-10*dx AND x LE xy(0)+10*dx)
          xf=x(i1)
          yf=y(i1)
          slit=(*uv.ptr[2]).slit
          peak_id=chemcam_detect_peak(yf,2*dx,thres=1.)
          if peak_id.nlines eq 1 then oplot,[xf[peak_id.ind],xf[peak_id.ind]],[ymin,ymax],col=2 else OPLOT,[xy(0),xy(0)],[ymin,ymax],col=2
         if peak_id.nlines eq 1 then a=[yf[peak_id.ind],xf[peak_id.ind],slit*dx,0.,0.] else  a=[its,xy(0),2*slit,0.,0.]
          sy=yf*0+1
          parinfo = REPLICATE({value:0.D, fixed:0, limited:[0,0],limits:[0.D,0.]},nt)
          ifx=0
          parinfo(ifx).limited(0)=1
          parinfo(ifx).limits(0)=0.
          ;              parinfo(ifx+1).fixed=1
          parinfo(ifx+1).limited(0)=1
          parinfo(ifx+1).limits(0)=xy(0)-2*slit*dx
          parinfo(ifx+1).limited(1)=1
          parinfo(ifx+1).limits(1)=xy(0)+2*slit*dx
          
          ;             parinfo(ifx+2).fixed=1
          parinfo(ifx+2).limited(0)=1
          parinfo(ifx+2).limits(0)=0.
          parinfo(ifx+2).limited(1)=1
          parinfo(ifx+2).limits(1)=4*dx*slit
          
          yfit = Mpfitpeak(xf, yf, a,nterms=nt,parinfo=parinfo,/lorentzian)
                  
  ;        PRINT,a
          
          (*uv.ptr[2]).x0[(*uv.ptr[2]).nclb]=a(1)
          
          sel_sl=l_el(il)
    
          name=sel_sl.elt+' '+sel_sl.ex_st
          i_name=SORT(name)
          name=name(i_name)
          
          name_list=name(UNIQ(name))
          line_list=STRARR(n_l)
          FOR nl=0,n_l-1 DO BEGIN
            line_list(nl)=sel_sl(nl).elt+' '+ sel_sl(nl).ex_st+$
              STRING(sel_sl(nl).wav,format='(F10.3)')+$
              STRING(FLOAT(sel_sl(nl).intensity),format='(F8.3)')+$
                     STRING(sel_sl(nl).wav-a(1),format='(F10.3)')
          END
          
          
  ;        ind_name=INTARR(N_ELEMENTS(name_list))
          WIDGET_CONTROL,(*uv.ptr[0]).base_clb_id,SENSITIVE=0
          Calib_menu,line_list,sel_sl,uv.ptr[2],(*uv.ptr[0]).base_clb_id,'elt'
          
       END

     END
   
  END

END


PRO syn_but,ev

  WIDGET_CONTROL, ev.id, GET_UVALUE=ptr
  WIDGET_CONTROL,ev.id,get_value=elt


  n = (*ptr[0]).n
  IF n EQ 0 THEN RETURN
  
  cmin=(*ptr[0]).cmin
  cmax=(*ptr[0]).cmax

  p=strpos(elt,'*')
  if p ge 0 then eltn=strmid(elt,0,p) else eltn=elt

  name=(*ptr[2]).name_list
  nind=where(strmatch(name,eltn) eq 1,ni)

  IF ni GT 0 THEN BEGIN
     IF  (*ptr[2]).ind_name[nind] EQ 1 THEN BEGIN
        (*ptr[2]).ind_name[nind] = 0 
        selt=name(nind)
        WIDGET_CONTROL,ev.id,SET_VALUE=selt[0]
     END ELSE BEGIN
        (*ptr[2]).ind_name[nind] = 1
        selt=name(nind)+'*'
        WIDGET_CONTROL,ev.id,SET_VALUE=selt[0]
     END
  END

 ind_name=(*ptr[2]).ind_name
 
 i_ind0 =where(ind_name eq 0,nelt0)
 i_ind1 =where(ind_name eq 1,nelt1)
  
  cmin=(*ptr[0]).cmin
  cmax=(*ptr[0]).cmax
 x = (*ptr[0]).wavelength(cmin:cmax)
 dx=ABS(MEAN(x(1:*)-x)) ; resolution
  y = (*ptr[0]).new_spectrum(cmin:cmax)
  col = (*ptr[2]).col

  y_el=fltarr(n_elements(x),(*ptr[2]).nelt)
;Impose Mars DB for wavelength calibration
;  db_file=!nist+'All_mars.dat'
  db_file=(*ptr[1]).db_file
  mx2=MAX(y)
  slit= (*ptr[2]).slit

 IF nelt1 GT 0 THEN BEGIN
 
    l_el=Read_nist_file(db_file,name(i_ind1(0)),exst=3,wmin=min(x),wmax=max(x),/silent)
    a1=Create_param_list(l_el.intensity,l_el.wav,FLTARR(N_ELEMENTS(l_el))+2.*slit*dx,/lorentz)
    y_el(*,i_ind1(0))=Lorentz(x,a1)
    y_el(*,i_ind1(0))= y_el(*,i_ind1(0))/max(y_el(*,i_ind1(0)))*mx2
 ;   icol(0)=col(i_ind1(0))

    FOR i=1,nelt1-1 DO BEGIN
       l1=Read_nist_file(db_file,name(i_ind1(i)),exst=3,wmin=min(x),wmax=max(x),/silent)
       l_el=[l1,l_el]
       a1=Create_param_list(l1.intensity,l1.wav,FLTARR(N_ELEMENTS(l1))+dx*1.5,/lorentz)
            ;             help,l1,a1
       y_el(*,i_ind1(i))=Lorentz(x,a1) 
       y_el(*,i_ind1(i))= y_el(*,i_ind1(i))/max(y_el(*,i_ind1(i)))*mx2
;       icol(i)=col(i_ind1(i))
         ;            help,l_el,a_el
    END
 END

if nelt1 eq 0 then l_el=0.
loadct,39,/silent

PLOT, x, y > 0, title=title, xtitle='Wavelength (nm)', ytitle='Intensity', /ynoz, xr=[MIN(x),MAX(x)],/xs 
 
for n_el=0,nelt1-1 do OPLOT,x,y_el(*,i_ind1(n_el)),col=col[i_ind1(n_el)]
; oplot,x,y-min(y)


wDraw=WIDGET_INFO(ev.top,FIND_BY_UNAME='DRAW')
cw=!p.clip

uv={ptr:ptr,l_el:l_el,cw:cw}
WIDGET_CONTROL,wDraw,SET_UVALUE=uv

; print,(*ptr[2]).ind_name
END

PRO Line_Cleanup, ID

  WIDGET_CONTROL,id,get_uvalue=uv1
   
  WIDGET_CONTROL,uv1.base_id,SENSITIVE=1

END

PRO line_menu,p,sel_sl,ptr,base_id,menu_id

  v1={but:'sel',sel_sl:sel_sl,ptr:ptr}
  v2={but:'done',sel_sl:sel_sl,ptr:ptr,base_id:base_id}
  WIDGET_CONTROL,base_id,SENSITIVE=0
 
  IF N_ELEMENTS(p) GE 20 THEN $
    base1=WIDGET_BASE(uvalue=v2,/COLUMN,/scroll,scr_ysize=800,scr_xsize=500,title=p(0),KILL_NOTIFY='Line_Cleanup') ELSE $
    base1=WIDGET_BASE(uvalue=v2,/COLUMN,title=p(0),xsize=350,KILL_NOTIFY='Line_Cleanup')
  gr_elt1=CW_BGROUP(base1,p(1:*),/NONEXCLUSIVE,uvalue=v1,FONT="Arial*18")
  dbut=WIDGET_BUTTON(base1, value='Done',uvalue=v2,/align_center,FONT="Arial*18")
  WIDGET_CONTROL,base1,/REALIZE
  XMANAGER,'line_menu',base1,/no_block
  
END

PRO line_menu_event,ev

 
  WIDGET_CONTROL,ev.id,get_value=v
  WIDGET_CONTROL,ev.id,get_uvalue=uv1
  WIDGET_CONTROL,ev.top,get_uvalue=uv
   
  ptr=uv1.ptr
  IF (uv1.but eq 'done') THEN BEGIN
     nl=N_ELEMENTS(uv1.sel_sl)
     ind_name=(*ptr).ind_name[0:nl-1]
     p=where(ind_name eq 1,np)
     IF np gt 0 then begin
        nplot=(*ptr).nplot
        sel_l=uv1.sel_sl
        for nl=0,np-1 do begin
           (*ptr).plot_l(nl+nplot).elt=sel_l(p(nl)).elt
           (*ptr).plot_l(nl+nplot).ex_st=sel_l(p(nl)).ex_st            
           (*ptr).plot_l(nl+nplot).wav=sel_l(p(nl)).wav            
           (*ptr).plot_l(nl+nplot).lwav=sel_l(p(nl)).lwav            
           (*ptr).plot_l(nl+nplot).intensity=sel_l(p(nl)).intensity
        end
        (*ptr).nplot += np
        WIDGET_CONTROL,/destroy,ev.top
        WIDGET_CONTROL,uv1.base_id,SENSITIVE=1
     END
  END ELSE  BEGIN
     (*ptr).ind_name=v
  END

 
END


PRO Draw_lines_data_event, ev

  WIDGET_CONTROL, ev.handler, GET_UVALUE=stash
 
  cw=stash.cw
  !x.s=stash.cx
  !y.s=stash.cy
 
  ptr=stash.ptr
;;  sel_sl=(*ptr[4]).plot_id
  sel_sl=stash.sel_sl

  ymnx=CONVERT_COORD(cw([0,2]),cw([1,3]),/device,/to_data)
  ymin=ymnx(1,0)
  ymax=ymnx(1,1)

  xc=stash.wl
 dx=ABS(MEAN(xc(1:*)-xc)) ; resolution
  yc=stash.rint
  
  noid_l={elt:' ',ex_st:' ',lwav:0.,wav:0.,relint:0.,intensity:0.,corr_gr:0.,corr_li:0.,group:1}

  ipeak_wl=uniq(sel_sl.wav) ; wavelength of identified peak over the threshokd
  peak_wl=sel_sl(ipeak_wl).wav
;  print,peak_wl
  IF (TAG_NAMES(ev, /STRUCTURE_NAME) EQ 'WIDGET_DRAW') THEN BEGIN
     IF ev.release NE 4 THEN BEGIN
    
      xy=CONVERT_COORD(ev.x,ev.y,/device,/to_data)
      iint=WHERE(stash.wl GE xy(0)-dx AND stash.wl LE xy(0)+dx,nint)
      IF Nint GT 0 THEN its=stash.rint(iint(0)) ELSE its=9999
      linf=WHERE(peak_wl GT xy(0)-dx AND peak_wl Lt xy(0)+dx,nc)
      IF nc GT 0 THEN BEGIN
          nel=linf(0)
         llab=STRING(peak_wl(nel),format='(F8.3)')
      END ELSE llab=' '
      WIDGET_CONTROL, stash.label1, $
        SET_VALUE='Wavelength: ' + STRING(xy(0),format='(F8.3)')
      WIDGET_CONTROL, stash.label2, $
        SET_VALUE='Intensity: ' + STRING(its,format='(G13.3)')
      WIDGET_CONTROL, stash.label3, $
        SET_VALUE='Line Detected: ' + llab

;Zoom in
      IF ev.release EQ 1 THEN BEGIN
         xy1=CONVERT_COORD(ev.x,ev.y,/device,/to_data)
         
         n0=n_elements(stash.wl)/2
         IF n0 GT 16 THEN BEGIN
            cmin=(*ptr[0]).cmin
            cmax=(*ptr[0]).cmax
            wl=(*ptr[0]).wavelength
            sp=(*ptr[0]).new_spectrum
            n=(*ptr[0]).n
            ix=where(wl GE xy1(0))
            ix0=ix(0)
            dx0=n0/2
            dx1=dx0
            
            IF ix0 - n0/2 LT 0 THEN BEGIN
               dx0=ix0
               dx1=n0/2
            END
         
            IF ix0 + n0/2 GT n THEN BEGIN
               dx1=n-ix0-1
               dx0=n0/2
            END
           
           ;; dx1=cmax-ix0
           ;; dx=min([dx0,dx1])/2
      ;;     print,ix0,n0,dx0,dx1
            (*ptr[0]).cmin=ix0-dx0
            (*ptr[0]).cmax=ix0+dx1
            (*ptr[0]).lmin=wl(ix0-dx0)
            (*ptr[0]).lmax=wl(ix0+dx1)
           
; Update RoI
            RoiId= (*ptr(0)).roi_id
            tmp=[ wl(ix0-dx),wl(ix0+dx)]
            WIDGET_CONTROL,RoiId,set_value=tmp
  
 ;          PRINT,ix0,stash.wl(ix0),dx
            draw_data,wl(ix0-dx0:ix0+dx1),sp(ix0-dx0:ix0+dx1),ptr,sel_sl
         END
      END

;Zoom out
         IF ev.release EQ 2 THEN BEGIN

            n=(*ptr[0]).n
            wl=(*ptr[0]).wavelength     
            sp=(*ptr[0]).new_spectrum     
            dx=max(stash.wl)-min(stash.wl)
            x0=dx*.5
            dm=(max(stash.wl)+min(stash.wl))*.5
            wl0=dm-dx
            wl1=dm+dx
   ;         print,dx,dm,wl0,wl1
            IF wl0 LT (*ptr[0]).lmin0 THEN BEGIN 
               wl0=(*ptr[0]).lmin0
               (*ptr[0]).cmin=0
            END ELSE BEGIN
               i0=where(wl GE wl0)
               (*ptr[0]).cmin=i0(0)
            END
            (*ptr[0]).lmin=wl0
     
            IF wl1 GT (*ptr[0]).lmax0 THEN BEGIN 
               wl1=(*ptr[0]).lmax0
               (*ptr[0]).cmax=n-1
            END ELSE BEGIN
               i1=where(wl GE wl1)
               (*ptr[0]).cmax=i1(0)
            END
            (*ptr[0]).lmax=wl1
; Update RoI
            RoiId= (*ptr(0)).roi_id
            tmp=[ wl0,wl1]
            WIDGET_CONTROL,RoiId,set_value=tmp
; Update RoI
 
    ;       PRINT,dx,wl0,wl1,(*ptr[0]).cmin,(*ptr[0]).cmax
            sel_sl=(*ptr[4]).Plot_id
            nid=(*ptr[4]).nid
             draw_data,wl((*ptr[0]).cmin:(*ptr[0]).cmax),sp((*ptr[0]).cmin:(*ptr[0]).cmax),ptr,sel_sl(0:nid-1)
           END


      IF (ev.press and nc gt 0) THEN BEGIN
          xmn=xy(0)-dx
          xmx=xy(0)+dx
  ;        OPLOT,[xy(0),xy(0)],[ymin,ymax],col=2
          il=where(sel_sl.wav ge xmn and sel_sl.wav le xmx,n_l)
;          print,n_l,xy(0)
          sel_l=sel_sl(il)
          if n_l gt 0 then begin         
              name=sel_l.elt+' '+sel_l.ex_st
              i_name=SORT(name)
              name=name(i_name)
              name_list=name
              name0=sel_l.elt
              i_name=SORT(name0)
              name0=name0(i_name)
              maxint=fltarr(n_elements(name0))
       
              for n=0,n_elements(name0)-1 do begin
                 if name0(n) ne '?' then begin
                    sl=read_nist_file((*ptr[1]).db_file,name0(n),/silent,exst=3)
                    maxint(n)=max(sl.intensity)
                 end else maxint(n)=0.

              end

              line_list=STRARR(n_l+2)
              line_list(0)='Peak at '+string(xy(0),format='(F8.3)')+ ' nm'
              dl=abs(sel_l(0).wav - sel_l.lwav)
              dl=sort(dl)
              sel_l=sel_l(dl)
              noid_l.elt='?'
              noid_l.ex_st='?'
              noid_l.wav=xy(0)
              noid_l.lwav=xy(0)
              noid_l.intensity=sel_l(0).intensity
              sel_l=[sel_l,noid_l]
              FOR nl=0,n_l-1 DO BEGIN
                 in=where(strmatch(name,sel_l(nl).elt))
                 line_list(nl+1)=STRING(sel_l(nl).elt+' '+ sel_l(nl).ex_st,format='(A6)')+$
                                 STRING(sel_l(nl).lwav,format='(F10.3)')+$
                                 STRING(sel_l(nl).relint/maxint(in)*100.,format='(F7.3)')+$
                                 STRING(sel_l(nl).corr_li,format='(F7.3)')+$
                                 STRING(sel_l(nl).corr_gr,format='(F7.3)')+$
                                 STRING(sel_l(nl).relint/maxint(in)*100.*sel_l(nl).corr_li*sel_l(nl).corr_gr,format='(F10.3)')
              END
              line_list(nl+1)='?'
 ;             print,line_list
              (*ptr[4]).ind_name=0
              line_menu,line_list,sel_l,ptr[4],(*ptr[0]).base_id,'elt'
              nel=(*ptr[4]).nplot

              IF nel GT 0 THEN BEGIN
                 plot_l=(*ptr[4]).plot_l(0:nel-1)
                 il=sort(plot_l.lwav)
                 plot_l=plot_l(il)
                 ilu=uniq(plot_l.lwav)
                 plot_l=plot_l(ilu)
                 nel=n_elements(plot_l.lwav)
                 (*ptr[4]).nplot=nel
                 (*ptr[4]).plot_l(0:nel-1)=plot_l
              END
         
          END

      END
 
  END ELSE BEGIN
  
    image_file_name=File_remove_ext((*ptr(1)).libs_fn_init)+'_lines.png'
    DEVICE, GET_DECOMPOSED=old_decomposed
    DEVICE, DECOMPOSED=0
    TVLCT,r,g,b,/get
    saveimg=TVRD()
                                ;       print,image_file_name_sel
    WRITE_IMAGE,image_file_name,'png',saveimg,r,g,b
    v=dialog_message('Saving PNG file: '+image_file_name,/information)
    DEVICE, DECOMPOSED=old_decomposed 
  
     nel=(*ptr[4]).nplot
     if nel gt 0 then begin
        image_file_name_sel=File_remove_ext((*ptr(1)).libs_fn_init)+'_sel.png'
        zero,/nice
        window,/free
  ;      print,!d.window
        wset,!d.window
        plot_l=(*ptr[4]).plot_l(0:nel-1)
        chemcam_plot,xc,yc,plot_l,title=File_remove_ext((*ptr[1]).libs_fn_init)+' Selected Lines'

       DEVICE, GET_DECOMPOSED=old_decomposed
        DEVICE, DECOMPOSED=0
        TVLCT,r,g,b,/get
         saveimg=TVRD()
 ;       print,image_file_name_sel
        WRITE_IMAGE,image_file_name_sel,'png',saveimg,r,g,b
        v=dialog_message('Saving PNG file: '+image_file_name_sel,/information)
        DEVICE, DECOMPOSED=old_decomposed 
         chemcam_plot,xc,yc,plot_l,ps=File_remove_ext((*ptr(1)).libs_fn_init)+'_sel_lines',title=File_remove_ext((*ptr[1]).libs_fn_init)+' Selected Lines'
        OPENW,1,File_remove_ext((*ptr(1)).libs_fn_init)+'_sel_lines.dat'
        FOR nl=0,nel-1 DO PRINTF,1,plot_l(nl),format='(2A4,3F10.3,F14.3,2F10.3,I5)'
  
        CLOSE,1
    
      end
 ;     WIDGET_CONTROL, ev.TOP, /DESTROY
  END
    
ENDIF

END

PRO Draw_data_event, ev
 
  WIDGET_CONTROL, ev.handler, GET_UVALUE=stash
  xc=stash.wl
  yc=stash.rint
  ptr=stash.ptr

  cw=!p.clip
  !x.s=stash.cx
  !y.s=stash.cy
 
 dx=ABS(MEAN(xc(1:*)-xc)) ; resolution
  
  IF (TAG_NAMES(ev, /STRUCTURE_NAME) EQ 'WIDGET_DRAW') THEN BEGIN
   
 
     IF ev.release NE 4 THEN BEGIN
       
; Zoom In
        IF ev.release EQ 1 THEN BEGIN
  
           xy1=CONVERT_COORD(ev.x,ev.y,/device,/to_data)
  
           n0=n_elements(stash.wl)/2
           IF n0 GT 16 THEN BEGIN
              cmin=(*ptr[0]).cmin
              cmax=(*ptr[0]).cmax
              wl=(*ptr[0]).wavelength
              sp=(*ptr[0]).new_spectrum
              n=(*ptr[0]).n
              ix=where(wl GE xy1(0))
              ix0=ix(0)
              dx0=n0/2
              dx1=dx0
 
              IF ix0 - n0/2 LT 0 THEN BEGIN
                 dx0=ix0
                 dx1=n0/2
              END

              IF ix0 + n0/2 GT n THEN BEGIN
                 dx1=n-ix0-1
                 dx0=n0/2
              END
           
           ;; dx1=cmax-ix0
           ;; dx=min([dx0,dx1])/2
      ;;     print,ix0,n0,dx0,dx1
              (*ptr[0]).cmin=ix0-dx0
              (*ptr[0]).cmax=ix0+dx1
              (*ptr[0]).lmin=wl(ix0-dx0)
              (*ptr[0]).lmax=wl(ix0+dx1)
           
; Update RoI
              RoiId= (*ptr(0)).roi_id
              tmp=[ wl(ix0-dx0),wl(ix0+dx1)]
              WIDGET_CONTROL,RoiId,set_value=tmp
              
              x=wl(ix0-dx0:ix0+dx1)
              y=sp(ix0-dx0:ix0+dx1)
 ;          PRINT,ix0,stash.wl(ix0),dx
              CASE stash.draw_type OF
                 -1: draw_data,x,y,ptr
                 0:Draw_data,x,y,ptr,(*ptr[0]).continuum[ix0-dx0:ix0+dx1],/continuum
                 2: draw_data,x,y,ptr,(*ptr[4]).plot_fit,yf=(*ptr[0]).fit(ix0-dx0:ix0+dx1)
                 ELSE:break
              END
           END

        END

;Zoom out
         IF ev.release EQ 2 THEN BEGIN

            n=(*ptr[0]).n

            wl=(*ptr[0]).wavelength     
            sp=(*ptr[0]).new_spectrum     
            dx=max(stash.wl)-min(stash.wl)
            x0=dx*.5
            dm=(max(stash.wl)+min(stash.wl))*.5
            wl0=dm-dx
            wl1=dm+dx
   ;         print,dx,dm,wl0,wl1
            IF wl0 LT (*ptr[0]).lmin0 THEN BEGIN 
               wl0=(*ptr[0]).lmin0
               (*ptr[0]).cmin=0
            END ELSE BEGIN
               i0=where(wl GE wl0)
               (*ptr[0]).cmin=i0(0)
            END
            (*ptr[0]).lmin=wl0
     
            IF wl1 GT (*ptr[0]).lmax0 THEN BEGIN 
               wl1=(*ptr[0]).lmax0
               (*ptr[0]).cmax=n-1
            END ELSE BEGIN
               i1=where(wl GE wl1)
               (*ptr[0]).cmax=i1(0)
            END
            (*ptr[0]).lmax=wl1
; Update RoI
            RoiId= (*ptr(0)).roi_id
            tmp=[ wl0,wl1]
            WIDGET_CONTROL,RoiId,set_value=tmp
  
    ;       PRINT,dx,wl0,wl1,(*ptr[0]).cmin,(*ptr[0]).cmax
         CASE stash.draw_type OF
            -1:  draw_data,wl((*ptr[0]).cmin:(*ptr[0]).cmax),sp((*ptr[0]).cmin:(*ptr[0]).cmax),ptr
            0: draw_data,wl((*ptr[0]).cmin:(*ptr[0]).cmax),sp((*ptr[0]).cmin:(*ptr[0]).cmax),ptr,(*ptr[0]).continuum[(*ptr[0]).cmin:(*ptr[0]).cmax],/continuum
            2:draw_data,wl((*ptr[0]).cmin:(*ptr[0]).cmax),sp((*ptr[0]).cmin:(*ptr[0]).cmax),ptr,(*ptr[4]).plot_fit,yf=(*ptr[0]).fit((*ptr[0]).cmin:(*ptr[0]).cmax)
            ELSE:break
           END
      END

    

      xy=CONVERT_COORD(ev.x,ev.y,/device,/to_data)
      iint=WHERE(stash.wl GE xy(0)-dx AND stash.wl LE xy(0)+dx,nint)
      IF Nint GT 0 THEN its=stash.rint(iint(0)) ELSE its=9999
      WIDGET_CONTROL, stash.label1, $
        SET_VALUE='Wavelength: ' + STRING(xy(0),format='(F8.3)')
      WIDGET_CONTROL, stash.label2, $
        SET_VALUE='Intensity: ' + STRING(its,format='(G13.3)')
        
    END ELSE BEGIN
 ;     rgb=coul8()       
        DEVICE, GET_DECOMPOSED=old_decomposed
        DEVICE, DECOMPOSED=0
  ;      TVLCT,r,g,b,/get
        saveimg=TVRD(/TRUE)
        WRITE_IMAGE,stash.fn,'png',saveimg
         v=dialog_message('Saving PNG file: '+stash.fn,/information)
       DEVICE, DECOMPOSED=old_decomposed 
  ;      WIDGET_CONTROL, ev.TOP, /DESTROY
    END
    
  ENDIF
  
END

PRO Draw_data, x,y,ptr,sl, denoise=denoise, continuum=continuum,yf=yf

;  WIDGET_CONTOL,ev.id,GET_UVALUE=ptr
  
  Draw = (*ptr[0]).text_id
  basep = (*ptr[0]).base_plot_id
  based =(*ptr[0]).base_id

  IF N_PARAMS() EQ 4 THEN BEGIN
    draw_type=3
    IF KEYWORD_SET(continuum) THEN draw_type=0
    IF KEYWORD_SET(denoise) THEN draw_type=1
    IF KEYWORD_SET(yf) THEN draw_type=2
 END ELSE BEGIN
    draw_type=-1
 END

 (*ptr[0]).draw_type=draw_type

  zero,/nice
  
  ; Retrieve the widget ID of the draw widget. Note that the widget
  ; hierarchy must be realized before you can retrieve this value.
  Bgeom=WIDGET_INFO(based,/GEOMETRY)
  dy=(*ptr[0]).head_size
;  Bdraw=WIDGET_INFO(draw,/GEOMETRY)
;  print,bgeom.xsize,bgeom.ysize,bgeom.xsize,bgeom.ysize
  WIDGET_CONTROL, draw, GET_VALUE=drawID,DRAW_XSIZE=bgeom.xsize,DRAW_YSIZE=Bgeom.ysize-dy
  
 
  ; Make the draw widget the current IDL drawable area.
  WSET, drawID
;  PRINT,N_PARAMS()
  loadct,3,/silent
  title=(*ptr(1)).libs_fn_init
 
  IF N_PARAMS() EQ 4 THEN BEGIN
    CASE draw_type OF
      0: BEGIN

        !p.multi=[0,0,2]
        PLOT, x,y ,title=title+' Continuum Removed Spectrum',xtitle='Wavelength (nm)', ytitle='Intensity',/xs,/ynoz
        PLOT, x,y+sl ,title=title+' Continuum ',xtitle='Wavelength (nm)', ytitle='Intensity',/xs,/ynoz
        OPLOT,x,sl,thick=2,line=2
      END
      1: BEGIN
        !p.multi=[0,0,2]
        PLOT, x, y, title=title+' Denoised Spectrum',xtitle='Wavelength (nm)', ytitle='Intensity', /ynoz, xr=[MIN(x),MAX(x)],/xs
        PLOT, x,sl, title='Noise',xtitle='Wavelength (nm)', ytitle='Intensity', /ynoz, xr=[MIN(x),MAX(x)],/xs
      END
      2: BEGIN
;         help,yf
        !p.multi=[0,0,2]
        Chemcam_plot,x,y,sl,title=title+ ' Lines Fit',yf=yf
        PLOT, x,y-yf ,title=title+' Fit Residual ',xtitle='Wavelength (nm)', ytitle='Intensity',/xs,/ynoz
     END
      3: BEGIN
         Chemcam_plot, x, y, sl,title=title+' Identified Lines'
 
        END
    END
  END ELSE BEGIN
    PLOT, x, y >0 ,title=title, xtitle='Wavelength (nm)', ytitle='Intensity', /ynoz, xr=[MIN(x),MAX(x)],/xs
    (*ptr(1)).image_file_name=File_remove_ext((*ptr(1)).libs_fn_init)+'.png'
  END
 ;  print, draw_type
   cw=!p.clip
   cx=!x.s
   cy=!y.s
 
  IF N_PARAMS() EQ 4 THEN BEGIN
    CASE draw_type OF
      0:image_file_name=File_remove_ext((*ptr(1)).libs_fn_init)+'_continuum.png'
      1:image_file_name=File_remove_ext((*ptr(1)).libs_fn_init)+'_denoised.png'
      2:image_file_name=File_remove_ext((*ptr(1)).libs_fn_init)+'_fit.png'
      3:image_file_name=File_remove_ext((*ptr(1)).libs_fn_init)+'_lines.png'
   END
END ELSE BEGIN
    image_file_name=File_remove_ext((*ptr(1)).libs_fn_init)+'.png'
 END
  
label1=(*ptr[0]).lbl1
label2=(*ptr[0]).lbl2

  ; Create an anonymous array to hold the spectrum data and widget IDs
  ; of the label widgets.
  stash = { fn:image_file_name,wl:x, rint:y, label1:label1, label2:label2,cw:cw,cx:cx,cy:cy,ptr:ptr,draw_type:draw_type}
  IF draw_type EQ 3 THEN BEGIN
     label3=(*ptr[0]).lbl3
    WIDGET_CONTROL, label3, $
        SET_VALUE='Line Info: '
  
    stash = {  fn:image_file_name,wl:x, rint:y, label1:label1, label2:label2, label3:label3,cw:cw,cx:cx,cy:cy,sel_sl:sl,ptr:ptr,draw_type:draw_type}
 ENDIF

  ;
  ; Set the user value of the top-level base widget equal to the
  ; 'stash' array.
  WIDGET_CONTROL, basep, SET_UVALUE=stash
 
  CASE draw_type OF
       3: XMANAGER, 'draw_lines_data', basep, /NO_BLOCK  
      
      ELSE: XMANAGER, 'draw_data', basep, /NO_BLOCK
  END

END

PRO Widget_chemcam_event,ev

  IF (TAG_NAMES(ev, /STRUCTURE_NAME) EQ 'WIDGET_TAB') THEN return
  WIDGET_CONTROL,ev.top,GET_UVALUE=ptr
;  print,ev.top
   wDraw=WIDGET_INFO(ev.top,FIND_BY_UNAME='DRAW_DATA')
   dy=(*ptr[0]).head_size
 
  IF (TAG_NAMES(ev, /STRUCTURE_NAME) NE 'WIDGET_DRAW') THEN BEGIN
      WIDGET_CONTROL,wDraw,DRAW_YSIZE=ev.y-dy,DRAW_XSIZE=ev.x
      wl= (*ptr[0]).wavelength
      spectrum = (*ptr[0]).new_spectrum
      cmin = (*ptr[0]).cmin
      cmax = (*ptr[0]).cmax
      x = wl[cmin:cmax]
      y = spectrum[cmin:cmax]
      IF (*ptr[0]).draw_type EQ -1 THEN BEGIN
          ; plot
         Draw_data,x,y,ptr
      END
      IF (*ptr[0]).draw_type EQ 0 THEN BEGIN
         sel_sl=(*ptr[0]).continuum[cmin:cmax]
         Draw_data,x,y,ptr,sel_sl,/continuum
      END

     IF (*ptr[0]).draw_type EQ 2 THEN BEGIN
         nid=(*ptr[4]).nid
         sel_sl=(*ptr[4]).plot_fit(0:nid-1)
         ; plot
         fit=(*ptr[0]).fit
         yf = fit[cmin:cmax]
        Draw_data,x,y,ptr,sel_sl,yf=yf
      END
      IF (*ptr[0]).draw_type EQ 3 THEN BEGIN
         nid=(*ptr[4]).nid
        sel_sl=(*ptr[4]).plot_id(0:nid-1)
         ; plot
         Draw_data,x,y,ptr,sel_sl
      END

 END  
END

PRO Widget_chemcam, ptr

  ;colorset,/quiet
  
  ; principal widgets creations:
  base_chem = WIDGET_BASE(title='CHEMCAM',/TLB_Size_Events,/column, $
    uname='BASE_CHEM',UVALUE=ptr,KILL_NOTIFY='Chemcam_cleanup')
  (*ptr[0]).base_id=base_chem
 
  tab_chem=widget_tab(base_chem)
  
  ; spectrum part---------------------------------------------------------------
  base_spectrum= WIDGET_BASE(tab_chem, /ROW, /align_center, frame=1,group_leader=base_chem,title='Spectrum')
  spectrum_title= WIDGET_LABEL(base_spectrum, value='Spectrum',/align_center)
 
  wOpen=WIDGET_BUTTON(base_spectrum,VALUE='Open',TOOLTIP='Load Spectrum',ysize=50,/MENU)
  wOpen_Ascii=WIDGET_BUTTON(wOpen,VALUE='ASCII',EVENT_PRO='OpenSpectrum',UVALUE=ptr,ysize=50)
 wOpen_EDR=WIDGET_BUTTON(wOpen,VALUE='EDR',ysize=50,/menu)
 print,wopen_edr
 wOpen_EDR_UV=WIDGET_BUTTON(wOpen_EDR,VALUE='UV',EVENT_PRO='OpenSpectrum',UVALUE=ptr,ysize=50)
 print,wopen_edr_uv
 wOpen_EDR_VIS=WIDGET_BUTTON(wOpen_EDR,VALUE='VIS',EVENT_PRO='OpenSpectrum',UVALUE=ptr,ysize=50)
 wOpen_EDR_VNIR=WIDGET_BUTTON(wOpen_EDR,VALUE='VNIR',EVENT_PRO='OpenSpectrum',UVALUE=ptr,ysize=50)
  wOpen_DP=WIDGET_BUTTON(wOpen,VALUE='DP',ysize=50,/MENU)
 wOpen_DP_UV=WIDGET_BUTTON(wOpen_DP,VALUE='UV',EVENT_PRO='OpenSpectrum',UVALUE=ptr,ysize=50)
 wOpen_DP_VIS=WIDGET_BUTTON(wOpen_DP,VALUE='VIS',EVENT_PRO='OpenSpectrum',UVALUE=ptr,ysize=50)
 wOpen_DP_VNIR=WIDGET_BUTTON(wOpen_DP,VALUE='VNIR',EVENT_PRO='OpenSpectrum',UVALUE=ptr,ysize=50)
 wOpen_SAV=WIDGET_BUTTON(wOpen,VALUE='IDL Save',ysize=50,/MENU)
 wOpen_SAV_UV=WIDGET_BUTTON(wOpen_SAV,VALUE='UV',EVENT_PRO='OpenSpectrum',UVALUE=ptr,ysize=50)
 wOpen_SAV_VIS=WIDGET_BUTTON(wOpen_SAV,VALUE='VIS',EVENT_PRO='OpenSpectrum',UVALUE=ptr,ysize=50)
 wOpen_SAV_VNIR=WIDGET_BUTTON(wOpen_SAV,VALUE='VNIR',EVENT_PRO='OpenSpectrum',UVALUE=ptr,ysize=50)


 wPlot=WIDGET_BUTTON(base_spectrum,VALUE='Plot',EVENT_PRO='PlotSpectrum',UVALUE=ptr,TOOLTIP='Plot Spectrum',ysize=50)
  wBack=WIDGET_BUTTON(base_spectrum,VALUE='Reset',EVENT_PRO='Reset',UVALUE=ptr,TOOLTIP='Reset to Original Spectrum')
  wDbase=WIDGET_BUTTON(base_spectrum,VALUE='Nist DB',UVALUE=ptr,/MENU,TOOLTIP='Load Line Database')
  dbv={ptr:ptr,wDbId:wDbase}
  wNist=WIDGET_BUTTON(wDbase,VALUE='Nist DB',UVALUE=dbv,EVENT_PRO='Dbase')
  wMars=WIDGET_BUTTON(wDbase,VALUE='Mars DB',UVALUE=dbv,EVENT_PRO='Dbase')
  wNorm=WIDGET_BUTTON(base_spectrum,VALUE='Normalise',UVALUE=ptr,/MENU,TOOLTIP='Spectrum normalisation')
  wNone=WIDGET_BUTTON(wNorm,VALUE='None',UVALUE=ptr,EVENT_PRO='Sp_Norm')
  wTotal=WIDGET_BUTTON(wNorm,VALUE='Total Emission',UVALUE=ptr,EVENT_PRO='Sp_Norm')
  wStd=WIDGET_BUTTON(wNorm,VALUE='Std. Dev.',UVALUE=ptr,EVENT_PRO='Sp_Norm')
  wQuit=WIDGET_BUTTON(base_spectrum,VALUE='Quit',EVENT_PRO='Quit',UVALUE=ptr)

 
  ; the RoI---------------------------------------------------------------------
  base_roi = WIDGET_BASE(base_chem, /ROW, /align_center, frame=1,group_leader=base_chem)
  roi_title = WIDGET_LABEL(base_roi, value='RoI (nm)',/align_center)
  roi_table = WIDGET_TABLE(base_roi,format='(F7.1)',uname='roi',$
    column_labels=['min','max'],/editable,$
    uvalue=ptr,$
    value=[[(*ptr[0]).lmin,(*ptr[0]).lmax]],$
    /no_row_headers,/align_center,event_pro='roi')
    (*ptr[0]).roi_id=roi_table
    
  ; denoise part----------------------------------------------------------------
    
  base_denoise = WIDGET_BASE(tab_chem, /ROW, frame=1, /align_center ,uname='denoise_base',group_leader=base_chem,title='Denoising')
  denoise_title = WIDGET_LABEL(base_denoise, value='Denoise',/align_center)
  go_but = WIDGET_BUTTON(base_denoise, value='  Go  ',uvalue=ptr,/align_center,event_pro='dns_go',TOOLTIP='Denoise Spectrum')
  ;help_but = WIDGET_BUTTON(base_denoise, value='  Help  ',uvalue='help',/align_center)
  denoise_table = WIDGET_TABLE(base_denoise,format='(F7.1)',$
    column_labels=['sigma'],/editable,$
    value=[(*ptr[0]).Sigma],uvalue=ptr,$
    /no_headers,/align_center,event_pro='dns_param')
  save_but = WIDGET_BUTTON(base_denoise, value='  Save  ',uvalue=ptr,/align_center,event_pro='dns_save',TOOLTIP='Save Denoised Spectrum [*.dns]')
  ;
  
  ; background part ------------------------------------------------------------
  base_back = WIDGET_BASE(tab_chem, /ROW, frame=1,/align_center,uname='back_base',group_leader=base_chem,title='Continuum Removal')
  back_title = WIDGET_LABEL(base_back, value='Continuum',/align_center)

 wBkgGo=WIDGET_BUTTON(base_back,VALUE='  Go  ',/MENU,TOOLTIP='Remove Continnuum')
  wBkgLin=WIDGET_BUTTON(wBkgGo,VALUE='Linear',UVALUE=ptr,event_pro='bkg_go')
  wBkgQuad=WIDGET_BUTTON(wBkgGo,VALUE='Quadratic',UVALUE=ptr,event_pro='bkg_go')
  wBkgSpl=WIDGET_BUTTON(wBkgGo,VALUE='Spline',UVALUE=ptr,event_pro='bkg_go')

  bkg_table = WIDGET_TABLE(base_back,format='(I5)',$
    column_labels=['Lv min'],/editable,$
    uvalue=ptr,$
    value=[(*ptr[0]).lvmin],$
    /no_headers,/align_center,event_pro='bkg_param')
  WBkgIR= WIDGET_BUTTON(base_back,VALUE='Instr. Res.',UVALUE=ptr,EVENT_PRO='clb_IR',TOOLTIP='Apply Instrument Response')
  WBkgsave = WIDGET_BUTTON(base_back, value='  Save  ',uvalue=ptr,/align_center,event_pro='bkg_save',TOOLTIP='Save Continuum removed Spectrum [*.bkg]')

  
  ; wavelength calib part ------------------------------------------------------
  base_calib = WIDGET_BASE(tab_chem, /ROW, frame=1,/align_center,uname='calib_base',group_leader=base_chem,title='Wavelength Calibration')
  calib_title = WIDGET_LABEL(base_calib, value='Calibration',/align_center)
  
  wClbSel= WIDGET_BUTTON(base_calib,VALUE='Select',/MENU)
  wClbSelSyn= WIDGET_BUTTON(wClbSel,VALUE='Synthetic',UVALUE=ptr,EVENT_PRO='clb_sel')
  wClbSelMatch= WIDGET_BUTTON(wClbSel,VALUE='Matching Filter',UVALUE=ptr,EVENT_PRO='clb_match')
  wClbFile = WIDGET_BUTTON(base_calib,VALUE='File',TOOLTIP='Load Calibrated Wavelength File [*.wcb]',UVALUE=ptr,EVENT_PRO='clb_file')

 WClbSave= WIDGET_BUTTON(base_calib,VALUE='Save',UVALUE=ptr,EVENT_PRO='clb_save',TOOLTIP='Resample and Save Wavelength Calibrated Spectrum [*.clb]')
;;  WClbConc= WIDGET_BUTTON(base_calib,VALUE='Concatenate',UVALUE=ptr,EVENT_PRO='clb_conc',TOOLTIP='Concatenate Calibrated Spectra [*_ALL.clb]')

  ; line identification part----------------------------------------------------
  base_id = WIDGET_BASE(tab_chem, /ROW, frame=1, /align_center,uname='plotid',group_leader=base_chem,title='Line Identification')
  id_title = WIDGET_LABEL(base_id, value='Line identification',/align_center)
  
;  base= WIDGET_BASE(base_id, /ROW, /align_center)
  wIdGo= WIDGET_BUTTON(base_id, value='  Go  ',uvalue=ptr,uname='line_id',/align_center,EVENT_PRO='Id_go',TOOLTIP='Perform Line Identification')

  wId_table1 = WIDGET_TABLE(base_id,format='(F7.2,F7.2)',$
    column_labels=['Filter size'],/editable,$
    uvalue=ptr,value=[(*ptr[0]).flt],$
    /no_headers,/align_center,EVENT_PRO='id_param1')
  wIdLoad= WIDGET_BUTTON(base_id, value='Load',uvalue=ptr,uname='load_id',/align_center,EVENT_PRO='Id_load',TOOLTIP='Load Line Identification File [*_lines.dat')
 wIdElt= WIDGET_BUTTON(base_id,VALUE='Element',UVALUE=ptr,EVENT_PRO='Id_elt',TOOLTIP='Select Elements to Plot')
  wIdPlt= WIDGET_BUTTON(base_id,VALUE='Plot Lines',UVALUE=ptr,EVENT_PRO='Id_plt',TOOLTIP='Plot Selected Elements above Threshold and Select Elements per Line')

  wId_table2 = WIDGET_TABLE(base_id,format='(G10.1)',$
    column_labels=['Value'],/editable,$
    uvalue=ptr, value=[(*ptr[0]).thresv],$
    /no_row_headers,/align_center,EVENT_PRO='id_param2')
  (*ptr[0]).id2_id=wId_table2
   
  ; fit part--------------------------------------------------------------------
  base_fit = WIDGET_BASE(tab_chem,frame=1, /align_center,/ROW,uname='fit_base',group_leader=base_chem,title='Line Fitting')
  title = WIDGET_LABEL(base_fit, value='Line Fit',/align_center)
  wFitLines =  WIDGET_BUTTON(base_fit, value='Lines',uname='line_fit',/MENU,TOOLTIP='Select Elements to Fit')
  wFitElt = WIDGET_BUTTON(wFitLines,value='Elements',uvalue=ptr,EVENT_PRO='Fit_elt')
  wFitSel = WIDGET_BUTTON(wFitLines,value='Selected Lines',uvalue=ptr,EVENT_PRO='Fit_elt')
  wFitGo = WIDGET_BUTTON(base_fit, value='Go',uname='go_fit',/MENU,TOOLTIP='Perform Fit and Save Fit Parametres')
  wFItGauss = WIDGET_BUTTON(wFitGo,VALUE='Gaussian',UVALUE=ptr,event_pro='fit_go')
  wFItLorentz = WIDGET_BUTTON(wFitGo,VALUE='Lorentz',UVALUE=ptr,event_pro='fit_go')
   wFItVoigt = WIDGET_BUTTON(wFitGo,VALUE='Voigt',UVALUE=ptr,event_pro='fit_go')
  
;

screen = get_screen_size()
wDrawBase = WIDGET_BASE(base_chem,UVALUE=ptr)
wDrawMain = WIDGET_DRAW(wDrawBase,xsize=screen(0)*.8,ysize=screen(1)*.6,/button_events,/MOTION_EVENTS,UNAME='DRAW_DATA')
;wDrawMain = WIDGET_DRAW(base_chem,xsize=2000,ysize=screen(1)*.4,x_scroll_size=1000,y_scroll_size=screen(1)*.4,/button_events,/MOTION_EVENTS,UNAME='DRAW_DATA')

(*ptr[0]).base_plot_id = wDrawBase
(*ptr[0]).text_id = wDrawMain

  label1 = WIDGET_LABEL(base_chem, /align_left, $
    VALUE='Wavelength:',FONT="Arial*18")
  label2 = WIDGET_LABEL(base_chem, /align_left, $
    VALUE='Intensity:',FONT="Arial*18")
  label3 = WIDGET_LABEL(base_chem, /align_left, $
      VALUE=' ',FONT="Arial*18",xsize=200)

  (*ptr[0]).lbl1 = label1
  (*ptr[0]).lbl2 = label2
  (*ptr[0]).lbl3 = label3

WIDGET_CONTROL, base_chem, /REALIZE
  
  XMANAGER, 'WIdget_chemcam', base_chem,/no_block

  Dgeom=WIDGET_INFO(wDrawMain,/GEOMETRY)
  Bgeom=WIDGET_INFO(base_chem,/GEOMETRY)

  dy=bgeom.ysize-dgeom.ysize
  (*ptr[0]).head_size = dy
;;  print,dy
END
