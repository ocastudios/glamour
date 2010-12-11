import pygame




splash = pygame.image.load('data/splash.png').convert(32)
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


from settings import *
splash_surface = pygame.display.set_mode(splash_size, pygame.NOFRAME).blit(splash,(0,0))
print "Creating and Setting Favicon"
pygame.display.set_icon(pygame.image.load("data/images/interface/favicon.png").convert_alpha())
print "Showing Splash Screen"
pygame.display.flip()

import utils.obj_images as obj_images

import os




size        = 1440,900
right_x     = 0
left_x      = 645
prep_images = []
drapes_dir = os.getcwd()+'/data/images/interface/omni/drapes/drapes/'
drapes_tiles = [pygame.image.load(drapes_dir+frame).convert_alpha() for frame in sorted(os.listdir(drapes_dir))]
tile_index = 0
speed       = 0
print 'Preparing drapes'
while right_x > -1000:
    drape_image = pygame.Surface(size,pygame.SRCALPHA)
    if tile_index < len(drapes_tiles):
        tile=drapes_tiles[tile_index]
        tile_index += 1
    else:
        tile=drapes_tiles[-1]
    tile_size = tile.get_size()
    [drape_image.blit(tile,(x,0)) for x in range(int(left_x),int(1440),int(110))]
    [drape_image.blit(pygame.transform.flip(tile,1,0),(x,0)) for x in range(int(right_x+(610)),int(-200),int(-110))]
    right_x = right_x - speed
    left_x  = left_x  + speed
    if speed < 15:
        speed += 3
    prep_images.append(obj_images.scale_image(drape_image))
del drapes_dir, drapes_tiles, tile_index




#pygame.time.wait(5000)
