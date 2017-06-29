function coul8

r=bytarr(8)
g=bytarr(8)
b=bytarr(8)

r(0)=0 & g(0)=0 & b(0)=0
r(1)=255 & g(1)=0 & b(1)=0
r(2)=0 & g(2)=255 & b(2)=0
r(3)=0 & g(3)=0 & b(3)=255
r(4)=255 & g(4)=255 & b(4)=0
r(5)=255 & g(5)=0 & b(5)=255
r(6)=0 & g(6)=255 & b(6)=255
r(7)=255 & g(7)=255 & b(7)=255

tvlct,r,g,b
rgb=transpose(reform([r,g,b],8,3))

return,rgb
end
