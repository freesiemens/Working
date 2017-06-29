;+
; NAME:
;	CCAM_READ_RMI
;
; PURPOSE:
;	Read ChemCam RMI images. Built many HK outputs
;
; EXPLANATION:
;	Read an RMI files built by JPL. Copy the input command. Build
;	structures for HK data: instrument parameters, Rover PRTs, RMI
;	parameters, Distance to target. On request, tell us a bit on
;	what has been read.  
;
; CALLING SEQUENCE:
;	image = CCAM_READ_RMI(rmifile [,convfile = ]  $
;               [,theimage][, cmd = ][, time = ][, /verbose]$
;               [, HK_prt = ][, HK_inst = ][,HK_rmi = ][, HK_dist = ])
;
; INPUTS:
;	rmifile    -  RMI filename, including path
;
; OPTIONAL INPUTS:
;       convfile    - Conversion filename, including path. If this*
;                      input is not provided, the system variable
;                      !CCAM_convfile will be used.
;
; OPTIONAL KEYWORD INPUTS:
;       none
;
; OUTPUTS:
;       return a 1024x1024 image
;
; OPTIONAL OUTPUTS:
;	theimage     -  1072x1056 image, that includes masked pixels.
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
;       HK_RMI       -  Return critical RMI parameters (structure)
;       FILE         -  Return the file name, size
;
; OPERATIONAL NOTES:
;       This program ony read .dat RMI data. It assumes that the
;       format after May 2011 is used. If not it will try the old
;       format which have a different series of PRTs.
;
;       Assume that the file soh_conversion.txt exists
;       somewhere. Provide the path or assume it is under !ChemCam_gdata
;       
;       Run Ccam_init.pro prior to use this program
;
; PROCEDURES CALLED:
;	PARSE_FOOTER(), PARSE_TRANSFERT(), PARSE_AFDATA()
;       LOAD_CONVERSION(), CCAM_MOTOR()
;
;       MYSTRING(), YMD2DN(), DATE_CONV()
;
; REVISION HISTORY:
;	S. Maurice, D. Delap, O. Gasnault       June 2011
;-

function ccam_read_rmi, $
             filename, theimage, $
             convfile = convfile, $
             time = thetime, cmd = cmd, file = thefile, $
             HK_prt = HK_prt, HK_inst = HK_inst, $
             HK_rmi = HK_rmi, HK_dist = HK_dist, $
             verbose = verbose
  
;+
;  PART 1
;  Read data 
;-

      ;  define variables
  
      uval=ulong(0)
      ival=uint(0)
      bval=byte(0)

      itf=bytarr(3)

      ruval=ulong(0)
      rbval=byte(0)
      rival=uint(0)

      num_status = 16
      num_mast = 39
      num_dpu = 9
      ndata = 7 
      
;
;  Load Conversion factors
;  Use default file if input not provided
;

      if not keyword_set(convfile) then $
         convfile = !ChemCam_sdata + 'soh_conversion.txt'

      load_conversion, convfile, $
           mast_struct, dpu_struct, switch_struct, laser_struct
      
;
;  Define various structures
;  Assume late data format
;
      
      early_fmt = 0

      inst_temps={$
                 mu_obox_tel_temp :float(0), $
                 mu_obox_tel_temp_st :long(0), $
                 mu_laser_if_temp:float(0), $
                 mu_laser_if_temp_st:long(0), $
                 mu_ebox_heatsink_temp:float(0), $
                 mu_ebox_heatsink_temp_st:long(0), $
                 mu_ebox_fpga_temp:float(0), $
                 mu_ebox_fpga_temp_st :long(0), $
                 bu_ccd_vnir_b_temp :float(0), $
                 bu_ccd_vnir_b_temp_st :long(0), $
                 bu_spect_b_temp :float(0), $
                 bu_spect_b_temp_st :long(0), $
                 bu_ccd_uv_a_temp :float(0), $
                 bu_ccd_uv_a_temp_st :long(0), $
                 bu_spect_a_temp :float(0), $
                 bu_spect_a_temp_st :long(0), $
                 bu_demux_a_temp :float(0), $
                 bu_demux_a_temp_st :long(0), $
                 bu_demux_b_temp :float(0), $
                 bu_demux_b_temp_st :long(0)}

      cmd_arguments={$
                    frame_id : long(0), $ 
                    frame_index : fix(0), $
                    coord_type : long(0), $
                    coord1 : ulong(0), $ 
                    coord2 : ulong(0), $ 
                    coord3 : ulong(0), $ 
                    focus : ulong(0), $
                    range : uint(0), $
                    exposure_type : long(0), $
                    exposure_time : uint(0), $
                    start_c_pixel : uint(0), $
                    start_r_pixel : uint(0), $
                    c_height : uint(0), $
                    r_height : uint(0), $
                    compression : long(0)}
      
      cmd_parameters={$
                     linkToUse : byte(0), $
                     upperThreshold : uint(0), $
                     lowerTheshold: uint(0), $
                     startimage : byte(0), $
                     AD_offset : byte(0), $
                     AD_gain : byte(0), $
                     CCD_cleanCount : byte(0), $
                     fromLimitSwitch : byte(0), $
                     Thumbnail_size : long(0), $
                     Thumbnail_compression : long(0), $
                     Thumbnail_DP_Priority : byte(0), $
                     Reference_Pix_DP_Priority : byte(0), $
                     Reference_Pix_DP : long(0)}
      
      soh_scidata={$
                  head1:uint(0), $
                  head2:uint(0), $
                  nbytes:ulong(0), $
                  RCEtime:ulong(0), $
                  curMsecCount:ulong(0), $
                  goodCmds:uint(0), $
                  badCmds:uint(0), $
                  mastCmds:uint(0), $
                  mastACKs:uint(0), $
                  mastNAKs:uint(0), $
                  mastResends:uint(0), $
                  mastPktsRecd:uint(0), $
                  mastPktsBad:uint(0), $
                  CCstate:uint(0), $
                  status:uint(0), $
                  memFPGAversion:uint(0), $
                  microFPGAversion:uint(0), $
                  spectFPGAversion:uint(0), $
                  images_sent:uint(0), $
                  SOH_sent:uint(0), $
                  spect_sent:uint(0), $
                  laser_data_Sent:uint(0), $
                  spare:uint(0), $
                  spare2:uint(0), $
                  Nfollowing:uint(0)}
      
      ccam_DPU_SOH={$
                   lastDAC:byte(0), $
                   DPU_Analog_ground:byte(0), $
                   DPU_5P_Digital:uint(0), $
                   DPU_2P5_Digital:uint(0), $
                   DPU_5P_Analog:uint(0), $
                   DPU_5N_Analog:uint(0), $
                   DPU_Temp:uint(0), $
                   Spectrometer_Temp:uint(0), $
                   LVPS_Temp:uint(0), $
                   Motor_Position:uint(0) }
      
      ccam_MU_SOH={$
                  MU_Status: uint(0), $
                  HK_heatsink_temp:uint(0), $
                  HK_current_3P3:uint(0), $
                  HK_current_30P:uint(0), $
                  HK_current_5N:uint(0), $
                  HK_current_12P:uint(0), $
                  HK_V_3P3:uint(0), $
                  HK_V_5P:uint(0), $
                  HK_V_5N:uint(0), $
                  HK_V_12P:uint(0), $
                  HK_V_12N:uint(0), $
                  HK_V_15P:uint(0), $
                  HK_V_30P:uint(0), $
                  Laser_diode_current:uint(0), $
                  CWL_temp:uint(0), $
                  HK_temp_limiter_1:uint(0), $
                  Autofocus_signal_output:uint(0), $
                  LMD18200_Temp:uint(0), $
                  HK_Temp_Laser_1:uint(0), $
                  HK_Temp_Laser_2:uint(0), $
                  HK_Temp_Laser_3:uint(0), $
                  HK_Temp_Laser_4:uint(0), $
                  HK_V_Stack_1:uint(0), $
                  HK_I_Stack_1:uint(0), $
                  HK_V_Stack_2:uint(0), $
                  HK_I_Stack_2:uint(0), $
                  HK_V_Stack_3:uint(0), $
                  HK_I_Stack_3:uint(0), $
                  Optical_Flux_Level:uint(0), $
                  HK_HV_Pockels:uint(0), $
                  HK_Limit_Switch:uint(0), $
                  HK_Spare_2:uint(0), $
                  HK_RMI:uint(0), $
                  HK_temp_FPGA_1:uint(0), $
                  HK_Telescope_1:uint(0), $
                  HK_Telescope_2:uint(0), $
                  FPGA_3P3:uint(0), $
                  Last_Steps_Moved:uint(0), $
                  Steps_Displacement:uint(0) }
      
      ccam_SOH_to_RCE={ $
                      time:ulong(0), $
                      DPU_SOH:ccam_DPU_SOH, $
                      MU_SOH:ccam_MU_SOH}
              
;
;  Read/Parse binary file
;
      
      doitagain:

      openr,ilun,filename,/get_lun,/swap_if_little
      
      ; the first data value should be sclk
      ; sclk is 4 byte U32

      readu,ilun,uval
      sclk=uval
      
      ; read inst_temps PRT

      readu,ilun,inst_temps

      ; read cmd_args

      readu,ilun,cmd_arguments

      ; read cmd_params

      readu,ilun,cmd_parameters
     
;
;  SOH data before
;

      readu,ilun,uval
      readu,ilun,bval
      opcode=bval

       ;  If this opcode cannot be met, we assume that we deal
       ;  with an early forat of the data and read the file again
       ;  If does not pass the second time, we have a problem

       if opcode ne 82B then begin

          if early_fmt eq 1 then message, ' Houston we have a problem'

          inst_temps={$
                     mu_obox_tel_temp :float(0), $
                     mu_obox_tel_temp_st :long(0), $
                     mu_laser_if_temp:float(0), $
                     mu_laser_if_temp_st:long(0), $
                     mu_ebox_heatsink_temp:float(0), $
                     mu_ebox_heatsink_temp_st:long(0), $
                     mu_ebox_fpga_temp:float(0), $
                     mu_ebox_fpga_temp_st :long(0), $
                     bu_ebox_temp :float(0), $
                     bu_ebox_temp_st :long(0), $
                     bu_spect_top_temp :float(0), $
                     bu_spect_top_temp_st :long(0), $
                     bu_spect_bottom_temp :float(0), $
                     bu_spect_bottom_temp_st :long(0), $
                     bu_demux_temp :float(0), $
                     bu_demux_temp_st :long(0)}

          close,ilun
          free_lun,ilun

          early_fmt = 1
          goto, doitagain
          
       endif

       ; Transfer status
 
       readu,ilun,itf
       parse_transfert, itf

       ; read SOH science

       readu,ilun,uval
       readu,ilun,soh_scidata

      ; Loop for soh_scidata.Nfollowing
    
       nsoh_before = soh_scidata.Nfollowing
       soh_before = replicate(ccam_soh_to_rce, nsoh_before)

       for j=0,nsoh_before-1 do begin                                  
          
          readu,ilun,ccam_SOH_to_RCE 
          soh_before[j] = ccam_SOH_to_RCE 

       endfor

       ; the last valid data is the checksum

       readu,ilun,uval
       checksum=uval

;
;  SOH data after
;

       readu,ilun,uval
       readu,ilun,bval
       opcode=bval

       if opcode ne 82B then message,' Houson wa have a problem'

      ;  Transfer status
 
       readu,ilun,itf
       parse_transfert, itf
 
      ; read SOH science

       readu,ilun,uval
       readu,ilun,soh_scidata

      ; Loop for soh_scidata.Nfollowing
    
       nsoh_after = soh_scidata.Nfollowing
       soh_after = replicate(ccam_soh_to_rce, nsoh_after)

       for j=0,nsoh_after-1 do begin                                  
          
          readu,ilun,ccam_SOH_to_RCE 
          soh_after[j] = ccam_SOH_to_RCE 

       endfor

       ; the last valid data is the checksum

       readu,ilun,uval
       checksum=uval

;
; AUTOFOCUS block
; values are for cmd_arguments.focus
; 0: No_FOCUS : don't move it
; 1: BASELINE (use CWL to find optimal focus position)
; 2: TBD (not used)
; 3: MANUAL position focused based on range argument (distToTarget)
; 4: AF_OFFSET: applies RMI offset from last autofocus solution (relative focus)
;

       if cmd_arguments.focus eq 1 then begin

          readu,ilun,uval 
          readu,ilun,bval 
          opcode=bval 

          if opcode ne 129B then message,' Houston we have a problem'

          ;  Transfer status

          readu,ilun,itf
          parse_transfert, itf
          
          ;  Byte count to follow
 
          readu,ilun,uval
          readu,ilun,bval
          if bval ne 194B then message,' Houson wa have a problem'

          ;  Gain

          readu,ilun,bval
          afgain = bval

          ; motor step position at start of scan

          readu,ilun,ival
          P1 = ival 
       
          ;  ??

          readu,ilun,uval 
          dpbytecount = uval 
       
          ;  Msec since last rec time??

          readu,ilun,uval 
          aftime = uval
 
          ;  Autofocu data (639 displacements)
          
          afdata = uintarr(639)
          readu,ilun,afdata 
          
          ;  Number of steps done in last displacement

          readu,ilun,ival 
          mtail1 = ival 

          ;  Number of dispalcement done

          readu,ilun,ival 
          mtail2 = ival 
        
          nb_displacements = fix(mtail2/16)
          ;Thermal_flag = 2 before last bits
          ;Limit_switch = 2 last bits

          ; read checksum

          readu,ilun,uval  
          checksum = uval

    endif

;
;  RMI image
;

      readu,ilun,uval
      readu,ilun,bval
      opcode=bval

      if opcode ne 119B then message,' Houson we have a problem'

      ;  Transfer status

      readu,ilun,itf
      parse_transfert, itf, ectf

      ; if  ectf 1 or 2 then 

      if ectf eq 1 or ectf eq 2 then begin
       
         readu,ilun,uval
         checksum=uval
         
      endif else message, '???'
      
      ; read size of RMI data
      
      readu,ilun,uval
      readu,ilun,bval
      opcode = bval
      
      if opcode ne 119B then message,' Houson we have a problem'
      
       ;  Transfer status

      readu,ilun,itf
      parse_transfert, itf
       
      ;  Read size

      readu,ilun,ruval
      readu,ilun,rbval
      opcode = rbval
      
      if opcode ne 119B then message,' Houson we have a problem'
      
      ; head2 is copy of reccontrol byte2
   
      readu,ilun,rbval
      head2=rbval

      readu,ilun,rbval
      retrys=rbval

      readu,ilun,rbval
      mastfpga=rbval

      readu,ilun,ruval
      rbytecount=ruval

      ; now we come to the data

      imgbuf=bytarr(1415040)
      readu,ilun,imgbuf
      tmp=reform(imgbuf,5,283008)
    
      ;  Image in 1072 x 1056

      image=intarr(4,283008)
      image[0,*]=ishft(fix(tmp[0,*]),2) OR ishft(tmp[1,*],-6)
      image[1,*]=ishft(fix(tmp[1,*] AND '3f'x),4) OR ishft(tmp[2,*],-4)
      image[2,*]=ishft(fix(tmp[2,*] AND 'f'x),6) OR ishft(tmp[3,*],-2)
      image[3,*]=ishft(fix(tmp[3,*] AND '3'x),8) OR tmp[4,*]
      theimage=transpose(reform(image,1072,1056))
    
      ;  Image in 1024 x 1024

      outimage=rotate(theimage[16:1039,43:1066],3)

      ;  Footer: read and parse

      footer=bytarr(20)
      readu,ilun,footer
      parse_footer, footer,  $
         cmd, exposure, offset, ADC_gain, clean, image_num

      ;  Checksum

      readu,ilun,uval
      checksum=uval

;
;  Close the file
;

      close,ilun
      free_lun,ilun
      
;+
;  PART 2
;  Generate output structures
;-

;  Some output structutres

     HK_laser_struct = {name: strarr(ndata), value: fltarr(ndata), $
                         unit: strarr(ndata), text: strarr(ndata) }

     HK_mu_struct = {when: strarr(num_mast), $
                     name: strarr(num_mast), value: fltarr(num_mast), $
                     unit: strarr(num_mast), text : strarr(num_mast) }

     HK_bu_struct = {when: strarr(num_dpu), $
                     name: strarr(num_dpu), value: fltarr(num_dpu), $
                     unit: strarr(num_dpu), text : strarr(num_dpu) }
     
     HK_status_struct = {when: strarr(num_status), $
                         name: strarr(num_status),value:strarr(num_status), $
                         unit: strarr(num_status), text : strarr(num_status)}
     
;  Rover PRTS
;  Two cases depending on the format

      if early_fmt then begin

         HK_prt = { Commment: 'All values are in deg C', $
                    MU_Obox_tel: inst_temps.(0), $
                    MU_Laser_if: inst_temps.(2), $
                    MU_EBOX_heatsink: inst_temps.(4), $
                    MU_FPGA: inst_temps.(6), $
                    BU_EBOX: inst_temps.(8), $
                    BU_Spect_top: inst_temps.(10), $
                    BU_Spect_bottom: inst_temps.(12), $
                    BU_Demux: inst_temps.(14)}

      endif else begin

         HK_prt = { Commment: 'All values are in deg C', $
                    MU_Obox_tel: inst_temps.(0), $
                    MU_Laser_if: inst_temps.(2), $
                    MU_EBOX_heatsink: inst_temps.(4), $
                    MU_FPGA: inst_temps.(6), $
                    BU_CCD_VNIR_B: inst_temps.(8), $
                    BU_Spect_B: inst_temps.(10), $
                    BU_CCD_UV_A: inst_temps.(12), $
                    BU_Spect_A: inst_temps.(14), $
                    BU_Demux_A: inst_temps.(16), $
                    BU_Demux_B: inst_temps.(18)}

      endelse
      
;  Save commands argurments and parameters
       
      Command = {arguments: cmd_arguments, $
                 parameters: cmd_parameters }
     
;  SOH before

      HK_MU_before = replicate(hk_mu_struct, nsoh_before)
      HK_BU_before = replicate(hk_bu_struct, nsoh_before)
      HK_status_before = replicate(hk_status_struct, nsoh_before)

      for j = 0, nsoh_before-1 do begin 

          ;  MU

          HK_MU_before[j].name = strcompress(mast_struct.name,$
                                             /remove_all)
          HK_MU_before[j].unit = mast_struct.units
          HK_MU_before[j].when = 'Before'

          for i=0,num_mast-1 do $
             HK_MU_before[j].value[i] = ccam_soh_to_rce.mu_soh.(i)*$
             mast_struct[i].mult + mast_struct[i].offset
    
          format = ['(i9)',replicate('(f9.2)',12),'(f10.4)',$
                    replicate('(f9.2)',24),'(i9)']

          for i=0,num_mast-1 do $
             HK_MU_before[j].text[i] = hk_mu_before[j].name[i]+' = '+$
             mystring(hk_mu_before[j].value[i],format[i])+' '+$
             hk_mu_before[j].unit[i]
          
          ;  BU
          
          HK_BU_before[j].name = strcompress(dpu_struct.name,$
                                             /remove_all)
          HK_BU_before[j].unit = dpu_struct.units
          HK_BU_before[j].when = 'Before'
          
          for i=0,num_dpu-1 do $
             HK_BU_before[j].value[i] = ccam_SOH_to_RCE.DPU_SOH.(i+1)*$
             dpu_struct[i].mult+dpu_struct[i].offset
          
          format = [replicate('(f9.2)',8),'(i9)']
          
          for i=0,num_dpu-1 do $
             HK_BU_before[j].text[i] = hk_bu_before[j].name[i]+' = '+$
             mystring(hk_bu_before[j].value[i],format[i])+' '+$
             hk_bu_before[j].unit[i]
          
          ;  STATUS

          HK_Status_before[j].name = strcompress(switch_struct.name,$
                                                 /remove_all)
          HK_Status_before[j].unit = ' '
          HK_Status_before[j].when = 'Before'
          
          for i=0,num_status-1 do $
             HK_status_before[j].value[i] = $
             switch_struct[i].status[ishft($
             ccam_soh_to_rce.mu_soh.mu_status,-i)AND 1] 

          for i=0,num_status-1 do $
             HK_status_before[j].text[i] = $
             hk_status_before[j].name[i]+' = '+$
                    hk_status_before[j].value[i]+' '+$
                    hk_status_before[j].unit[i]
       
       endfor

;  SOH after

      HK_MU_after = replicate(hk_mu_struct, nsoh_after)
      HK_BU_after = replicate(hk_bu_struct, nsoh_after)
      HK_status_after = replicate(hk_status_struct, nsoh_after)
      
      for j=0,nsoh_after-1 do begin

          ;  MU
          
         HK_MU_after[j].name = strcompress(mast_struct.name,/remove_all)
         HK_MU_after[j].unit = mast_struct.units
         HK_MU_after[j].when = 'After'
         
         for i=0,num_mast-1 do $
            HK_MU_after[j].value[i] = ccam_soh_to_rce.mu_soh.(i)*$
            mast_struct[i].mult + mast_struct[i].offset
      
         format = ['(i9)',replicate('(f9.2)',12),'(f10.4)',$
                   replicate('(f9.2)',24),'(i9)']
         
         for i=0,num_mast-1 do $
            HK_MU_after[j].text[i] = hk_mu_after[j].name[i]+' = '+$
            mystring(hk_mu_after[j].value[i], format[i])+' '+$
            hk_mu_after[j].unit[i]
      
          ;  BU

         HK_BU_after[j].name = strcompress(dpu_struct.name,/remove_all)
         HK_BU_after[j].unit = dpu_struct.units
         HK_BU_after[j].when = 'After'
      
         for i=0,num_dpu-1 do $
            HK_BU_after[j].value[i] = ccam_SOH_to_RCE.DPU_SOH.(i+1)*$
            dpu_struct[i].mult+dpu_struct[i].offset
          
         format = [replicate('(f9.2)',8),'(i9)']
         
         for i=0,num_dpu-1 do $
            HK_BU_after[j].text[i] = hk_bu_after[j].name[i]+' = '+$
            mystring(hk_bu_after[j].value[i], format[i])+' '+$
            hk_bu_after[j].unit[i]
         
          ;  STATUS

         HK_Status_after[j].name = strcompress(switch_struct.name,/remove_all)
         HK_Status_after[j].unit = ' '
         HK_Status_after[j].when = 'After'
         
         for i=0,num_status-1 do $
            HK_status_after[j].value[i] = $
            switch_struct[i].status[ishft($
            ccam_soh_to_rce.mu_soh.mu_status,-i)AND 1] 
         
         for i=0,num_status-1 do $
            HK_status_after[j].text[i] = hk_status_after[j].name[i]+' = '+$
            hk_status_after[j].value[i]+' '+$
            hk_status_after[j].unit[i]
         
      endfor       

;  Concatenate SOH before and after

      nsoh = nsoh_before + nsoh_after

      HK_MU = replicate( HK_MU_Struct, nsoh)
      HK_MU(0:nsoh_before-1) = HK_MU_before
      HK_MU(nsoh_before:nsoh_before+nsoh_after-1) = HK_MU_after
       
      HK_BU = replicate( HK_BU_Struct, nsoh)
      HK_BU(0:nsoh_before-1) = HK_BU_before
      HK_BU(nsoh_before:nsoh_before+nsoh_after-1) = HK_BU_after

      HK_Status = replicate( HK_Status_Struct, nsoh)
      HK_Status(0:nsoh_before-1) = HK_Status_before
      HK_Status(nsoh_before:nsoh_before+nsoh_after-1) = HK_Status_after
       
      HK_inst = {MU: HK_MU, BU: HK_BU, STATUS: HK_STATUS, $
                 nbefore: nsoh_before, nafter: nsoh_after}

;
;  Save a few HK RMI from footer
;

     HK_RMI = {exposure_msec: exposure, offset: offset, $
               ADC_gain: ADC_gain, num_clean: clean, $
               num_image: image_num}

;
;  HK for position
;

     focus_value = cmd_arguments.focus
     
     case cmd_arguments.focus of 

        0: focus_text = 'No focus'
        1: focus_text = 'Focus with CWL'
        3: focus_text = 'Manual focus'
        4: focus_text = 'Relative focus'

     endcase

     ;  Autofocus data for focus_value = 1

     if cmd_arguments.focus eq 1 then begin
        
        parse_afdata, afdata, p1, x, y, xx, yy, focus
        
        focus_afdata = {xvalues: x, yvalues: y, $
                        xsym: xx, ysym: yy, focus : focus}

     endif else focus_afdata = -1

     ; Current motor position

     l = n_elements(hk_inst.bu)
     pmotor = hk_inst.bu[l-1].value[8]

     dum = ccam_motor(pmotor,/dist)       
     
     dist_meter = dum/1000.
     dist_text = mystring(dist_meter,'(f8.2)')+' m'

     ;  Distance guess

     dist_guess = cmd_arguments.range/1000.
    
     ;  Save distance structure

     HK_dist = {focus_value: focus_value, focus_text: focus_text, $
                focus_afdata: focus_afdata, $
                dist_pmotor: pmotor, dist_meter : dist_meter, $
                dist_text: dist_text, dist_guess: dist_guess}

;
;  Time data
;

     thetime = parse_sclk(sclk)

;
;  A few data on the file itself
;

     thefile = {file_name: ' ', file_size: ' '}

     dum = strpos(filename,'\',/reverse_search)
     thefile.file_name = strmid(filename,dum+1,100)
       
     dum = file_info(filename)
     thesize = dum.size/1000.
     thefile.file_size = mystring(thesize,'(i9)')+' KB'

;+
;  PART 3 
;  Talk to me
;-

     if keyword_set(verbose) then begin

        print,' '
        print,' Filename     : ' + thefile.file_name
        print,' Date         : ' + thetime.date  
        print,' Distance     : ' + HK_dist.dist_text
        print,' Motor pos.   : ' + mystring(HK_dist.dist_pmotor,'(i6)')
        print,' Nb HK before : ' + mystring(HK_inst.nbefore,'(i2)')
        print,' Nb HK after  : ' + mystring(HK_inst.nafter,'(i2)')
        print,' Focus        : ' + HK_dist.focus_text
        print,' Exposure     : ' + mystring(HK_rmi.exposure_msec,'(i8)')+' msec'
        print,' PRT Laser    : ' + mystring(HK_prt.MU_laser_IF,'(f7.2)')
      
        if early_fmt then $
           print,' PRT Spect    : ' + mystring(HK_prt.BU_Spect_top,'(f7.2)') $
        else $ 
           print,' PRT Spect    : ' + mystring(HK_prt.BU_Spect_A,'(f7.2)')
        
        print,' '

        ;  Visualize 1/4 resolution
      
        window, xsize=256, ysize=256, title = '1/4 resolution
        dum = outimage[0:1023:4, 0:1023:4]
        tvscl, dum
         
     endif
    
;  End

return, outimage
end
