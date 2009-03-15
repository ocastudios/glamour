#!/usr/bin/env python

from getscreen import *
from globals import *
import camera
import mousepointer
import menu
import os
from pygame.locals import *


gamemenu = menu.MenuScreen((360,200))
mainmenu = menu.Menu(gamemenu)
mainmenu.instantiate_stuff()
level = 'menu'
screen_surface = pygame.display.set_mode((os_screen.current_w,os_screen.current_h),FULLSCREEN,32)
while level == 'menu':
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            if event.key == K_i:
                level = Level_01
            elif event.key == K_e:
                level = Level_02

    gamemenu.update_all(screen_surface)
    try:
        if once:
            pygame.display.update((0,0),(900,900))
    except:
        pygame.display.flip()
        once = True



game_clock = GameClock(level)
clock_pointer = ClockPointer(level)
#level.bathhouse_street(clock_pointer)
level.instantiate_stuff(clock_pointer)



mouse_pos = pygame.mouse.get_pos()
game_mouse = mousepointer.MousePointer(mouse_pos,level)
gamecamera = camera.GameCamera([level])
screen_surface = pygame.display.set_mode((os_screen.current_w,os_screen.current_h),FULLSCREEN,32)

pygame.mouse.set_visible(0)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
#            fecha = os.popen2('killall ogg123')
            del level.musica
            break
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            if event.key == K_LEFT:
                dir = 'left'
                action[1] = 'move'
            if event.key == K_RIGHT:
                dir = 'right'
                action[1] = 'move'
            if event.key == K_LCTRL:
                action[0] = 'kiss'
            if event.key == K_LSHIFT:
                action[0] = 'spin'
            if event.key == K_SPACE:
                action[0] = 'celebrate'
            if event.key == K_UP:
                if level.princess.jump == 0:
                    action[0] ='jump'

            if event.key == K_c:
                action[0] = 'change'
            if event.key == K_i:
                action[0] = 'changedress'
            if event.key == K_h:
                action[0] = 'changehair'

        elif event.type == KEYUP:
            action[0]=None
            level.princess.doonce = False
            if (dir == 'left' and event.key == K_LEFT) or (dir == 'right' and event.key == K_RIGHT):
                action[1] = 'stand'

    game_mouse.update()
    time_passed = clock.tick(15)
    screen_surface.fill([255,255,255])
    level.update_all(screen_surface,action,dir,universe,clock_pointer)
    clock_pointer.update_image()

    pygame.display.flip()
exit()
