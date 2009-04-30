import scenarios
import obj_images
import enemy
import skies
import floors
import clouds
import random
import moving_scenario
import glamour_stars
import princess
import os
import panel
import pygame

#TODO Insert every rect that is moving in stage class self.all and use main display.update to update only the different rects.
#TODO substitute all these lists by a single list, blitting on the screen using the class to estipulate the order.

class Stage():
    princess = None
    enemy_dir = 'data/images/enemies/'
    maindir        = 'data/images/scenario/'
    def __init__(self,level,size,universe,directory):
        self.universe       = universe
        self.maindir        = 'data/images/scenario/'
        self.directory      = self.maindir+directory
        self.cameras        = []
        self.gates          = []
        self.clock          = []
        self.floor_heights  = {}
        self.floor          = universe.floor-186
        self.level          = level
        self.menus          = []
        self.panel          = []
        self.pointer        = []
        self.princess       = None
        self.scenarios_front= []
        self.set_floor()
        self.size = size


    def what_is_my_height(self,object):
        try:        y_height = self.floor_heights[object.center_distance+(object.size[0]/2)]
        except:     y_height = 186 
        return      y_height

    def update_all(self,surface,act,dir,universe):

        self.act = act
        self.direction = self.dir = dir

        for i in self.cameras:
            i.update_all(self.princess)

        universe.movement(self.direction)

        [surface.blit(i.background,(0,0)) for i in self.sky]

        for att in ('clouds','background','moving_scenario','scenarios','gates','enemies','menus'):
            exec('[surface.blit(i.image,i.pos) for i in self.'+att+' if i.rect.colliderect(self.cameras[0].rect)]')
            exec('for i in self.'+att+': i.update_all(self)')

        for part in self.princess.parts:
            if self.princess.got_hitten > 5:
                if self.princess.got_hitten % 2 == 0 and part != None:
                    surface.blit(part.image,part.pos)
            else:
                if part != None:
                    surface.blit(part.image,part.pos)

        for effect in self.princess.effects:
            surface.blit(effect[0],effect[1])

        self.princess.update_all(dir,act)

        for i in self.scenarios_front:
            if i.rect.colliderect(self.cameras[0].rect):
                surface.blit(i.image,i.pos)
            i.update_all(self)

        for i in self.gates:
            if self.princess.rect.colliderect(i.rect)== True:
                surface.blit(i.arrow_image,i.arrow_pos)

        for i in self.floor_image:
            if i.__class__ == floors.Floor or floors.Bridge:
                if i.rect.colliderect(self.cameras[0].rect):
                    surface.blit(i.image,i.pos)
                i.update_all()
        for i in self.floor_image:
            if i.__class__ == floors.Water:
                if i.rect.colliderect(self.cameras[0].rect):
                    surface.blit(i.image,i.pos)
                i.update_all()
        for i in self.floor_image:
            if i.__class__ == floors.Water2:
                if i.rect.colliderect(self.cameras[0].rect):
                    surface.blit(i.image,i.pos)
                i.update_all()

        for i in self.clock:
            surface.blit(i.image,i.pos)
        for i in self.panel:
            surface.blit(i.label,i.pos)
            i.update(self.princess.glamour_points)
        for i in self.pointer:
            surface.blit(i.image,i.pos)

class BathhouseSt(Stage):
    """This class is meant to create the levels of the game. One of its most importante features is to blit everything on the screen and define what should be in each of the stages.
It is still in its early development"""


    def instantiate_stuff(self):
        self.background= [scenarios.Background(110,self,0,self.maindir+'ballroom/ballroom_day/')]


        self.clouds     = [clouds.Cloud((random.randint(100,25000),random.randint(0,300)),[self]) for cl in range(50)]



        self.scenarios  = [scenarios.Scenario(0,    self.directory+'left_corner_house/base/',self,index=0),
                           scenarios.Flower(0, 'data/images/scenario/omni/flower_0/',self,4),
                           scenarios.Scenario(2350, self.directory+'left_house/base/',       self,index=0),
                           scenarios.Scenario(2920, self.directory+'small_house/base/',      self,index=0),
                           scenarios.Scenario(4700, self.directory+'right_house/base/',      self,index=0),
                           scenarios.Building(550,self.directory+'bathhouse/bathhouse/',self,
                                  {'pos':(270,540),'directory':self.directory+'bathhouse/door/'},index =0),
                           scenarios.Building(3400,self.directory+'home/castelo/',self,
                                  {'pos':(537,490),'directory':self.directory+'home/door/'},index =0),
                           scenarios.Building(5790,self.directory+'magic_beauty_salon/base/',self,
                                  {'pos':(787,513),'directory':self.directory+'magic_beauty_salon/door/'},index=0)]

        self.scenarios.extend([scenarios.Scenario(i,self.directory+'light_post/post/',self) for i in [2300,3350,4700,5470,5770]])


        self.gates.extend( [scenarios.Gate(300, self.maindir+'omni/gate/',self,index = 0),
                            scenarios.Gate(5510,self.maindir+'omni/gate/',self,index = 0)])


        self.enemies    = [enemy.Carriage(3,self.enemy_dir+'carriage/',3000,self),
                           enemy.OldLady(2,self.enemy_dir+'old_lady/',4000,self),
                           enemy.Schnauzer(10,self.enemy_dir+'schnauzer/',2600,self,[22,22,22,22],dirty=True),
                           enemy.Butterfly(4,self.enemy_dir+'butterflies/',6000,self)]


        self.floor_image= [floors.Floor(c,self.directory+'floor/tile/',self) for c in range(30)]
        floors.Bridge(self.directory+'floor/japanese_bridge/',4,self)

        self.sky             = [skies.Sky(self.maindir+'skies/daytime/daytime.png',self,self.universe.clock_pointer)]


        self.moving_scenario = [moving_scenario.MovingScenario(1,self,self.directory+'billboard_city/billboard/')]


        self.scenarios_front = [scenarios.FrontScenario(6440,self.directory+'magic_beauty_salon/portal/',self,index=0)]

        self.pointer         = [glamour_stars.Glamour_Stars((0,0),self,True)]


        try:       pygame.mixer.music.play()
        except:    print "Warning: no music loaded."

        self.princess = self.princess or princess.Princess(self)
        panel.Data('', self.princess.glamour_points, (300, 0), self,0,size=120)


    def set_floor(self):
        self.floor_heights = {}
        count = 0
        n = 1120
        a = 15
        while count < 1200:
            self.floor_heights[n+count] = 186
            if count >= 250:
                self.floor_heights[n+count] = 186 + a
            if count >= 290:
                self.floor_heights[n+count] = 196 + a
            if count >= 320:
                self.floor_heights[n+count] = 206 + a
            if count >= 350:
                self.floor_heights[n+count] = 216 + a
            if count >= 390:
                self.floor_heights[n+count] = 236 + a
            if count >= 430:
                self.floor_heights[n+count] = 246 + a
            if count >= 490:
                self.floor_heights[n+count] = 256 + a
            if count >= 740:
                self.floor_heights[n+count] = 246 + a
            if count >= 800:
                self.floor_heights[n+count] = 236 + a
            if count >= 850:
                self.floor_heights[n+count] = 226 + a
            if count >= 890:
                self.floor_heights[n+count] = 216 + a
            if count >= 920:
                self.floor_heights[n+count] = 206 + a
            if count >= 950:
                self.floor_heights[n+count] = 196 + a
            if count >= 979:
                self.floor_heights[n+count] = 186
            count += 1
class DressSt(Stage):
    def instantiate_stuff(self):
        self.background =  [scenarios.Background(110,self,0,'data/images/scenario/ballroom/ballroom_day/')]

        self.clouds     =  [clouds.Cloud((random.randint(100,25000),random.randint(0,300)),[self])]

        self.scenarios  =  [scenarios.Building(0,self.directory+'Dress_Tower/',self,
                                {'pos':(155,350),'directory':self.directory+'Dress_Tower/door/'},index =0),
                            scenarios.Scenario(0,self.directory+'Dress_Tower/flag/',self,index=0),
                            scenarios.Scenario(700,self.directory+'fachwerk_2/',self,index=0),
                            scenarios.Scenario(1400,self.directory+'fachwerk_3/',self,index=0),
                            scenarios.Scenario(2150,self.directory+'apple_pillar/',self,index=0),
                            scenarios.Scenario(2050,self.directory+'fence/',self,index=0),
                            scenarios.Scenario(2500,self.directory+'knight_statue/',self,index=0),
                            scenarios.Scenario(2850,self.directory+'chair/',self,index=0),
                            scenarios.Scenario(2250,self.directory+'flowers/',self,index=0),

                            scenarios.Scenario(3100,self.directory+'fachwerk_1/',self,index=0),
                            scenarios.Scenario(4300,self.directory+'snow_white_castle/',self,
                                {'pos':(155,350),'directory':self.directory+'snow_white_castle/door/'})]


        self.enemies    = [ enemy.Carriage(3,self.enemy_dir+'carriage/',3000,self),
                            enemy.OldLady(2,self.enemy_dir+'old_lady/',4000,self),
                            enemy.Schnauzer(10,self.enemy_dir+'schnauzer/',2600,self,[22,22,22,22],dirty=True),
                            enemy.Butterfly(4,self.enemy_dir+'butterflies/',6000,self)]

        self.gates.extend( [scenarios.Gate(1100,'data/images/scenario/omni/gate/',self,index = 0),
                            scenarios.Gate(3840,'data/images/scenario/omni/gate/',self,index = 0)])

        self.floor_image= [floors.Floor(c,self.directory+'floor/',self) for c in range(30)]

        self.sky        = [skies.Sky('data/images/scenario/skies/daytime/daytime.png',self,self.universe.clock_pointer)]
        self.moving_scenario = [moving_scenario.MovingScenario(1,self,'data/images/scenario/bathhouse_st/billboard_city/billboard/')]
        self.scenarios_front = []

        self.pointer = [glamour_stars.Glamour_Stars((0,0),self,True)]

        pygame.mixer.music.load("data/NeMedohounkou.ogg")
        try:       pygame.mixer.music.play()
        except:    print "Warning: no music loaded."

        self.princess = self.princess or princess.Princess(self, distance = 3000)

        panel.Data('', self.princess.glamour_points, (300, 0), self,0,size=120)

    def set_floor(self):
        self.floor_heights = {}
        count = 0
        n = 0
        a = 0
        while count < 1200:
            self.floor_heights[n+count] = 186
            if count >= 60:
                self.floor_heights[n+count] = 255 + a
            if count >= 220:
                self.floor_heights[n+count] = 240 + a
            if count >= 250:
                self.floor_heights[n+count] = 215 + a
            if count >= 300:
                self.floor_heights[n+count] = 195
            if count >= 300:
                self.floor_heights[n+count] = 186
            count += 1
class AccessorySt(Stage):
    def instantiate_stuff(self):

        self.background =  [scenarios.Background(110,self,0,'data/images/scenario/ballroom/ballroom_day/')]
        self.clouds     =  [clouds.Cloud((random.randint(100,25000),random.randint(0,300)),[self]) for cl in range(50)]
        self.scenarios  =  [scenarios.Scenario(-3,self.directory+'accessory_tower/',self,index=0),
                            scenarios.Scenario(800,self.directory+'accessory_tower/banner/',self,index = 0),
                            scenarios.Scenario(1350,self.directory+'cathedral/base/',self),
                            scenarios.Scenario(2500,self.directory+'hut/base/',self),
                            scenarios.Scenario(3400,self.directory+'house/base/',self),
                            scenarios.Scenario(4400,self.directory+'statue/base/',self),
                            scenarios.Scenario(5700,self.directory+'viking_house/base/',self)
]
        self.enemies    = [ enemy.Carriage(3,self.enemy_dir+'carriage/',3000,self),
                            enemy.OldLady(2,self.enemy_dir+'old_lady/',4000,self),
                            enemy.Schnauzer(10,self.enemy_dir+'schnauzer/',2600,self,[22,22,22,22],dirty=True),
                            enemy.Butterfly(4,self.enemy_dir+'butterflies/',6000,self)]

        self.gates.extend([scenarios.Gate(1100,'data/images/scenario/omni/gate/',self,index = 0),
                          scenarios.Gate(5510,'data/images/scenario/omni/gate/',self,index = 0)])

        self.floor_image= [floors.Floor(fl,self.directory+'floor/tile/',self) for fl in range(30)]
        self.floor_image.extend([floors.Water(wat,self.directory+'water/tile/',self) for wat in range(11)])
        self.floor_image.extend([floors.Water2(wat,self.directory+'water/tile/',self) for wat in range(11)])


        self.sky        = [skies.Sky('data/images/scenario/skies/daytime/daytime.png',self,self.universe.clock_pointer)]

        self.moving_scenario = [moving_scenario.MovingScenario(1,self,'data/images/scenario/bathhouse_st/billboard_city/billboard/')]
        self.scenarios_front = [scenarios.Scenario(178,self.directory+'accessory_tower/front/',self,index=0),
                                scenarios.Scenario(3400,self.directory+'house/front/',self)

]
        self.pointer = [glamour_stars.Glamour_Stars((0,0),self,True)]


        pygame.mixer.music.load("data/NeMedohounkou.ogg")

        try:       pygame.mixer.music.play()
        except:    print "Warning: no music loaded."
        self.princess = self.princess or princess.Princess(self,distance = 5400)

        panel.Data('', self.princess.glamour_points, (300, 0), self,0,size=120)


    def set_floor(self):
        pass

