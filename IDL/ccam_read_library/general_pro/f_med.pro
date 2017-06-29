function f_med,z,delt,THRES=thres,SIGN=sign,SILENT=silent

if(NOT KEYWORD_SET(sign)) then sign=0
 
b1=size(z)
if b1(0) eq 1 then z1=fltarr(b1(1)+2*delt) else z1=fltarr(b1(1)+2*delt,b1(2)+2*delt)
if b1(0) eq 1 then begin 
z1(delt+1:b1(1)+delt)=z
z1(0:delt-1)=reverse(z(0:delt-1))
z1(b1(1)+delt:*)=reverse(z(b1(1)-delt:*))
end else begin
z1(delt+1:b1(1)+delt,delt+1:b1(2)+delt)=z
z1(0:delt-1,*)=reverse(z(0:delt-1,*))
z1(b1(1)+delt:*,*)=reverse(z(b1(1)-delt:*,*))
z1(*,0:delt-1)=reverse(z(*,0:delt-1))
z1(*,b1(2)+delt:*)=reverse(z(*,b1(2)-delt:*))
end

z1m=z1
if(NOT KEYWORD_SET(THRES)) then thress=3 *stddev(z1-median(z1,delt)) else thress=thres*stddev(z1-median(z1,delt))

if(NOT KEYWORD_SET(silent)) then print,'Thres :',thress

ni=0
if(b1(0) eq 3) then ni=b1(3)-1
for i=0,ni do begin
   zi=z1(*,*,i)
;         i0=where(zi  eq 0)  
;         si0=size(i0) & if(si0(0) eq 1) then zi(i0)=1
   z1m=median(zi,delt)

   case sign of
      1: i1=where( zi-z1m  gt thress,n)
      -1: i1=where( z1m-z1  gt thress,n)
      else: i1=where( abs(z1m-z1)  gt thress,n)
   end

   if(n ne 0) then  zi(i1)=z1m(i1)
   z1(*,*,i)=zi
end  
if b1(0) eq 1 then z1=z1(delt+1:b1(1)+delt) else z1=z1(delt+1:b1(1)+delt,delt+1:b1(2)+delt)

return,z1
end
