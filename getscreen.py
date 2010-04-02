import pygame
pygame.display.init()

splash = pygame.image.load('data/splash.png').convert(32)
pygame.mixer.pre_init(44100,16,256)
pygame.mixer.init()
pygame.mixer.set_reserved(3)
pygame.init()
import os
os_screen = pygame.display.Info()
os.environ['SDL_VIDEO_CENTERED'] = '1'
splash_surface = pygame.display.set_mode(splash.get_size(), pygame.NOFRAME).blit(splash,(0,0))
pygame.display.flip()
pygame.time.wait(5000)
