function fmad,d,mad

n=n_elements(d)
md=d
med=median(d)

for i=0,n-1 do md(i)=abs(d(i)-med)
mad=median(md)

md=md/(1.48*mad)

return,md
end

function pdf_mad,d,md,thres

im=where(md le thres)

return,d(im)
end
