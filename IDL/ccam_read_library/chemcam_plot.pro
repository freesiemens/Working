pro chemcam_plot,x,y,sp,yf=yf,ps=ps,wn=wn,wmin=wmin,wmax=wmax,thres=thres,title=title


xmn=min(x)
xmx=max(x)
if keyword_set(wmin) then xmn=wmin
if keyword_set(wmax) then xmx=wmax

il=where(x gt xmn and x lt xmx,nx)

; print,xmn,xmx
sp1=sp(sort(sp.wav))

if keyword_set(thres) then begin
    it=where(sp1.intensity ge thres,nt)
    if nt gt 0 then sp1=sp1(it) else return
end
l=sp1.lwav

if keyword_set(wn) then begin
	l=reverse(10000./l)
end

dx=min(abs(x-shift(x,1)))
dx0=0
i_s=where(l gt xmn and l lt xmx,nl)

; coul8
; A = FINDGEN(17) * (!PI*2/16.)
;  Define the symbol to be a unit circle with 16 points,
;  and set the filled flag:
; USERSYM, COS(A), SIN(A), /FILL
; plot,x,y1,psym=8,symsize=1.5

if nl gt 0  then begin

ymx2= max(y(il))
if keyword_set(fit) then ymx1=max(fit(il)) else ymx1=ymx2
ymx=max( ymx1,ymx2)

dy=ymx/25.
ds=ymx/20.

if keyword_set(ps) then begin
   old_dev=!d.name
    set_plot,'ps'
    
    file='./'+ps+'.ps'
    if keyword_set(fit) then file='./'+ps+'_fit.ps'
    device,file=file,/color,bits=8
    !p.font=0 
    device,/helvetica,isolatin1=0
end else DEVICE, SET_FONT='helvetica', /TT_FONT

if keyword_set(title) then title=title else title=''
plot,x(il),y(il),/xs,yr=[0,ymx+2*dy],title=title,xtitle='Wavelength (nm)',ytitle='Intensity'

i=0
;il=where(x gt l(i_s(i))-2*dx and x lt  l(i_s(i))+2*dx)
yl=sp1(i_s(i)).intensity
ex_st=sp1(i_s(i)).ex_st
if sp1(i_s(i)).elt eq '?' then begin 
    dx0=2*dx
    ex_st=' '
end

xyouts,sp1(i_s(i)).lwav+dx0,yl+dy,sp1(i_s(i)).elt+' '+ex_st,charsize=1.3,align=.5

for i=1,nl-1 do begin
    yl=sp1(i_s(i)).intensity
    ex_st=sp1(i_s(i)).ex_st
    if sp1(i_s(i)).elt eq '?' then begin
        dx0=2*dx
        ex_st=' '
    end
    dl=abs(sp1(i_s(i)).wav - sp1(i_s(i-1)).wav)

    if (dl lt 4*dx) then dy=dy+ds else dy=ymx/25.
    xyouts,sp1(i_s(i)).lwav+dx0,yl+dy,sp1(i_s(i)).elt+' '+ex_st,charsize=1.3,align=.5
end

if keyword_set(yf) then begin 
   loadct,3,/silent
   oplot,x,yf,col=200
   loadct,0,/silent
end

if keyword_set(ps) then begin
   device,/close

    set_plot,old_dev
end

end

end
