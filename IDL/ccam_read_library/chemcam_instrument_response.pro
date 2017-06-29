PRO chemcam_instrument_response,ptr
  
  IF (*ptr[5]).instresp THEN BEGIN
     v=dialog_message('Instrument Response already done',/center)
  END ELSE BEGIN
  n=(*ptr[0]).n
  wl=(*ptr[0]).wavelength(0:n-1)
  y=(*ptr[0]).new_spectrum(0:n-1)
  
  sp_type=detect_sp_type((*ptr[1]).libs_fn_init)

;;Resolution
    dx=abs(wl(1:*)-wl)
    dx=[dx,dx[-1]]
;; Telescope aperture and distance correction (mm)
    distt=(*ptr[5]).dist*1e6
    ap=distt/(!pi*54.2*.100)^2
;; Retrieve instrument response
  restore,!CHEMCAM+'/data/gain_info.sav'
  CASE sp_type OF
     'UV':gain=alluvdata[50:2097].tvac
     'VIS':gain=allvisdata[50:2097].tvac
     'VNIR':BEGIN
        gain=allvnirdata[50:2097].tvac
        ;; yt=y(1650:*)
        ;; lv=FIX(ALOG(n-1651)/ALOG(2))
        ;; Remove_continuum,wl(1650:*),yt,lv,2,2
        ;; y(1650:*)=yt
     END
     ELSE:BREAK
  END

  
  y=y*gain*ap/dx
; Thresholding
  ;; yt=y(0:255)
  ;; ;; w=watrous(yt,2)
  ;; ;; b=get_noise(w(*,0))
  ;; ;; i0=where(w(*,0) LE 3.*b,n0)
  ;; b=get_noise(yt)
  ;; i0=where(abs(yt-mean(yt)) LE 9.*b,n0)

  ;; IF n0 GT 0 THEN yt(i0)=0.
  ;; y(0:255)=yt
  ;; yt=y(1792:*)
  ;; ;; w=watrous(yt,2)
  ;; ;; b=get_noise(w(*,0))
  ;; ;; i0=where(w(*,0) LE 3.*b,n0)
  ;; b=get_noise(yt)
  ;; i0=where(abs(yt-mean(yt)) LE 9.*b,n0)

  ;; IF n0 GT 0 THEN yt(i0)=0.
  ;; y(1792:*)=yt

  (*ptr[0]).denoised_spectrum(0:n-1)=y
  (*ptr[0]).new_spectrum(0:n-1)=y
  (*ptr[5]).instresp=1
;update normalisation and threhold
  Id2id=(*ptr(0)).id2_id
  (*ptr[0]).thresv= (*ptr[0]).thress*stddev(y)
  tmp=[(*ptr[0]).thresv]
  WIDGET_CONTROL,Id2id,set_value=tmp

  Draw_data,wl,y,ptr
END

END
