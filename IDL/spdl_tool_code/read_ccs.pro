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
;-
FUNCTION read_ccs,fn,shot=shot,fn_good_index=fn_good_index,quiet=quiet

nf=n_elements(fn)

nft=0
n0=5
spp=ptrarr(nf,/allocate_heap)
fn_good=fn
if not(quiet) then progbar=Obj_New('cgProgressBar',/start,percent=0,title='Reading '+strtrim(nf,2)+' files for ICA')

if keyword_set(shot) then begin
    for i=0,nf-1 do begin
      restore,fn[i]
  
      nf=n_elements(UV[*,0]);nshots
      sp=transpose([[uv],[vis],[vnir]])
       *spp[nft]=sp
      nft+=1
      if not(quiet) then progbar->Update,float(i+1)/nf*100
    end

end else begin
   for i=0,nf-1 do begin
      restore,fn[i]
      suv=size(uv)
      if(suv(1) gt 1) then begin
         if n0 lt suv(1) then begin 
            sp0=mean(uv(n0:*,*),dim=1) 
            sp1=mean(vis(n0:*,*),dim=1)
            sp2=mean(vnir(n0:*,*),dim=1)
         end else begin
            sp0=muv
            sp1=mvis
            sp2=mvnir
         end
         
         *spp[nft]=[sp0,sp1,sp2]
         nft+=1
         if not(quiet) then progbar->Update,float(i+1)/nf*100
      end
      if (suv(1) le 1) then fn_good[i]=''
      
   end
   
   spp=spp(0:nft-1)
end
if not(quiet) then progbar->Destroy
fn_good_index=where(fn_good ne '')

gain=fltarr(6144)
restore,'gain_mars.sav'
gain(0:2047)=alluvdata[50:2097].mars
gain(2048:4095)=allvisdata[50:2097].mars
gain(4096:*)=allvnirdata[50:2097].mars

i0=where(gain ne 0, nbr0)
if nbr0 eq 0 then message,'Unexpected gain values (1).'
i1=where(gain eq 0, nbr1)
if nbr1 eq 0 then message,'Unexpected gain values (2).'

for i=0,nft-1 do begin 
   sp=*spp[i]
   ssp=size(sp)
   if ssp(0) eq 1 then ns=1 else ns=ssp(2)
   for n=0,ns-1 do sp(i0,n)=sp(i0,n)/gain(i0)
   for n=0,ns-1 do sp(i1,n)=0.

   *spp[i]=sp
end

if not keyword_set(shot) then begin
   spout=fltarr(n_elements(gain),nft)
   for n=0,nft-1 do spout(*,n)=*spp(n)
end else spout=spp



return,spout
end




