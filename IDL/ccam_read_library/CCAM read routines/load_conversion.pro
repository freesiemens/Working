pro load_conversion, file, mast_struct, dpu_struct, switch_struct, laser_struct

;  Load conversion factors
;  input: filename
;  output: structures for mast, dpu and switch
;
      
      num_mast = 39
      num_dpu = 9
ndata=7 ; ndata for laserdata


      openr,lun,file,/get_lun
      
      mast_struct=replicate({name:'',mult:0.0,offset:0.0,units:''},num_mast)
      readf,lun,mast_struct,format='(a30,f8.6,f7.3,a4)'
      
      dpu_struct=replicate({name:'',mult:0.0,offset:0.0,units:''},num_dpu)
      readf,lun,dpu_struct,format='(a30,f8.6,f7.3,a4)'

      switch_struct=replicate({name:'',status:strarr(2)},16)
      readf,lun,switch_struct,format='(a30,a8,a8)'
laser_struct=replicate({name:'',mult:0.0,offset:0.0,units:''},ndata)
                readf,lun,laser_struct,format='(a30,f8.6,f7.3,a4)'

      
      free_lun,lun

return
end
