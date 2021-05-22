from turtle import *

from random import randint # randint function returns random number

# speed of pen
speed(0)
                    
bgcolor('black')
      
x = 1
      
while x < 400:
    
    # changes color eveyr time through the loop
	# gets individual compenents
	# random numbers in color range
    r = randint(0,255)
    g = randint(0,255)
    b = randint(0,255)

    colormode(255) # initializes color mode
    
    
    pencolor(r,g,b) # changes the color of the pen to the rgb coordinates
    
    # moves pen in a square motion
    fd(50 + x)
    rt(90.911)
    
    # iterate through the loop
    x = x+1 

exitonclick() 
