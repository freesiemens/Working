function chemcam_detect_peak,sp,fsize,thres=thres

  kern=mex1(fsize/sqrt(2))
 
 spc=convol(sp,kern)
 ymx=stddev(spc)
 if keyword_set(thres) then begin 
     sm=where(abs(spc) lt thres*ymx)
     spc(sm)=0
 end
 n=n_elements(sp)
 ip=lonarr(n)

 for i=1,n-2 do if( spc(i) gt spc(i+1) and spc(i) gt spc(i-1)) then ip(i)=1

 ii=where(ip eq 1,nlines)

if nlines gt 0 then peak_id={nlines:nlines,ind:ii} else peak_id={nlines:0,ind:0}

return,peak_id
end
