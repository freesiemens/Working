function watrous,z,scale,kernel=kernel

z=float(z)
s=size(z)

If( not keyword_set(kernel)) then kernel=[1.,4.,6.,4.,1.]/16.

sk=size(kernel)

case 1 of
s(0) eq 1: begin
    n=s(1)

    w=fltarr(s(1)*3,scale)
    w(0:n-1,0)=reverse(z(0:n-1))
    w(n:s(1)+n-1,0)=z
    w(s(1)+n:*,0)=reverse(z(s(1)-n:*))
  for i=0,scale-2 do begin
        k1=fltarr((sk(1)-1)*2.^i+1)
        i1=indgen(sk(1))*2.^i
        k1(i1)=kernel
        tsmooth=convolve(w(*,i),k1)
;        tsmooth=convol(w(*,i),k1,/edge_wrap)
        w(*,i)=w(*,i)-tsmooth
        w(*,i+1)=tsmooth
    end
   w=w(n:s(1)+n-1,*)
end
s(0) eq 2: begin
    w=fltarr(s(1),s(2),scale)
    w(*,*,0)=z
    for i=0,scale-2 do begin
        k1=fltarr((sk(1)-1)*2.^i+1)
        i1=indgen(sk(1))*2.^i
        k1(i1)=kernel
        k2=k1#k1
        tsmooth=convolve(w(*,*,i),k2)
;        tsmooth=convol(w(*,*,i),k2,/edge_wrap)
        w(*,*,i)=w(*,*,i)-tsmooth
        w(*,*,i+1)=tsmooth
    end
end
s(0) eq 3: begin
    w=fltarr(s(1),s(2),s(3),scale)
    for l=0,s(3)-1 do begin
        w(*,*,l,0)=z(*,*,l)
        for i=0,scale-2 do begin
            k1=fltarr((sk(1)-1)*2.^i+1)
            i1=indgen(sk(1))*2.^i
            k1(i1)=kernel
            k2=k1#k1
            tsmooth=convolve(w(*,*,l,i),k2)
            ;tsmooth=convol(w(*,*,l,i),k2,/edge_wrap)
            w(*,*,l,i)=w(*,*,l,i)-tsmooth
            w(*,*,l,i+1)=tsmooth
        end
    end
end
else: begin
    print,'Erreur de dimensions'
    return,-1
end
endcase


return,w
end


