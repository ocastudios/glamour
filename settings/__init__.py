import os
import pygame
import pygame
print "Welcome to Glamour"
print "This is an Open Source/Public Domain game developed by Oca Studios"
print "Feel free to contribute at www.ocastudios.com"
print "or visit the project at http://launchpad.com/glamour"
print "..."
print "Initializing Pygame Display"
pygame.display.init()

os_screen = pygame.display.Info()
resolution = os_screen.current_w,os_screen.current_h

if resolution[0] < 1440:
    scale = resolution[0]/1440
    if 900*scale > resolution[1]:
        scale = resolution[1]/900
else:
    scale = 1

scale =0.666666667


main_dir = os.getcwd()
Snow_White      = {'skin': 'pink', 'hair': 'hair_snowwhite', 'icon': 'princess-icon-apple.png',   'name' : 'Snow_White'}
Cinderella      = {'skin': 'tan' , 'hair': 'hair_cinderella','icon': 'princess-icon-shoe.png'   , 'name' : 'Cinderella'}
Rapunzel        = {'skin': 'pink', 'hair': 'hair_rapunzel'  ,'icon': 'princess-icon-brush.png'  , 'name' : 'Rapunzel'}
Sleeping_Beauty = {'skin': 'pink', 'hair': 'hair_sleeping'  ,'icon': 'princess-icon-spindle.png', 'name' : 'Sleeping_Beauty'}
def p(positions):
    return [int(round(i*scale)) for i in positions ]
