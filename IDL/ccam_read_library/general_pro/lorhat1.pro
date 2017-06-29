Function lorhat1,a

n=round(a*4.5)
x=(findgen(2*n+1)-n)^2.
f=(a*a-3.*x)/(a*a+x)^3*a*a*2
;normalisation.
f=f/9.*2.*sqrt(3)*a
return,f

end
