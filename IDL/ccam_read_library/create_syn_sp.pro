function create_syn_sp,x,elt,rel_int=rel_int,exst=exst

dx=mean(shift(x(1:*),-1)-x)   ; resolution

l_el=read_nist_file(elt,exst=exst,/silent,rel_int=rel_int)
a_el=create_param_list(l_el.intensity,l_el.wav,fltarr(n_elements(l_el))+dx*2.,/lorentz)
y_el=lorentz(x,a_el)


return,y_el
end

