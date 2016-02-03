;+
; NAME:
;        SPDL_TOOL_ADVANCED
;        Includes also:
;           SPDL_TOOL_EVENT
;           PDL_TOOL_CLEANUP
;
; PURPOSE:
; This program runs the GUI that calls calc_comp, the main program for calculating ChemCam major element compositions using a combination of ICA and PLS
; This is the "advanced" version, which has more options.
;
; CALLING SEQUENCE:
;        spdl_tool
; INPUTS:
;        No direct inputs. GUI allows user to choose what directory to search, whether to search recursively, and whether to get single shot results.e, to be written in each output file
;        
; OPTIONAL INPUTS:
;        None
;
; KEYWORD PARAMETERS:
;        
; OUTPUTS:
;       
; OPTIONAL OUTPUTS:
;       
; RESTRICTIONS:
;         Requires a configuration file containing paths to necessary files and directories such as the master list, mask file, PLS settings, etc.
; EXAMPLE:
;       
; MODIFICATION HISTORY:
; R. Anderson: May-June 2015 - Write initial code (adapted from the original GUI code used for the previous PLS tool)
; R. Anderson: June-July 2015 - Modified so that the config file is passed to calc_comp instead of reading it here and passing a bunch of variables to be used there.
;                        - Added hard-coded options for suppressing pop-ups, separate ICA and PLS output,
;                          and for including shot-to-shot stdev results along with the mean results 
;                        - Removed single shot option, hard-coded default to calculate stdev from single shots
;-


pro pdl_tool_event, event
;cd,'/Users/jfr/CCAM_ops/Software/spdl_tool_advanced/'
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
   
   'shots': begin
    if (calcparam.shots EQ 1) then begin
      calcparam.shots = 0
    endif else if (calcparam.shots EQ 0) then begin
      calcparam.shots = 1
    endif 
    
    print, 'Single Shots = ', calcparam.shots
  end 
  
  'PLS': begin
    if (calcparam.pls EQ 1) then begin
      calcparam.pls = 0
    endif else if (calcparam.pls EQ 0) then begin
      calcparam.pls = 1
    endif 
    
    print, 'PLS', calcparam.pls
  end 
  
  'ICA': begin
    if (calcparam.ica EQ 1) then begin
      calcparam.ica = 0
    endif else if (calcparam.ica EQ 0) then begin
      calcparam.ica = 1
    endif 
    
    print, 'ICA', calcparam.ica
  end 
  
  'Stdevs': begin
    if (calcparam.calcstdevs EQ 1) then begin
      calcparam.calcstdevs = 0
    endif else if (calcparam.calcstdevs EQ 0) then begin
      calcparam.calcstdevs = 1
    endif 
    
    print, 'stdevs', calcparam.calcstdevs
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
status:calcparam.status,configdata:calcparam.configdata,pls:calcparam.pls,$
ica:calcparam.ica,calcstdevs:calcparam.calcstdevs,recursive:calcparam.recursive,shots:calcparam.shots}
*calcparamptr = result
end

pro spdl_tool_advanced
software_version="sPDL Tool v2.0 (Last edited 16 July 2015)"
;configfile='/Users/jfr/CCAM_ops/Software/spdl_tool_advanced/pdl_tool_config.csv'
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

; create pls button widget
plsbut = widget_button(checkbase, value='Output PLS', uvalue='PLS')
widget_control,plsbut,set_button=1   ;set to recursive search by default

; create ica button widget
icabut = widget_button(checkbase, value='Output ICA', uvalue='ICA')
widget_control,icabut,set_button=1   ;set to recursive search by default

; create calcstdev button widget
shotsbut = widget_button(checkbase, value='Single Shots', uvalue='shots')
widget_control,shotsbut,set_button=1   ;set to recursive search by default


; create calcstdev button widget
stdevbut = widget_button(checkbase, value='Calculate Stdevs', uvalue='Stdevs')
widget_control,stdevbut,set_button=1   ;set to recursive search by default


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

calcparam = {workpath:mepath, searchdir:searchdir,pls:1,ica:1,calcstdevs:1,recursive:1, $
status:'Cancel', text1:text1,configdata:configdata,shots:1}

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
  calc_comp,result.searchdir,result.shots,result.recursive,configfile,software_version,$
    quiet=quiet,pls_output=result.pls,ica_output=result.ica,calcstdevs=result.calcstdevs
  
    
  xmess ,"Processing complete" 
  wait,1
endif

end

