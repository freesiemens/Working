;+
; NAME:
;       CCAM_READ_LIBS_EDR
;
; PURPOSE:
;       Read ChemCam LIBS spectra EDR Built many HK outputs
;
; EXPLANATION:
;       Read an LIBS files built by JPL. Copy the input command. Build
;       structures for HK data: instrument parameters, Rover PRTs, LIBS
;       parameters, Distance to target, label information. On request, 
;       tell us a bit on what has been read.
;
; CALLING SEQUENCE:
;       spectra = CCAM_READ_LIBS_EDR(libsfile [,LABEL_info = ]  $
;               [,thespectra][, cmd = ][, time = ][, /verbose]$
;               [, HK_prt = ][, HK_inst = ][,HK_libs = ][, HK_dist = ])
;
; INPUTS:
;       libsfile    -  LIBS filename, including path
;
; OPTIONAL INPUTS:
;
; OPTIONAL KEYWORD INPUTS:
;       none
;
; OUTPUTS:
;       return a [3,nb_of_spectra,2048] spectrum
;
; OPTIONAL OUTPUTS:
;       thespectra   -  [3, nb_of_spectra,2148], that includes masked pixels.
;       TIME         -  Read and parse S/C clock into human readable
;                       day/hr, etc...(structure)
;       CMD          -  Return parameters/arguments of the command.
;                       This is a structure
;       HK_PRT       -  Return the instrument PRTs which are read by
;                       the rover (structure)
;       HK_INST      -  Return structure for the Housekeeping. Make
;                       the distinction for HK taken before/after (structure)
;       HK_DIST      -  Return current motor position and focus data
;                       when they exist(structure)
;       HK_LIBS      -  Return critical LIBS parameters (structure)
;       FILE         -  Return the file name, size
; OPERATIONAL NOTES:
;
;       Assume that the file soh_conversion.txt exists
;       somewhere. Provide the path or assume it is under !ChemCam_gdata
;
;       Assume that the !CCAM_convfile is defined 
;       will need to distinguish between EM and FM  for now EM
;
; PROCEDURES CALLED:
;       CCAM_READ_LIBS()
;       PARSE_TRANSFERT(), LOAD_CONVERSION(), CCAM_MOTOR()
;
;       MYSTRING(), YMD2DN(), DATE_CONV()
;
; REVISION HISTORY:
;       D. DeLapp   January 2012
;-

function ccam_read_libs_edr,filename,LABEL_info = LABEL_info,thespectra, $
             time = thetime, cmd = cmd, file = thefile, $
             HK_prt = HK_prt, HK_inst = HK_inst, $
             HK_libs = HK_libs, HK_dist = HK_dist, $
             verbose = verbose
;LABEL_info line one
LABEL_info="PDS_VERSION_ID                   = PDS3"
sol=99999
partial=0
line=""
;filename='data/CL0_404858033EDR_F0010044CCAM00030M1.DAT'
openr,ilun,filename,/get_lun,/swap_if_little
readf,ilun,line
readf,ilun,line
while (strpos(line,"OBJECT ") lt 0) do begin
   LABEL_info=[LABEL_info,line]
   readf,ilun,line
; skip first line in EDR
; replace with above line
;then read until first "OBJECT "
if strpos(line,'RECORD_BYTES') ge 0 then begin
        eloc=strpos(line,'=')
        rsize=fix(strmid(line,eloc+2,strlen(line)-(eloc+2)))
endif
if strpos(line,'LABEL_RECORDS') ge 0 then begin
    eloc=strpos(line,'=')
    nlrec=fix(strmid(line,eloc+2,strlen(line)-(eloc+2)))
endif
if strpos(line,'Sol-') ge 0 then begin
     eloc=strpos(line,'Sol-')+4
     sol=fix(strmid(line,eloc,5))
endif
if strpos(line,'pdat') ge 0 then begin
    partial=1
endif
; versions of EDR differ
; need to check FSW id
if strpos(line,'FLIGHT_SOFTWARE_VERSION_ID') ge 0 then begin
    fswvid=strsplit(line,'"',/extract)
    fmtv=3
    if (long(fswvid(1)) lt 99820433) then fmtv=1
    if (long(fswvid(1)) ge 99820433) and (long(fswvid(1)) lt 119210150) then fmtv=2
; will need to add if greater than 125280776 when 10.5 ready to test for fmtv3
;for now default to v3
endif

endwhile
close,ilun
free_lun,ilun
spectra=CCAM_read_libs(filename,edr=1,rsize=rsize,nlrec=nlrec,hk_prt=hk_prt,hk_dist=hk_dist)
return,spectra
end
