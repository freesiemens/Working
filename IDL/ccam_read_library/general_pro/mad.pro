function fmad,d

n=n_elements(d)
md=d
med=median(d)

for i=0,n-1 do md(i)=abs(d(i)-med)
mad=median(md)

md=md/(1.48*mad)

im=where(md lt 3,np)

d1=d(im)
return,d1
end
