import pygame
import os
from settings import directory


def splash_image():
#	splash = pygame.image.load(os.path.join(directory.data,'splash.png')).convert(32)
	introdir = os.path.join(directory.data,'images', 'intro','quanti')
	splash =[pygame.image.load(os.path.join(introdir,i)).convert(32) for i in sorted(os.listdir(introdir))]
	splash_size = splash[0].get_size()
	print "Setting SDV_VIDEO_CENTERED to True"
	os.environ['SDL_VIDEO_CENTERED'] = '1'
	print "Creating Splash Screen"

	splash_surface = pygame.display.set_mode(splash_size, pygame.NOFRAME)
	print "Creating and Setting Favicon"
	pygame.display.set_icon(pygame.image.load(os.path.join(directory.interface,'favicon.png')).convert_alpha())
	print "Showing Splash Screen"
	tempclock = pygame.time.Clock()
	for i in splash:
		splash_surface.blit(i,(0,0))
		pygame.display.flip()
		tempclock.tick(40)
	del tempclock
