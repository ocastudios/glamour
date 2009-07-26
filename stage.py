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
import itertools
import mousepointer
import inside
import ball

#TODO Insert every rect that is moving in stage class self.all and use main display.update to update only the different rects.
#TODO substitute all these lists by a single list, blitting on the screen using the class to estipulate the order.

class Stage():
    enemy_dir = 'data/images/enemies/'
    maindir        = 'data/images/scenario/'
    princesses = None
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
        self.scenarios_front= []
        self.animated_scenarios =[]
        self.size = size
        self.blitlist = ('sky', 'background', 'moving_scenario', 'scenarios', 'animated_scenarios' ,'gates', 'enemies', 'menus', 'princesses')
        self.foreground = []
        self.white = Foreground(self.universe)
        self.down_bar = Bar(self,'down')
        self.up_bar   = Bar(self,'up')
        self.bar_height = self.up_bar.tile_size[1]
        self.down_bar_y = self.universe.height
        self.up_bar_y   = - self.bar_height
        self.bar_goal   = self.universe.height/3
        self.bar_speed  = 1
        self.game_mouse = mousepointer.MousePointer(pygame.mouse.get_pos(),self, type = 2)
        self.pointer = [glamour_stars.Glamour_Stars(self),self.game_mouse]
        self.dress_castle = inside.Inside(self,'dress',('pink','plain','red','yellow'))
        self.accessory_castle = inside.Inside(self,'accessory',('crown','purse','ribbon','shades'))
        self.makeup_castle = inside.Inside(self,'face',('eyelids','eyeshades','lipstick','simple'))
        self.hair_castle = inside.Inside(self,'hair',('black','brown','cinderella','rapunzel','rastafari', 'red', 'short', 'sleeping', 'snowwhite', 'yellow'))
        self.shoes_castle = inside.Inside(self,'shoes',('crystal','red','slipper','white'))
        self.inside = self.dress_castle
        self.fairy = False
        self.omni_directory = 'data/images/scenario/omni/'
        self.ball = None

    def what_is_my_height(self,object):
        try:        y_height = self.floor_heights[object.center_distance+(object.size[0]/2)]
        except:     y_height = 186 
        return      y_height

    def update_all(self):
        self.game_mouse.update()
        act = self.act = self.universe.action
        dir = self.direction = self.universe.dir
        if self.universe.clock_pointer.time == 'ball':
            self.ball = self.ball or ball.Ball(self, self.universe, self.princesses[0])
            self.ball.update_all    ()
        else:
            self.cameras[0].update_all()
            self.universe.movement(self.direction)
            for att in self.blitlist:
                exec('[self.universe.screen_surface.blit(i.image,i.pos) for i in self.'+att+' if i and i.image ]')
                exec('[i.update_all() for i in self.'+att+' if i]')

            for effect in self.princesses[0].effects:
                self.universe.screen_surface.blit(effect[0],effect[1])

            for i in self.scenarios_front:
                self.universe.screen_surface.blit(i.image,i.pos)
                i.update_all()
            [self.universe.screen_surface.blit(i.arrow_image,i.arrow_pos)
                            for i in self.gates if self.princesses[0].rect.colliderect(i.rect) and i.arrow_image]

            for i in self.floor_image:
                self.universe.screen_surface.blit(i.image,i.pos)
                i.update_all()
            for i in self.foreground:
                self.universe.screen_surface.blit(i.image,i.pos)
                i.update_all()

            if self.princesses[0].inside:
                self.update_insidebar()
            elif self.sky[0].night_image:
                self.universe.screen_surface.blit(self.sky[0].night_image,(0,0))

            for i in self.clock:
                self.universe.screen_surface.blit(i.image,i.pos)
            for i in self.panel:
                self.universe.screen_surface.blit(i.label,i.pos)
                i.update(self.princesses[0].glamour_points)
            for i in self.pointer:
                self.universe.screen_surface.blit(i.image,i.pos)
                i.update_all()
            if self.fairy:
                for i in self.fae:
                    self.universe.screen_surface.blit(i.image,i.pos)
                    i.update_all()

    def update_insidebar(self):
        self.universe.screen_surface.blit(self.white.image,(0,0))
        self.universe.screen_surface.blit(self.down_bar.image,(0,self.down_bar_y))
        self.universe.screen_surface.blit(self.up_bar.image,(0,self.up_bar_y))

        if self.inside.status == 'inside':
            self.up_bar_y = -self.bar_height
            self.down_bar_y = self.universe.height
            self.white.alpha_value = 0
            self.inside.status = 'loading'

        elif self.inside.status == 'loading':
            self.white.image.set_alpha(self.white.alpha_value)
            if self.white.alpha_value < 200:
                self.white.alpha_value += 10
            if self.down_bar_y > 2*self.bar_goal:
                self.down_bar_y -= self.bar_speed
            if self.up_bar_y + self.bar_height< self.bar_goal:
                self.up_bar_y += self.bar_speed
            if self.bar_speed < 20:
                self.bar_speed += self.bar_speed
            if self.white.alpha_value > 150:
                self.inside.status = 'choosing'

        elif self.inside.status == 'choosing':
            self.universe.screen_surface.blit(self.princesses[0].image,
                                    ((self.universe.width/2)-(self.princesses[0].image_size[0]/2),
                                    (self.universe.height/2)-(self.princesses[0].image_size[1]/2)))
            [self.universe.screen_surface.blit(i.image,i.pos) for i in self.inside.buttons]
            [i.update_all() for i in self.inside.buttons]
            [self.universe.screen_surface.blit(i.image,i.pos) for i in self.inside.items if i.queue]
            [i.update_all() for i in self.inside.items]

        elif self.inside.status == 'done':
            self.down_bar_y += self.bar_speed
            self.up_bar_y -= self.bar_speed
            if self.bar_speed < 20:
                self.bar_speed += self.bar_speed
            if self.white.alpha_value > 0:
                self.white.alpha_value -= 10
                self.white.image.set_alpha(self.white.alpha_value)
            else:
                self.white.image.alpha_value = 0
            self.white.image.set_alpha(self.white.alpha_value)

            if self.down_bar_y > self.universe.height and self.up_bar_y < -self.bar_height and self.white.alpha_value == 0:
                self.inside.status = 'openning'

        elif self.inside.status == 'openning':
#            self.level.blitlist = ('sky','background','moving_scenario','scenarios','gates','enemies','menus','princesses')
            for i in self.gates:
                if i.rect.colliderect(self.princesses[0].rect):
                    i.open = True
                    if i.images.number >= i.images.lenght -1:
                        self.inside.status = 'closing'

        elif self.inside.status == 'closing':
            for i in self.gates:
                if i.rect.colliderect(self.princesses[0].rect):
                    i.outside()
            self.princesses[0].inside = False

    def BathhouseSt(self):
        self.gates = []
        self.directory = self.maindir+'bathhouse_st/'
        self.background= [scenarios.Background(110,self,self.maindir+'ballroom/ballroom_day/')]
        self.scenarios_prep  = [scenarios.Scenario(i[0],i[1],self) for i in (
                                (100, self.omni_directory+'tree_2/'),
                                (200, self.omni_directory+'bush/'),
                                (0,    self.directory+'left_corner_house/base/'),
                                (793,  self.directory+'bathhouse/bathhouse/'),
                                (3280, self.omni_directory+'tree_2/'),
                                (2810, self.directory+'left_house/base/'),
                                (2795, self.omni_directory+'small_bush_1/'),
                                (3384, self.omni_directory+'small_bush_1/'),
                                (3499, self.omni_directory+'small_bush_1/'),
                                (3948, self.omni_directory+'tree_2/'),
                                (3677, self.directory+'small_house/base/'),
                                (4060, self.omni_directory+'small_bush_2/'),
                                (4479, self.omni_directory+'tree_1/'),
                                (4671,self.directory+'home/castelo/'),
                                (3948, self.omni_directory+'tree_2/'),
                                (7014, self.omni_directory+'tree_1/'),
                                (7826, self.omni_directory+'tree_1/'),
                                (7147, self.directory+'right_house/base/',),
                                (5975, self.omni_directory+'tree_2/'),
                                (6354, self.omni_directory+'bush/'),
                                (6584, self.omni_directory+'tree_2/'),
                                (6917, self.omni_directory+'bush/'),
                                (7552, self.omni_directory+'small_bush_1/'),
                                (7828, self.omni_directory+'small_bush_2/'),
                                (8517,self.directory+'magic_beauty_salon/base/'),
                                (8562,self.omni_directory+'small_bush_2/'),
                                (8696,self.omni_directory+'small_bush_1/'))]
        self.scenarios_prep.extend([scenarios.Scenario(i,self.directory+'light_post/post/',self)
                                for i in [405,2730,4217,6041,8469]])

        self.gates =   [scenarios.BuildingDoor((1064,453),self.directory+'bathhouse/door/',self,self.dress_castle),
                        scenarios.BuildingDoor((5226,500),self.directory+'home/door/',self,self.hair_castle),
                        scenarios.BuildingDoor((8737,503),self.directory+'magic_beauty_salon/door/',self,self.shoes_castle),
                        scenarios.Gate(480, self.maindir+'omni/gate/',self,self.DressSt,index = 0),
                        scenarios.Gate(8138,self.maindir+'omni/gate/',self,self.AccessorySt,index = 0)]

        self.scenarios = BigScenario(self),

        for i in self.scenarios_prep:
            self.scenarios[0].image.blit(i.image,i.pos)

        self.enemies    = [enemy.Carriage(3,self.enemy_dir+'carriage/',3000,self),
                           enemy.OldLady(2,self.enemy_dir+'old_lady/',4000,self),
                           enemy.Schnauzer(10,self.enemy_dir+'schnauzer/',2600,self,[22,22,22,22],dirty=True),
                           enemy.Butterfly(4,self.enemy_dir+'butterflies/',6000,self),
                           enemy.FootBoy(9000,self)
                            ]

        self.floor_image= [floors.Floor(c,self.directory+'floor/tile/',self) for c in range(24)]
        floors.Bridge(self.directory+'floor/japanese_bridge/',5,self)

        self.sky             = [skies.Sky(self.maindir+'skies/daytime/daytime.png',self,self.universe.clock_pointer)]
        self.clouds     = [clouds.Cloud(self) for cl in range(3)]
        [self.sky[0].image.blit(i.image,i.pos) for i in self.clouds]

        self.moving_scenario = [moving_scenario.Billboard(self)]

        self.scenarios_front = [
                                scenarios.Scenario(3535,self.omni_directory+'fence_1/',self),
                                scenarios.Scenario(4322,self.omni_directory+'fence_1/',self),
                                scenarios.Flower(4161,     self.omni_directory+'flower_9/',self,8),
                                scenarios.Flower(4243,     self.omni_directory+'flower_6/',self,8),
                                scenarios.Flower(4389,     self.omni_directory+'flower_4/',self,8),
                                scenarios.Flower(4332,     self.omni_directory+'flower_7/',self,8),
                                scenarios.Flower(6303,     self.omni_directory+'flower_9/',self,8),
                                scenarios.Flower(6218,     self.omni_directory+'flower_6/',self,8),
                                scenarios.Flower(6528,     self.omni_directory+'flower_4/',self,8),
                                scenarios.Flower(6665,     self.omni_directory+'flower_4/',self,8),
                                scenarios.Flower(6620,     self.omni_directory+'flower_7/',self,8),
                                scenarios.Flower(7123,     self.omni_directory+'grass_2/',self,8),
                                scenarios.Flower(7197,     self.omni_directory+'grass_1/',self,8),

                                scenarios.Scenario(6058,self.omni_directory+'grass_1/',self),
                                scenarios.Scenario(6754,self.omni_directory+'fence_1/',self),
                                scenarios.FrontScenario(8600,self.directory+'magic_beauty_salon/portal/',self,index=0)]

        self.fae = ([fairy.Fairy(20,self)])

        try:       pygame.mixer.music.play()
        except:    print "Warning: no music loaded."


        self.princesses = self.princesses or [princess.Princess(self,save=self.universe.file),None]
        panel.Data('', self.princesses[0].glamour_points, (300, 0), self,0,size=120)

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
        self.animated_scenarios =[]
    def DressSt(self):
        self.gates = []
        self.directory = self.maindir+'dress_st/'
        self.scenarios_prep  =  [
                                scenarios.Scenario(1086,self.omni_directory+'tree_2/',self),
                                scenarios.Scenario(0,self.directory+'Dress_Tower/',self),
                                scenarios.Scenario(1307,self.directory+'fachwerk_3/base/',self),
                                scenarios.Scenario(1127,'data/images/scenario/bathhouse_st/light_post/post/',self),
                                scenarios.Scenario(1992,self.omni_directory+'hydrant/',self),
                                scenarios.Scenario(2091,self.directory+'fachwerk_2/base/',self),
                                scenarios.Scenario(2538,'data/images/scenario/bathhouse_st/light_post/post/',self),
                                scenarios.Scenario(2901,self.omni_directory+'tree_2/',self),
                                scenarios.Scenario(2659,self.directory+'flowers/base/',self),
                                scenarios.Scenario(3085,self.directory+'chair/',self,invert = True),
                                scenarios.Scenario(3039,self.omni_directory+'grass_2/',self),
                                scenarios.Scenario(3605,self.directory+'knight_statue/',self),
                                scenarios.Scenario(4625,self.directory+'apple_pillar/',self),
                                scenarios.Scenario(4038,'data/images/scenario/bathhouse_st/light_post/post/',self),
                                scenarios.Scenario(4682,self.omni_directory+'tree_1/',self),
                                scenarios.Scenario(4878,self.directory+'chair/',self),
                                scenarios.Scenario(5128,self.omni_directory+'hydrant/',self),
                                scenarios.Scenario(5337,self.omni_directory+'tree_2/',self),
                                scenarios.Scenario(5600,self.omni_directory+'tree_1/',self),
                                scenarios.Scenario(5657,self.omni_directory+'grass_3/',self),
                                scenarios.Scenario(5220,self.directory+'flowers/base/',self),
                                scenarios.Scenario(6095,'data/images/scenario/bathhouse_st/light_post/post/',self),
                                scenarios.Scenario(6192,self.directory+'fachwerk_4/',self),
                                scenarios.Scenario(6148,self.omni_directory+'bush/',self),
                                scenarios.Scenario(6454,self.omni_directory+'flower_7/',self),
                                scenarios.Scenario(6393,self.omni_directory+'flower_8/',self),
                                scenarios.Scenario(6628,self.omni_directory+'flower_7/',self),
                                scenarios.Scenario(6724,self.omni_directory+'tree_2/',self),
                                scenarios.Scenario(6735,self.omni_directory+'bush/',self),
                                scenarios.Scenario(7310,self.omni_directory+'tree_2/',self),
                                scenarios.Scenario(7105,self.directory+'fachwerk_2/base/',self),
                                scenarios.Scenario(7536,self.directory+'fachwerk_1/',self),
                                scenarios.Scenario(8107,self.omni_directory+'tree_1/',self),
                                scenarios.Scenario(8398,'data/images/scenario/bathhouse_st/light_post/post/',self),
                                scenarios.Scenario(8917,self.directory+'snow_white_castle/',self)]

        self.scenarios = BigScenario(self),
        for i in self.scenarios_prep:
            self.scenarios[0].image.blit(i.image,i.pos)

        self.animated_scenarios = [scenarios.Scenario(0,self.directory+'Dress_Tower/flag/',self,index=0)]

        self.enemies    = [ enemy.Carriage(3,self.enemy_dir+'carriage/',3000,self),
                            enemy.OldLady(2,self.enemy_dir+'old_lady/',4000,self),
                            enemy.Schnauzer(10,self.enemy_dir+'schnauzer/',2600,self,[22,22,22,22],dirty=True),
                            enemy.Butterfly(4,self.enemy_dir+'butterflies/',6000,self)]

        self.gates = [scenarios.BuildingDoor((100,450),self.directory+'Dress_Tower/door/',self),
                      scenarios.BuildingDoor((4577,300),self.directory+'snow_white_castle/door/',self),
                      scenarios.Gate(800,'data/images/scenario/omni/gate/',self,self.BathhouseSt,index = 0),
                      scenarios.Gate(8471,'data/images/scenario/omni/gate/',self,self.MakeupSt,index = 0)]

        self.floor_image= [floors.Floor(c,self.directory+'floor/',self) for c in range(30)]
        self.sky        = [skies.Sky('data/images/scenario/skies/daytime/daytime.png',self,self.universe.clock_pointer)]
        self.clouds     = [clouds.Cloud(self) for cl in range(3)]
        [self.sky[0].image.blit(i.image,i.pos) for i in self.clouds]
        self.scenarios_front = [scenarios.Scenario(i[0],i[1],self) for i in (
                                (557,self.directory+'fence/base/'),
                                (719,self.omni_directory+'grass_4/'),
                                (1200,self.omni_directory+'grass_3/'),
                                (1905,self.omni_directory+'grass_3/'),
                                (2098,self.omni_directory+'grass_4/'),
                                (2464,self.omni_directory+'grass_2/'),
                                (3408,self.directory+'fence/base/'),
                                (3665,self.omni_directory+'grass_3/'),
                                (4408,self.directory+'fence/base/'),
                                (4606,self.omni_directory+'grass_2/'),
                                (5855,self.directory+'fence/base/'),
                                (7004,self.omni_directory+'grass_3/'),
                                (7576,self.omni_directory+'grass_3/'),
                                (8416,self.omni_directory+'grass_3/'),
                                (8822,self.omni_directory+'grass_3/')
                                )]

        pygame.mixer.music.load("data/NeMedohounkou.ogg")
        try:
            pygame.mixer.music.play()
        except:
            print "Warning: no music loaded."
        self.princesses = self.princesses or [princess.Princess(self,save=self.universe.file),None]
        panel.Data('', self.princesses[0].glamour_points, (300, 0), self,0,size=120)

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
        self.scenarios_prep  =  [scenarios.Scenario(i[0],i[1],self) for i in 
                               ((-3,self.directory+'accessory_tower/'),
                                (800,self.directory+'accessory_tower/banner/'),
                                (2575,self.omni_directory+'tree_2/'),
                                (1795,self.directory+'statue/base/'),
                                (1757,self.omni_directory+'small_bush_2/'),
                                (1852,self.omni_directory+'small_bush_1/'),
                                (2800,self.omni_directory+'small_bush_2/'),
                                (2871,self.omni_directory+'small_bush_1/'),
                                (2896,self.directory+'cathedral/base/'),
                                (3336,self.omni_directory+'small_bush_1/'),
                                (4400,self.omni_directory+'tree_2/'),
                                (4497,self.directory+'hut/base/'),
                                (6405,self.omni_directory+'tree_2/'),
                                (5470,self.directory+'house/base/'),
                                (3903,self.omni_directory+'fence_1/'),
                                (5249,self.omni_directory+'small_bush_1/'),
                                (5499,self.omni_directory+'small_bush_1/'),
                                (6560,self.directory+'viking_house/base/'),
                                (6420,self.omni_directory+'small_bush_1/'),
                                (6512,self.omni_directory+'small_bush_2/'),
                                (7446,self.omni_directory+'small_bush_2/'),
                                (7531,self.omni_directory+'small_bush_1/'),
                                (7644,self.omni_directory+'bush/'),
                                (8218,self.directory+'castle/base/'),
                                (9000,self.omni_directory+'grass_1/'),
                                (9114,self.omni_directory+'grass_4/'),
                                (9200,self.omni_directory+'grass_1/'),
                                (9313,self.omni_directory+'small_bush_2/'),
                                (9374,self.omni_directory+'flower_8/'),
                                (9476,self.omni_directory+'small_bush_1/'),
                            )]
        self.scenarios = BigScenario(self),
        for i in self.scenarios_prep:
            self.scenarios[0].image.blit(i.image,i.pos)

        self.enemies    = [ enemy.Carriage(3,self.enemy_dir+'carriage/',3000,self),
                            enemy.OldLady(2,self.enemy_dir+'old_lady/',4000,self),
                            enemy.Schnauzer(10,self.enemy_dir+'schnauzer/',2600,self,[22,22,22,22],dirty=True),
                            enemy.Butterfly(4,self.enemy_dir+'butterflies/',6000,self)]
        self.gates.extend([
                            scenarios.Gate(1497,'data/images/scenario/omni/gate/',self,self.DressSt,index = 0),
                            scenarios.Gate(4174,'data/images/scenario/omni/gate/',self,self.MakeupSt,index = 0),
                            scenarios.Gate(7836,'data/images/scenario/omni/gate/',self,self.BathhouseSt ,index = 0)])
        self.floor_image= [floors.Floor(fl,self.directory+'floor/tile/',self) for fl in range(30)]
        self.floor_image.extend([floors.Water(wat,self.directory+'water/tile/',self) for wat in range(11)])
        self.floor_image.extend([enemy.VikingShip(9000,self)])
        self.floor_image.extend([floors.Water2(wat,self.directory+'water/tile/',self) for wat in range(11)])

        self.sky        = [skies.Sky('data/images/scenario/skies/daytime/daytime.png',self,self.universe.clock_pointer)]
        self.clouds     = [clouds.Cloud(self) for cl in range(3)]
        [self.sky[0].image.blit(i.image,i.pos) for i in self.clouds]

        self.scenarios_front = [
                                scenarios.Scenario(3903,self.omni_directory+'fence_1/',self),
                                scenarios.Scenario(178,self.directory+'accessory_tower/front/',self),
                                scenarios.Scenario(5470,self.directory+'house/front/',self)]
        pygame.mixer.music.load("data/NeMedohounkou.ogg")
        try:       pygame.mixer.music.play()
        except:    print "Warning: no music loaded."
        self.princesses = self.princesses or [princess.Princess(self,save=self.universe.file),None]
        panel.Data('', self.princesses[0].glamour_points, (300, 0), self,0,size=120)

        ### Set Floor ###
        self.floor_heights = {}
        self.animated_scenarios =[]
    def MakeupSt(self):
        self.gates = []
        self.directory = self.maindir+'makeup_st/'
        self.scenarios_prep  =  [scenarios.Scenario(i[0],i[1],self) for i in 
                                (
                                (0,self.directory+'make-up_castle/base/'),
                                (0,self.directory+'make-up_castle/front_1/'),
                                (1484,self.omni_directory+'bush/'),
                                (1635,self.omni_directory+'hydrant/'),
                                (1605,self.directory+'temple/base/'),
                                (2576,self.omni_directory+'tree_2/'),
                                (2576,self.omni_directory+'fence_1/'),
                                (4160,self.omni_directory+'tree_2/'),
                                (2923,self.directory+'zoo/background/'),
                                (4800,self.omni_directory+'grass_3/'),
                                (4952,self.omni_directory+'flower_7/'),
                                (4891,self.omni_directory+'flower_8/'),
                                (5126,self.omni_directory+'flower_7/'),
                                (5252,self.omni_directory+'grass_3/'),
                                (5239,self.omni_directory+'grass_3/'),
                                (5481,self.omni_directory+'grass_3/'),
                                (5335,self.omni_directory+'tree_1/'),
                                (5571,self.omni_directory+'flower_8/'),
                                (5632,self.omni_directory+'flower_7/'),
                                (5607,self.omni_directory+'grass_3/'),
                                (5600,self.omni_directory+'tree_1/'),
                                (6700,self.omni_directory+'tree_2/'),
                                (6021,self.directory+'little_house/base/'),
                                (5693,self.omni_directory+'bush/'),
                                (5844,self.omni_directory+'hydrant/'),
                                (7900,self.omni_directory+'tree_1/'),
                                (7217,self.directory+'right/base/'),
                                (8426,self.directory+'sleeping_castle/base/')
                                )
                                ]
        self.scenarios = [BigScenario(self)]
        for i in self.scenarios_prep:
            self.scenarios[0].image.blit(i.image,i.pos)

        self.enemies    = [ enemy.Carriage(3,self.enemy_dir+'carriage/',3000,self),
                            enemy.OldLady(2,self.enemy_dir+'old_lady/',4000,self),
                            enemy.Schnauzer(10,self.enemy_dir+'schnauzer/',2600,self,[22,22,22,22],dirty=True),
                            enemy.Butterfly(4,self.enemy_dir+'butterflies/',6000,self),
                            ]
        self.gates.extend([ scenarios.Gate(1200,'data/images/scenario/omni/gate/',self,self.AccessorySt,index = 0),
                            scenarios.Gate(4661,'data/images/scenario/omni/gate/',self,self.DressSt,index = 0),
                            scenarios.Gate(8231,'data/images/scenario/omni/gate/',self,self.BathhouseSt ,index = 0)])
        self.floor_image= [floors.Floor(fl,self.directory+'floor/',self) for fl in range(30)]

        self.sky        = [skies.Sky('data/images/scenario/skies/daytime/daytime.png',self,self.universe.clock_pointer)]
        self.clouds     = [clouds.Cloud(self) for cl in range(3)]
        [self.sky[0].image.blit(i.image,i.pos) for i in self.clouds]
        self.scenarios_front = [scenarios.Scenario(0,self.directory+'make-up_castle/front/',0)]
        pygame.mixer.music.load("data/NeMedohounkou.ogg")
        try:       pygame.mixer.music.play()
        except:    print "Warning: no music loaded."
        self.princesses = self.princesses or [princess.Princess(self,save=self.universe.file),None]
        panel.Data('', self.princesses[0].glamour_points, (300, 0), self,0,size=120)
        ### Set Floor ###
        self.floor_heights = {}
        self.animated_scenarios = [ enemy.Lion(3200,self),
                                    enemy.Monkey(3500,self),
                                    scenarios.Scenario(2923,self.directory+'zoo/base/',self)]
        self.animated_scenarios.insert(1,self.animated_scenarios[0].tail)


class Foreground():
    def __init__(self,universe):
        self.pos = 0,0
        self.image = pygame.Surface((universe.width,universe.height)).convert()
        self.image.fill((255,255,255))
        self.alpha_value = 0
        self.image.set_alpha(self.alpha_value)

    def update_all(self):
        if self.inside:
            if self.alpha_value < 200:
                self.alpha_value += 10
        else:
            if self.alpha_value > 0:
                self.alpha_value -= 15
            if self.alpha_value < 0:
                self.image.set_alpha(self.alpha_value)
                alpha_value = 0
        if 180 > self.alpha_value > 40:
            self.image.set_alpha(self.alpha_value)


class Bar():
    def __init__(self,level, up_or_down):
        self.tile = down_bar = pygame.image.load('data/images/interface/omni/small_bar/0.png').convert_alpha()
        if up_or_down == 'up':
            self.tile = pygame.transform.flip(self.tile,0,1)
        screen_size = level.universe.width, level.universe.height
        self.tile_size   = self.tile.get_size()
        self.image  = pygame.Surface((screen_size[0],self.tile_size[1]),pygame.SRCALPHA).convert_alpha()
        bar_positions = range(0,(screen_size[0]/self.tile_size[0]+1))
        [self.image.blit(self.tile,(i*self.tile_size[0],0)) for i in bar_positions]


class BigScenario():
    def __init__(self,level):
        self.level      = level
        self.image      = pygame.Surface((9600,level.universe.height),pygame.SRCALPHA).convert_alpha()
        self.pos = [self.level.universe.center_x,0]

    def update_all(self):
        self.pos[0]         = self.level.universe.center_x


