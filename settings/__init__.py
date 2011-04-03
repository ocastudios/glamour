import os
import pygame

def welcome():    ####temporary hard coded scale ####
    print "###  Welcome to Glamour  ###"
    print "This is an Open Source/Public Domain game developed by Oca Studios"
    print 'The game is based on the "Glamour" table-top game by Oca Studios'
    print "in loving memory of Cilda and Patricia"
    print "Feel free to contribute at www.ocastudios.com"
    print "or visit the project at http://launchpad.net/glamour"
    print "... lauching game ..."

def initialize_mixer():
    print "Setting Pygame Mixer Configuration"
    #pygame.mixer.pre_init(44100,16,256)
    print "Initializing Pygame Mixer"
    pygame.mixer.init()
    print "Setting Reserved Channels"
    pygame.mixer.set_reserved(3)
    print "Initializing Pygame"

welcome()
import os
import os
import pygame

print "Initializing Pygame Display"
pygame.display.init()
pygame.display.set_caption("Glamour - OcaStudios")

#### Princesses #### 
Snow_White      = {'skin': 'pink', 'hair': 'hair_snowwhite', 'icon': 'princess-icon-apple.png',   'name' : 'Snow_White'}
Cinderella      = {'skin': 'tan' , 'hair': 'hair_cinderella','icon': 'princess-icon-shoe.png'   , 'name' : 'Cinderella'}
Rapunzel        = {'skin': 'pink', 'hair': 'hair_rapunzel'  ,'icon': 'princess-icon-brush.png'  , 'name' : 'Rapunzel'}
Sleeping_Beauty = {'skin': 'pink', 'hair': 'hair_sleeping'  ,'icon': 'princess-icon-spindle.png', 'name' : 'Sleeping_Beauty'}

#### Screen Resolution ####
print "Detecting screen resolution"

os_screen = pygame.display.Info()

resolution = os_screen.current_w,os_screen.current_h

if resolution[0] < 1440:
    scale = resolution[0]/1440.0
    if 900*scale > resolution[1]:
        scale = resolution[1]/900.0
else:
    scale = 1
print "The game will run with resolution "+str(round(1440*scale))+"x"+str(round(900*scale))
if scale < 0.3333333337:
    scale = 0.333333337
####              temporary hard coded scale            ####
#### used to develop in a different resolution in order #### 
#scale = 0.666666667


#### Scale function ####
def p(positions,r=True):
    if positions.__class__ in (list, tuple):
        if round:
            return [int(round(i*scale)) for i in positions ]
        else:
            return [i*scale for i in positions]
    elif positions.__class__ in (int,float):
        if round:
            return round(positions*scale)
        else:
            return positions*scale

def d(positions,r=True):
    if positions.__class__ in (list, tuple):
        if round:
            return [int(round(i/scale)) for i in positions ]
        else:
            return [i/scale for i in positions]
    elif positions.__class__ in (int,float):
        if round:
            return round(positions/scale)
        else:
            return positions/scale
#### Main directories ####


homedir = os.path.expanduser('~')
main_dir    = os.path.join('/','home','nelson','glamour')
data_dir    = os.path.join(main_dir,"data")
saves_dir   = os.path.join(homedir ,'.glamour')
try:
    os.listdir(saves_dir)
except:
    os.mkdir(saves_dir)

#### Translation function ####
import gettext
localization_support = gettext.translation('glamour', os.path.join(main_dir,'locale'))
t = localization_support.ugettext
