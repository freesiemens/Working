pro pdl_tool_event, event

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
    searchdir=repstr(searchdir,'\','/')
    calcparam.searchdir=searchdir
    ;Write the searchdir to the config file for future use
    calcparam.configdata[1,0]=searchdir
    
    write_csv,'pdl_tool_config.csv',calcparam.configdata  
    print, calcparam.searchdir
    widget_control,calcparam.text1,set_value=searchdir
   end

  
  
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
       calcparam.status = 'OK'
       print,calcparam.status
       *calcparamptr = calcparam
       widget_control,event.top,/destroy
    endelse
   end
  
  
  'Cancel': begin
    calcparam.status = 'Cancel'
    *calcparamptr = calcparam
    widget_control,event.top,/destroy
  end
  else : ok = Error_Message('Event not recognized!')
  
endcase

help,calcparam,/struct

; save state information
*calcparamptr = calcparam

end

pro pdl_tool_cleanup, ID

print, 'cleaning up'

; get state information
widget_control, id, get_uvalue=calcparamptr
calcparam=*calcparamptr



result = {workpath:calcparam.workpath, searchdir:calcparam.searchdir, $
status:calcparam.status,singleshots:calcparam.singleshots,recursive:calcparam.recursive,configdata:calcparam.configdata}
*calcparamptr = result



end

pro spdl_tool
software_version="sPDL Tool v2.0 (July 7, 2015)"
configfile='pdl_tool_config.csv'
configdata=rd_tfile(configfile,/autocol,delim=',')
configdata=repstr(repstr(configdata,'"',''),'\','/')

searchdir=configdata[1,0]


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

; realize widgets
widget_control, tlb, /realize

; define working directory path
cd,current=mepath
   
    defsysv,'!work_dir',mepath

; create and store state information

calcparam = {workpath:mepath, searchdir:searchdir, $
status:'Cancel', text1:text1,singleshots:0,Recursive:1,configdata:configdata}

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
print, 'status =', result.status

print, 'done creating widgets!'

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
if (result.status EQ 'OK') then begin

  widget_control,/hourglass
  quiet=0
  ica_output=1
  pls_output=1
  calcstdevs=1
  calc_comp,result.searchdir,result.singleshots,result.recursive,configfile,software_version,$
    quiet=quiet,pls_output=pls_output,ica_output=ica_output,calcstdevs=calcstdevs
  
    
  xmess ,"Processing complete" 
  wait,1
endif

end

