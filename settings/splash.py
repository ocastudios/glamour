import pygame
import os
from settings import directory


def splash_image():
    splash = pygame.image.load(os.path.join(directory.data,'splash.png')).convert(32)
    splash_size = splash.get_size()
    print "Setting SDV_VIDEO_CENTERED to True"
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    print "Creating Splash Screen"

    splash_surface = pygame.display.set_mode(splash_size, pygame.NOFRAME).blit(splash,(0,0))
    print "Creating and Setting Favicon"
    pygame.display.set_icon(pygame.image.load(os.path.join(directory.interface,'favicon.png')).convert_alpha())
    print "Showing Splash Screen"
    pygame.display.flip()
