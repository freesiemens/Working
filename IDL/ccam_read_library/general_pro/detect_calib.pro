function detect_calib,fn

fn_type=detect_sp_type(fn)
CASE fn_type OF
'UV' : BEGIN
   p0=strpos(fn,'UV')
   p1=p0+2
   END
'VIS' : BEGIN
   p0=strpos(fn,'VIS')
   p1=p0+3
   END
'VNIR' : BEGIN
   p0=strpos(fn,'VNIR')
   p1=p0+4
END
END
fn_uv=strmid(fn,0,p0)+'UV'+strmid(fn,p1,strlen(fn)-p1)
fn_vis=strmid(fn,0,p0)+'VIS'+strmid(fn,p1,strlen(fn)-p1)
fn_vnir=strmid(fn,0,p0)+'VNIR'+strmid(fn,p1,strlen(fn)-p1)

fn_uv_clb=file_search(fn_uv+'.clb')
fn_vis_clb=file_search(fn_vis+'.clb')
fn_vnir_clb=file_search(fn_vnir+'.clb')

clb_fmt={file_clb:strarr(4),s_clb:0b}

IF fn_uv_clb NE '' then clb_fmt.s_clb=1b
IF fn_vis_clb NE '' then clb_fmt.s_clb += ishft(1b,1) 
IF fn_vnir_clb NE '' then clb_fmt.s_clb += ishft(1b,2)
clb_fmt.file_clb[0]=strmid(fn,0,p0)+'ALL'+strmid(fn,p1,strlen(fn)-p1)+'.clb'
clb_fmt.file_clb[1]=fn_uv_clb
clb_fmt.file_clb[2]=fn_vis_clb
clb_fmt.file_clb[3]=fn_vnir_clb
;stop
RETURN,clb_fmt
END


