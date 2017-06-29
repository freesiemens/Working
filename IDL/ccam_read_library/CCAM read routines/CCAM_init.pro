pro CCAM_init

;  Initialize a few system variables
;  Should be adapted to each setup

;  Main ChemCam workplace

     defsysv, '!ChemCam', $
              'D:\Mes documents\IDLWorkspace\ChemCam\'

;  Location of ground data

     defsysv, '!ChemCam_gdata', $
              'C:\Big_data\CcamData\CCAM_ground\'

;  Location of suppor data

     defsysv, '!ChemCam_sdata', $
              'D:\Mes documents\IDLWorkspace\ChemCam\lib\Support data\'

;  Reference of S/C clock

     defsysv, '!CCAM_sclk_ref', julday(1,1,2000,11,58,54.816)

return
end
