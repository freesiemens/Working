
function ccam_motor, x, $
                     pmotor = pmotor, distance = distance

     coef = [63.107, -70730., 0.00681936, 0.1987]
     
     if keyword_set(distance) then $ ;  turn motor into distance (in mm)
        y = (-coef[3]*x+coef[1])/(coef[2]*x-coef[0])
     
     if keyword_set(pmotor) then $  ; turn distance (mm) into pas moteur
        y = (coef[0]*x+coef[1])/(coef[2]*x+coef[3])

     return, y

end

