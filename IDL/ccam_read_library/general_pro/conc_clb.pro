PRO conc_clb,fn_all_clb

h1=fn_all_clb(n_elements(fn_all_clb)-1)
  FOR nall=0,n_elements(fn_all_clb)-2 DO BEGIN
     openw,1,fn_all_clb(nall)
     p0=strpos(fn_all_clb(nall),h1)
     fn_uv=strmid(fn_all_clb(nall)0,p0)+'UV_'+h1
     readcol,fn_uv,wl,sp,/silent
     for il=0,n_elements(wl)-1 DO printf,1,wl(il),sp(il),FORMAT='(2F10.3)'
     fn_vis=strmid(fn_all_clb(nall)0,p0)+'VIS_'+h1
     readcol,fn_vis,wl,sp,/silent
     for il=0,n_elements(wl)-1 DO printf,1,wl(il),sp(il),FORMAT='(2F10.3)'
     fn_vis=strmid(fn_all_clb(nall)0,p0)+'VNIR_'+h1
     readcol,fn_vnir,wl,sp,/silent
     for il=0,n_elements(wl)-1 DO printf,1,wl(il),sp(il),FORMAT='(2F10.3)'
     close,1
  END 
