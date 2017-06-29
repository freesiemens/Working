
      CCAM_init

;  RMI test

      ;  Test of data AFTER SW change
      path = !ChemCam_gdata + '\ATLO_FSWupdate\RMI_RAW\'
      files = file_search(path + 'CcamRmiImage*.dat', count=n)
       
      image = CCAM_read_rmi(files[10], /verbose)

      ;  Test of data BEFORE SW change
      path = !ChemCam_gdata + '\ATLO_STT\RMI_RAW\'
      files = file_search(path + 'CcamRmiImage*.dat', count=n)
       
      image = CCAM_read_rmi(files[4], /verbose)
      
;  LIBS test
 
      ;  Test of data AFTER SW change
      path = !ChemCam_gdata + '\ATLO_FSWupdate\SPECTRA_RAW\'
      files = file_search(path + 'CcamSpectra*.dat', count=n)
       
      image = CCAM_read_libs(files[10], /verbose)
  
      ;  Test of data BEFORE SW change
      path = !ChemCam_gdata + '\ATLO_STT\Spectra_RAW\'
      files = file_search(path + 'CcamSpectra*.dat', count=n)
      
      spectra = CCAM_read_libs(files[2], /verbose)


end
