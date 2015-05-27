function data_sav,fn,n0,wl,name,fn0,sol,dst,tot=tot,std=std,irf=irf,mars=mars,shot=shot,rdr=rdr


nf=n_elements(fn)

nft=0
spp=ptrarr(nf,/allocate_heap)
name=strarr(nf)
dst=fltarr(nf)
fn0=strarr(nf)
sol=strarr(nf)

if keyword_set(shot) then begin
    for i=0,nf-1 do begin
      restore,fn[i]
      if keyword_set(rdr) then begin
         uv=dnuv
         vis=dnvis
         vnir=dnvnir
         muv=dnmuv
         mvis=dnmvis
         mvnir=dnmvnir
      end

      nf=nshots
      sp=transpose([[uv],[vis],[vnir]])
      dst[nft]=distt
      p0=strpos(fn(i),'.',/reverse_search)
      p1=strpos(fn(i),'CL5')
      name[nft]=strmid(fn[i],p1+37,p0-p1-37)
      fn0[nft]=fn[i]
      sol[nft]=strmid(fn[i],p1+29,5)
      *spp[nft]=sp
      nft+=1
    end

end else begin
   for i=0,nf-1 do begin
      restore,fn[i]
      if keyword_set(rdr) then begin
         uv=dnuv
         vis=dnvis
         vnir=dnvnir
         muv=dnmuv
         mvis=dnmvis
         mvnir=dnmvnir
      end
      
      suv=size(uv)
      if(suv(1) gt 1 and n0 lt suv(1)) then begin
         if isa(uv) then sp0=avg(uv(n0:*,*),0) else sp0=muv
         if isa(vis) then sp1=avg(vis(n0:*,*),0) else sp1=mvis
         if isa(vnir) then sp2=avg(vnir(n0:*,*),0) else sp2=mvnir
         if isa(distt) then  dst[nft]=distt
         *spp[nft]=[sp0,sp1,sp2]
         dst[nft]=distt
         p0=strpos(fn(i),'.',/reverse_search)
         p1=strpos(fn(i),'CL5')
         name[nft]=strmid(fn[i],p1+37,p0-p1-37)
         fn0[nft]=fn[i]
         sol[nft]=strmid(fn[i],p1+29,5)
         nft+=1
      end      
   end
   spp=spp(0:nft-1)
   dst=dst(0:nft-1)
   name=name(0:nft-1)
   fn0=fn0(0:nft-1)
   sol=sol(0:nft-1)
end

wl=[defuv,defvis,defvnir]
gainc=wl*0.
gainm=wl*0.


restore,'gain_mars.sav'
gainm(0:2047)=alluvdata[50:2097].mars
gainm(2048:4095)=allvisdata[50:2097].mars
gainm(4096:*)=allvnirdata[50:2097].mars

restore,'gain_info.sav'
gainc(0:2047)=alluvdata[50:2097].clean
gainc(2048:4095)=allvisdata[50:2097].clean
gainc(4096:*)=allvnirdata[50:2097].clean

if keyword_set(mars) then gain=gainm else gain=gainc

i0=where(gain ne 0)

ap=(dst/(!pi*54.2*.100))^2

if keyword_set(rdr) then begin
   dx=deriv(defuv)
   dy=deriv(defvis)
   dz=deriv(defvnir)
   for i=0,nft-1 do begin
      sp=*spp[i]
      ssp=size(sp)
      if ssp(0) eq 1 then ns=1 else ns=ssp(2)
      for n=0,ns-1 do begin
         sp(0:2047,n)=sp(0:2047,n)/dx*ap(i)
         sp(2048:4095,n)=sp(2048:4095,n)/dy*ap(i)
         sp(4096:*,n)=sp(4096:*,n)/dz*ap(i)
      end
      *spp[i]=sp
      gain(*)=1
end
end

for i=0,nft-1 do begin 
   sp=*spp[i]
   ssp=size(sp)
   if ssp(0) eq 1 then ns=1 else ns=ssp(2)
   if keyword_set(irf) then for n=0,ns-1 do sp(i0,n)=sp(i0,n)/gain(i0)


   if keyword_set(tot) then begin
      case tot of
         1: begin
            for n=0,ns-1 do begin      
               sp(*,n)=sp(*,n)/total(sp(*,n))
            end
         end
         3: begin
            for n=0,ns-1 do begin      
               sp(0:2047,n)=sp(0:2047,n)/total(sp(0:2047,n))
               sp(2048:4095,n)=sp(2048:4095,n)/total(sp(2048:4095,n))
               sp(4096:*,n)=sp(4096:*,n)/total(sp(4096:*,n))
            end
         end
      end
   end

   if keyword_set(std) then begin
      case std of
    1: begin
            for n=0,ns-1 do begin      
               sp(*,n)=sp(*,n)/stddev(sp(*,n))
            end
         end
         3: begin
            for n=0,ns-1 do begin      
               sp(0:2047,n)=sp(0:2047,n)/stddev(sp(0:2047,n))
               sp(2048:4095,n)=sp(2048:4095,n)/stddev(sp(2048:4095,n))
               sp(4096:*,n)=sp(4096:*,n)/stddev(sp(4096:*,n))
            end
         end
      end
   end
   *spp[i]=sp
end

if not keyword_set(shot) then begin
   spout=fltarr(n_elements(wl),nft)
   for n=0,nft-1 do spout(*,n)=*spp(n)
end else spout=spp

;;stop

return,spout
end




