function read_line_file,fn,norm

readcol,fn,el,ex,l1,l2,ri,ity,c1,c2,g,nrm,format=('a,a,f,f,f,f,f,f,i,i'),/silent
sps={elt:'',ex_st:'',lwav:0.,wav:0.,relint:0.,intensity:0.,corr_gr:0.,corr_li:0.,group:1}
if ~isa(el) then return,sps

nlines=n_elements(l1)

sp_sel=replicate(sps,nlines)

sp_sel(*).elt=el
sp_sel(*).ex_st=ex
sp_sel(*).lwav=l1
sp_sel(*).wav=l2
sp_sel(*).relint=ri
sp_sel(*).intensity=ity
;; sp_sel(*).ak=ak
;; sp_sel(*).ek=ek*1.24*1.e-4 ; convert cm-1 to eV
;; sp_sel(*).gk=gk
sp_sel(*).corr_gr=c1
sp_sel(*).corr_li=c2
sp_sel(*).group=g
norm=nrm[0]

return,sp_sel
end





