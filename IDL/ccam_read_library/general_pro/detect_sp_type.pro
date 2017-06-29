function detect_sp_type,filename

p=strarr(4)
p(0)=strpos(filename,'UV')
p(1)=strpos(filename,'VIS')
p(2)=strpos(filename,'VNIR')
p(3)=strpos(filename,'ALL')

ip=where(p ne -1,np)

IF np GT 0 then begin
   CASE ip of
      0:sp_type='UV'
      1:sp_type='VIS'
      2:sp_type='VNIR'
      3:sp_type='ALL'
      ELSE:sp_type='UNKNOWN'
   END
END else sp_type='UNKNOWN'

RETURN,sp_type

END
