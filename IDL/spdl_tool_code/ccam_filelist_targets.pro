function ccam_filelist_targets,masterfile,filelist,quiet=quiet

for i=0,n_elements(masterfile)-1 do begin
  
mastertemp=rd_tfile(masterfile[i],/autocol,delim=',',hskip=2,header=header)  ;Read the master list

header=strsplit(header[1],',',/extract)
mastertemp=mastertemp[0:n_elements(header)-1,*]

if i eq 0 then master=mastertemp 
if i gt 0 then master=[[master],[mastertemp]]

endfor

master_targets=master(5,*)  ;extract the target names from the master list
master_nshots=master(11,*)
master_dists=master(8,*)
master_amps=master(17,*)

filelist_targets=strarr(n_elements(filelist['filelist']))  ;create an array to hold the target names in the file list
filelist_nshots=intarr(n_elements(filelist['filelist']))
filelist_dists=fltarr(n_elements(filelist['filelist']))
filelist_amps=strarr(n_elements(filelist['filelist']))
if not(quiet) then progbar=Obj_New('cgProgressBar',/start,percent=0,title='Looking up info for '+strtrim(n_elements(filelist['filelist']),2)+' files...')

for i=0,n_elements(filelist['filelist'])-1 do begin
  
   matchindex=(where(strupcase(master(2,*)) eq (filelist['sclock'])(i)))(0) ;look up where the sclock in the master list matches the sclock for the file list
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
if not(quiet) then progbar -> Update, float(i+1)/n_elements(filelist['filelist'])*100

endfor
if not(quiet) then progbar -> Destroy

strreplace,filelist_targets,' ','_'
strreplace,filelist_targets,' ','_'
strreplace,filelist_targets,' ','_'


;Replace cal target numbers with actual sample name
namelist_search=['Cal_Target_1','Cal_Target_2','Cal_Target_3','Cal_Target_4','Cal_Target_5','Cal_Target_6',$
  'Cal_Target_7','Cal_Target_8','Cal_Target_9','Cal_Target_10','Cal_Target_10_Titanium',$
  'CCCT_01','CCCT_02','CCCT_03','CCCT_04','CCCT_05','CCCT_06','CCCT_07','CCCT_08','CCCT_09','CCCT_10']
namelist_replace=['Macusanite','Norite','Picrite','Shergottite','Graphite','Kga-d_Med-S','NAu-2_Low-S',$
  'NAu-2_Med-S','NAu-2_Hi-S','Ti','Ti','Macusanite','Norite','Picrite','Shergottite','Graphite',$
  'Kga-d_Med-S','NAu-2_Low-S','NAu-2_Med-S','NAu-2_Hi-S','Ti']

for i=0,n_elements(namelist_search)-1 do begin
  ind=where(filelist_targets eq namelist_search[i])
  if max(ind) ne -1 then filelist_targets[ind]=namelist_replace[i]
endfor  

filelist=filelist+hash('nshots',filelist_nshots,'dists',filelist_dists,'amps',filelist_amps,'targets',filelist_targets)
return,filelist
end