pro calcpls_event, event
; this is the calcpls event handler
; history: modifications by J. Lasue 2012 07 08
; R. Anderson 2012 09 29 - Modified to allow user to select between single shots and averaged spectra
; R. Anderson 2013 Jan-March - Modified to allow recursive searches, min and max sols, and to automatically load the last-used datapath
; R. Anderson 2013 April-May - Lots of edits to implement PLS1
; R. Andeson 2013 August - Added options to normalize and scale to stdev

print, 'Event detected !'

; get state information
widget_control, event.top, get_uvalue=plsparamptr
plsparam = *plsparamptr

; identify widget which caused the event
widget_control, event.id, get_uvalue=widget
help, widget

; handle events
case widget of

  'Choose': begin
    datapath=Dialog_pickfile( $
      title="Select the directory to search...",/directory,path=datapath)
    sizepath=strlen(datapath)
      
    plsparam.datapath=datapath  
    print, plsparam.datapath
    widget_control,plsparam.text1,set_value=datapath
    ;help,goodcompsfile,datapath,fixedfileEl,fixedfileOx
    ;stop
    ;save,goodcompsfile,datapath,fixedfileEl,fixedfileOx,filename='calcpls_paramfile.sav' ;save the datapath so that it can be restored next time the program is run 
  end
  
  'ChooseFile': begin
    goodcompsfile=Dialog_pickfile( $
      title="Select the desired file...",path=datapath)
         
    plsparam.goodcompsfile=goodcompsfile  
    print, plsparam.goodcompsfile
    widget_control,plsparam.goodcompstext1,set_value=goodcompsfile
    ;help,goodcompsfile,datapath,fixedfileEl,fixedfileOx
    ;stop
    ;save,goodcompsfile,datapath,fixedfileEl,fixedfileOx,filename='calcpls_paramfile.sav' ;save the file path so that it can be restored next time the program is run 
  end
  
  'ChooseNormFile': begin
    normfile=Dialog_pickfile( $
      title="Select the desired file...",path=datapath)
         
    plsparam.normfile=normfile  
    print, plsparam.normfile
    widget_control,plsparam.normfiletext1,set_value=normfile
    ;help,goodcompsfile,datapath,fixedfileEl,fixedfileOx
    ;stop
    ;save,goodcompsfile,datapath,fixedfileEl,fixedfileOx,filename='calcpls_paramfile.sav' ;save the file path so that it can be restored next time the program is run 
  end
  
  'ChooseMasterFile': begin
    masterfile=Dialog_pickfile( $
      title="Select the desired file...",path=datapath)
         
    plsparam.masterfile=masterfile  
    print, plsparam.masterfile
    widget_control,plsparam.masterfiletext1,set_value=masterfile
  end
  
  'ChooseFoldFile': begin
    foldfile=Dialog_pickfile( $
      title="Select the desired file...",path=datapath)
         
    plsparam.foldfile=foldfile  
    print, plsparam.foldfile
    widget_control,plsparam.foldfiletext,set_value=foldfile
    ;help,goodcompsfile,datapath,fixedfileEl,fixedfileOx
    ;stop
    ;save,goodcompsfile,datapath,fixedfileEl,fixedfileOx,filename='calcpls_paramfile.sav' ;save the file path so that it can be restored next time the program is run 
  end
  
  ;'ChooseFixedFileEl': begin
  ;  fixedfileEl=Dialog_pickfile( $
  ;    title="Select the desired file...",path=datapath)
  ;       
  ;  plsparam.fixedfileEl=fixedfileEl  
  ;  print, plsparam.fixedfileEl
  ;  widget_control,plsparam.fixedtextEl1,set_value=fixedfileEl
    ;help,goodcompsfile,datapath,fixedfileEl,fixedfileOx
    ;stop
    ;save,goodcompsfile,datapath,fixedfileEl,fixedfileOx,filename='calcpls_paramfile.sav' ;save the file path so that it can be restored next time the program is run 
  ;end
  
  'ChooseFixedFileOx': begin
    fixedfileOx=Dialog_pickfile( $
      title="Select the desired file...",path=datapath)
         
    plsparam.fixedfileOx=fixedfileOx  
    print, plsparam.fixedfileOx
    widget_control,plsparam.fixedtextOx1,set_value=fixedfileOx
    
  end
  
  
  'Recursive': begin
    if (plsparam.Recursive EQ 1) then begin
      plsparam.Recursive = 0
    endif else if (plsparam.Recursive EQ 0) then begin
      plsparam.Recursive = 1
    endif else begin
      ok = Error_Message('Not a recognized Mask value!')
    endelse
    
    print, 'Recursive = ', plsparam.Recursive
  end

  
  
  'GlobalMin': begin
    
      plsparam.nc_type = 1
      plsparam.opt_min = 1
      plsparam.opt_ose = 0
    print, 'nc_type = ', plsparam.nc_type
    print, 'opt_min = ',plsparam.opt_min
    print, 'opst_ose = ',plsparam.opt_ose
    
  end


'OneStdErr': begin
  
      plsparam.nc_type = 1
      plsparam.opt_min = 0
      plsparam.opt_ose = 1
    print, 'nc_type = ', plsparam.nc_type
    print, 'opt_min = ',plsparam.opt_min
    print, 'opst_ose = ',plsparam.opt_ose
  end
  
 'Fixed': begin
      plsparam.nc_type = 0
      plsparam.opt_min = 0
      plsparam.opt_ose = 0
    print, 'nc_type = ', plsparam.nc_type
    print, 'opt_min = ',plsparam.opt_min
    print, 'opst_ose = ',plsparam.opt_ose
    ;if plsparam.recalc eq 1 and plsparam.nc_type eq 0 then begin
    ;   print,'CASE 1'
    ;   xmess,"ERROR: 'Fixed' and 'Recalculate' cannot both be selected. Please change one!"
    ;endif
  end 
  
  'PLS1': plsparam.pls = 0
  'PLS2': plsparam.pls = 1

 ; print,'PLS2 = ', plsparam.pls 




  'Single Shots': begin
      plsparam.singleshots = 1
    print, 'singleshots = ', plsparam.singleshots
  end
  
  'Averaged': begin
      plsparam.singleshots = 0
    print, 'singleshots = ', plsparam.singleshots
  end

  'Mask': begin
    
    maskfile=Dialog_pickfile( $
      title="Select the desired file...",path=datapath)
         
    plsparam.mask=maskfile  
    print, plsparam.mask
    widget_control,plsparam.masktext,set_value=maskfile
    print, 'Mask = ', plsparam.Mask
  end
  
  'Database': begin
    
    dbfile=Dialog_pickfile( $
      title="Select the desired file...",path=datapath)
         
    plsparam.dbfile=dbfile  
    print, plsparam.dbfile
    widget_control,plsparam.dbtext,set_value=dbfile
    print, 'Database Spectra = ', plsparam.dbfile
  end
  
  'CompDatabase': begin
    
    compdbfile=Dialog_pickfile( $
      title="Select the desired file...",path=datapath)
         
    plsparam.compdbfile=compdbfile  
    print, plsparam.compdbfile
    widget_control,plsparam.compdbtext,set_value=compdbfile
    print, 'Database Compositions = ', plsparam.compdbfile
  end
  
'Recalculate': begin
    if (plsparam.recalc EQ 1) then begin
      plsparam.recalc = 0
    endif else if (plsparam.recalc EQ 0) then begin
      plsparam.recalc = 1
    endif else begin
      ok = Error_Message('Not a recognized Recalc value!')
    endelse
    if plsparam.recalc eq 1 and plsparam.nc_type eq 0 then begin
       print,'CASE 2'
       xmess,"ERROR: 'Fixed' and 'Recalculate' cannot both be selected. Please change one!"
    endif
       print, 'Recalc = ', plsparam.recalc
  end
  'OK': begin
    ; check that data has been defined, if not error message
    ;stop
    if strlen(plsparam.datapath) EQ 0 then begin
      ok = Error_Message('Need to define the data path first!')
    endif else begin
      ; check the number of components entered by the user
      WIDGET_CONTROL,plsparam.text2,GET_VALUE=indata
      print, indata
      ; check validity
      if plsparam.recalc eq 1 and plsparam.nc_type eq 0 then begin
         ok = Error_Message("Can't have 'fixed' and 'recalculate' both selected! Exiting...")
         widget_control,event.top,/destroy
         
      endif
      
      if((indata GT 0) AND (indata LE 50)) then begin
        plsparam.nc=indata
        ; gets the OK if that is fine
        plsparam.status = 'OK'
; widget not destroyed after selecting the calculations
        widget_control,event.top,/destroy
      endif else if ((indata GT 0) AND (indata GT 50)) then begin
        ok = Error_Message('Number of components too high, reset to 10!')
        plsparam.nc=10
      endif else begin
        ok = Error_Message('Number of components value not allowed, reset to 10!')
        plsparam.nc=10
      endelse    
    endelse
    
  end
  'Cancel': begin
    plsparam.status = 'Cancel'
    widget_control,event.top,/destroy
  end
  'Help': begin
    plsparam.status = 'Cancel'
     ok = Error_Message('Please refer to the user guide, or contact Ryan Anderson (rbanderson@usgs.gov).')
  end
  'minsol': begin

  widget_control,plsparam.minsol_text2,get_value=minsol_temp ;read text in the widget as it is typed
  plsparam.minsol=minsol_temp
  print,plsparam.minsol
  end
  
  'maxsol': begin

  widget_control,plsparam.maxsol_text2,get_value=maxsol_temp ;read text in the widget as it is typed
  plsparam.maxsol=maxsol_temp
  print,plsparam.maxsol
  end

 'Weights_UV': begin

  widget_control,plsparam.uvweight_text2,get_value=uvweight_temp ;read text in the widget as it is typed
  plsparam.weights[0]=uvweight_temp
  print,plsparam.weights
  end
  
  'Weights_VIS': begin

  widget_control,plsparam.visweight_text2,get_value=visweight_temp ;read text in the widget as it is typed
  plsparam.weights[1]=visweight_temp
  print,plsparam.weights
  end
  
  'Weights_VNIR': begin

  widget_control,plsparam.vnirweight_text2,get_value=vnirweight_temp ;read text in the widget as it is typed
  plsparam.weights[2]=vnirweight_temp
  print,plsparam.weights
  end

  
  'testnum': begin

  widget_control,plsparam.testnumtext2,get_value=testnum_temp ;read text in the widget as it is typed
  
  plsparam.testnum=testnum_temp
  print,plsparam.testnum
  end
  
  'Stdevscale': begin
    if (plsparam.Stdevscale EQ 1) then begin
      plsparam.Stdevscale = 0
    endif else if (plsparam.Stdevscale EQ 0) then begin
      plsparam.Stdevscale = 1
    endif
    
  
    
    print, 'Stdevscale = ', plsparam.stdevscale
  end
  
  'NormTot': begin
    if (plsparam.normtot EQ 1) then begin
      plsparam.normtot = 0
    endif else if (plsparam.normtot EQ 0) then begin
      plsparam.normtot = 1
    endif
        
    print, 'Normtot = ', plsparam.normtot
  end
  'clipzero': begin
    if (plsparam.clipzero EQ 1) then begin
      plsparam.clipzero = 0
    endif else if (plsparam.clipzero EQ 0) then begin
      plsparam.clipzero = 1
    endif
        
    print, 'clipzero = ', plsparam.clipzero
  end
  
  'Norm1': begin
      plsparam.normval = 1
    print, 'normval = ', plsparam.normval
  end
  
  'Norm3': begin
      plsparam.normval = 3
    print, 'normval = ', plsparam.normval
  end
   
  
  else : ok = Error_Message('Event not recognized!')
  
    
  
endcase



; save state information
*plsparamptr = plsparam

end

pro calcpls_cleanup, ID

print, 'cleaning up'

; get state information
widget_control, id, get_uvalue=plsparamptr
plsparam=*plsparamptr

;clear the fixed # of components file unless PLS1 and Fixed are selected
if plsparam.pls eq 1 or plsparam.nc_type eq 1 then plsparam.fixedfileox=''

; save result

save,plsparam,filename=plsparam.workpath+'calcpls_paramfile.sav'


result = {workpath:plsparam.workpath, datapath:plsparam.datapath, $
nc:plsparam.nc, nc_type:plsparam.nc_type, Mask:plsparam.Mask, $
status:plsparam.status,singleshots:plsparam.singleshots,recursive:plsparam.recursive,minsol:plsparam.minsol,$
maxsol:plsparam.maxsol,pls:plsparam.pls,goodcompsfile:plsparam.goodcompsfile, opt_ose:plsparam.opt_ose, opt_min:plsparam.opt_min, $
fixedfileOx:plsparam.fixedfileOx,recalc:plsparam.recalc,dbfile:plsparam.dbfile,compdbfile:plsparam.compdbfile,$
normfile:plsparam.normfile,stdevscale:plsparam.stdevscale,normtot:plsparam.normtot,clipzero:plsparam.clipzero,$
foldfile:plsparam.foldfile,testnum:plsparam.testnum,masterfile:plsparam.masterfile,weights:plsparam.weights}
*plsparamptr = result

end

pro calcpls
; this is the pls virtual machine GUI v2
; history: modifications by J. Lasue 2012 07 04

configdata=rd_tfile('pdl_tool_config.csv',/autocol,delim=',')
searchdir=configdata[1,where(configdata[0,*] eq 'searchdir')]
masterlist=configdata[1,where(configdata[0,*] eq 'masterlist')]
maskfile=configdata[1,where(configdata[0,*] eq 'maskfile')]
meancenters_file=configdata[1,where(configdata[0,*] eq 'meancenters_file')]
settings_coeffs_file=configdata[1,where(configdata[0,*] eq 'settings_coeffs_file')]
blend_array_dir=configdata[1,where(configdata[0,*] eq 'blend_array_dir')]


;restore,'calcpls_paramfile.sav'  ;restore a save file containing the paths used last time the function was run
;datapath=plsparam.datapath
;fixedfileox=plsparam.fixedfileOx
;fixedfileel=plsparam.fixedfileel
;goodcompsfile=plsparam.goodcompsfile
;maskfile=plsparam.mask
;dbfile=plsparam.dbfile
;compdbfile=plsparam.compdbfile
;normfile=plsparam.normfile
;foldfile=plsparam.foldfile
;testnum=plsparam.testnum
;masterfile=plsparam.masterfile
;weights=[1.0,1.0,1.0]

undefine,plsparam ;clear all info in plsparam so it can be properly set again

; create top level base
tlb=widget_base(column=1, title="CALCPLS", $
  tlb_frame_attr=1)
  
; create base to hold everything except buttons
main=widget_base(tlb, column=1, frame=1)

; create file widgets
;fbase = widget_base(main, row=1, /base_align_center)
;label = widget_label(fbase, value='Search Directory:')
;text1 = widget_text(fbase, /editable, xsize=50)
;butt = widget_button(fbase, value = 'Browse...', uvalue='Choose')
;
;print,'Starting datapath: '+datapath
;widget_control,text1,set_value=datapath  ;fill the search box with the most recently used path

; create file widgets
;masterfilebase = widget_base(main, row=1, /base_align_center)
;masterfilelabel = widget_label(masterfilebase, value='Master list:')
;masterfiletext1 = widget_text(masterfilebase, /editable, xsize=50)
;masterfilebutt = widget_button(masterfilebase, value = 'Browse...', uvalue='ChooseMasterFile')
;widget_control,masterfiletext1,set_value=masterfile

;stop

labelbase=widget_base(main,row=1,/align_center)
;;Minsol
;minsolbase = widget_base(main, /row,/base_align_center)
;minsol_label = widget_label(minsolbase, value='Minimum Sol:')
;minsol_text2 = widget_text(minsolbase, value='0', uvalue='minsol', /editable,/all_events, xsize=10)
;;Maxsol
;;maxsolbase = widget_base(main, /row, /base_align_center)
;maxsol_label = widget_label(minsolbase, value='Maximum Sol:')
;maxsol_text2 = widget_text(minsolbase, value='1000', uvalue='maxsol', /editable, /all_events, xsize=10)
; create recursive button widget
recurbase = widget_base(main, row=1, /align_center, /nonexclusive)
recurbut = widget_button(recurbase, value='Recursive', uvalue='Recursive')
widget_control,recurbut,set_button=1   ;set to recursive search by default
;; create PLS1/ PLS2 Branches
;plsbase=widget_base(main,row=1,/align_center,/exclusive)
;buttonA=widget_button(plsbase, value='PLS1',uvalue='PLS1')
;buttonB=widget_button(plsbase, value='PLS2',uvalue='PLS2')
;widget_control,buttonA,set_button=1 ;set the PLS1 button to be selected by default


;Create buttons to select single shots vs averaged
nshotsbase=widget_base(main,row=1,/align_center,/exclusive)
buttonA=widget_button(nshotsbase, value='Single Shots',uvalue='Single Shots')
buttonB=widget_button(nshotsbase, value='Averaged',uvalue='Averaged')
widget_control,buttonB,set_button=1 ;set the averaged button to be selected by default

;; create database file widgets 
;dbbase = widget_base(main, row=1, /base_align_center)
;dblabel = widget_label(dbbase, value='Database spectra:')
;dbtext = widget_text(dbbase, /editable, xsize=50)
;dbbutt = widget_button(dbbase, value = 'Browse...', uvalue='Database')
;widget_control,dbtext,set_value=dbfile
;
;compdbbase = widget_base(main, row=1, /base_align_center)
;compdblabel = widget_label(compdbbase, value='Database compositions:')
;compdbtext = widget_text(compdbbase, /editable, xsize=50)
;compdbbutt = widget_button(compdbbase, value = 'Browse...', uvalue='CompDatabase')
;widget_control,compdbtext,set_value=compdbfile

;; create mask file widget
;maskbase = widget_base(main, row=1, /base_align_center)
;masklabel = widget_label(maskbase, value='Mask file:')
;masktext = widget_text(maskbase, /editable, xsize=50)
;maskbutt = widget_button(maskbase, value = 'Browse...', uvalue='Mask')
;widget_control,masktext,set_value=maskfile
;
;; create PLS type of calculations widget
;
;calcbase = widget_base(main, row=1, /align_center, /exclusive)
;button1=widget_button(calcbase, value='Fixed', uvalue='Fixed')
;button2=widget_button(calcbase, value='Optimized (Global Min)', uvalue='GlobalMin')
;button3=widget_button(calcbase, value='Optimized (One Std. Err.)', uvalue='OneStdErr')
;widget_control,button1,set_button=1 ;set the fixed button to be selected by default
;; create recalculate button widget
;forcebase = widget_base(main, row=1, /align_center,/nonexclusive)
;forcebut = widget_button(forcebase, value='Recalculate RMSEP (Optimized only)', uvalue='Recalculate')
;;stop
;; create PLS number of components widget
;abase = widget_base(main, row=1, $
;  /grid_layout, /base_align_center)
;label = widget_label(abase, value='Max. # of components (ignored by fixed PLS1):')
;text2 = widget_text(abase, value='9', uvalue='nc', /editable, xsize=8)
;
;labelbase=widget_base(main,row=1,/align_center)
;label=widget_label(labelbase,value='----------------PLS1 Options----------------')
;; create stdev scale button widget
;stdevscalebase = widget_base(main, row=1, /align_center, /nonexclusive)
;stdevscalebut = widget_button(stdevscalebase, value='Scale pixels by training set standard deviation', uvalue='Stdevscale')
;widget_control,stdevscalebut,set_button=0   ;set to NOT do stdev scaling by default

;;create normalization widget
;normtotbase=widget_base(main,row=1,/align_center,/nonexclusive)
;normtotbut=widget_button(normtotbase,value='Normalize totals to 100%',uvalue='NormTot')
;widget_control,normtotbut,set_button=0 ;set Norm1 to NOT be selected by default
;clipzerobut=widget_button(normtotbase,value='Set negative results to 0%',uvalue='clipzero')
;widget_control,clipzerobut,set_button=0 ;set zero-clipping to be OFF by default
;
;;set spectrometer weights
;weightsbase = widget_base(main, /row,/base_align_center)
;uvweight_label = widget_label(weightsbase, value='UV Weight:')
;uvweight_text2 = widget_text(weightsbase, value='1.0', uvalue='Weights_UV', /editable,/all_events, xsize=10)
;
;visweight_label = widget_label(weightsbase, value='VIS Weight:')
;visweight_text2 = widget_text(weightsbase, value='1.0', uvalue='Weights_VIS', /editable, /all_events, xsize=10)
;
;vnirweight_label = widget_label(weightsbase, value='VNIR Weight:')
;vnirweight_text2 = widget_text(weightsbase, value='1.0', uvalue='Weights_VNIR', /editable, /all_events, xsize=10)

;create "fixed option" input file widgets
;
;labelbase=widget_base(main,row=1,/align_left)
;label=widget_label(labelbase,value='# of components for each oxide (only used for fixed PLS1):')
;
;fixedbaseOx = widget_base(main, row=1, /base_align_center)
;fixedlabelOx = widget_label(fixedbaseOx,value='')
;fixedtextOx1 = widget_text(fixedbaseOx, /editable, xsize=50)
;fixedbuttOx = widget_button(fixedbaseOx, value = 'Browse...', uvalue='ChooseFixedFileOx')
;
;widget_control,fixedtextOx1,set_value=fixedfileOx
;
;; create file widgets
;goodcompbase = widget_base(main, row=1, /base_align_center)
;goodcomplabel = widget_label(goodcompbase, value='Training set file:')
;goodcompstext1 = widget_text(goodcompbase, /editable, xsize=50)
;goodcompbutt = widget_button(goodcompbase, value = 'Browse...', uvalue='ChooseFile')
;widget_control,goodcompstext1,set_value=goodcompsfile

;; create file widgets
;normfilebase = widget_base(main, row=1, /base_align_center)
;normfilelabel = widget_label(normfilebase, value='Normalization file:')
;normfiletext1 = widget_text(normfilebase, /editable, xsize=50)
;normfilebutt = widget_button(normfilebase, value = 'Browse...', uvalue='ChooseNormFile')
;widget_control,normfiletext1,set_value=normfile
;
;labelbase=widget_base(main,row=1,/align_left)
;label=widget_label(labelbase,value='k-fold validation file (leave-one-out used if no file specified):')
;; create file widgets
;foldfilebase = widget_base(main, row=1, /base_align_center)
;foldfilelabel = widget_label(foldfilebase, value='')
;foldfiletext = widget_text(foldfilebase, /editable, xsize=50)
;foldfilebutt = widget_button(foldfilebase, value = 'Browse...', uvalue='ChooseFoldFile')
;widget_control,foldfiletext,set_value=foldfile
;;Specify fold number of test set
;testnumbase = widget_base(main, row=1,/grid_layout, /base_align_center)
;testnumlabel = widget_label(testnumbase, value='Fold # of test set (0 for no test set):')
;testnumtext2 = widget_text(testnumbase, value=strtrim(testnum,2), uvalue='testnum', /editable, /all_events, xsize=4)



; create OK and Cancel buttons
butsize=75
okbase=widget_base(tlb,row=1,/align_center)
okbut1=widget_button(okbase, value='OK', uvalue='OK', xsize=butsize)
okbut2=widget_button(okbase, value='Cancel', uvalue='Cancel', xsize=butsize)
;okbut3=widget_button(okbase, value='Help', uvalue='Help', xsize=butsize)


; realize widgets
widget_control, tlb, /realize

; define working directory path
    help,/source_files,output=source_list
;    xmess, source_list
; look for calcpls
; if not there then inc me
    me=where(strpos(source_list,'calcpls') ge 0)
    pname=strpos(source_list(me),'calcpls')
    if pname(0) gt 0 then begin
       fullpath=source_list(me(0))
    endif else begin
       ok = Error_Message('Source path is not detected!')
    endelse

    start=strpos(fullpath,"CALCPLS")

; strip off extra
    if start(0) ge 0 then begin

        therest=strmid(fullpath,start(0)+8,strlen(fullpath)-8)
               
    endif else begin
        therest=fullpath
    endelse
    shorter=strtrim(therest(0),1)
;    xmess, shorter
;;; VM comment ;;;
   mepos=strpos(shorter,'calcpls.pro') ; for tests
;   mepos=strpos(shorter,'calcpls.sav') ; for virtual machine
    print,mepos
    ;stop
    mepath=strmid(shorter,0,mepos(0))
    defsysv,'!work_dir',mepath
    print,'working directory',mepath
;    xmess, mepath
    cd, mepath

; create and store state information

plsparam = {workpath:mepath, datapath:datapath, $
nc:9, nc_type:0, Mask:maskfile,masktext:masktext, status:'Cancel', text1:text1, text2:text2,pls:0,singleshots:0,$
Recursive:1,maxsol:1000,minsol:0,maxsol_text2:maxsol_text2,minsol_text2:minsol_text2,goodcompsfile:goodcompsfile,$
goodcompstext1:goodcompstext1,opt_min:0,opt_ose:0,$
fixedfileOx:fixedfileOx,fixedtextOx1:fixedtextOx1,recalc:0,dbfile:dbfile,dbtext:dbtext,compdbfile:compdbfile,$
compdbtext:compdbtext,normfile:normfile,stdevscale:0,normtot:0,normfiletext1:normfiletext1,clipzero:0,foldfile:foldfile, $
foldfiletext:foldfiletext,testnum:testnum,testnumtext2:testnumtext2,masterfile:masterfile,masterfiletext1:masterfiletext1,$
weights:weights,uvweight_text2:uvweight_text2,visweight_text2:visweight_text2,vnirweight_text2:vnirweight_text2}
plsparamptr = ptr_new(plsparam)
widget_control, tlb, set_uvalue=plsparamptr

; manage events
xmanager, 'calcpls', tlb, cleanup='calcpls_cleanup'

; get results
result = *plsparamptr
ptr_free, plsparamptr
help, result
print, 'workpath =', result.workpath
print, 'datapath =', result.datapath
print, 'number components =', result.nc
print, 'nc type =', result.nc_type
print, 'Mask =', result.Mask
print, 'status =', result.status

;xmess, [result.workpath, result.datapath]


print, 'done creating widgets!'
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
if (result.status EQ 'OK') then begin
  print, 'start the PLS calculations'
  
  xmess,"Please Wait, Calculating...",/nowait,wid=wid
  print,result.pls
  widget_control,/hourglass
  ;stop
  if (result.pls) then $
  ccpls2, result.workpath, result.datapath, $
    nc=result.nc, type=result.nc_type, mask=result.Mask, singleshot=result.singleshots,minsol=result.minsol,$
    maxsol=result.maxsol,recursive=result.recursive,opt_min=result.opt_min,opt_ose=result.opt_ose,recalc=result.recalc,dbfile=result.dbfile,compdbfile=result.compdbfile else $ 
  stop
  ccpls1, result.workpath, result.datapath, nc=result.nc, type=result.nc_type, mask=result.Mask, $
    singleshot=result.singleshots,minsol=result.minsol, maxsol=result.maxsol,recursive=result.recursive, $
    normfile=result.normfile,goodcompsfile=result.goodcompsfile,opt_min=result.opt_min, opt_ose=result.opt_ose, $
    fixedfileox=result.fixedfileox,recalc=result.recalc,dbfile=result.dbfile,compdbfile=result.compdbfile, $
    stdevscale=result.stdevscale, normtot=result.normtot,clipzero=result.clipzero,nfoldfile=result.foldfile,testset=result.testnum,masterfile=result.masterfile,spectrometer_weights=result.weights
  
  widget_control,/dest,wid
  xmess ,"Processing complete" 
  wait,1
endif

end

