#!/usr/bin/env python

from globals import *
from moving_scenario import *
from camera import *
from clouds import *
from enemy import *
from floor import *
from getscreen import *
from getscreen import os_screen
from glamour_stars import *
from mousepointer import *
from panel import *
from princess import *
from pygame.locals import *
from scenarios import *
from skies import *

try:
    import Numeric
    import pygame.surfarray as surfarray
except ImportError:
    raise ImportError, "Numeric and Surfarray are required."


pygame.display.init()
pygame.mixer.music.load("data/NeMedohounkou.ogg")
pygame.init()


def create_clouds(number):
    for i in range(number):
        nuvem = Cloud((random.randint(100,25000),random.randint(0,300)),[Level_01])
def create_trees(number):
    for i in range(number):
        tree = Scenario((random.randint(100,25000),random.randint(0,300)),'data/images/cenario/apple-tree/',[Level_01],1,1,'alea')
def create_posts(number):
    posts = [3000, 3600,5200, 5800]
    for i in posts:
        post = Scenario((i,0),'data/images/scenario/bathhouse_st/light_post/post/',[Level_01])
def create_floor(number):
    for i in range(number):
        floor = Floor(count,'data/images/scenario/bathhouse_st/floor/tile/',[Level_01])

#Instancing Stuff
bilboard = MovingScenario(1,[Level_01],'data/images/scenario/bathhouse_st/billboard_city/billboard/')
gate1 = Gate((300,0),'data/images/scenario/omni/gate/',[Level_01],index = 0)
bathhouse = Scenario((550,0),'data/images/scenario/bathhouse_st/bathhouse/bathhouse/',[Level_01],index =0)
smallhouse = Scenario((3400,100),'data/images/scenario/bathhouse_st/small_house/base/',[Level_01],index =0)
home = Scenario((3800,100),'data/images/scenario/bathhouse_st/home/castelo/',[Level_01],index =0)
#bathhouse_door = Scenario((920,90),'data/images/scenario/bathhouse_st/bathhouse/door_close/',[Level_01])
carriage = Carriage(3,'data/images/enemies/carriage/',3000,[Level_01],[10,10,10,10],[10,10,10,10],[10,10,10,10])
oldlady = OldLady(2,'data/images/enemies/old_lady/',4000,[Level_01])
schnauzer = Schnauzer(10,'data/images/enemies/schnauzer/',2600,[Level_01],[22,22,22,22],[22,22,22,22],[22,22,22,22],dirty=True)
butterflies = Butterfly(4,'data/images/enemies/butterflies/',6000,[Level_01])
fundo = Sky('data/images/scenario/skies/daytime/daytime.png',[Level_01],clock_pointer)
create_posts(15)
create_floor(30)
create_clouds(50)
Main_Star= Glamour_Stars((0,0),True)

try:       pygame.mixer.music.play()
except:    print "Warning: no music loaded."

princess = Princess([Level_01])
info_glamour_points = Data('', princess.glamour_points, (300, 0), [Level_01],0,size=120)
castle = Background((110,0),[Level_01],0,'data/images/scenario/ballroom/ballroom_day/')
pygame.init()
stage = Level_01
japanese_bridge = Bridge('data/images/scenario/bathhouse_st/floor/japanese_bridge/',4,[Level_01])
mouse_pos = pygame.mouse.get_pos()
mousepointer = MousePointer(mouse_pos,[Level_01])


screen_surface = pygame.display.set_mode((os_screen.current_w,os_screen.current_h),FULLSCREEN,32)
gamecamera = GameCamera([Level_01])


pygame.mouse.set_visible(0)
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
                    princess.jump_sound.play()
            if event.key == K_c:
                action[0] = 'change'
            if event.key == K_i:
                action[0] = 'changedress'
            if event.key == K_h:
                action[0] = 'changehair'

                
        elif event.type == KEYUP:
            action[0]=None
            princess.doonce = False
            if (dir == 'left' and event.key == K_LEFT) or (dir == 'right' and event.key == K_RIGHT):
                action[1] = 'stand'
    mouse_pos = pygame.mouse.get_pos()
    mousepointer.update(mouse_pos)
    keystate = pygame.event.get()
    time_passed = clock.tick(15)
    screen_surface.fill([255,255,255])

    info_glamour_points.update(princess.glamour_points)
    stage.blit_all(screen_surface,action,dir,universe,clock_pointer)

    clock_pointer.update_image()

    pygame.display.update()
