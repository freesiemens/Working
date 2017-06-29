pro zero, nice=nice, couleur = couleur

	!ymax=!ymin
	!xmax=!xmin
	
	!p.multi=0
	!p.region=0
	!p.ticklen=0.02
	!p.position=0

	!mtitle='!6'
	!ytitle=''
	!xtitle=''

	!p.background = 0
        !p.color = 255
	!p.thick=1
	!p.charthick=1
	!p.charsize=1.
        !x.thick = 1
        !y.thick = 1
        !p.font = -1

   if keyword_set(couleur) then couleur

   if keyword_set(nice) then begin

	!p.background = 255
        !p.color = 0
        !p.thick=1
        !x.thick=1
        !y.thick=1
        !p.charsize=1.
        !p.charthick=1.3
	!p.font = -1

        if !d.name eq 'PS' then begin

       		!p.font=0 
		device,/helvetica,isolatin1=0

        endif

   endif

	return
	end
