import pygame
from settings import *
splash = pygame.image.load(main_dir+'/data/splash.png').convert(32)
splash_size = splash.get_size()
print "Setting Pygame Mixer Configuration"
#pygame.mixer.pre_init(44100,16,256)
print "Initializing Pygame Mixer"
pygame.mixer.init()
print "Setting Reserved Channels"
pygame.mixer.set_reserved(3)
print "Initializing Pygame"
pygame.init()
import os

print "Setting SDV_VIDEO_CENTERED to True"
os.environ['SDL_VIDEO_CENTERED'] = '1'
print "Creating Splash Screen"

splash_surface = pygame.display.set_mode(splash_size, pygame.NOFRAME).blit(splash,(0,0))
print "Creating and Setting Favicon"
pygame.display.set_icon(pygame.image.load(main_dir+"/data/images/interface/favicon.png").convert_alpha())
print "Showing Splash Screen"
pygame.display.flip()

import utils.obj_images as obj_images

import os

print 'preparing drapes'
drape_images = obj_images.OneSided(main_dir+'/data/images/interface/omni/drapes/rendered_drapes/')
prep_images = drape_images.list
'done'
