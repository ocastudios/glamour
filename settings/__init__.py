import os
import pygame
import directory

#### Fonts ####
# Default fonts may be overriden when instantiating interfaces.widget.GameText class
main_font = "ArchitectsDaughter.ttf" #Ordinary texts
main_font_size = 30
second_font = "GreatVibes-Regular.otf"  #Baroque texts
second_font_size = 40
third_font = main_font #Fairy speaches and keyboard
third_font_size = 20

#### Screen Resolution ####
# Screen resolution is detected automatically if no custom_resolution is set
custom_resolution = None
custom_resolution = (800,600)

#### Princesses #### 
Snow_White = {'skin': 'pink', 'hair': 'hair_snowwhite', 'icon': 'princess-icon-apple.png',   'name' : 'Snow_White'}
Cinderella = {'skin': 'tan' , 'hair': 'hair_cinderella','icon': 'princess-icon-shoe.png'   , 'name' : 'Cinderella'}
Rapunzel = {'skin': 'pink', 'hair': 'hair_rapunzel'  ,'icon': 'princess-icon-brush.png'  , 'name' : 'Rapunzel'}
Sleeping_Beauty = {'skin': 'pink', 'hair': 'hair_sleeping'  ,'icon': 'princess-icon-spindle.png', 'name' : 'Sleeping_Beauty'}

#### Mininum Glamour Points ####
# For each Ball the player will earn this much Glamour points unless the player did not change any garment
minimum_glamour_points = 1

#### Screen Resolution ####
print "Detecting screen resolution"

os_screen = pygame.display.Info()
if not custom_resolution:
	resolution = os_screen.current_w,os_screen.current_h
else:
	resolution = custom_resolution
if resolution[0] < 1440:
	scale = resolution[0]/1440.0
	if 900*scale > resolution[1]:
		scale = resolution[1]/900.0
else:
	scale = 1
print "The game will run with resolution "+str(round(1440*scale))+"x"+str(round(900*scale))
if scale < 0.3333333337:
	scale = 0.333333337
####			  temporary hard coded scale			####
#### used to develop in a different resolution in order to avoid bugs#### 
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

#scale font size
if (scale!=1):
	main_font_size = int(round(p(main_font_size)))
	second_font_size = int(round(p(second_font_size)))
	third_font_size = int(round(p(third_font_size)))


#### Translation function ####
import gettext
import locale

current_locale, encoding = locale.getdefaultlocale()
for i in (	directory.personal, 
			directory.saves, 
			directory.cache, 
			os.path.join(directory.cache,'images'),
			):
	try:
		os.listdir(i)
	except:
		os.mkdir(i)

try:
	localization_support = gettext.translation('glamour', directory.locale, [current_locale])
except:
	localization_support = gettext.translation('glamour', directory.locale, ['en_US'])
	
localization_support.install()
t = localization_support.ugettext
