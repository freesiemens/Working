
pro parse_footer, footer0, $
         cmd, exposure, offset, ADC_gain, clean, image_num

      ;  input footer

      foottmp=reform(footer0,5,4)

      ;  output

      footer=intarr(4,4)

      footer[0,*]=ishft(fix(foottmp[0,*]),2) OR ishft(foottmp[1,*],-6)

      footer[1,*]=ishft(fix(foottmp[1,*] AND '3f'x),4) OR $
                  ishft(foottmp[2,*],-4)

      footer[2,*]=ishft(fix(foottmp[2,*] AND 'f'x),6) OR $
                  ishft(foottmp[3,*],-2)

      footer[3,*]=ishft(fix(foottmp[3,*] AND '3'x),8) OR $
                  foottmp[4,*]

      footer=reform(footer,1,16)
      
      ;  Output variables

      cmd = footer[7]
      exposure = ishft(fix(footer[8]),8) OR footer[9]
      offset = footer[10]
      ADC_gain = footer[11]
      clean = footer[12]
      image_num = footer[13]
      
return
end
