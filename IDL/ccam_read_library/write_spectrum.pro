;+
; NAME:
;       WRITE_SPECTRUM
;
; PURPOSE:
;       This routine save a processed chemcam spectrum
;
; CALLING SEQUENCE:
;       WRITE_SPECTRUM, wl, spectrum,param_list,type=['denoise','background','calib']
;
;-


FUNCTION Write_spectrum, wl, sp, param_list, file, type=type
  
  IF KEYWORD_SET(type) THEN BEGIN
 
     def_file=file_remove_ext(file)
     CASE type OF
        'denoise': BEGIN
           title='Select denoised spectrum to save'
           filter=['*.dns']
           ext='.dns'
        END
        'background': BEGIN
           title='Select background substracted spectrum to save'
           filter=['*.bkg']
           ext='.bkg'
        END
        'calib' :BEGIN
           title='Select wavelength calibrated spectrum to save'
           filter=['*.clb']
           ext='.clb'
           IF param_list.instresp EQ 1 THEN BEGIN
              prf=strpos(file,'_RF')
              IF prf EQ -1 THEN def_file=file_remove_ext(file)+'_RF'
           END

        END
     END

     wfile = DIALOG_PICKFILE(path=!work_dir,filter=filter, /fix_filter,$
                             get_path=sel_path,file=def_file,title=title, /write)

  
; if the user did not click on the cancel button of the dialog pickfile:
     IF ( wfile NE '' ) THEN BEGIN
        IF KEYWORD_SET(type) THEN BEGIN
           p=STRPOS(wfile,ext)
           IF p EQ -1 THEN wfile=wfile+ext
        END
        OPENW,lun,wfile,/get_lun
        PRINTF,lun,'; File creation:'+SYSTIME()
        PRINTF,lun,'; Input File:'+param_list.infile
        PRINTF,lun,'; Output File:'+wfile
        PRINTF,lun,'; Wavelength range:',param_list.wrange
        PRINTF,lun,'; Normalisation:'+param_list.norm
 
        IF KEYWORD_SET(type) THEN BEGIN
           CASE type OF
              'denoise': BEGIN
                 PRINTF,lun,'; Noise threshold:',param_list.sigma
              END
              'background': BEGIN
                 PRINTF,lun,'; Background scale:',param_list.scale
                 PRINTF,lun,'; Method:',param_list.method
              END
              'calib' :BEGIN
                 PRINTF,lun,'; Instrument response:',param_list.instresp
              END
              ELSE:BREAK
           END
        END

        FOR nel=0,N_ELEMENTS(wl)-1 DO PRINTF,lun,wl(nel),sp(nel),format='(F13.4,G13.4)'
        CLOSE,lun
        free_lun,lun
     END
  END

  RETURN,wfile
END


