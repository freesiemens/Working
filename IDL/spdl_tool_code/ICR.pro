;+
; NAME:
;       ICR (Independent Component Regression)
;
; PURPOSE:
;       Compute the composition of CCam spectra using the Independent
;       Component Regression
;
; CALLING SEQUENCE:
;       Composition = ICR(CCam_CCS_File, SHOT=shot)
;
; INPUTS:
;       CCam_CCS_File: Array of ChemCam CCS SAV file names including path
;
; OPTIONAL INPUTS:
;       None
;
; KEYWORD PARAMETERS:
;       SHOT: If set computes the shot to shot composition.
;       quiet: If set, suppress pop-up progress bar in read_ccs
; OUTPUTS:
;       Array of composition:  Dimension [Nb of spectra, 8] if
;       mean spectra composition is computed; Pointer array of Nb of
;       spectra with dimension [Nb of shots, 8] if shot to shot
;       composition is computed.
;
; OPTIONAL OUTPUTS:
;       None
;
; SIDE EFFECTS:
;      If something went wrong, returns -1
;
; RESTRICTIONS:
;       Two files are required:
;           'cp_ica_new.sav': File with a structure containing element name, ICA
;           component and Normalisation parameter.
;           'ica_rgr_new.sav': File with a structure containing element
;           name,regression coefficients and regression law.
;
; PROCEDURE:
;        READ_CCS
;        ICA_FIXED_COMP
;        REGRESS_ICA
;
; EXAMPLE:
;        File_List=file_search('CL5*CCS*.SAV')
;        Compo = ICR(File_List,/shot)
;
;
; MODIFICATION HISTORY:
; O. Forni: May 2015
; R. Anderson: May 26, 2015 - Added output of "good" file name index
; R. Anderson: July 7, 2015 - Added "quiet" option
; R. Anderson: July 10, 2015 - Added status pop-up for calculations. 
;                            - Modified so that both mean and single shot calculations
;                              can be run in the same call to this function
;-
FUNCTION ICR,fn,shot=shot,fn_good_index=fn_good_index,quiet=quiet,both=both
if keyword_set(both) then shot=1

restore,'cp_ica_new.sav'
restore,'ica_rgr_new.sav'

s=read_ccs(fn,shot=shot,fn_good_index=fn_good_index,quiet=quiet,spout_means=spout_means)
;s_old=read_ccs_old(fn,shot=shot,fn_good_index=fn_good_index)
;s_old_mean=read_ccs_old(fn,shot=0,fn_good_index=fn_good_index)
stop
;stop
comp_out=hash()
if keyword_set(both) or not(keyword_set(shot)) then begin
   if not(quiet) then xmess,"Running ICA calculations",/nowait,wid=wid
   cf=ica_fixed_comp(spout_means,cp_ica_new,/norm,/std)
   comp_means=regress_ica(cf,ica_rgr_new)
   comp_out=comp_out+hash('means',comp_means)
   if not(quiet) then widget_control,/dest,wid
   
endif

if keyword_set(shot) then begin
   if not(quiet) then xmess,"Running single-shot ICA calculations",/nowait,wid=wid    
   cf=ica_fixed_comp(s,cp_ica_new,/norm,/std)
   comp=regress_ica(cf,ica_rgr_new)
   comp_out=comp_out+hash('shots',comp)
   if not(quiet) then widget_control,/dest,wid
   
endif
    
   
return,comp_out


end


