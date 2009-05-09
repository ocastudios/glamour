import pygame
pygame.mixer.init(11025,8,1,4096)
pygame.display.init()

splash = pygame.image.load('data/splash.png').convert(32)
pygame.init()
import os
os_screen = pygame.display.Info()
os.environ['SDL_VIDEO_CENTERED'] = '1' 
splash_surface = pygame.display.set_mode(splash.get_size(), pygame.NOFRAME).blit(splash,(0,0))
pygame.display.flip()
