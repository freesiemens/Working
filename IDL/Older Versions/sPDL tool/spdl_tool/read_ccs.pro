;+
; NAME:
;        READ_CCS
;
; PURPOSE:
;        Read CCS SAV file and remove instrument response
;
; CALLING SEQUENCE:
;        Spectra = Read_CCS(File_List, SHOT=shot) 
;
; INPUTS:
;        File_List:List of CCS SAV file
;
; OPTIONAL INPUTS:
;        None
;
; KEYWORD PARAMETERS:
;        Shot: If set read the individual shots for shot to shot analysis
;        quiet: If set, then suppress pop-up progress bar
; OUTPUTS:
;       Spectra: Dimension [Nb of spectra, 8] if
;       mean spectra composition is computed; Pointer array of Nb of
;       spectra with dimension [Nb of shots, 8] if shot to shot
;       composition is computed.
;       fn_good_index = index of filenames considered "good"
;       spout_means = This keyword contains the mean spectra if "shots" is set
;                     This  allows the function to return single shot data as the
;                     primary output and the mean data at the same time, avoiding 
;                     the need to read the files twice if you want both.
;
;
; OPTIONAL OUTPUTS:
;       None
;
; RESTRICTIONS:
;       Need the instrument response function file 'gain_mars.sav'

; PROCEDURE:
;
; EXAMPLE:
;       fn=file_search('CL5*CCS*.SAV')
;       sp=read_ccs(fn,shot=shot)
;
;
; MODIFICATION HISTORY:
; O. Forni: May 2015
; R. Anderson: May 26, 2015 - Added output of index for "good" file names
; R. Anderson: June 2, 2015 - Added Progress Bar
; O. Forni: June 24, 2015 - Correction to return zeros where the response function is 0.
; O. Gasnault: June 27, 2015 - Add NBR0 and NBR1 to confirm that we have both
;    non-0 and 0 values in GAIN.
; R. Anderson: July 7, 2015 - Added 'quiet' option 
; R. Anderson: July 10, 2015 - Modified so that this function only needs to be called once, even if you want to get both mean and single-shot data
; R. Anderson: July 23, 2015 - Fixed bug introduced in last edit relating to observations with just one shot
; R. Anderson - August 26, 2016 - Added mask to first two pixels of UV to improve compatibility with lab data
;-
FUNCTION read_ccs,fn,shot=shot,fn_good_index=fn_good_index,quiet=quiet,spout_means=spout_means

nf=n_elements(fn)

nft=0
n0=5
spp=ptrarr(nf,/allocate_heap)
spp_means=ptrarr(nf,/allocate_heap)
fn_good_index=[]
if not(quiet) then progbar=Obj_New('cgProgressBar',/start,percent=0,title='Reading '+strtrim(nf,2)+' files for ICA')


for i=0,nf-1 do begin
   restore,fn[i]
   ;Mask the first two pixels of the UV range
   muv[0:1]=0
   uv[*,0:1]=0
   auv[0:1]=0
   
   
   suv=size(uv)
   
   if(suv(1) gt 1) then begin  ;Ensure there is more than one shot
      fn_good_index=[fn_good_index,i]
      if n0 lt suv(1) then begin 
         sp0=mean(uv(n0:*,*),dim=1) 
         sp1=mean(vis(n0:*,*),dim=1)
         sp2=mean(vnir(n0:*,*),dim=1)
      end else begin
         sp0=muv
         sp1=mvis
         sp2=mvnir
      endelse
         
      *spp_means[nft]=[sp0,sp1,sp2]
      
      if keyword_set(shot) then begin

         nf=n_elements(UV[*,0]);nshots
         sp=transpose([[uv],[vis],[vnir]])
         *spp[nft]=sp
      endif 
      nft+=1
      if not(quiet) then progbar->Update,float(i+1)/nf*100
   endif

endfor

spp_means=spp_means(0:nft-1)
spp=spp(0:nft-1)

if not(quiet) then progbar->Destroy

gain=fltarr(6144)
restore,'gain_mars.sav'
gain(0:2047)=alluvdata[50:2097].mars
gain(2048:4095)=allvisdata[50:2097].mars
gain(4096:*)=allvnirdata[50:2097].mars

i0=where(gain ne 0, nbr0)
if nbr0 eq 0 then message,'Unexpected gain values (1).'
i1=where(gain eq 0, nbr1)
if nbr1 eq 0 then message,'Unexpected gain values (2).'

spout_means=fltarr(n_elements(gain),nft)
for i=0,nft-1 do begin 
    if keyword_set(shot) then begin
       sp=*spp[i]
       ssp=size(sp) 
       if ssp(0) eq 1 then ns=1 else ns=ssp(2)
       for n=0,ns-1 do sp(i0,n)=sp(i0,n)/gain(i0)
       for n=0,ns-1 do sp(i1,n)=0.
       *spp[i]=sp
    endif
   
   sp_mean=*spp_means[i]
   ssp_mean=size(sp_mean)
   if ssp_mean(0) eq 1 then ns=1 else ns=ssp_mean(2)
   for n=0,ns-1 do sp_mean(i0,n)=sp_mean(i0,n)/gain(i0)
   for n=0,ns-1 do sp_mean(i1,n)=0.
   spout_means[*,i]=sp_mean
end


if not(keyword_set(shot)) then spout=spout_means else spout=spp


return,spout
end




