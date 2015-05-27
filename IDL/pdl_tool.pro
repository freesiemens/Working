pro pdl_tool_event, event
; this is the pdl_tool event handler
; history: modifications by J. Lasue 2012 07 08
; R. Anderson 2012 09 29 - Modified to allow user to select between single shots and averaged spectra
; R. Anderson 2013 Jan-March - Modified to allow recursive searches, min and max sols, and to automatically load the last-used searchdir
; R. Anderson 2013 April-May - Lots of edits to implement PLS1
; R. Andeson 2013 August - Added options to normalize and scale to stdev

print, 'Event detected !'

; get state information
widget_control, event.top, get_uvalue=calcparamptr
calcparam = *calcparamptr

; identify widget which caused the event
widget_control, event.id, get_uvalue=widget
help, widget

; handle events
case widget of

  'Choose': begin
    searchdir=Dialog_pickfile( $
      title="Select the directory to search...",/directory,path=searchdir)
    sizepath=strlen(searchdir)
      
    calcparam.searchdir=searchdir  
    print, calcparam.searchdir
    widget_control,calcparam.text1,set_value=searchdir
    ;help,goodcompsfile,searchdir,fixedfileEl,fixedfileOx
    ;stop
    ;save,goodcompsfile,searchdir,fixedfileEl,fixedfileOx,filename='pdl_tool_paramfile.sav' ;save the searchdir so that it can be restored next time the program is run 
  end
;  
;  'ChooseFile': begin
;    goodcompsfile=Dialog_pickfile( $
;      title="Select the desired file...",path=searchdir)
;         
;    calcparam.goodcompsfile=goodcompsfile  
;    print, calcparam.goodcompsfile
;    widget_control,calcparam.goodcompstext1,set_value=goodcompsfile
;    ;help,goodcompsfile,searchdir,fixedfileEl,fixedfileOx
;    ;stop
;    ;save,goodcompsfile,searchdir,fixedfileEl,fixedfileOx,filename='pdl_tool_paramfile.sav' ;save the file path so that it can be restored next time the program is run 
;  end
  
;  'ChooseNormFile': begin
;    normfile=Dialog_pickfile( $
;      title="Select the desired file...",path=searchdir)
;         
;    calcparam.normfile=normfile  
;    print, calcparam.normfile
;    widget_control,calcparam.normfiletext1,set_value=normfile
;    ;help,goodcompsfile,searchdir,fixedfileEl,fixedfileOx
;    ;stop
;    ;save,goodcompsfile,searchdir,fixedfileEl,fixedfileOx,filename='pdl_tool_paramfile.sav' ;save the file path so that it can be restored next time the program is run 
;  end
  
;  'ChooseMasterFile': begin
;    masterfile=Dialog_pickfile( $
;      title="Select the desired file...",path=searchdir)
;         
;    calcparam.masterfile=masterfile  
;    print, calcparam.masterfile
;    widget_control,calcparam.masterfiletext1,set_value=masterfile
;  end
  
;  'ChooseFoldFile': begin
;    foldfile=Dialog_pickfile( $
;      title="Select the desired file...",path=searchdir)
;         
;    calcparam.foldfile=foldfile  
;    print, calcparam.foldfile
;    widget_control,calcparam.foldfiletext,set_value=foldfile
;    ;help,goodcompsfile,searchdir,fixedfileEl,fixedfileOx
;    ;stop
;    ;save,goodcompsfile,searchdir,fixedfileEl,fixedfileOx,filename='pdl_tool_paramfile.sav' ;save the file path so that it can be restored next time the program is run 
;  end
  
  ;'ChooseFixedFileEl': begin
  ;  fixedfileEl=Dialog_pickfile( $
  ;    title="Select the desired file...",path=searchdir)
  ;       
  ;  calcparam.fixedfileEl=fixedfileEl  
  ;  print, calcparam.fixedfileEl
  ;  widget_control,calcparam.fixedtextEl1,set_value=fixedfileEl
    ;help,goodcompsfile,searchdir,fixedfileEl,fixedfileOx
    ;stop
    ;save,goodcompsfile,searchdir,fixedfileEl,fixedfileOx,filename='pdl_tool_paramfile.sav' ;save the file path so that it can be restored next time the program is run 
  ;end
  
;  'ChooseFixedFileOx': begin
;    fixedfileOx=Dialog_pickfile( $
;      title="Select the desired file...",path=searchdir)
;         
;    calcparam.fixedfileOx=fixedfileOx  
;    print, calcparam.fixedfileOx
;    widget_control,calcparam.fixedtextOx1,set_value=fixedfileOx
;    
;  end
  
  
  'Recursive': begin
    if (calcparam.Recursive EQ 1) then begin
      calcparam.Recursive = 0
    endif else if (calcparam.Recursive EQ 0) then begin
      calcparam.Recursive = 1
    endif else begin
      ok = Error_Message('Not a recognized Mask value!')
    endelse
    
    print, 'Recursive = ', calcparam.Recursive
  end

  
   'Single Shots': begin
    if (calcparam.singleshots EQ 1) then begin
      calcparam.singleshots = 0
    endif else if (calcparam.singleshots EQ 0) then begin
      calcparam.singleshots = 1
    endif 
    
    print, 'Single Shots = ', calcparam.singleshots
  end 
 
  'OK': begin
    ; check that data has been defined, if not error message

    if strlen(calcparam.searchdir) EQ 0 then begin
      ok = Error_Message('Need to define the data path first!')
    endif else begin
      ; check the number of components entered by the user
;      WIDGET_CONTROL,calcparam.text2,GET_VALUE=indata
;      print, indata
      ; check validity
;      if calcparam.recalc eq 1 and calcparam.nc_type eq 0 then begin
;         ok = Error_Message("Can't have 'fixed' and 'recalculate' both selected! Exiting...")
;         widget_control,event.top,/destroy
;         
;      endif
      
;      if((indata GT 0) AND (indata LE 50)) then begin
;        calcparam.nc=indata
        ; gets the OK if that is fine
        calcparam.status = 'OK'
; widget not destroyed after selecting the calculations
        widget_control,event.top,/destroy
;      endif else if ((indata GT 0) AND (indata GT 50)) then begin
;        ok = Error_Message('Number of components too high, reset to 10!')
;        calcparam.nc=10
;      endif else begin
;        ok = Error_Message('Number of components value not allowed, reset to 10!')
;        calcparam.nc=10
;      endelse    
    endelse
print,calcparam.status    
  end
  'Cancel': begin
    calcparam.status = 'Cancel'
    widget_control,event.top,/destroy
  end

  

   
  
  else : ok = Error_Message('Event not recognized!')
  
    
  
endcase



; save state information
*calcparamptr = calcparam

end

pro pdl_tool_cleanup, ID

print, 'cleaning up'

; get state information
widget_control, id, get_uvalue=calcparamptr
calcparam=*calcparamptr

; save result

save,calcparam,filename=calcparam.workpath+'pdl_tool_paramfile.sav'


result = {workpath:calcparam.workpath, searchdir:calcparam.searchdir, $
status:calcparam.status,singleshots:calcparam.singleshots,recursive:calcparam.recursive,masterlist:calcparam.masterlist}
*calcparamptr = result

end

pro pdl_tool

configdata=rd_tfile('pdl_tool_config.csv',/autocol,delim=',')
searchdir=configdata[1,where(configdata[0,*] eq 'searchdir')]
masterlist=configdata[1,where(configdata[0,*] eq 'masterlist')]
maskfile=configdata[1,where(configdata[0,*] eq 'maskfile')]
meancenters_file=configdata[1,where(configdata[0,*] eq 'meancenters_file')]
settings_coeffs_file=configdata[1,where(configdata[0,*] eq 'settings_coeffs_file')]
blend_array_dir=configdata[1,where(configdata[0,*] eq 'blend_array_dir')]
pls_testresult_dir=configdata[1,where(configdata[0,*] eq 'pls_testresult_dir')]

meancenters=rd_tfile(meancenters_file,/autocol,delim=',')
meancenter_labels=meancenters[1:*,0]
ymeancenters=double(meancenters[1:*,1])
meancenters=double(meancenters[1:*,2:*])

pls_settings=rd_tfile(settings_coeffs_file,/autocol,delim=',')
pls_settings_labels=pls_settings[1:*,0]
pls_norms=fix(pls_settings[1:*,1])
pls_ncs=fix(pls_settings[1:*,2])
pls_coeffs=double(pls_settings[1:*,3:*])


;restore,'pdl_tool_paramfile.sav'  ;restore a save file containing the paths used last time the function was run
;searchdir=calcparam.searchdir
;fixedfileox=calcparam.fixedfileOx
;fixedfileel=calcparam.fixedfileel
;goodcompsfile=calcparam.goodcompsfile
;maskfile=calcparam.mask
;dbfile=calcparam.dbfile
;compdbfile=calcparam.compdbfile
;normfile=calcparam.normfile
;foldfile=calcparam.foldfile
;testnum=calcparam.testnum
;masterlist=calcparam.masterlist
;weights=[1.0,1.0,1.0]

undefine,calcparam ;clear all info in calcparam so it can be properly set again

; create top level base
tlb=widget_base(column=1, title="PDL_TOOL", $
  tlb_frame_attr=1)
  
; create base to hold everything except buttons
main=widget_base(tlb, column=1, frame=1)

; create file widgets
fbase = widget_base(main, row=1, /base_align_center)
label = widget_label(fbase, value='Search Directory:')
text1 = widget_text(fbase, /editable, xsize=50)
butt = widget_button(fbase, value = 'Browse...', uvalue='Choose')
widget_control,text1,set_value=searchdir

labelbase=widget_base(main,row=1,/align_center)

; create recursive button widget
checkbase = widget_base(main, row=1, /align_center, /nonexclusive)
recurbut = widget_button(checkbase, value='Recursive', uvalue='Recursive')
widget_control,recurbut,set_button=1   ;set to recursive search by default

shotsbut = widget_button(checkbase, value='Single Shots', uvalue='Single Shots')
widget_control,shotsbut,set_button=0   ;set to recursive search by default
 
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
; look for pdl_tool
; if not there then inc me
    me=where(strpos(source_list,'pdl_tool') ge 0)
    pname=strpos(source_list(me),'pdl_tool')
    if pname(0) gt 0 then begin
       fullpath=source_list(me(0))
    endif else begin
       ok = Error_Message('Source path is not detected!')
    endelse

    start=strpos(fullpath,"PDL_TOOL")

; strip off extra
    if start(0) ge 0 then begin

        therest=strmid(fullpath,start(0)+8,strlen(fullpath)-8)
               
    endif else begin
        therest=fullpath
    endelse
    shorter=strtrim(therest(0),1)
;    xmess, shorter
;;; VM comment ;;;
   mepos=strpos(shorter,'pdl_tool.pro') ; for tests
;   mepos=strpos(shorter,'pdl_tool.sav') ; for virtual machine
    ;print,mepos
    ;stop
    mepath=strmid(shorter,0,mepos(0))
    defsysv,'!work_dir',mepath
    ;print,'working directory',mepath
;    xmess, mepath
    cd, mepath

; create and store state information

calcparam = {workpath:mepath, searchdir:searchdir, $
Mask:maskfile, status:'Cancel', text1:text1, pls:0,singleshots:0,$
Recursive:1,masterlist:masterlist,pls_settings_labels:pls_settings_labels,$
pls_norms:pls_norms,pls_ncs:pls_ncs,pls_coeffs:pls_coeffs,meancenter_labels:meancenter_labels,$
ymeancenters:ymeancenters,meancenters:meancenters,blend_array_dir:blend_array_dir,pls_testresult_dir:pls_testresult_dir}
calcparamptr = ptr_new(calcparam)
widget_control, tlb, set_uvalue=calcparamptr

; manage events
xmanager, 'pdl_tool', tlb, cleanup='pdl_tool_cleanup'

; get results
result = *calcparamptr
ptr_free, calcparamptr
help, result
print, 'workpath =', result.workpath
print, 'searchdir =', result.searchdir
;print, 'number components =', result.nc
;print, 'nc type =', result.nc_type
print, 'Mask =', result.Mask
print, 'status =', result.status

;xmess, [result.workpath, result.searchdir]


print, 'done creating widgets!'

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
if (result.status EQ 'OK') then begin
  
  print, 'start the PLS calculations'
  
  xmess,"Please Wait, Calculating...",/nowait,wid=wid
  print,result.pls
  widget_control,/hourglass
  
  comps=calc_comp(result.searchdir,result.singleshots,result.mask,result.masterlist,result.recursive,result.pls_settings_labels,$
    result.pls_norms,result.pls_ncs,result.pls_coeffs,result.meancenter_labels,result.ymeancenters,result.meancenters,result.blend_array_dir,$
    result.pls_testresult_dir)
  
  
  ;stop
;  if (result.pls) then $
;  ccpls2, result.workpath, result.searchdir, $
;    nc=result.nc, type=result.nc_type, mask=result.Mask, singleshot=result.singleshots,minsol=result.minsol,$
;    maxsol=result.maxsol,recursive=result.recursive,opt_min=result.opt_min,opt_ose=result.opt_ose,recalc=result.recalc,dbfile=result.dbfile,compdbfile=result.compdbfile else $ 
;  stop
;  ccpls1, result.workpath, result.searchdir, nc=result.nc, type=result.nc_type, mask=result.Mask, $
;    singleshot=result.singleshots,minsol=result.minsol, maxsol=result.maxsol,recursive=result.recursive, $
;    normfile=result.normfile,goodcompsfile=result.goodcompsfile,opt_min=result.opt_min, opt_ose=result.opt_ose, $
;    fixedfileox=result.fixedfileox,recalc=result.recalc,dbfile=result.dbfile,compdbfile=result.compdbfile, $
;    stdevscale=result.stdevscale, normtot=result.normtot,clipzero=result.clipzero,nfoldfile=result.foldfile,testset=result.testnum,masterlist=result.masterlist,spectrometer_weights=result.weights
;  
  widget_control,/dest,wid
  xmess ,"Processing complete" 
  wait,1
endif

end

