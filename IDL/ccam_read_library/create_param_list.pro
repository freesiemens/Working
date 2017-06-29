function create_param_list,amp,pos,sig,GAUSS=gauss,LORENTZ=lorentz,VOIGT=voigt,MOFFAT=moffat

npar=3 & np0=2
if keyword_set(voigt) then npar=4
if keyword_set(gauss) then np0=0
ncomp=n_elements(amp)

a=fltarr(npar*ncomp+np0)

for i=0,ncomp-1 do begin
    a(npar*i)=amp(i)
    a(npar*i+1)=pos(i)
    a(npar*i+2)=sig(i)
    if keyword_set(voigt) then a(npar*i+3)=sig(i)
end

return,a

end



