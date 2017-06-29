function moffat, x, a ,all=all

np0=0
npar=4
;y0=a[0] + a[1]*x + a[2]*x^2    ;continuum
nbcomp = fix(n_elements(a)/npar)-np0

all = fltarr(n_elements(x), nbcomp)

for i=0, nbcomp-1 do all(*,i) = 1.d*a(npar*i+np0)/(((x-a(npar*i+1+np0))/a(npar*i+2+np0))^2+1.)^a(npar*i+3+np0)
if (nbcomp gt 1) then  y = total(all, 2) else y = all

return, y

end

