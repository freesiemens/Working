function ccam_filelist_targets,masterfile,filelist,filelist_sclock,filelist_nshots=filelist_nshots,filelist_dists=filelist_dists,filelist_amps=filelist_amps

for i=0,n_elements(masterfile)-1 do begin
  
mastertemp=rd_tfile(masterfile[i],/autocol,delim=',',hskip=2,header=header)  ;Read the master list

header=strsplit(header[1],',',/extract)
mastertemp=mastertemp[0:n_elements(header)-1,*]
;Add spacer so that all masterlists (from seasons 1,2,3) have same number of columns
if n_elements(header) eq 25 then begin
  
spacer=strarr(3,n_elements(mastertemp[0,*]))
mastertemp=[mastertemp[0:19,*],spacer,mastertemp[20:*,*]]
endif
if n_elements(header) eq 26 then begin
  
  spacer=strarr(2,n_elements(mastertemp[0,*]))
  mastertemp=[mastertemp[0:19,*],spacer,mastertemp[20:*,*]]
endif

if i eq 0 then master=mastertemp 
if i gt 0 then master=[[master],[mastertemp]]

endfor

master_targets=master(5,*)  ;extract the target names from the master list
master_nshots=master(11,*)
master_dists=master(8,*)
master_amps=master(17,*)

filelist_targets=strarr(n_elements(filelist))  ;create an array to hold the target names in the file list
filelist_nshots=intarr(n_elements(filelist))
filelist_dists=fltarr(n_elements(filelist))
filelist_amps=strarr(n_elements(filelist))
progbar=Obj_New('cgProgressBar',/start,percent=0,title='Looking up info for '+strtrim(n_elements(filelist),2)+' files...')

for i=0,n_elements(filelist)-1 do begin
  
   matchindex=(where(strupcase(master(2,*)) eq filelist_sclock(i)))(0) ;look up where the sclock in the master list matches the sclock for the file list
   if matchindex ne -1 then begin
      
      filelist_targets(i)=master_targets(matchindex) ;If there is a sclock match, then assign the appropriate target name 
      filelist_nshots(i)=master_nshots(matchindex)
      filelist_dists(i)=master_dists(matchindex)
      filelist_amps(i)=master_amps(matchindex)
      
   endif else begin
     filelist_targets(i)='' ;If there is not a sclock match, then don't label it
     filelist_nshots(i)=0
     filelist_dists(i)=0
     filelist_amps(i)=''
   endelse
progbar -> Update, float(i+1)/n_elements(filelist)*100

endfor
progbar -> Destroy

strreplace,filelist_targets,' ','_'
strreplace,filelist_targets,' ','_'
strreplace,filelist_targets,' ','_'
;stop

;Replace cal target numbers with actual sample name
if max(where(filelist_targets eq 'Cal_Target_1')) ne -1 then filelist_targets(where(filelist_targets eq 'Cal_Target_1'))='Macusanite'
if max(where(filelist_targets eq 'Cal_Target_2')) ne -1 then filelist_targets(where(filelist_targets eq 'Cal_Target_2'))='Norite'
if max(where(filelist_targets eq 'Cal_Target_3')) ne -1 then filelist_targets(where(filelist_targets eq 'Cal_Target_3'))='Picrite'
if max(where(filelist_targets eq 'Cal_Target_4')) ne -1 then filelist_targets(where(filelist_targets eq 'Cal_Target_4'))='Shergottite'
if max(where(filelist_targets eq 'Cal_Target_5')) ne -1 then filelist_targets(where(filelist_targets eq 'Cal_Target_5'))='Graphite'
if max(where(filelist_targets eq 'Cal_Target_6')) ne -1 then filelist_targets(where(filelist_targets eq 'Cal_Target_6'))='Kga-d_Med-S'
if max(where(filelist_targets eq 'Cal_Target_7')) ne -1 then filelist_targets(where(filelist_targets eq 'Cal_Target_7'))='NAu-2_Low-S'
if max(where(filelist_targets eq 'Cal_Target_8')) ne -1 then filelist_targets(where(filelist_targets eq 'Cal_Target_8'))='NAu-2_Med-S'
if max(where(filelist_targets eq 'Cal_Target_9')) ne -1 then filelist_targets(where(filelist_targets eq 'Cal_Target_9'))='NAu-2_Hi-S'
if max(where(filelist_targets eq 'Cal_Target_10')) ne -1 then filelist_targets(where(filelist_targets eq 'Cal_Target_10'))='Ti'
if max(where(filelist_targets eq 'Cal_Target_10_Titanium')) ne -1 then filelist_targets(where(filelist_targets eq 'Cal_Target_10_Titanium'))='Ti'

if max(where(filelist_targets eq 'CCCT_01')) ne -1 then filelist_targets(where(filelist_targets eq 'CCCT_01'))='Macusanite'
if max(where(filelist_targets eq 'CCCT_02')) ne -1 then filelist_targets(where(filelist_targets eq 'CCCT_02'))='Norite'
if max(where(filelist_targets eq 'CCCT_03')) ne -1 then filelist_targets(where(filelist_targets eq 'CCCT_03'))='Picrite'
if max(where(filelist_targets eq 'CCCT_04')) ne -1 then filelist_targets(where(filelist_targets eq 'CCCT_04'))='Shergottite'
if max(where(filelist_targets eq 'CCCT_05')) ne -1 then filelist_targets(where(filelist_targets eq 'CCCT_05'))='Graphite'
if max(where(filelist_targets eq 'CCCT_06')) ne -1 then filelist_targets(where(filelist_targets eq 'CCCT_06'))='Kga-d_Med-S'
if max(where(filelist_targets eq 'CCCT_07')) ne -1 then filelist_targets(where(filelist_targets eq 'CCCT_07'))='NAu-2_Low-S'
if max(where(filelist_targets eq 'CCCT_08')) ne -1 then filelist_targets(where(filelist_targets eq 'CCCT_08'))='NAu-2_Med-S'
if max(where(filelist_targets eq 'CCCT_09')) ne -1 then filelist_targets(where(filelist_targets eq 'CCCT_09'))='NAu-2_Hi-S'
if max(where(filelist_targets eq 'CCCT_10')) ne -1 then filelist_targets(where(filelist_targets eq 'CCCT_10'))='Ti'



return,filelist_targets
end