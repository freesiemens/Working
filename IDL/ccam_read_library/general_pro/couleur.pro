pro couleur, name = name

;
;  set some color table
;  many colors (start with basics), name return their name
;


;
;  Read X11 colors
;

    openr,1,!ccam_pro+'rgb.txt'

    b = ' '
    readf,1,b

    red = 0. & green = 0. & blue = 0.
    name = 'name'

    while not eof(1) do begin

	readf,1,b

	red = [red, float(strmid(b,0,3))]
        green = [green, float(strmid(b,4,3))]
        blue = [blue, float(strmid(b,8,3))]
        name = [name, strmid(b,13,20),' ']

    endwhile

    close,1

    green = green[1:*]
    blue = blue[1:*]
    red = red[1:*]
    name = strlowcase(name[1:*])

    a1 = string(red,format='(i3.3)')
    a2 = string(blue,format='(i3.3)')
    a3 = string(green,format='(i3.3)')
    aa = a1+a2+a3

    s = uniq(aa)
    green = green[s]
    blue = blue[s]
    red = red[s]
    name = name[s]

    red1   = [0, 1, 1, 0, 0, 1, 0, 1,1]*255
    green1 = [0, 1, 0, 1, 0, 1, 1, 0,0]*255
    blue1  = [0, 1, 0, 0, 1, 0, 1, 1,0]*255
    name1 = ['black','white','red','green','blue','yellow','cyan','magenta']

    ; first color table

    d1 = findgen(124)*2

    red_1 = [red1,red[d1],red[d1+256]]
    green_1 = [green1,green[d1],green[d1+256]]
    blue_1 = [blue1,blue[d1],blue[d1+256]]
    name_1 = [name1,name[d1],name[d1+256]]


        ;message,' Loading table 256 colors',/continue

	red = red_1
        green = green_1
        blue = blue_1
        name = name_1

	red[9] = red[58]
	green[9] = green[58]
	blue[9] = blue[58]
	name[9] = name[58]


	red_8old=red[8]
	green_8old=green[8]
	blue_8old=blue[8]
	name_8old=name[8]

	red[8] = red[41]
	green[8] = green[41]
	blue[8] = blue[41]
	name[8] = name[41]


	red_10old=red[10]
	green_10old=green[10]
	blue_10old=blue[10]
	name_10old=name[10]

	red[10] = red[220]
	green[10] = green[220]
	blue[10] = blue[220]
	name[10] = name[220]

	red_11old=red[11]
	green_11old=green[11]
	blue_11old=blue[11]
	name_11old=name[11]

	red[11] = red[61]
	green[11] = green[61]
	blue[11] = blue[61]
	name[11] = name[61]


	red_12old=red[12]
	green_12old=green[12]
	blue_12old=blue[12]
	name_12old=name[12]

	red[12] = red[31]
	green[12] = green[31]
	blue[12] = blue[31]
	name[12] = name[31]

;	red_13old=red[13]
;	green_13old=green[13]
;	blue_13old=blue[13]
;	name_13old=name[13]

	red[13] = red[204]
	green[13] = green[204]
	blue[13] = blue[204]
	name[13] = name[204]

	red_14old=red[14]
	green_14old=green[14]
	blue_14old=blue[14]
	name_14old=name[14]

	red[14] = red[158]
	green[14] = green[158]
	blue[14] = blue[158]
	name[14] = name[158]

	red_15old=red[15]
	green_15old=green[15]
	blue_15old=blue[15]
	name_15old=name[15]

	red[15] = red[24]
	green[15] = green[24]
	blue[15] = blue[24]
	name[15] = name[24]

	red[255] = 255
	green[255] = 255
	blue[255] = 255
	name[255] = 'blanc'

        tvlct, red, green, blue
        return

end
