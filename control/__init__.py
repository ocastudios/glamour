import pygame
import interactive.universe as universe
from pygame.locals import *
from sys import exit
import interactive.stage as stage

def main_menu(universe):
    universe.click = False
    universe.action[0] = None
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                print "Escape pressed"
                exit()
            elif event.key == K_UP:
                universe.action[0] = 'up'
            elif event.key == K_DOWN:
                universe.action[0] = 'down'
            elif event.key == K_LEFT:
                universe.action[0] = 'left'
            elif event.key == K_RIGHT:
                universe.action[0] = 'right'
        elif event.type == KEYUP:
            if event.key in (K_a,K_b,K_c,K_d,K_e,K_f,K_g,K_h,K_i,K_j,K_k,K_l,K_m,K_n,K_o,K_p,K_q,K_r,K_s,K_t,K_u,K_v,K_w,K_x,K_y,K_z, K_BACKSPACE, K_SPACE):
                universe.action[0] = pygame.key.name(event.key)
            if event.key == K_RETURN:
                print "Enter pressed"
                universe.click = True
        elif event.type == MOUSEBUTTONUP:
            universe.click = True
    pygame.event.clear()

def stage(universe):
    pointersize = None
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if not universe.level.paused:
                    universe.level.pause.status = "inside"
                    universe.level.paused = True
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
        elif event.type == KEYUP:
            universe.action[0]=None
            if universe.level.princesses[0]:
                universe.level.princesses[0].doonce = False
            if (universe.dir == 'left' and event.key == K_LEFT) or (universe.dir == 'right' and event.key == K_RIGHT):
                universe.action[1] = 'stay'
        elif event.type == USEREVENT:
            pygame.mixer.music.queue(universe.level.music)
        elif event.type == MOUSEMOTION:
            pointersize = pointersize or universe.level.game_mouse.size
            mouse_pos           = pygame.mouse.get_pos()
            universe.level.game_mouse.pos = (mouse_pos[0]-(pointersize[0]/2),mouse_pos[1]-(pointersize[1]/2))

        if event.type == MOUSEBUTTONUP:
            universe.click = True
        else:
            universe.click = False

        if universe.action[1] == 'walk' and universe.action[0] == 'open_door':
            universe.action[0] = None

    pygame.event.clear()

def story_menu(universe):
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
