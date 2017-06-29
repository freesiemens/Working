;+
; NAME:
;       WCHEMCAM
;
; PURPOSE:
;       This routine allows read, plot and fit the CHEMCAM spectra
;
; CALLING SEQUENCE:
;       wchemcam
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
;      Added Instrument response Jeremie December 2011 
; v5.3 Added Instrument Response function January  2012 
; V6.0 Added EDR and DP reading routine from Dot January  2012 
; V6.1 Added Calibration Status and Concatenate January  2012 
;O. FORNI IRAP-CNRS
;-
PRO printlog,msg

printf,99,msg
RETURN
END

pro wchemcam

; define work directory and library paths

intro_msg=strarr(9)
intro_msg(0)='                    ChemCam v6.1        '
intro_msg(1)='           Developed by the ChemCam Team '
intro_msg(2)='   This code uses part of the following packages  '
intro_msg(3)='    MPFIT package developed by Craig Markwardt     '
intro_msg(4)=' http://cow.physics.wisc.edu/~craigm/idl/idl.html '
intro_msg(5)='    MRS package developed by J.-L. Starck et al. '
intro_msg(6)='              http://jstarck.free.fr/mrs.html     '
intro_msg(7)='                   IDL ASTRON Library'
intro_msg(8)='              http://idlastro.gsfc.nasa.gov '

; Open logfile
logfile='./ChemCam_logfile_'+strmid(systime(0),8,2)+strmid(systime(0),4,3)+$
strmid(systime(0),20,4)+'.'+strmid(systime(0),11,2)+strmid(systime(0),14,2)+$
strmid(systime(0),17,2)

openw,99,logfile

printlog,'Loading Path Definition File'
printlog,''
v=dialog_message(intro_msg,/center,/information)
path_fn=dialog_pickfile(title='Load Path Definition File',/must_exist,filter=['*.def'])
if path_fn ne '' then begin
 def=strarr(3)
 on_ioerror, Err
flh=file_lines(path_fn)
if flh ne 3 then  goto,err
 openr, lun, path_fn,/get_lun
 readf,lun,def
 GOTO, Done 
 Err:Begin
   v=dialog_message('WARNING: Wrong Path Definition File')
   printlog,'Wrong Path Definition File'
   close,99
   return
 END

 Done: close,lun
 free_lun,lun
 Ccam_root=def[0]
 defsysv,'!CHEMCAM',Ccam_root
 defsysv,'!work_dir',def[1]
 defsysv,'!Nist',def[2]
 path_msg=strarr(3)
 path_msg(0)='Main ChemCam Software Directory set to: '+!Chemcam
 path_msg(1)='ChemCam Working Directory set to: '+!Work_dir
path_msg(2)='ChemCam Line Database Directory set to: '+!Nist
    v=dialog_message(path_msg,/center,/cancel,/information)
   printlog,path_msg
   if v eq 'Cancel' then begin
      close,99
      return
   end

end else begin
   close,99
   return
end


;Ccam_root='/home/forni/chemcam/ChemCam_v1.0/'
;; Ccam_root='C:\DOCUMENTS AND SETTINGS\OLIVIER\MES DOCUMENTS\CHEMCAM\ChemCam_v3.0\'
;; defsysv,'!CHEMCAM',Ccam_root
;; cd,!CHEMCAM
;; ;defsysv,'!work_dir','/home/forni/chemcam'
;; defsysv,'!work_dir','C:\DOCUMENTS AND SETTINGS\OLIVIER\MES DOCUMENTS\CHEMCAM\'

;; defsysv,'!Nist',!CHEMCAM+'Nist/'
;; defsysv,'!Ccam_pro',!CHEMCAM+'general_pro/'
;; defsysv,'!Ccam_mpfit',!CHEMCAM+'mpfit/'
p=strpos(!path,!chemcam)
p_sep=path_sep(/search_path)
if p eq -1 then !path = !path + p_sep + EXPAND_PATH('+'+!CHEMCAM,/all_dirs)
ASTRON_DIR='C:\DOCUMENTS AND SETTINGS\OLIVIER\MES DOCUMENTS\ASTRON\'
;DEFSYSV, '!ASTRON_DIR',getenv("ASTRON_DIR")
;DEFSYSV, '!ASTRON_DIR',ASTRON_DIR
;p=strpos(!path,!astron_dir)
;if p eq -1 then begin
;  !PATH = !PATH + p_sep + EXPAND_PATH('+'+!ASTRON_DIR)
;  astrolib
;end

device,decomposed=0,retain=2
; define variables

file={libs_fn_init:'',libs_fn_dns:'',libs_fn_bkg:'',libs_fn_clb:'',$
libs_fn_wcb:'',image_file_name:'',db_file:''}

sps={elt:' ',ex_st:' ',lwav:0.,wav:0.,relint:0.,intensity:0.,corr_gr:0.,corr_li:0.,group:1}
sp_sel=replicate(sps,10000)
lines={nlines:0,sp_sel:sp_sel}

nelt=13
col=lindgen(nelt)*17+30
calib={nelt:nelt,ind_name:intarr(nelt),name_list_uv:['Al','C','Ca','Fe','Mg','Na','S','Si','Ti'],name_list_vis:['Al','Ba','Ca','Fe','Mg','S','Si'],name_list_vnir:['Ca','Fe','K','Li','Mg','Na','O','Si'],name_list:['Al','Ba','C','Ca','Fe','K','Li','Mg','Na','O','S','Si','Ti'],nclb:0,x0:fltarr(20),x1:fltarr(20),col:col,slit:0.1}

plot_l=replicate(sps,300)
plot_id=plot_l
plot_fit=plot_l
ident={nlines:0,nelt:100,ind_name:lonarr(200),name_list:strarr(200),sel_sl:sp_sel,nplot:0,nid:0,plot_l:plot_l,plot_id:plot_id,plot_fit:plot_fit,type:''}

info={spectrum0:fltarr(20000),$
      wavelength0:fltarr(20000),$
      spectrum:fltarr(20000),$
      denoised_spectrum:fltarr(20000),$
      new_spectrum:fltarr(20000),$
      clb_wavelength:fltarr(20000),$
      clb_spectrum:fltarr(20000),$
      continuum:fltarr(20000),$
      fit:fltarr(20000),$
      wavelength:fltarr(20000),$
      n:0,$
      n_clb:0,$
      lmin0:0.,$
      lmax0:0.,$
      cmin0:0,$
      cmax0:0,$
      lmin:0.,$
      lmax:0.,$
      cmin:0,$
      cmax:0,$
      sigma:3.,$
      niter:10.,$
      lvmin:6.,$
      method:'',$
      flt:1.2,$
      thresv:0.,$
      thress:3.,$
      text_id:-1l,$
      base_plot_id:-1l,$
      base_id:-1l,$
      draw_type:-2l,$
      base_clb_id:-1l,$
      roi_id:-1l,$
      id2_id:-1l,$
      slit_id:-1l,$
      lbl1:-1l,$
      lbl2:-1l,$
      lbl3:-1l,$
      head_size:-1l,$
      norm_st0:0l,$
      norm_st1:0l,$
      norm_fact:fltarr(4)}

hk={dist:3.0,instresp:0b}

ptr=ptrarr(6,/allocate_heap)
ptr(0)=ptr_new(info,/no_copy)
ptr(1)=ptr_new(file)
ptr(2)=ptr_new(calib)
ptr(3)=ptr_new(lines)
ptr(4)=ptr_new(ident)
ptr(5)=ptr_new(hk)

widget_chemcam,ptr

end
