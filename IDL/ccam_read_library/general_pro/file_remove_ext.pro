FUNCTION file_remove_ext,fn

  ; remove file extension
  p=STRPOS(fn,'.',/reverse_search)
  IF p NE -1 THEN fn1=STRMID(fn,0,p)
  
  RETURN,fn1
  
END
