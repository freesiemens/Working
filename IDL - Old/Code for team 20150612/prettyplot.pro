pro prettyplot,x,y,psym=psym,color=color,thick=thick,xrange=xrange,yrange=yrange,xtitle=xtitle,ytitle=ytitle,charsize=charsize,$
xthick=xthick,ythick=ythick,oplot=oplot,symsize=symsize,xsize=xsize,ysize=ysize,title=title,xlog=xlog,ylog=ylog,nofill=nofill,ctable=ctable,linestyle=linestyle,winnum=winnum,pixmap=pixmap


;create the axes
if not(keyword_set(xrange)) then xrange=[min(x),max(x)]
if not(keyword_set(yrange)) then yrange=[min(y),max(y)]
if not(keyword_set(xthick)) then xthick=1
if not(keyword_set(ythick)) then ythick=1
if not(keyword_set(symsize)) then symsize=1
if not(keyword_Set(color)) then color=0
if not(keyword_set(xsize)) then xsize=2000
if not(keyword_set(ysize)) then ysize=2000
if not(keyword_set(title)) then title=''
if not(keyword_set(xlog)) then xlog=0
if not(keyword_set(ylog)) then ylog=0
if not(keyword_set(nofill)) then nofill=0
if not(keyword_set(psym)) then psym=0
if not(keyword_set(thick)) then thick=2
if not(keyword_set(pixmap)) then pixmap=0

if not keyword_set(oplot) then begin
  device,decomposed=0,set_font='Helvetica',/tt_font
  loadct,0
  if n_elements(winnum) gt 0 then window,winnum,xsize=xsize,ysize=ysize,pixmap=pixmap else window,/free,xsize=xsize,ysize=ysize,pixmap=pixmap
  
  
  if n_elements(linestyle) eq 0 then begin
    plot,[1,1],[1,1],psym=3,background=255,color=0,xtitle=xtitle,ytitle=ytitle,xrange=xrange,yrange=yrange,font=1,charsize=charsize,xthick=xthick,ythick=ythick,title=title,xstyle=1,ystyle=1,xlog=xlog,ylog=ylog,thick=thick 
  endif else begin
    plot,[1,1],[1,1],linestyle=linestyle,background=255,color=0,xtitle=xtitle,ytitle=ytitle,xrange=xrange,yrange=yrange,font=1,charsize=charsize,xthick=xthick,ythick=ythick,title=title,xstyle=1,ystyle=1,xlog=xlog,ylog=ylog,thick=thick
  endelse

endif
print,'Color = '+strtrim(color,2)
if n_elements(winnum) gt 0 then wset,winnum

if n_elements(ctable) eq 0 then loadct,13 else loadct,ctable
if n_elements(linestyle) eq 0 then begin
   for j=0,n_elements(x)-1 do begin
     if nofill ne 1 then plotsym,psym,symsize,/fill,color=color else plotsym,psym,symsize,color=color
     oplot,x([j,j]),y([j,j]),psym=8
     if thick gt 0 then begin
       plotsym,psym,symsize,color=0,thick=thick
       oplot,x([j,j]),y([j,j]),psym=8
     endif
   endfor
endif
if n_elements(linestyle) ne 0 then oplot,x,y,color=color,linestyle=linestyle,thick=thick

end