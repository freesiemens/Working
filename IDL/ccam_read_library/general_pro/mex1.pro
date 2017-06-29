FUNCTION MEX1,  SIGMA
n=round(sigma*4.5)

X=(FINDGEN(2*N+1)-N)^2.
F=(1-X/SIGMA^2)*EXP(-X/(2*SIGMA^2))/(SIGMA*SQRT(2*!PI))
RETURN,F/total(abs(f))
END












