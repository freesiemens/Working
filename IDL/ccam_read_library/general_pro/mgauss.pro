function mgauss, x, a, all=all

npar=3
np0=0
y0=x*0.
;y0=a[0] + a[1]*x + a[2]*x^2    ;continuum
nbcomp = fix(n_elements(a)/npar)-np0

all = fltarr(n_elements(x), nbcomp)

for i=0, nbcomp-1 do all(*,i) = 1.d*(a(npar*i+np0)*exp(-((x-a(npar*i+1+np0))/a(npar*i+2+np0))^2/2.))
if (nbcomp gt 1) then  y = y0+total(all, 2) else y = y0+all
if (n_elements(a)-nbcomp*3) gt 0 then y = y+a(npar*nbcomp)

return, y

end

