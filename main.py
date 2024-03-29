#!/usr/bin/python3
# -*- coding: utf-8 -*-
print("###  Welcome to Glamour  ###")
print("This is an Open Source/Public Domain game developed by Oca Studios")
print('The game is based on the "Glamour" table-top game by Oca Studios')
print("in loving memory of Cilda and Patricia")
print("Feel free to contribute at www.ocastudios.com")
print("or visit the project at http://launchpad.net/glamour")
print("... lauching game ...")
print("Initializing Pygame Display")

import os
import pygame
import settings
from settings import directory
from interface.splash import splash
from interface.icon import set_icon

splash()
set_icon()

pygame.mixer.pre_init(44100, 16, 256)
settings.reset_scale()
pygame.mixer.init()
pygame.mixer.set_num_channels(9)
pygame.mixer.set_reserved(9)

pygame.init()

import interactive.universe as universe
import interface.menu as menu
import control
import settings
import sqlite3
import sys

try:
    test = sys.argv[1] == 'test'
except IndexError:
    test = False

if __name__ == "__main__":
    universe = universe.Universe(test=test)
    pygame.mouse.set_visible(0)
    while True:
        if universe.LEVEL == "menu":
            control.main_menu(universe)
        elif universe.LEVEL == "game":
            control.stage(universe)
        universe.update_all()
        pygame.display.flip()
