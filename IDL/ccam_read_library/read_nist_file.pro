function read_nist_file,DB_file,el,MED=med,WMIN=wmin,WMAX=wmax,REL_INT=rel_int,EXST=exst,T_EK=t_ek,SILENT=silent

;nist_dir='$HOME/chemcam/Nist/'
;nist_dir='Nist/'
el_list=['Al','As','Ba','C','Ca','Cl','Cr','Fe','H','K','Li','Mg','Mn','N','Na','Ni','O','P','Rb','S','Si','Sr','Ti','V','All']
q_list=['AA','A','B+','B','C+','C','D+','D',' ']
ex_list=['I','II','III','IV','V','VI']

;sp={elt:' ',ex_st:' ',wav:0.,intensity:0.,accuracy:-1}
sp={elt:'',ex_st:' ',wav:0.,intensity:0.,accuracy:0,ak:0.}

p=where(strmatch (el_list,el) eq 1)
if p eq -1 then begin
    print,'Element not found'
    return,sp
end

readcol,DB_file,elt,ex,wl,ri,format=('a,a,f,f'),/silent
;readcol,fn,elt,ex,wl,ri,ak,acc,format=('a,a,f,f,f,a'),/silent

if ~isa(elt) then return,sp

if el ne 'All' then begin
   is=where(elt eq el)
   elt=elt(is)
   ex=ex(is)
   wl=wl(is)
   ri=ri(is)
end

is=sort(wl)
elt=elt(is)
ex=ex(is)
wl=wl(is)
ri=ri(is)

nlines=n_elements(wl)
;elt=elt(nlines)
;ex=ex(nlines)
;wl=wl(nlines)
;ri=ri(nlines)
;ak=ak(nl)
;acc=acc(nl)
sp_nist=replicate(sp,nlines)

for nl=0,nlines-1 do begin
   sp_nist(nl).elt=strcompress(elt(nl),/remove_all)
   sp_nist(nl).ex_st=strcompress(ex(nl),/remove_all)

    sp_nist(nl).wav=wl(nl)
    sp_nist(nl).intensity=ri(nl)

 ;   p=where(strmatch(q_list,strcompress(acc(nl),/remove_all)) eq 1)
  ;  sp_nist(nl).accuracy=p
;
 ;   sp_nist(nl).ak=ak(nl)

end
;readcol,fn,el1,ex,wl,ri,acc,format=('a,a,f,f,x,a'),/silent


imin=0 & imax=nlines-1
if keyword_set(wmin) then begin
    w=where(wl ge wmin,n)
    if n gt 0 then imin=w(0) else imin=nlines
end

if keyword_set(wmax) then begin
    w=where(wl le wmax,n)
    if n gt 0 then imax=w(n-1) else imax=-1
end

if(imin gt imax) then begin
   if not keyword_set(silent) then  print,'No lines in the inteval for element '+el
   sp_sel=sp_nist(0)
    sp_sel(0).elt='No'
    sp_sel(0).intensity=-1.
    return,sp_sel
end


sp_sel=sp_nist(imin:imax)



if keyword_set(rel_int) then begin
    r=where(sp_sel.intensity ge rel_int,n)
    if n eq 0 then r=lindgen(n_elements(sp_sel))

    sp_sel=sp_sel(r)
end

if keyword_set(t_ek) then begin
    e=where(sp_sel.ek le t_ek,n)
    if n eq 0 then e=lindgen(n_elements(sp_sel))

    sp_sel=sp_sel(e)
end

 if keyword_set(exst) then begin
     ex_ind=fltarr(n_elements(sp_sel))
     for nsl=0,n_elements(sp_sel)-1 do begin
         p=where(strmatch(ex_list,sp_sel(nsl).ex_st) eq 1)
         ex_ind(nsl)=p+1
     end

    q=where(ex_ind lt exst,n)
    if n eq 0 then q=lindgen(n_elements(sp_sel))
    sp_sel=sp_sel(q)
 end

;; if keyword_set(prec)  then begin
;;     p=where(strmatch( q_list,strcompress(prec,/remove_all)) eq 1)
;;     if p eq -1 then p=0
;;     q=where(sp_sel.accuracy le p(0) and sp_sel.accuracy ge 0, n)
;;     if n eq 0 then q=lindgen(n_elements(sp_sel))
;;     sp_sel=sp_sel(q)
;; end

return,sp_sel(sort(sp_sel.wav))

end
