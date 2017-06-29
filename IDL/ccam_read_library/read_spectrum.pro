;+
; NAME:
;       READ_SPECTRUM
;
; PURPOSE:
;       This routine opens a chemcam spectrum
;
; CALLING SEQUENCE:
;       READ_SPECTRUM, wl, spectrum
;
;-


FUNCTION READ_SPECTRUM, wl, spectrum,fmt,sp_type,dist


; -----------------------------------------------------------------
;                     Read the spectrum
; -----------------------------------------------------------------
; dialog to select the file:
CASE fmt OF
   'Open':BEGIN
      filter = ['*.txt', '*.dat','*.Scope','*.dns','*.bkg','*.clb','*.edr','*.dp']
      file = dialog_pickfile(path=!work_dir, filter=filter, /fix_filter,$
                           get_path=sel_path,$
                           title='Select Data Spectrum to Read', /must_exist)

                                ; if the user did not click on the cancel button of the dialog pickfile:
      if ( file ne '' ) then begin
                                ; read ASCII file
         readcol,file,wl,spectrum,/silent,comment=';',format='f,f' 
         defsysv,"!work_dir",sel_path
      end else begin
         wl=0.
         spectrum=0.
      end
   END
   'EDR':BEGIN
      filter = ['CL*.dat']
      file = dialog_pickfile(path=!work_dir, filter=filter, /fix_filter,$
                           get_path=sel_path,$
                           title='Select Data Spectrum to Read', /must_exist)
       if ( file ne '' ) then begin
          s=ccam_read_libs_edr(file,hk_dist=hk_dist)
          dist=hk_dist.dist_meter
          CASE sp_type OF
             'UV':BEGIN
                spectrum=avg(s(0,*,*),1)
                readcol,!chemcam+'/data/UV_wvl.wcb',wl,format='f',/silent
             END
             'VIS':BEGIN
                spectrum=avg(s(1,*,*),1)
                readcol,!chemcam+'/data/VIS_wvl.wcb',wl,format='f',/silent
             END
             'VNIR':BEGIN
                spectrum=avg(s(2,*,*),1)
                readcol,!chemcam+'/data/VNIR_wvl.wcb',wl,format='f',/silent
             END
           END
          file=file_remove_ext(file)+'_'+sp_type+'.edr'
        defsysv,"!work_dir",sel_path
      end else begin
         wl=0.
         spectrum=0.
      end

   END

   'DP':BEGIN
      filter = ['CcamSpectra*.dat']
      file = dialog_pickfile(path=!work_dir, filter=filter, /fix_filter,$
                           get_path=sel_path,$
                           title='Select Data Spectrum to Read', /must_exist)
       if ( file ne '' ) then begin
          s=ccam_read_libs(file,edr=0,hk_dist=hk_dist)
          dist=hk_dist.dist_meter
  ;;      wl=wvl_basis_order4(sp_type,dindgen(2048))
          CASE sp_type OF
               'UV':BEGIN
                spectrum=avg(s(0,*,*),1)
                readcol,!chemcam+'/data/UV_wvl.wcb',wl,format='f',/silent
             END
             'VIS':BEGIN
                spectrum=avg(s(1,*,*),1)
                readcol,!chemcam+'/data/VIS_wvl.wcb',wl,format='f',/silent
             END
             'VNIR':BEGIN
                spectrum=avg(s(2,*,*),1)
                readcol,!chemcam+'/data/VNIR_wvl.wcb',wl,format='f',/silent
             END
           END
          file=file_remove_ext(file)+'_'+sp_type+'.dp'
 
          defsysv,"!work_dir",sel_path
      end else begin
         wl=0.
         spectrum=0.
      end
   END

   'IDL Save':BEGIN
      filter = ['*.sav','*.SAV']
      file = dialog_pickfile(path=!work_dir, filter=filter, /fix_filter,$
                           get_path=sel_path,$
                           title='Select Data Spectrum to Read', /must_exist)
       if ( file ne '' ) then begin
          restore,file
  ;;        dist=hk_dist.dist_meter
  ;;      wl=wvl_basis_order4(sp_type,dindgen(2048))
          CASE sp_type OF
               'UV':BEGIN
                  IF isa(auv) THEN spectrum=auv
                  IF isa(auvdata) THEN spectrum=auvdata(50:2097) ELSE BEGIN
                     wl=0.
                     spectrum=0.
                  END
              IF isa(defuv) THEN  wl=defuv ELSE  readcol,!chemcam+'/data/UV_wvl.wcb',wl,format='f',/silent
             END
             'VIS':BEGIN
                  IF isa(avis) THEN spectrum=avis
                  IF isa(avisdata) THEN spectrum=avisdata(50:2097) ELSE BEGIN
                     wl=0.
                     spectrum=0.
                  END
              IF isa(defvis) THEN  wl=defvis ELSE  readcol,!chemcam+'/data/VIS_wvl.wcb',wl,format='f',/silent
             END
             'VNIR':BEGIN
                 IF isa(avnir) THEN spectrum=avnir
                  IF isa(avnirdata) THEN spectrum=avnirdata(50:2097) ELSE BEGIN
                     wl=0.
                     spectrum=0.
                  END
              IF isa(defvnir) THEN  wl=defvnir ELSE  readcol,!chemcam+'/data/VNIR_wvl.wcb',wl,format='f',/silent
              END
           END
          file=file_remove_ext(file)+'_'+sp_type+'.idl'
 
          defsysv,"!work_dir",sel_path
      end else begin
         wl=0.
         spectrum=0.
      end
   END

END

fn=strmid(file,strlen(sel_path))
cd,!work_dir
RETURN,fn
END

