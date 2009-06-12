import pygame
from pygame.locals import *

def main_menu(universe):
    universe.click = False
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            if event.key == K_i:
                universe.LEVEL = 'close'
            elif event.key == K_e:
                universe.LEVEL = 'close'
            elif event.key == K_a:
                universe.LEVEL = 'close'
        if event.type == MOUSEBUTTONUP:
            universe.click = True
        else:
            universe.click = False
    pygame.event.clear()
def choose_menu(universe):
    universe.click = False
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            if event.key == K_i:
                universe.LEVEL = 'close'
            elif event.key == K_e:
                universe.LEVEL = 'close'
            elif event.key == K_a:
                universe.LEVEL = 'close'
        if event.type == MOUSEBUTTONUP:
            universe.click = True
        else:
            universe.click = False
    pygame.event.clear()
def name_menu(universe):
    universe.click = False
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            if event.key == K_i:
                universe.LEVEL = 'start'
            elif event.key == K_e:
                universe.LEVEL = 'start'
            elif event.key == K_a:
                universe.LEVEL = 'start'
        if event.type == MOUSEBUTTONUP:
            universe.click = True
        else:
            universe.click = False
    pygame.event.clear()
def stage(universe):
    for event in pygame.event.get():
        if event.type == QUIT:
            universe.level.princesses[0].save()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                universe.level.princesses[0].save()
                exit()
            if event.key == K_LEFT:
                universe.dir = 'left'
                universe.action[1] = 'walk'
            if event.key == K_RIGHT:
                universe.dir = 'right'
                universe.action[1] = 'walk'
            if event.key == K_LCTRL:
                universe.action[0] = 'kiss'
            if event.key == K_SPACE:
                universe.action[0] = 'jump'
            if event.key == K_UP:
                if universe.level.princesses[0].jump == 0:
                    universe.action[0] ='open_door'
            if event.key == K_y:
                universe.action[0]='celebrate'
            if event.key == K_c:
                universe.action[0] = 'change'
            if event.key == K_i:
                universe.action[0] = 'changedress'
            if event.key == K_h:
                universe.action[0] = 'changehair'
            if event.key == K_x:
                universe.action[0] = 'changehair2'
            if event.key == K_s:
                universe.action[0] = 'changeshoes'
            if event.key == K_p:
                universe.action[0] = 'changeskin'
            if event.key == K_z:
                universe.action[0] = 'yellow_dress'
        elif event.type == KEYUP:
            universe.action[0]=None
            if universe.level.princesses[0]:
                universe.level.princesses[0].doonce = False
            if (universe.dir == 'left' and event.key == K_LEFT) or (universe.dir == 'right' and event.key == K_RIGHT):
                universe.action[1] = 'stay'

        if event.type == MOUSEBUTTONUP:
            universe.click = True
        else:
            universe.click = False
    pygame.event.clear()
