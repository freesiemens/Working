function chemcam_line_ident1,wl,spt,fsize,db_file,elt,tlb,SILENT=silent,THRES=thres,WMIN=wmin,WMAX=wmax,WRANGE=wrange


x=wl
xmn=min(x)
xmx=max(x)
if keyword_set(wmin) then xmn=wmin
if keyword_set(wmax) then xmx=wmax

il=where(x gt xmn and x lt xmx,nx)

  n=n_elements(spt(il))
;  dx=abs(mean(wl(1:*)-wl))
  dx=abs(wl(1:*)-wl)
  if not keyword_set(wrange) then wrange=1.2*dx
;  print,wrange
  sps={elt:' ',ex_st:' ',lwav:0.,wav:0.,relint:0.,intensity:0.,corr_gr:0.,corr_li:0.,group:1}
  x=wl(il)
  spt1=spt(il)
 
  if keyword_set(silent) then begin
     sp=read_nist_file(db_file,elt,exst=3,/silent,wmin=xmn,wmax=xmx)
  end else begin
     sp=read_nist_file(db_file,elt,exst=3,wmin=xmn,wmax=xmx)
  end
 ; if keyword_set(thres) then spt1= spt1 > thres -thres+1e-6

  sp=sp(sort(sp.wav))
  if fsize le 1 then fsize=1
  peak_id=chemcam_detect_peak(spt1,fsize,thres=thres)

  nlines=peak_id.nlines
  ii=peak_id.ind

  sl_sel=sps
  if nlines gt 0 then begin
     nli=0
     for nl=0,nlines-1 do begin
 ;       il=where(x(ii(nl)) ge sp.wav-wrange and x(ii(nl)) le sp.wav+wrange,nel)
        il=where(x(ii(nl)) ge sp.wav-wrange(ii(nl)) and x(ii(nl)) le sp.wav+wrange(ii(nl)),nel)
        if nel gt 0 then begin

           sp_sel=replicate(sps,nel)

           sp_sel(*).elt=sp(il).elt
           sp_sel(*).ex_st=sp(il).ex_st
           sp_sel(*).lwav=sp(il).wav
           sp_sel(*).wav=x(ii(nl))
           sp_sel(*).relint=sp(il).intensity
           sp_sel(*).intensity=spt1(ii(nl))
           nli=nli+nel
           end else begin
               sp_sel=sps
               sp_sel.elt='?'
               sp_sel.ex_st='?'
               sp_sel.lwav=x(ii(nl))
               sp_sel.wav=x(ii(nl))
               sp_sel.intensity=spt1(ii(nl))
               nli=nli+1
          end
          sl_sel=[sl_sel,sp_sel]

      end
 end
 if n_elements(sl_sel) gt  1 then begin

sl_sel=sl_sel(1:*)
i_name=sort(sl_sel.elt)
sl_sel=sl_sel(i_name)
p_name=uniq(sl_sel.elt)
;print,sl_sel(p_name).elt
for np=0,n_elements(p_name)-1 do begin
    el=where(sl_sel.elt eq sl_sel(p_name(np)).elt,nl)
;    chemcam_message,'Processing '+string(nl)+'
;    '+sl_sel(p_name(np)).elt+ ' lines',wait=2
    TVLCT,130, 255,  47, 20
    msg='Initialising '+sl_sel(p_name(np)).elt+ ' Processing'
    progressTimer = Obj_New("ShowProgress", tlb, Color=20,message=msg,xsize=200)
    printlog,'Processing '+string(nl)+' '+sl_sel(p_name(np)).elt+ ' lines'
    progressTimer->start
    wvl=sl_sel(el).lwav
    yf=Chemcam_fit(x,spt1,wvl,fp,pf,/lorentz)
    nf=n_elements(yf)
    cont=yf(nf-3:nf-1)
    sl_sel(el).corr_gr=correlate(yf,spt1)
    count = 0
    msg='Processing '+string(nl)+' '+sl_sel(p_name(np)).elt+ ' lines'
    progressTimer->Update, (count*100./nl),message_text=msg
    for nel=0,nl-1 do begin
        a_el=pf(3*nel:3*nel+2)
        a_el=[a_el,cont]
        i1=where(x ge a_el(1)-5*dx and x le a_el(1)+5*dx)
        x1=x(i1)
        y1=spt1(i1)
        yf1=lorentz(x1,a_el)
        sl_sel(el(nel)).corr_li=correlate(yf1,y1)
        count = count + 1
        progressTimer->Update, (count*100./nl )
        wait,0.05
    end
       progressTimer->destroy
 ;stop
end

end

;stop

 if n_elements(sl_sel) eq 1 then begin
    sl_sel(0).elt='No'
    printlog,'No identified lines'
    return,sl_sel(0)
end else begin
    is=sort(sl_sel.wav)
    sl_sel=sl_sel(is)
    return,sl_sel(1:*)
end


end




