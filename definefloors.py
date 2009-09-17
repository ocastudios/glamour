# -*- coding: utf-8 -*-
#!/usr/bin/env python

import pygame
pygame.display.init()
pygame.init()
import os
os_screen = pygame.display.Info()
os.environ['SDL_VIDEO_CENTERED'] = '1' 

os_screen = pygame.display.Info()
screen = pygame.display.set_mode((os_screen.current_w,os_screen.current_h),pygame.FULLSCREEN,32)
directory = 'data/images/reference/overviews/'
savefile  = 'bathhouse_stadj'
background = pygame.image.load(directory+savefile+'.png').convert_alpha()

x = 0
y = 0
d = 0
a = 0
speed = 1
xlist = range(9001)
mouse_pos = [x+d,y+a]
command = None
floorlist = [0]*9001

while True:
    screen.fill((255,255,255))
    screen.blit(background,(x,y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                count = 0
                result = []
                for i in floorlist:
                    if i == 0:
                        i = 186
                    result.append(i)
                    count += 1
                open(directory+savefile+'.txt','w').write(str(result))
                exit()

            if event.key == pygame.K_LEFT:
                command = 'l'
            elif event.key == pygame.K_RIGHT:
                command = 'r'
            elif event.key == pygame.K_SPACE:
                command = None
            elif event.key == pygame.K_UP:
                speed += 1
            elif event.key == pygame.K_DOWN:
                speed -= 1
            else:
                command = None




    if command == 'l':
        x += speed
    if command == 'r':
        x -= speed
    


    mpos = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed() == (1,0,0):
        floorlist[mpos[0]+abs(x)]=mpos[1]
    for i in range(9001):
        screen.fill((0,0,0),pygame.Rect((i+x,floorlist[i]),(3,3)))

    if x > 0:
        x = 0
    if x < -9001:
        x = -9001
    pygame.display.flip()


