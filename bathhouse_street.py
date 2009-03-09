#!/usr/bin/env python

from getscreen import *
from globals import *
import moving_scenario
import camera
import clouds
import enemy
import floors
import glamour_stars
import mousepointer
import panel
import princess
from pygame.locals import *
import scenarios
import skies

pygame.display.init()
pygame.mixer.music.load("data/NeMedohounkou.ogg")
pygame.init()

def create_clouds(number):
    count = 0
    while count <= number:
        nuvem = clouds.Cloud((random.randint(100,25000),random.randint(0,300)),[Level_01])
        count += 1
def create_posts(number):
    posts = [2300,3350,4700, 5470,5770]
    for i in posts:
        post = scenarios.Scenario((i,0),'data/images/scenario/bathhouse_st/light_post/post/',Level_01)
def create_floor(number):
    count = 0
    while count <= number:
        tile = floors.Floor(count,'data/images/scenario/bathhouse_st/floor/tile/',[Level_01])
        count +=1

#Instancing Stuff
lef_corner_house = scenarios.Scenario((0,100),'data/images/scenario/bathhouse_st/left_corner_house/base/',Level_01,index=0)
gate1 = scenarios.Gate((300,0),'data/images/scenario/omni/gate/',Level_01,index = 0)
bathhouse = scenarios.Scenario((550,0),'data/images/scenario/bathhouse_st/bathhouse/bathhouse/',Level_01,index =0)
left_house = scenarios.Scenario((2350,100),'data/images/scenario/bathhouse_st/left_house/base/',Level_01,index = 0)
smallhouse = scenarios.Scenario((2920,100),'data/images/scenario/bathhouse_st/small_house/base/',Level_01,index =0)
home = scenarios.Scenario((3400,100),'data/images/scenario/bathhouse_st/home/castelo/',Level_01,index =0)
right_house = scenarios.Scenario((4700,100),'data/images/scenario/bathhouse_st/right_house/base/',Level_01,index=0)
gate2 = scenarios.Gate((5510,0),'data/images/scenario/omni/gate/',Level_01,index = 0)
magic_beauty_salon = scenarios.Scenario((5790,100),'data/images/scenario/bathhouse_st/magic_beauty_salon/base/',Level_01,index=0)
magic_beauty_salon_portal = scenarios.FrontScenario((5790,100),'data/images/scenario/bathhouse_st/magic_beauty_salon/portal/',Level_01,index=0)
#bathhouse_door = scenarios.Scenario((920,90),'data/images/scenario/bathhouse_st/bathhouse/door_close/',[Level_01])
carriage = enemy.Carriage(3,'data/images/enemies/carriage/',3000,[Level_01],[10,10,10,10],[10,10,10,10],[10,10,10,10])
oldlady = enemy.OldLady(2,'data/images/enemies/old_lady/',4000,[Level_01])
schnauzer = enemy.Schnauzer(10,'data/images/enemies/schnauzer/',2600,[Level_01],[22,22,22,22],[22,22,22,22],[22,22,22,22],dirty=True)
butterflies = enemy.Butterfly(4,'data/images/enemies/butterflies/',6000,[Level_01])
fundo = skies.Sky('data/images/scenario/skies/daytime/daytime.png',[Level_01],clock_pointer)
create_posts(15)
create_floor(30)
create_clouds(50)
bilboard = moving_scenario.MovingScenario(1,[Level_01],'data/images/scenario/bathhouse_st/billboard_city/billboard/')
Main_Star= glamour_stars.Glamour_Stars((0,0),Level_01,True)

try:       pygame.mixer.music.play()
except:    print "Warning: no music loaded."
doll = princess.Princess(Level_01)

info_glamour_points = panel.Data('', doll.glamour_points, (300, 0), [Level_01],0,size=120)
castle = scenarios.Background((110,0),Level_01,0,'data/images/scenario/ballroom/ballroom_day/')
pygame.init()
stage = Level_01
japanese_bridge = floors.Bridge('data/images/scenario/bathhouse_st/floor/japanese_bridge/',4,[Level_01])
mouse_pos = pygame.mouse.get_pos()
game_mouse = mousepointer.MousePointer(mouse_pos,[Level_01])

screen_surface = pygame.display.set_mode((os_screen.current_w,os_screen.current_h),FULLSCREEN,32)
gamecamera = camera.GameCamera([Level_01])

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
                if doll.jump == 0:
                    action[0] ='jump'
                    doll.jump_sound.play(0,0)
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

