;+
; NAME:
;        CCAM_FILELIST_TARGETS
;
; PURPOSE:
; This is used to look up target name and other info for ChemCam data files, using the Master List files
;
; CALLING SEQUENCE:
;        file_data=ccam_filelist_targets(masterlist,file_data,quiet=quiet)
; INPUTS:
;        masterlist = Array containing paths to master list files. These files are assumed to have the same format.
;        file_data = hash produced by ccam_filelist.pro, containing file names, sclocks, paths, etc.
;        
; OPTIONAL INPUTS:
;        
;
; KEYWORD PARAMETERS:
;        quiet = Set to 1 to suppress progress bars
; OUTPUTS:
;        file_data = Metadata such as target name, laser energy, target distance, etc. are added to the file_data hash that is provided as input
; OPTIONAL OUTPUTS:
;       
; RESTRICTIONS:
;         Master list files must all have the same number of columns, and the columns must be organized as expected
; EXAMPLE:
;       
; MODIFICATION HISTORY:
; R. Anderson July 2015: - I wrote this code a while ago (2013?) but made many modifications to get it to the current form
; R. Anderson May 2017: Made the routine more robust to masterlists with mismatching # of columns or column names
;-



function ccam_filelist_targets,masterfile,file_data,quiet=quiet
master=[]
headers=[]
pointers=[]
for i=0,n_elements(masterfile)-1 do begin
    if file_test(masterfile[i]) ne 0 then begin
       mastertemp=rd_tfile(masterfile[i],/autocol,delim=',',hskip=2,header=header)  ;Read the master list
       
    endif else begin
       xmess ,"Masterlist file "+masterfile[i]+" not found!"
       exit
    endelse
    header=strsplit(header[1],',',/extract)
    if where(header eq 'Distance (mm)') ne -1 then header[where(header eq 'Distance (mm)')]='Distance (m)' ;manually fix the confusion about distance units in the master list column names 
    mastertemp=mastertemp[0:n_elements(header)-1,*]
    pointers=[[pointers],ptr_new(mastertemp,/no_copy)]
    headers=[[headers],ptr_new(header,/no_copy)]
endfor

ncols=[]
for h=0,n_elements(headers)-1 do begin
  ncols=[[ncols],n_elements(*headers[h])]
endfor

;check to make sure the master lists have the same number of columns
if n_elements(uniq(ncols,sort(ncols))) ne 1 then begin
  xmess,'The masterlist files provided do not have a matching number of columns! Cannot concatenate them together!'
  exit  ;If the columns don't match, quit
endif else begin
  
  for h=0,n_elements(headers)-1 do begin
    if h eq 0 then begin
      headervals=*headers[h]
      master=*pointers[h]
    endif
    if h gt 0 then begin
      ;Check to make sure the column names match before concatenating, to avoid inadvertently mixing different data types
      ;If the column names don't match, warn but proceed.
      if not array_equal(headervals[*,h-1],*headers[h]) then xmess,'The column names in the master lists do not all match! Proceed with caution. The column names from the first file will be used to look up information.'
      headervals=[[headervals],[*headers[h]]]
      master=[[master],[*pointers[h]]]
    endif
  endfor
endelse

master=hash('targets',master[where(headervals[*,0] eq 'Target'),*],$
             'nshots',master[where(headervals[*,0] eq 'Nbr of Shots'),*],$
              'dists',master[where(headervals[*,0] eq 'Distance (m)'),*],$
               'amps',master[where(headervals[*,0] eq 'Laser Energy'),*],$
             'sclock',master[where(headervals[*,0] eq 'Spacecraft Clock'),*])
nfiles=n_elements(file_data['filelist'])
file_data=file_data+hash('targets',strarr(nfiles),'nshots',intarr(nfiles),'dists',fltarr(nfiles),'amps',strarr(nfiles))

if not(quiet) then progbar=Obj_New('cgProgressBar',/start,percent=0,title='Looking up info for '+strtrim(nfiles,2)+' files...')

for i=0,nfiles-1 do begin
  
   matchindex=(where(strupcase(master['sclock']) eq file_data['sclock',i]))(0) ;look up where the sclock in the master list matches the sclock for the file list
   if matchindex ne -1 then begin
     ;If there is a sclock match, then assign the appropriate target name and info
    file_data['targets',i]=master['targets',matchindex]
    file_data['nshots',i]=master['nshots',matchindex]
    file_data['dists',i]=master['dists',matchindex]
    file_data['amps',i]=master['amps',matchindex]
    
   endif else begin
    file_data['targets',i]='Target not found'
    file_data['nshots',i]=0
    file_data['dists',i]=0
    file_data['amps',i]=''
    
    endelse
   
   if not(quiet) then progbar -> Update, float(i+1)/nfiles*100
endfor
if not(quiet) then progbar -> Destroy
   file_data['targets']=repstr(file_data['targets',*],' ','_')
   
;Replace cal target numbers with actual sample name
   namelist_search=['Cal_Target_1','Cal_Target_2','Cal_Target_3','Cal_Target_4','Cal_Target_5','Cal_Target_6',$
   'Cal_Target_7','Cal_Target_8','Cal_Target_9','Cal_Target_10','Cal_Target_10_Titanium',$
   'CCCT_01','CCCT_02','CCCT_03','CCCT_04','CCCT_05','CCCT_06','CCCT_07','CCCT_08','CCCT_09','CCCT_10']
   namelist_replace=['Macusanite','Norite','Picrite','Shergottite','Graphite','Kga-d_Med-S','NAu-2_Low-S',$
   'NAu-2_Med-S','NAu-2_Hi-S','Ti','Ti','Macusanite','Norite','Picrite','Shergottite','Graphite',$
   'Kga-d_Med-S','NAu-2_Low-S','NAu-2_Med-S','NAu-2_Hi-S','Ti']
   for j=0,n_elements(namelist_search)-1 do begin
      ind=where(file_data['targets'] eq namelist_search[j])
      if ind[0] ne -1 then file_data['targets',ind]=namelist_replace[j]
   endfor

   return,file_data
end