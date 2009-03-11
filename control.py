import pygame
from pygame.locals import *



def get_keyboard():
    for event in pygame.event.get():
        if 

control_result = {}
while True:
    for event in pygame.event.get():
        if event.type == KEYUP:
            if event.key == K_LCTRL:
                control_result['action']    = 'kiss'
            if event.key == K_LSHIFT:
                control_result['action']    = 'spin'
            if event.key == K_SPACE:
                control_result['action']    = 'celebrate'
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                control_result['direction'] ='left'
                control_result['movement']  = 'move'
            if event.key == K_RIGHT:
                control_result['direction'] = 'right'
                control_result['movement']  = 'move'
            if event.key == K_UP:
                if doll.jump == 0:
                    control_result['action']='jump'
            if event.key == K_c:
                action[0] = 'change'
            if event.key == K_i:
                action[0] = 'changedress'
            if event.key == K_h:
                action[0] = 'changehair'

        elif event.type == KEYUP:
            action[0]=None
            doll.doonce = False
            if (dir == 'left' and event.key == K_LEFT) or (dir == 'right' and event.key == K_RIGHT):
                action[1] = 'stand'
    mouse_pos = pygame.mouse.get_pos()
    game_mouse.update(mouse_pos)
    keystate = pygame.event.get()
    time_passed = clock.tick(15)
    screen_surface.fill([255,255,255])
    info_glamour_points.update(doll.glamour_points)
    stage.blit_all(screen_surface,action,dir,universe,clock_pointer)

    clock_pointer.update_image()

    pygame.display.update()
