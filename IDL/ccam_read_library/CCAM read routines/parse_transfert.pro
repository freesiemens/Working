

pro parse_transfert, $
         itf, $  ; input
         ectf, dpf, crf, nss, bss, cwlh, $ ; output
         amph, osch, RMIS,  RMIok, specok, $ ; output
         lvps, mastok, libshv, libsrs, cwlnr, stf, cmdretry ; output

; get Error Control Type Flag for later use
       ectf=ishft(itf[0],-6) AND 3
; get datapresent flag 1=data 0=nodata
       dpf=ishft(itf[0],-5) AND 1
; get cmdreply flag 1=cmdreply 0=dataproduct
       crf=ishft(itf[0],-4) AND 1
; get notSafe status 0=safe 1=Bu doesn't know 
; that MU mortors are in sun-safe position
       nss=ishft(itf[0],-3) AND 1
; get BootSource status 0= INIT0 1=INIT1
       bss=ishft(itf[0],-2) AND 1
; get CommSide status 0=RCE A or none 1= RCE B
       css=ishft(itf[0],-1) AND 1
; get CWL HEAter not on status 0= on 1= not on
       cwlh=ishft(itf[0],0) AND 1
; get AMP heater not on status 0=on 1=noton
       amph=ishft(itf[1],-7) AND 1
; get OSC heater not on status 0= on 1=not on
       osch=ishft(itf[1],-6) AND 1
; get RMI not on status 0=on 1= not on
       RMIS=ishft(itf[1],-5) AND 1
; get RMI data not ok status 0=ok 1= not ok
       RMIok=ishft(itf[1],-4) AND 1
; get spectra data not ok status 0=ok 1= not ok
       specok=ishft(itf[1],-3) AND 1
; get lVPS not on status 0=on 1=off
       lvps=ishft(itf[1],-2) AND 1
; get mast not ok statys 0= ok 1=not ok
       mastok=ishft(itf[1],-1) AND 1
; get libs hv not on status 0=on 1 =not on
       libshv=ishft(itf[1],0) AND 1
; get libs not ready status 0=ready 1=notready
       libsrs=ishft(itf[2],-7) AND 1
; get CWL not ready status 0=ready 1=not ready
       cwlnr=ishft(itf[2],-6) AND 1
; get self test failed should be 0 not used
       stf=ishft(itf[2],-5) AND 1
; get cmdretry status
;  0=reserved
;  1=first time command
;  2=retry command (cmd reply frame)
; 18= retry command (sci frame)
       cmdretry=ishft(itf[2],0) AND 31

return
end
