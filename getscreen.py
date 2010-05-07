import pygame
print "Initializing Pygame Display"

pygame.display.init()
splash = pygame.image.load('data/splash.png').convert(32)
print "Setting Pygame Mixer Configuration"
#pygame.mixer.pre_init(44100,16,256)
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
import obj_images
import os
from settings import *
size        = 1440*scale,900*scale
right_x     = 0
left_x      = 645*scale
prep_images = []
drapes_dir = os.getcwd()+'/data/images/interface/omni/drapes/drapes/'
drapes_tiles = [obj_images.image(drapes_dir+frame) for frame in sorted(os.listdir(drapes_dir))]
tile_index = 0
speed       = 0
print 'Preparing drapes'
while right_x > -1000*scale:
    drape_image = pygame.Surface(size,pygame.SRCALPHA)
    if tile_index < len(drapes_tiles):
        tile=drapes_tiles[tile_index]
        tile_index += 1
    else:
        tile=drapes_tiles[-1]
    tile_size = tile.get_size()
    [drape_image.blit(tile,(x,0)) for x in range(int(left_x),int(1440*scale),int(110*scale))]
    [drape_image.blit(pygame.transform.flip(tile,1,0),(x,0)) for x in range(int(right_x+(610*scale)),int(-200*scale),int(-110*scale))]
    right_x = right_x - speed
    left_x  = left_x  + speed
    if speed < 15*scale:
        speed += 3*scale
    prep_images.append(drape_image)
del drapes_dir, drapes_tiles, tile_index




#pygame.time.wait(5000)
