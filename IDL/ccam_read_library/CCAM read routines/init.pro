pro init

;  Initialize a few system variables
;  Should be adapted to each setup

     defsysv, '!ChemCam_gdata', $
              'data\'

;  Location of support data
;  this is where the soh conversions reside
;  and also where database save sets reside

     defsysv, '!ChemCam_sdata', $
              '.\'

;  Reference of S/C clock

     defsysv, '!CCAM_sclk_ref', julday(1,1,2000,11,58,54.816)

return
end
