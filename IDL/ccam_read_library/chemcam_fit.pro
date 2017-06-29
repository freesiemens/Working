function chemcam_fit, x,y,l,pf,fp,voigt=voigt,lorentz=lorentz,moffat=moffat,wn=wn,maxit=maxit,wmin=wmin,wmax=wmax,fixwav=fixwav

;nel=n_elements(x)

y1=y

npar=3 & np0 =0
myfunct='gauss_mpfit'

if keyword_set(lorentz) then begin
   np0=3
   myfunct='lorentz_mpfit'
end

if keyword_set(voigt)  then begin
   npar=4
   np0=3
   myfunct='voigt_mpfit'
end

if keyword_set(moffat)  then begin
   npar=4
   myfunct='moffat_mpfit'
end

xmn=min(x)
xmx=max(x)
if keyword_set(wmin) then xmn=wmin
if keyword_set(wmax) then xmx=wmax
il=where(x gt xmn and x lt xmx,nx)
;dx=mean(x(il(1:nx-1))-x(il(0:nx-2)))
dx=x(il(1:nx-1))-x(il(0:nx-2))
;print,dx

;print,xmn,xmx
if keyword_set(wn) then begin
	l=reverse(10000./l)
end


i_s=where(l gt xmn and l lt xmx,nl)

;print,nl

nbcomp=nl
np=n_elements(x(il))
ncoef=npar*(nbcomp)+np0

if (np lt ncoef) then begin
    print,'Pas assez de points pour realiser le fit'
    return,-1
end

p0=fltarr(ncoef)
if (keyword_set (voigt) or keyword_set (lorentz)) then begin
;;if (keyword_set (voigt)  then begin
   p0(ncoef-3)=0
   p0(ncoef-2)=0
   p0(ncoef-1)=0.
end



for j=0,nl-1 do begin
        ix=where(l(i_s(j)) ge x-dx and l(i_s(j)) le x+dx)
        mx=ix(0)
	m=where(x ge l(i_s(j)))
	p0(j*npar)=y1(m(0))
	p0(j*npar+1)=l(i_s(j))
	p0(j*npar+2)=dx(mx)*2
	if keyword_set (voigt) then p0(j*npar+3)=dx(mx)*2
	if keyword_set (moffat) then p0(j*npar+3)=1.
end

fp=p0

 errval=x(il)*0.+sqrt(abs(y(il)))
inerr=where(errval gt 0,nerr)
 ierr=where(errval eq 0,nerr)
if nerr gt 0 then errval(ierr)=1e-6
errval=1./errval

parinfo = replicate({value:0.D, fixed:0, limited:[0,0],limits:[0.D,0.]},ncoef)

ifx=indgen(nbcomp)*npar
; parinfo(ifx+1).fixed=1
parinfo(ifx).limited(0)=1
parinfo(ifx).limits(0)=0.
if keyword_set(fixwav) then parinfo(ifx+1).fixed=1 else begin
    parinfo(ifx+1).limited(0)=1
    parinfo(ifx+1).limits(0)=fp(ifx+1)-dx(mx)
    parinfo(ifx+1).limited(1)=1
    parinfo(ifx+1).limits(1)=fp(ifx+1)+dx(mx)
end

parinfo(ifx+2).limited(0)=1
parinfo(ifx+2).limits(0)=dx(mx)*.5
parinfo(ifx+2).limited(1)=1
parinfo(ifx+2).limits(1)=5*dx(mx)

if keyword_set (voigt) then begin
parinfo(ifx+3).limited(0)=1
parinfo(ifx+3).limits(0)=dx(mx)*.5
parinfo(ifx+3).limited(1)=1
parinfo(ifx+3).limits(1)=dx(mx)*5.
;parinfo(nbcomp*npar).fixed=1
;parinfo(nbcomp*npar+1).fixed=1
end

if keyword_set (moffat) then begin
parinfo(ifx+3).limited(0)=1
parinfo(ifx+3).limits(0)=0.
end

;;functargs = {XVAL:x(il), YVAL:y1(il), ERRVAL:errval}
functargs = {XVAL:x(il), YVAL:y1(il)}

pf=mpfit(myfunct, p0,parinfo=parinfo,functargs=functargs,bestnorm=norm,status=st, niter=nit,maxiter=maxit, /quiet)

printlog,'Stautus = '+ string(st,format='(I3)')
;print,pf
;;stop
return,call_function(myfunct,pf,xval=x,/model_out)

end

