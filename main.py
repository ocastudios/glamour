#!/usr/bin/env python
#importando modulosimport pygame
from getscreen import *
import os
import random
from math import *
from pygame.locals import *
from sys import exit
from princess import *
from clouds import *
from bunny import *
from scenarios import *
from enemy import *
from glamour_stars import *
from globals import *
from moving_scenario import *
from skies import *
from panel import *
pygame.display.init()
pygame.mixer.pre_init(44100, 8, 1, 4096)
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("data/NeMedohounkou.ogg")+

def create_clouds(number):
    count = 0
    while count <= number:
        nuvem = Cloud((random.randint(100,25000),random.randint(0,300)),[Level_01])
        count += 1


#Scenario((0,88),'data/images/scenario/bathhouse_st/billboard_city/',[Level_01],0,0.5)

def compare_deep(x,y):
    if x.deep>y.deep:
        return 1
    elif x.deep == y.deep:
        return 0
    else:
        return -1

def create_trees(number):
    count = 0
    while count <= number:
        tree = Scenario((random.randint(100,25000),random.randint(0,300)),'data/images/cenario/apple-tree/',[Level_01],1,1,'alea')
        #scenario_stuff.append(tree)
        count += 1
def create_posts(number):
    count =0
    while count <= number:
        post = Scenario((count*500,100),'data/images/scenario/bathhouse_st/light_post/post/',[Level_01])
        count += 1
def create_floor(number):
    count = 0
    while count <= number:
        floor = Floor(count,'data/images/scenario/bathhouse_st/floor/tile/',[Level_01])
        count +=1


bilboard = MovingScenario(1,[Level_01],'data/images/scenario/bathhouse_st/billboard_city/billboard/')



#main_panel = Panel((0,0),(os_screen.current_w, 100),None)

schnauzer = Schnauzer(10,'data/images/enemies/schnauzer/',2600,[Level_01],[22,22,22,22],[22,22,22,22],[22,22,22,22],dirty=True)
carriage = Carriage(3,'data/images/enemies/carriage/',3000,[Level_01],[10,10,10,10],[10,10,10,10],[10,10,10,10])
butterflies = Butterfly(4,'data/images/enemies/butterflies/',6000,[Level_01])
#casa = Scenario((750,universe.floor-315),'data/casa/',[Level_01])

fundo = Sky('data/images/scenario/skies/daytime/daytime.png',[Level_01])
#fundo = pygame.image.load('data/images/scenario/skies/daytime/daytime.png').convert()

#Instance Stuff
#create_trees(20)
create_posts(15)
create_floor(30)
create_clouds(50)
Main_Star= Glamour_Stars((0,0),True)
#while count < 10:
#    Glamour_Stars((random.randint(1600,10600),random.randint(300,700)))
#    Bunny((random.randint(1400,15000),150))
#    count +=1
try:
    pygame.mixer.music.play()
except:
    print "Warning: no music loaded."

info_glamour_points = Data('Glamour Points', princess.glamour_points, (0, 100), [Level_01],0,160)
info_schnauzer_pos = Data('Enemy pos',schnauzer.pos, (0,0),[Level_01],1)
info_princess_life = Data('Life',princess.life, (0,50), [Level_01],2)
info_schnauzer_rect = Data('Enemy rect',schnauzer.rect, (0,150),[Level_01],3)
info_princess_rect = Data('princess rect',princess.rect, (0,200), [Level_01],4)
castle = Background((110,0),[Level_01],0,'data/images/scenario/ballroom/ballroom_day/')
pygame.init()
#create_screen()
#Grande Loop
stage = Level_01
#create_screen()
screen_surface = pygame.display.set_mode((os_screen.current_w,os_screen.current_h),FULLSCREEN,32)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
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
                if princess.jump == 0:
                    action[0] ='jump'
            if event.key == K_c:
                action[0] = 'change'
            if event.key == K_i:
                action[0] = 'changedress'
        elif event.type == KEYUP:
            action[0]=None
            princess.doonce = False
            if (dir == 'left' and event.key == K_LEFT) or (dir == 'right' and event.key == K_RIGHT):
                action[1] = 'stand'
    #desenha o fundo
    #screen_surface.blit(fundo,(0,0))
    keystate = pygame.event.get()
    time_passed = clock.tick(12)    
    #screen_surface.fill([255,255,255])
    info_schnauzer_pos.update(schnauzer.pos)
    info_glamour_points.update(princess.glamour_points)
    info_princess_life.update(princess.life)
    info_schnauzer_rect.update(schnauzer.rect)
    info_princess_rect.update(princess.rect)
#    for n in clouds:
#        n.movement(dir, action)
#        screen_surface.blit(n.image,n.pos)
    stage.blit_all(screen_surface,action,dir)
    #clouds.sort(compare_deep)
    princess.control(dir,action)
    princess.ive_been_caught()
    for star in stars:
        if star.fixed!= True:
            star.move()
        else:
            star.update_images()
    if action[1] == 'move':
        universe.movement(dir,10)
    
    for b in bunnies:
        b.set_pos()
        screen_surface.blit(b.image,b.pos)
    


    clock_pointer.update_image()

    pygame.display.update()
