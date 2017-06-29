function int_line,fp,fit_func
 
  int_line=0
  case fit_func of
     'Voigt' : begin
        npar=4 & np0=3
        cf=fltarr(npar+np0)
        cf(0:npar-1)=fp
        a=fp(1)-(fp(2)+fp(3))*10
        b=fp(1)+(fp(2)+fp(3))*10
  	if (b-a) gt 1e-2 then begin

        xf=findgen(1001)/1000.*(b-a)+a
        int_line=int_tabulated(xf,fvoigt(xf,cf))
        end
      end

     'Lorentz' :begin
        npar=3 & np0=3
        cf=fltarr(npar+np0)
        cf(0:npar-1)=fp
        a=fp(1)-fp(2)*10
        b=fp(1)+fp(2)*10
 ;       print,a,b,fp
;        if (b-a) gt 1e-2  then begin
 ;          xf=findgen(1001)/1000.*(b-a)+a
  ;         int_line=int_tabulated(xf,lorentz(xf,cf))
   ;     end
        int_line=!pi*fp(0)*fp(2)
     end

     'Gaussian' :begin
        npar=3 & np0=0
        cf=fltarr(npar+np0)
        cf(0:npar-1)=fp
        a=fp(1)-fp(2)*10
        b=fp(1)+fp(2)*10
   	if (b-a) gt 1e-2  then begin
           xf=findgen(1001)/1000.*(b-a)+a
           int_line=int_tabulated(xf,mgauss(xf,cf)) 
        end
     end


  end
  return,int_line

end
