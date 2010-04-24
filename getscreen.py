import pygame
print "Initializing Pygame Display"

pygame.display.init()
splash = pygame.image.load('data/splash.png').convert(32)
print "Setting Pygame Mixer Configuration"
pygame.mixer.pre_init(44100,16,256)
print "Initializing Pygame Mixer"
pygame.mixer.init()
print "Setting Reserved Channels"
pygame.mixer.set_reserved(3)
print "Initializing Pygame"
pygame.init()
import os
os_screen = pygame.display.Info()
print "Setting SDV_VIDEO_CENTERED to True"
os.environ['SDL_VIDEO_CENTERED'] = '1'
print "Creating Splash Screen"
splash_surface = pygame.display.set_mode(splash.get_size(), pygame.NOFRAME).blit(splash,(0,0))
print "Creating and Setting Favicon"
pygame.display.set_icon(pygame.image.load("data/images/interface/favicon.png").convert_alpha())
print "Showing Splash Screen"
pygame.display.flip()
pygame.time.wait(5000)
