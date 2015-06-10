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
      
    calcparam.searchdir=searchdir  
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

; save result
configinfo=$
  [['searchdir',calcparam.searchdir],$
  ['masterlist1',calcparam.masterlist[0]],$
  ['masterlist2',calcparam.masterlist[1]],$
  ['masterlist3',calcparam.masterlist[2]],$
  ['maskfile',calcparam.mask],$
  ['meancenters_file',calcparam.meancenters_file],$
  ['settings_coeffs_file',calcparam.settings_coeffs_file],$
  ['blend_array_dir',calcparam.blend_array_dir],$
  ['testresult_dir',calcparam.testresult_dir]]
  
write_csv,'pdl_tool_config.csv',configinfo

result = {workpath:calcparam.workpath, searchdir:calcparam.searchdir, $
status:calcparam.status,singleshots:calcparam.singleshots,recursive:calcparam.recursive,masterlist:calcparam.masterlist,$
mask:calcparam.mask,pls_settings_labels:calcparam.pls_settings_labels,pls_norms:calcparam.pls_norms,pls_ncs:calcparam.pls_ncs,$
pls_coeffs:calcparam.pls_coeffs,meancenter_labels:calcparam.meancenter_labels,ymeancenters:calcparam.ymeancenters,meancenters:calcparam.meancenters,$
blend_Array_dir:calcparam.blend_array_dir,testresult_dir:calcparam.testresult_dir}
*calcparamptr = result



end

pro pdl_tool

configcheck=file_search('pdl_tool_config.csv')
if strlen(configcheck[0]) eq 0 then begin
  xmess ,'No config file found! Click ok to create one!'
  searchdir='.'
  masterlist1=dialog_pickfile(title='Choose the Season 1 masterlist file')
  masterlist2=dialog_pickfile(title='Choose the Season 2 masterlist file')
  masterlist3=dialog_pickfile(title='Choose the Season 3 masterlist file')
  maskfile=dialog_pickfile(title='Choose the mask file')
  meancenters_file=dialog_pickfile(title='Choose the PLS meancenters file')
  settings_coeffs_file=dialog_pickfile(title='Choose the PLS settings and coefficients file')
  blend_array_dir=dialog_pickfile(title='Choose the directory with PLS blend settings files',/directory)
  testresult_dir=dialog_pickfile(title='Choose the directory with the test set result files',/directory)
  configdata=$
    [['searchdir',searchdir],$
    ['masterlist1',masterlist1],$
    ['masterlist2',masterlist2],$
    ['masterlist3',masterlist3],$
    ['maskfile',maskfile],$
    ['meancenters_file',meancenters_file],$
    ['settings_coeffs_file',settings_coeffs_file],$
    ['blend_array_dir',blend_array_dir],$
    ['testresult_dir',testresult_dir]]
  write_csv,'pdl_tool_config.csv',configdata
  
endif

configdata=rd_tfile('pdl_tool_config.csv',/autocol,delim=',')
configdata=repstr(repstr(configdata,'"',''),'\','/')

searchdir=configdata[1,0]
masterlist1=configdata[1,1]
masterlist2=configdata[1,2]
masterlist3=configdata[1,3]
masterlist=[masterlist1,masterlist2,masterlist3]
maskfile=configdata[1,4]
meancenters_file=configdata[1,5]
settings_coeffs_file=configdata[1,6]
blend_array_dir=configdata[1,7]
testresult_dir=configdata[1,8]

meancenters=rd_tfile(meancenters_file,/autocol,delim=',')

meancenter_labels=meancenters[1:*,0]
ymeancenters=double(meancenters[1:*,1])
meancenters=double(meancenters[1:*,2:*])

pls_settings=rd_tfile(settings_coeffs_file,/autocol,delim=',')
pls_settings_labels=pls_settings[1:*,0]
pls_norms=fix(pls_settings[1:*,1])
pls_ncs=fix(pls_settings[1:*,2])
pls_coeffs=double(pls_settings[1:*,3:*])


undefine,calcparam ;clear all info in calcparam so it can be properly set again

; create top level base
tlb=widget_base(column=1, title="PDL_TOOL", $
  tlb_frame_attr=1)
  
; create base to hold everything except buttons
main=widget_base(tlb, column=1, frame=1)
warning = widget_label(main, value='WARNING: THIS IS NOT THE FINAL VERSION OF THE TOOL!!')
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
Mask:maskfile, status:'Cancel', text1:text1, pls:0,singleshots:0,$
Recursive:1,masterlist:masterlist,pls_settings_labels:pls_settings_labels,$
pls_norms:pls_norms,pls_ncs:pls_ncs,pls_coeffs:pls_coeffs,meancenter_labels:meancenter_labels,$
ymeancenters:ymeancenters,meancenters:meancenters,meancenters_file:meancenters_file,settings_coeffs_file:settings_coeffs_file,$
blend_array_dir:blend_array_dir,testresult_dir:testresult_dir}

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
  
  comps=calc_comp(result.searchdir,result.singleshots,result.mask,result.masterlist,result.recursive,result.pls_settings_labels,$
    result.pls_norms,result.pls_ncs,result.pls_coeffs,result.meancenter_labels,result.ymeancenters,result.meancenters,result.blend_array_dir,$
    result.testresult_dir);,os=os)
  
    
  xmess ,"Processing complete" 
  wait,1
endif

end

