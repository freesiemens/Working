FUNCTION wvl_basis_order4,sp_type,x

  cvnir=[4.6181E+02, 2.2790E-01, -8.3751E-06, 1.1493E-09, -4.0917E-13]
  cvis =[2.6889E+02, 5.2987E-02, 4.9907E-07, -6.2579E-10, 4.3565E-14]
  cuv = [240.81117 ,0.053683237, -2.3627422e-06, -7.7319997e-13, 1.8810857e-016]
;; 2.4101E+02, 5.3219E-02, -1.1635E-05, 8.5616E-09, -1.9373E-12] 

  ;; CASE sp_type OF
  ;;    'UV':wave = 240.536 + 0.0536753*x - 2.35919E-6*x^2
  ;;    'VIS':wave= 381.783 + 0.0483610*x - 2.85796E-6*x^2
  ;;    'VNIR':wave=471.423 +  0.228638*x - 8.26295E-6*x^2
  ;;    ELSE:wave=x0
  ;; END
;; 4th Order Polynomials Basis 

  wave=x*0.
  CASE sp_type OF
     'UV': for i=0,4 do wave = wave + cuv[i]*x^i
     'VIS': for i=0,4 do wave = wave + cvis[i]*(x+2198)^i
     'VNIR': for i=0,4 do wave = wave + cvnir[i]*(x+50)^i
     ELSE:wave=wave -1.
  END

RETURN,wave
END
