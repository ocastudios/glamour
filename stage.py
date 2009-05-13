import scenarios
import obj_images
import enemy
import skies
import fairy
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
    def __init__(self,size,universe):
        self.universe       = universe
        self.cameras        = []
        self.gates          = []
        self.clock          = []
        self.floor_heights  = {}
        self.floor          = universe.floor-186
        self.menus          = []
        self.panel          = []
        self.pointer        = []
        self.princess       = None
        self.scenarios_front= []
        self.size = size
        self.rects = []
    def what_is_my_height(self,object):
        try:        y_height = self.floor_heights[object.center_distance+(object.size[0]/2)]
        except:     y_height = 186 
        return      y_height
    def update_all(self,act,dir,universe):
        surface = self.universe.screen_surface
        self.rects = []
        self.act = act
        self.direction = self.dir = dir
        for i in self.cameras:
            i.update_all(self.princess)
        universe.movement(self.direction)
        [surface.blit(i.background,(0,0)) for i in self.sky]

        for att in ('clouds','background','moving_scenario','scenarios','gates','enemies','menus'):
            exec('[surface.blit(i.image,i.pos) for i in self.'+att+' if i.rect.colliderect(self.cameras[0].rect)]')
            exec('for i in self.'+att+': i.update_all()')


        if self.princess.got_hitten>5:
            if self.princess.got_hitten%2 == 0:
                surface.blit(self.princess.image, self.princess.pos)
        else:
            surface.blit(self.princess.image, self.princess.pos)

        for effect in self.princess.effects:
            surface.blit(effect[0],effect[1])
        self.princess.update_all(dir,act)

        for i in self.scenarios_front:
            if i.rect.colliderect(self.cameras[0].rect):
                surface.blit(i.image,i.pos)
            i.update_all()

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
            i.update_all()

    def BathhouseSt(self):
        self.gates = []
        self.directory = self.maindir+'bathhouse_st/'
        self.background= [scenarios.Background(110,self,self.maindir+'ballroom/ballroom_day/')]

        self.clouds     = [clouds.Cloud(random.randint(100,25000),random.randint(0,300),self) for cl in range(10)]

        self.scenarios  = [scenarios.Scenario(0,    self.directory+'left_corner_house/base/',self,index=0),
                           scenarios.Scenario(2350, self.directory+'left_house/base/',       self,index=0),
                           scenarios.Scenario(2920, self.directory+'small_house/base/',      self,index=0),
                           scenarios.Scenario(4700, self.directory+'right_house/base/',      self,index=0),

                           scenarios.Building(550,self.directory+'bathhouse/bathhouse/',self,
                                  {'pos':(270,540),'directory':self.directory+'bathhouse/door/'},index =0),
                           scenarios.Building(3400,self.directory+'home/castelo/',self,
                                  {'pos':(537,490),'directory':self.directory+'home/door/'},index =0),
                           scenarios.Building(5790,self.directory+'magic_beauty_salon/base/',self,
                                  {'pos':(787,513),'directory':self.directory+'magic_beauty_salon/door/'},index=0),
                           scenarios.Flower(0, 'data/images/scenario/omni/flower_0/',self,8),
                           scenarios.Flower(350, 'data/images/scenario/omni/flower_1/',self,12),
                           scenarios.Flower(3135, 'data/images/scenario/omni/flower_3/',self,10),
                           scenarios.Flower(3126, 'data/images/scenario/omni/colorful_tree_1/',self,8),]

        self.scenarios.extend([scenarios.Scenario(i,self.directory+'light_post/post/',self) for i in [2300,3350,4700,5470,5770]])

        self.gates.extend( [scenarios.Gate(300, self.maindir+'omni/gate/',self,self.DressSt,index = 0),
                            scenarios.Gate(5510,self.maindir+'omni/gate/',self,self.AccessorySt,index = 0)])

        self.enemies    = [enemy.Carriage(3,self.enemy_dir+'carriage/',3000,self),
                           enemy.OldLady(2,self.enemy_dir+'old_lady/',4000,self),
                           enemy.Schnauzer(10,self.enemy_dir+'schnauzer/',2600,self,[22,22,22,22],dirty=True),
                           enemy.Butterfly(4,self.enemy_dir+'butterflies/',6000,self)]


        self.floor_image= [floors.Floor(c,self.directory+'floor/tile/',self) for c in range(18)]
        floors.Bridge(self.directory+'floor/japanese_bridge/',4,self)

        self.sky             = [skies.Sky(self.maindir+'skies/daytime/daytime.png',self,self.universe.clock_pointer)]


        self.moving_scenario = [moving_scenario.MovingScenario(1,self,self.directory+'billboard_city/billboard/')]

        self.scenarios_front = [scenarios.FrontScenario(6440,self.directory+'magic_beauty_salon/portal/',self,index=0)]

        self.pointer         = [glamour_stars.Glamour_Stars((0,0),self,True),
                                fairy.Fairy(20,self)]

        try:       pygame.mixer.music.play()
        except:    print "Warning: no music loaded."

        self.princess = self.princess or princess.Princess(self)
        panel.Data('', self.princess.glamour_points, (300, 0), self,0,size=120)

        ### set_floor ###
        self.floor_heights = {}
        count = 0
        n = 1120
        a = 15
        FDICT= [(250,186), (290,196), (320,206), (350,216), (390,236), (430,246), (490,256),
                (740,246), (800,236), (850,226), (890,216), (920,206), (950,196), (979,186-a)]
        while count < 1200:
            self.floor_heights[n+count] = 186
            for i in FDICT:
                if count >= i[0]:
                    self.floor_heights[n+count] = i[1] + a
            count += 1

    def DressSt(self):
        self.gates = []
        self.directory = self.maindir+'dress_st/'
        self.background =  [scenarios.Background(110,self,'data/images/scenario/ballroom/ballroom_day/')]
        self.clouds     = [clouds.Cloud(random.randint(100,25000),random.randint(0,300),self) for cl in range(10)]
        self.scenarios  =  [scenarios.Building(0,self.directory+'Dress_Tower/',self,
                                {'pos':(155,350),'directory':self.directory+'Dress_Tower/door/'},index =0),
                            scenarios.Scenario(0,self.directory+'Dress_Tower/flag/',self,index=0),
                            scenarios.Scenario(700,self.directory+'fachwerk_2/',self,index=0),
                            scenarios.Scenario(1400,self.directory+'fachwerk_3/',self,index=0),
                            scenarios.Scenario(2150,self.directory+'apple_pillar/',self,index=0),
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
        self.gates.extend( [scenarios.Gate(1100,'data/images/scenario/omni/gate/',self,self.BathhouseSt,index = 0),
                            scenarios.Gate(3840,'data/images/scenario/omni/gate/',self,self.AccessorySt,index = 0)])
        self.floor_image= [floors.Floor(c,self.directory+'floor/',self) for c in range(30)]
        self.sky        = [skies.Sky('data/images/scenario/skies/daytime/daytime.png',self,self.universe.clock_pointer)]
        self.moving_scenario = [moving_scenario.MovingScenario(1,self,'data/images/scenario/bathhouse_st/billboard_city/billboard/')]
        self.scenarios_front = [scenarios.Scenario(2050,self.directory+'fence/',self,index=0),]
        self.pointer = [glamour_stars.Glamour_Stars((0,0),self,True)]
        pygame.mixer.music.load("data/NeMedohounkou.ogg")
        try:       pygame.mixer.music.play()
        except:    print "Warning: no music loaded."
        self.princess = self.princess or princess.Princess(self, distance = 3000)
        panel.Data('', self.princess.glamour_points, (300, 0), self,0,size=120)

        ### set floor ###
        self.floor_heights = {}
        count = 0
        n = 0
        a = 0
        FDICT = [(60,255),(220,240),(250,215),(300,186-a)]
        while count < 1200:
            for i in FDICT:
                if count >= i[0]:
                    self.floor_heights[n+count] = i[1] + a
            count += 1

    def AccessorySt(self):
        self.gates = []
        self.directory = self.maindir+'accessory_st/'
        self.gates = []
        self.background =  [scenarios.Background(110,self,'data/images/scenario/ballroom/ballroom_day/')]
        self.clouds     = [clouds.Cloud(random.randint(100,25000),random.randint(0,300),self) for cl in range(10)]
        self.scenarios  =  [scenarios.Scenario(i[0],self.directory+i[1],self) for i in 
                               ((-3,'accessory_tower/'),
                                (800,'accessory_tower/banner/'),
                                (1350,'cathedral/base/'),
                                (2500,'hut/base/'),
                                (3400,'house/base/'),
                                (4400,'statue/base/'),
                                (5700,'viking_house/base/'),
                                (7500,'castle/base/'))]
        self.enemies    = [ enemy.Carriage(3,self.enemy_dir+'carriage/',3000,self),
                            enemy.OldLady(2,self.enemy_dir+'old_lady/',4000,self),
                            enemy.Schnauzer(10,self.enemy_dir+'schnauzer/',2600,self,[22,22,22,22],dirty=True),
                            enemy.Butterfly(4,self.enemy_dir+'butterflies/',6000,self)]
        self.gates.extend([scenarios.Gate(1100,'data/images/scenario/omni/gate/',self,self.DressSt,index = 0),
                          scenarios.Gate(5510,'data/images/scenario/omni/gate/',self,self.BathhouseSt ,index = 0)])
        self.floor_image= [floors.Floor(fl,self.directory+'floor/tile/',self) for fl in range(30)]
        self.floor_image.extend([floors.Water(wat,self.directory+'water/tile/',self) for wat in range(11)])
        self.floor_image.extend([floors.Water2(wat,self.directory+'water/tile/',self) for wat in range(11)])
        self.sky        = [skies.Sky('data/images/scenario/skies/daytime/daytime.png',self,self.universe.clock_pointer)]
        self.moving_scenario = [moving_scenario.MovingScenario(1,self,'data/images/scenario/bathhouse_st/billboard_city/billboard/')]
        self.scenarios_front = [scenarios.Scenario(178,self.directory+'accessory_tower/front/',self,index=0),
                                scenarios.Scenario(3400,self.directory+'house/front/',self)]
        self.scenarios_front.extend([scenarios.Scenario(3000+i,'data/images/scenario/omni/grass_'+str(random.randint(1,4))+'/',self) for i in (2,50,80,120,180,210,300)])
        self.pointer = [glamour_stars.Glamour_Stars((0,0),self,True)]
#        os.popen4('ogg123 ~/Bazaar/Glamour/glamour/data/NeMedohounkou.ogg')
        pygame.mixer.music.load("data/NeMedohounkou.ogg")
        try:       pygame.mixer.music.play()
        except:    print "Warning: no music loaded."
        self.princess = self.princess or princess.Princess(self,distance = 5400)
        panel.Data('', self.princess.glamour_points, (300, 0), self,0,size=120)

        ### Set Floor ###
        self.floor_heights = {}
