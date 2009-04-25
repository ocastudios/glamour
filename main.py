#!/usr/bin/env python

from getscreen import *
from globals import *
from pygame.locals import *
pygame.mixer.init()
import random
from sys import exit
from math import *
from random import randint
import game_clock
import obj_images
from numpy import uint8
import camera
import mousepointer
import menu
import universe
import control



#Create lists


clock = pygame.time.Clock()
universe = universe.Universe(os_screen.current_w,os_screen.current_h)

gamemenu = menu.MenuScreen((360,200))

screen_surface = pygame.display.set_mode((os_screen.current_w,os_screen.current_h),FULLSCREEN,32)

while True:
    while universe.level == 'menu':
        control.main_menu(universe)
        gamemenu.update_all(screen_surface)
        pygame.display.flip()
    while universe.level == 'choose':
        control.choose_menu(universe)
        gamemenu.update_choose(screen_surface)
        pygame.display.flip()


    universe.define_level()


    universe.actual_level.instantiate_stuff()
    game_mouse = mousepointer.MousePointer(universe.mouse_pos,universe.actual_level)
    gamecamera = camera.GameCamera(universe.actual_level)

    run_level = True


    pygame.mouse.set_visible(0)

    while run_level:
        for i in universe.actual_level.gates:
            if i.change_level:
                universe.level = i.level
                gamemenu.mainmenu.level = i.level
                run_level = False
                i.change_level = False
                break
        control.stage(universe)
        game_mouse.update()
        time_passed = clock.tick(15)
        screen_surface.fill([255,255,255])
        universe.actual_level.update_all(screen_surface,universe.action,universe.dir,universe)
        universe.clock_pointer.update_image()
        pygame.display.flip()

    screen_surface.fill([0,0,0])
    pygame.display.flip()

    run_level = True

    for attr,value in universe.level.__dict__.iteritems():
        exec('universe.level.'+attr+'= None')

    del universe.level
    universe.level = 'menu'
