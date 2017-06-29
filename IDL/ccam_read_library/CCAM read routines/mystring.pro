function mystring, x, fmt

      y = strcompress(string(float(x),format=fmt),/remove_all)
      return, y

end

