#!/usr/bin/python
# -*- coding: utf-8 -*-
print "###  Welcome to Glamour  ###"
print "This is an Open Source/Public Domain game developed by Oca Studios"
print 'The game is based on the "Glamour" table-top game by Oca Studios'
print "in loving memory of Cilda and Patricia"
print "Feel free to contribute at www.ocastudios.com"
print "or visit the project at http://launchpad.net/glamour"
print "... lauching game ..."
print "Initializing Pygame Display"

import os
import pygame

pygame.display.init()
pygame.display.set_caption("Glamour - OcaStudios")
import settings
from settings import directory

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
print "Setting Pygame Mixer Configuration"
#pygame.mixer.pre_init(44100,16,256)
print "Initializing Pygame Mixer"
pygame.mixer.init()
print "Setting Reserved Channels"
pygame.mixer.set_reserved(3)
print "Initializing Pygame"
import pygame
pygame.init()

import interactive.universe as universe
import interface.menu as menu
import control
import settings
import sqlite3

if __name__=="__main__":
	universe = universe.Universe()
	pygame.mouse.set_visible(0)
	while True:
		if universe.LEVEL == 'menu':
			control.main_menu(universe)
		elif universe.LEVEL == 'game':
			control.stage(universe)
		universe.clock.tick(universe.fps)
		universe.update_all()
		pygame.display.flip()
