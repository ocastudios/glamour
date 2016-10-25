import os
import pygame
import directory


#### Fonts ####
# Default fonts may be overriden when instantiating interfaces.widget.GameText class
main_font = "ArchitectsDaughter.ttf" #Ordinary texts
default_main_font_size = 28
second_font = "GreatVibes-Regular.ttf"  #Baroque texts
default_second_font_size = 40
third_font = main_font #Fairy speaches and keyboard
default_third_font_size = 20
default_fairy_font_size = 14

#### Princesses #### 
Snow_White = {'skin': 'pink', 'hair': 'hair_snowwhite', 'icon': 'princess-icon-apple.png', 'name': 'Snow_White'}
Cinderella = {'skin': 'tan' , 'hair': 'hair_cinderella','icon': 'princess-icon-shoe.png', 'name': 'Cinderella'}
Rapunzel = {'skin': 'pink', 'hair': 'hair_rapunzel', 'icon': 'princess-icon-brush.png', 'name': 'Rapunzel'}
Sleeping_Beauty = {'skin': 'pink', 'hair': 'hair_sleeping', 'icon': 'princess-icon-spindle.png', 'name' : 'Sleeping_Beauty'}

#### Mininum Glamour Points ####
# For each Ball the player will earn this much Glamour points unless the player did not change any garment
minimum_glamour_points = 1

#### Screen Resolution ####
print "Detecting screen resolution"

#### Screen Resolution ####
# Screen resolution is detected automatically if no custom_resolution is set
#custom_resolution = (800,600)
custom_resolution = None
screen_resolutions = {
	'high' : 0.8,
	'low' : 0.5,
}
active_resolution = 'high'
active_full = False
config_file = False
configurations = {}
if 'config' in os.listdir(directory.personal):
	config_file = open(os.path.join(directory.personal, 'config'),'r').read().split('\n')
	for i in config_file:
		c = [ii.strip() for ii in i.split(':')]
		if len(c)>1:
			configurations[c[0].lower()] = c[1]
if 'fullscreen' in configurations and configurations['fullscreen']=='True':
	active_full = True
if 'resolution' in configurations and configurations['resolution'] in ('high','low'):
	active_resolution = configurations['resolution']

os_screen = pygame.display.Info()

def reset_scale(percentage='high', full_screen = False):
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
	if not full_screen or percentage == 'low':
		scale = scale*screen_resolutions[percentage]
	if scale < 0.3333333337:
		scale = 0.333333337
	print "Game resolution: "+str(int(round(1440*scale)))+"x"+str(int(round(900*scale)))
	return scale

scale = reset_scale(percentage=active_resolution, full_screen=active_full)

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

# Calculating resulting resolution #
resolution = (p(1440),p(900))

#scale font size

if (scale!=1):
	main_font_size = int(round(p(default_main_font_size)))
	second_font_size = int(round(p(default_second_font_size)))
	third_font_size = int(round(p(default_third_font_size)))
	fairy_font_size = int(round(p(default_fairy_font_size)))
else:
	main_font_size = default_main_font_size
	second_font_size = default_second_font_size
	third_font_size = default_third_font_size
	fairy_font_size = int(round(p(default_fairy_font_size)))


#### Translation function ####
import gettext
import locale

current_locale, encoding = locale.getdefaultlocale()
for i in (directory.personal, 
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

#### Boyfriends ####
boyfriend_rank = (
		[  30,  70, 'gentleman_decent', t('Gentleman Decent')],
		[  70, 110, 'knight_reliable', t('Knight Reliable')],
		[ 110, 150, 'baron_serious', t('Baron Serious')],
		[ 150, 200, 'count_loving', t('Count Loving')],
		[ 200, 250, 'marquess_attractive', t('Marquess Attractive')],
		[ 250, 350, 'duke_intelligent', t('Duke Intelligent')],
		[ 350, 400, 'prince_charming', t('Prince Charming')],
		[ 400, 500, 'king_kindhearted', t('King Kindhearted')],
		[ 500, 700, 'emperor_awesome', t('Emperor Awesome')]
		)
