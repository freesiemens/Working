pro parse_afdata, afdata, pstart, x, y, xx, yy, focus

      ;  input: afdata, pstart
      ;  output: (x,y) courbe autofocus
      ;  output: (xx,yy) lieux des milieux
      ;  output: focus, moyenne des milieux
    
      y = afdata
      x = findgen(639)*4 + pstart

;  Running median

      y1 = y*0.
      
      for k=0+4,638-4 do begin

         dum = y[k-4:k+4]
         y1[k] = median(dum)
      
      endfor

      top = max(y1)

; Index at 15%

      i = 0
      while y1[i] lt top*0.15 do begin
         
         dum = i
         i=i+1

      endwhile 
      i1 = i

; Index at 80%

      i = 0
      while y1[i] lt top*0.8 do begin
         
         dum = i
         i=i+1
         
      endwhile 
      i2 = i
      
; Index at 80%

      i = 638
      while y1[i] lt top*0.8 do begin
         
         dum = i
         i=i-1
         
      endwhile 
      i3 = i
      
;  Get the symmétrie

      correc = 0
      focus_list = fltarr(i2-i1+1)

      xx = 0. & yy = 0.

      for i=i1,i2 do begin
         
         val1 = y1[i]
         val2 = y1[i3]
         j = i3

         while val1 lt val2 and j lt 638 do begin
            
            val2 = y1[j]
            j = j+1

         endwhile
         
         j = j-1

         if j lt 638 then begin
            
            p = x[i] + x[j] + (x[j]-x[j-1])*(y1[i]-y1[j])/(y1[j]-y1[j-1])
            focus_list[i-correc-i1] = 0.5*P
            
            plots,focus_list[i-correc-i1],y1[i],psym=3
            
            xx = [xx, focus_list[i-correc-i1]]
            yy = [yy, y1[i]]

         endif else correc = correc + 1
         
      endfor
      
      xx = xx[1:*]
      yy = yy[1:*]

;  Get the final value

      focus = mean(focus_list)
     
return
end
