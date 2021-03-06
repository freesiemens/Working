;This function generates a list of CCAM LIBS files for use in other programs. It searches (optionally recursively) for CCAM LIBS files,
;removes duplicates, constrains the list to a specified sol range, and keeping the highest version in cases where there are two different versions
;of the same observation
;
; searchdir - the directory to search for LIBS files
; recursive - set to 1 do a recursive search in the specified directory
; minsol - keyword to specify the minimum sol for the files in the final file list
; maxsol - keyword to specify the maximum sol for the files in the final file list
; searchstring - The string to search for. If not specified, the default is: 'CL5*CCS*CCAM?????P*.SAV'
; allversions - Set to 1 to skip version checking and return all versions of an observation
; 
; Modified 19-JUN-2015 by Olivier Gasnault. In case of OS=Windows then add " to the path (see 20150619 tag).
; Modified 27-JUN-2015 by Olivier Gasnault. Add /NULL in search for CCAM15305 in case that seqID is not present;
;                                           Add a TEST to see if there is any GOODSOLS left.
;Modified 9 Jul 2015 by Ryan Anderson. Return a hash with data rather than using a bunch of keywords.
;Modified 13 Jul 2015 by Ryan Anderson: Return an array of hashes instead

function ccam_filelist,searchdir,searchstring=searchstring,minsol=minsol,maxsol=maxsol,recursive=recursive,allversions=allversions
;check operating system
help,!version,output=ver_info
os=ver_info(where(strpos(ver_info,'OS_FAMILY') ne -1))
os=repstr(repstr(repstr(repstr(os,' ',''),'OS_FAMILY',''),'STRING',''),"'",'')

cd,current=currentdir ;Find the current directory
if searchdir ne currentdir then cd,searchdir ;change to the search directory if not already there

if not(keyword_set(searchstring)) then searchstring='CL5*CCS*CCAM*P*.SAV'
if keyword_set(recursive) then begin
    if os eq 'Windows' then begin
      ; 20150619 tag: Add " to be compatible with spaces in the path
      print,'dir "'+repstr(searchdir+searchstring,'/','\')+'" /s /b'
      spawn,'dir "'+repstr(searchdir+searchstring,'/','\')+'" /s /b',filelist      
    endif
    
    if os ne 'Windows' then begin
      print,'find '+searchdir+' -type f -name "'+searchstring+'"'
      spawn,'find '+searchdir+' -type f -name "'+searchstring+'"',filelist
    endif
    
    filelist=repstr(filelist,'\','/') 
    pathlist=strarr(n_elements(filelist))
    
    
    for i=0,n_elements(filelist)-1 do begin

       split_temp=strsplit(filelist(i),'/',/extract)

        pathlist(i)=strjoin(split_temp(0:n_elements(split_temp)-2),'/')+'/'
        if os ne 'Windows' then pathlist(i)='/'+pathlist(i)

    filelist(i)=split_temp(n_elements(split_temp)-1)
    endfor

endif else begin
  
  filelist=file_search(searchstring)
  pathlist=strarr(n_elements(filelist))+searchdir
endelse 
 

;Remove exact duplicates in the file list  
pathlist=pathlist(uniq(filelist,sort(filelist)))
filelist=filelist(uniq(filelist,sort(filelist)))

;extract the sols from the filenames
filelist_sols=fix(strmid(filelist,31,3))
filelist_sols[where(strmid(filelist,25,9) eq 'CCAM15305', /NULL)]=19  ;Correct for erroneous seqID on Peacock Hills

;Apply sol constraints, if present
if n_elements(maxsol) eq 0 then maxsol=max(filelist_sols)
if n_elements(minsol) eq 0 then minsol=min(filelist_sols)
print,'Keep only files between sol '+strtrim(minsol,2)+' and sol '+strtrim(maxsol,2)
goodsols=where(filelist_sols ge minsol and filelist_sols le maxsol, test)
if test eq 0 then message,'No data left after selection on Sol numbers.'
filelist=filelist(goodsols) ;restrict file list to specified sol range
filelist_sols=filelist_sols(goodsols) ;likewise restrict sol array
pathlist=pathlist(goodsols) ;likewise restrict the path list
;print,pathlist

;Keep only the highest version number in cases where multiple versions exist
filelist_sclock=strmid(filelist,4,9)  ;extract the sclock from the file names
filelist_sclock_uniq=filelist_sclock(uniq(filelist_sclock,sort(filelist_sclock))) ;Make a list of unique sclock values
;xmess,'Checking for and removing old versions of the files...',/nowait,wid=wid2
if not(keyword_set(allversions)) then begin
    for i=0,n_elements(filelist_sclock_uniq)-1 do begin  ;loop through the list of unique values
       count=where(filelist_sclock eq filelist_sclock_uniq(i))  ;find the indices of versions of the same observation
       if n_elements(count) gt 1 then begin   ;if there are duplicates, then restore each one and find its version
           for j=0,n_elements(count)-1 do begin
               vnum=fix(strmid(filelist(count(j)),35,1))
              if j eq 0 then calversion=[vnum] else calversion=[calversion,vnum] ;if there are more than one version, extract the version number from the variable "matchedfilter" in the .sav files
           endfor
           bestversion=(where(calversion eq max(calversion)))[0]
           if n_elements(keep) eq 0 then keep=count(bestversion) else keep=[keep,count(bestversion)] ;keep the highest version number 
       endif else begin
          if n_elements(keep) eq 0 then keep=count else keep=[keep,count] ;if there are not duplicates, then just keep the single version
       endelse 
    
    endfor
    
    filelist=filelist(keep)  ;restrict the file list to the highest version numbers
    filelist_sols=filelist_sols(keep)  ;restrict the sol list the same way
    pathlist=pathlist(keep) ;restrict the path list the same way
    filelist_sclock=filelist_sclock(keep)
endif
cd,currentdir ;change back to the original working directory

out_data=hash('filelist',filelist,'sclock',filelist_sclock,'sols',filelist_sols,'pathlist',pathlist)
return,out_data

end