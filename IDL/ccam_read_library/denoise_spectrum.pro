function denoise_spectrum, sp_in,SIG=sig,NITER=niter

s=n_elements(sp_in)

lv=fix(alog(s)/alog(2))-1
;if lv gt 5 then lv=5

ws=watrous(sp_in,lv)
ws1=ws


if (not keyword_set(SIG)) then sig=3.
if (not keyword_set(niter)) then niter=4

for i=0,lv-2 do begin 
   b=get_noise(ws(*,i),niter=niter)
   tmp=ws(*,i)
   ou=where(abs(tmp) lt sig*b,nou)
   if nou gt 0 then tmp(ou)=0
   ws1(*,i)=tmp
end

return,total(ws1,2)

end


