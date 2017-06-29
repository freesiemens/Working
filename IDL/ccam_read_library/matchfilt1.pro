pro MatchFilt1, x1, array1, array2, optishift, optiarray, $
    MaxShift=maxshift, DOPLOT = doplot, SPLINE=spline, Window=window, degree=degree
;+
; NAME:
;       MatchFilt
;       
; VERSION:
;       3.1
;
; PURPOSE:
;       Compute the optimized pixel shift between array1 and array2 
;       and interpolate array2 so that it is  on the same 
;       baseline x1 as the original spectrum array1.
;       the pixel shift function is interpolated using polynomial
;       of degree 3 by default, but can be changed by the user.
;       New version 3.0 uses a sliding window over 1/4 of the size of the 
;       user defined window
;       new version 3.1 does not stop if there is a bad correlation value,
;       but removes it from the pool of values used to do the polynomial fit.
;       If less than 10 correlation values remain for the polynomial fit, 
;       an error message is sent to the user and the program stopped
;       (probably data is too noisy)
;
; CALLING SEQUENCE:
;       MatchFilt, x1, array1, x2, array2,  optishift, optiarray, 
;       [MaxShift=, /DOPLOT, INTERP=, Window=, degree=]
;
; INPUTS:
;       arrays - any number idl arrays for x1, x2, array1 and array2
;       x1 and x2 are the wavelengths baselines
;       array1 and array2 are the CCam spectra (one spectral range at a time).
;               
; OUTPUTS: 
;       optiarray - new CCam spectrum interpolated on the x1 baseline 
;       with optimized pixel shift 
;       optishift - optimal pixel shift function
;
; OPTIONAL INPUT KEYWORD:
;      /Maxshift - expected maximum pixel shift. Default is 3. The function 
;      calculation time increases linearly with this parameter. The function
;      gives an error if the best pixel shift is equal to +/- Maxshift.
;      /doplot - if set, a plot of the pixel shift distance function is plotted.
;      and a superposition of the different arrays is shown.  
;      /spline - type of interpolation for obtaining the new array.
;      /window - width of the window used to generate the matched filter 
;      pixel shift function. Default is 250.0     
;      /degree - degree of polynomial fit for the pixel shift function.
;      default=3
; MODIFICATION HISTORY:
;       version 3.1 J. Lasue  27 January 2012
;       Removes poor correlation values from the polynomial fit
;       Error message appears if less than 10 values remain for the 
;       polynomial fit. 
;       version 3.0 J. Lasue  09 November 2011
;       Uses a sliding window over the 1/4 size of the window. 
;       version 2.1 J. Lasue  05 October 2011
;       Normalize the data to 1 to optimize the correlation.
;       change the windows so that the plots are not erased 
;       (keep in memory by IDL: RETAIN=2) 
;       version 2.0 J. Lasue  04 October 2011
;       The new function uses non linear interpolation to obtain the new 
;       baseline.
;       version 1.0 J. Lasue  September 2011
;       The function uses brute force analysis to determine the best pixel 
;       shift between two given arrays at 0.05 pixel value. Then interpolation 
;       is used to detemine the array on the new baseline.  
;       
;- Tests of the function call
;pro MatchFilt, x1, array1, x2, array2, optishift, optiarray, 
;    MaxShift=maxshift, DOPLOT = doplot, SPLINE=spline, Window=window
if(n_params() ne 5) then $
  message, 'Usage: MatchFilt, x1, array1, array2, optishift, optiarray'
; number of elements
if(n_elements(x1) ne 2048) then $
  message, 'x1 does not correspond to a 2048 spectral wavelength'
;if(n_elements(x2) ne 2048) then $
;  message, 'x2 does not correspond to a 2048 spectral wavelength'
if(n_elements(array1) ne 2048) then $
  message, 'array1 does not correspond to a 2048 spectral intensity'
if(n_elements(array2) ne 2048) then $
  message, 'array2 does not correspond to a 2048 spectral intensity'
if(n_elements(optishift) ne 2048) then $
  message, 'optishift does not correspond to a 2048 spectral shift function'
if(n_elements(optiarray) ne 2048) then $
  message, 'optiarray does not correspond to a 2048 spectral intensity'
; number of dimensions
if(size(x1, /n_dimensions) ne 1) then $
  message, 'x1 must be a 1D array'
;if(size(x2, /n_dimensions) ne 1) then $
;  message, 'x2 must be a 1D array'
if(size(array1, /n_dimensions) ne 1) then $
  message, 'array1 must be a 1D array'
if(size(array2, /n_dimensions) ne 1) then $
  message, 'array2 must be a 1D array'
if(size(optishift, /n_dimensions) ne 1) then $
  message, 'optishift must be a 1D array'
if(size(optiarray, /n_dimensions) ne 1) then $
  message, 'optiarray must be a 1D array'
; Define the default keywords if not passed as arguments
if(n_elements(MaxShift) eq 0) then $
  MaxShift=3.0
if(n_elements(SPLINE) eq 0) then $
  SPLINE=1
if(n_elements(Window) eq 0) then $
  Window=256
if(n_elements(degree) eq 0) then $
  degree=3

; Begin the match filter algorithm
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Define the pixel shift function values size and vector
; and correlation vector...
npixshift=floor((2048-window)*4.d0/window)
pixshift=findgen(npixshift)
pixcorr = findgen(npixshift)
;print, npixshift
; normalize the data, new temporary arrays
tarray1=array1/TOTAL(array1)
tarray2=array2/TOTAL(array2)
; first plot the difference between the two spectra
if (keyword_set(doplot)) then begin
print,'click on plot for next window'
print,'click to the left of the y-axis to stop'
i=1
x = !x.crange[0]+1
while i ne npixshift+1 and x gt !x.crange[0] do begin
;print, i, (window*(i-1)/4),(window*(i+3)/4)
  window, 2, RETAIN=2,  xsize=700  
  plot, x1[(window*(i-1)/4):(window*(i+3)/4-1)], tarray1[(window*(i-1)/4):(window*(i+3)/4-1)], $
    title="Comparison between default and new spectrum"
  oplot, x1[(window*(i-1)/4):(window*(i+3)/4-1)], tarray2[(window*(i-1)/4):(window*(i+3)/4-1)], color=160 
  cursor,x,y,/up
  i = i + 1
endwhile
endif

TVLCT,130, 255,  47, 20
msg='Initialising Processing'
progressTimer = Obj_New("ShowProgress", tlb, Color=20,message=msg,xsize=200)
progressTimer->start
count=0
progressTimer->Update, 0,message_text=msg
; calculates the best pixel shift values within a given window.
for i = 1, npixshift do begin
   count = count + 1

   msg='Processing Window '+string(i)
   progressTimer->Update, (count*100./npixshift),message_text=msg

   ; make calculations in pixels instead of wavelengths 
  ; => redefine baseline in terms of pixels 
  xpix=findgen(window)
  win1=xpix
  win2=xpix
  ; print, size(xpix)
  ; define the intensity within the windows considered
  win1=tarray1[(window*(i-1)/4):(window*(i+3)/4-1)]
  win2=tarray2[(window*(i-1)/4):(window*(i+3)/4-1)]  
  ; initialize steps to take in pixels and shift vector
  step=0.01
  Maxstep=2*CEIL(Maxshift/step)
  ;print, step, Maxshift, Maxstep
  shift=findgen(Maxstep+1)
  xshift=findgen(Maxstep+1)
  ; start looking for the optimized pixel shift
  ; brute force because not a big shift
  ; calculates a vector of all correlation values to avoid local minima...
  for nstep=0, Maxstep Do begin
    tempx=xpix-Maxshift+float(nstep)*step
;    print, size(tempx), size(win2), size(xpix)
    xshift[nstep]=float(nstep)*step-Maxshift
    tempy2=interpol(win2,tempx,xpix,spline=spline)
    shift[nstep]=correlate(win1,tempy2)
  endfor
  ; define the maximum of shift and the pixel shift required
  maxcorr=max(shift,max_subscript)
  ; check for border effects
  if ((max_subscript EQ 0)||(max_subscript EQ Maxstep)) then begin
     v =dialog_message( 'ERROR: border effects, maximum obtained at the end of the window')
;;   print, 'border effects, maximum obtained at the end of the
;;   window'
;;    print, 'The user needs to increase the size of the window !!!'
 ;;   print, 'iteration: ', i, ' window:', window*(i-1), (window*i-1)
    return
  endif
; poor correlation test has been moved out of the loop, 
; uses function 'where' to remove the values below a given threshold.
  pixshift[i-1]=xshift[max_subscript]
  pixcorr[i-1]=maxcorr
  ;print, maxcorr, max_subscript, xshift[max_subscript]
endfor
progressTimer->destroy
 
; printout the results to check
;print, 'pixshift=', pixshift
;print, 'pixcorr=', pixcorr
;define the shift function for each pixels from 0 to 2048
; first redefine the data to be the middle of the window
winmid=floor(window/2.d0)
winshift=floor(window/4.d0)
pixpos=findgen(npixshift)
for i=0, npixshift-1 do pixpos[i]=winmid+i*winshift
; if there are poor correlations, redefine the vector where the fit will be made
; where the correlation is good enough.
rmwin=where(pixcorr GT 0.6)
srmwin=size(rmwin)
if ((n_elements(pixcorr)-srmwin[1]) GT 0) then begin
; chech if there are enough data to do the fit (need more than 10)
  if (srmwin[1] LT 8) then begin
    v=dialog_message('ERROR: not enough data points to do the polynomial fit',/center)
;;    print, 'not enough data points to do the polynomial fit'
    return
  endif 
  pixcorr=pixcorr[rmwin]  
  pixpos=pixpos[rmwin]
  pixshift=pixshift[rmwin]
endif  
;print, 'pixcorr', pixcorr
;print, 'pixshift', pixshift
;print, 'pixpos', pixpos
; fit a polynomial of degree 3 to the data
resultfit=poly_fit(pixpos,pixshift,degree)
;print, 'polynomial fit of degree: ', degree
;print, 'coefficients:', resultfit

; calculate the results for all the pixels from 0 to 2048
totpixpos=findgen(2048)
totpixshift=findgen(2048)
for i= 0, 2047 do begin
  tmpval=0.d0
  for k=0,degree do begin
      tmpval=tmpval+resultfit[k]*totpixpos[i]^k
  endfor
  totpixshift[i]=tmpval
endfor 
; generate plot to check the fit
if (keyword_set(doplot)) then begin
  window, 0, RETAIN=2
  plot, totpixpos, totpixshift, title="Pixel shift and polynomial fit"
  oplot, pixpos, pixshift, color=160
endif

; define the output data do comparison plot 
; optishift =  new pixels positions
optishift=totpixpos+totpixshift
optiarray=interpol(array2,optishift,totpixpos,spline=spline)
tarray2=interpol(tarray2,optishift,totpixpos,spline=spline)

if (keyword_set(doplot)) then begin
print,'click on plot for next window'
print,'click to the left of the y-axis to stop'
i=1
x = !x.crange[0]+1
while i ne npixshift+1 and x gt !x.crange[0] do begin
  window, 1, RETAIN=2, xsize=700  
  plot, x1[(window*(i-1)/4):(window*(i+3)/4-1)], tarray1[(window*(i-1)/4):(window*(i+3)/4-1)], $
    title="Comparison between default and interpolated spectrum"
  oplot, x1[(window*(i-1)/4):(window*(i+3)/4-1)], tarray2[(window*(i-1)/4):(window*(i+3)/4-1)], color=160 
  cursor,x,y,/up
  i = i + 1
endwhile
endif

v = dialog_message( 'SUCCESS: global correlation= '+ string( correlate(tarray1,tarray2),format='(f4.2)'),/center,/information) ;
;;print, 'global correlation= ', correlate(tarray1,tarray2) ;

return
end
