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
        self.size = size
        self.blitlist = ('sky','background','moving_scenario','scenarios','gates','enemies','menus','princesses')
        self.foreground = []
        self.white = Foreground(self.universe)

        self.down_bar = Bar(self,'down')
        self.up_bar   = Bar(self,'up')
        self.bar_height = self.up_bar.tile_size[1]
        self.down_bar_y = self.universe.height
        self.up_bar_y   = - self.bar_height
        self.bar_goal   = self.universe.height/3
        self.bar_speed  = 1

        self.game_mouse = mousepointer.MousePointer(pygame.mouse.get_pos(),self)
        self.pointer = [glamour_stars.Glamour_Stars(self),self.game_mouse]

        self.dress_castle = inside.Inside(self,'dress',('pink','plain','red','yellow'))
        self.accessory_castle = inside.Inside(self,'accessory',('crown','purse','ribbon','shades'))
        self.makeup_castle = inside.Inside(self,'face',('eyelids','eyeshades','lipstick','simple'))
        self.hair_castle = inside.Inside(self,'hair',('black','brown','cinderella','rapunzel'))
        self.shoes_castle = inside.Inside(self,'shoes',('crystal','red','slipper','white'))

        self.inside = self.dress_castle

        self.fairy = False

    def what_is_my_height(self,object):
        try:        y_height = self.floor_heights[object.center_distance+(object.size[0]/2)]
        except:     y_height = 186 
        return      y_height

    def update_all(self):
        self.game_mouse.update()
        act = self.act = self.universe.action
        dir = self.direction = self.universe.dir
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
            if i.__class__ == floors.Floor or floors.Bridge:
                self.universe.screen_surface.blit(i.image,i.pos)
                i.update_all()
        for i in self.floor_image:
            if i.__class__ == floors.Water:
                self.universe.screen_surface.blit(i.image,i.pos)
                i.update_all()
        for i in self.floor_image:
            if i.__class__ == floors.Water2:
                self.universe.screen_surface.blit(i.image,i.pos)
                i.update_all()
        for i in self.foreground:
            self.universe.screen_surface.blit(i.image,i.pos)
            i.update_all()

        if self.princesses[0].inside:
            if self.white.inside:
                self.update_insidebar()
            else:
                self.update_outsidebar()

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
        self.universe.screen_surface.blit(self.down_bar.image,(0,self.down_bar_y))
        self.universe.screen_surface.blit(self.up_bar.image,(0,self.up_bar_y))

        if self.down_bar_y > 2*self.bar_goal:
            self.down_bar_y -= self.bar_speed
        if self.up_bar_y + self.bar_height< self.bar_goal:
            self.up_bar_y += self.bar_speed
        if self.white.alpha_value > 150:
            self.universe.screen_surface.blit(self.princesses[0].image, ((self.universe.width/2)-(self.princesses[0].image_size[0]/2),
                                               (self.universe.height/2)-(self.princesses[0].image_size[1]/2)))
            self.princesses[0].update_all()
            [self.universe.screen_surface.blit(i.image,i.pos) for i in self.inside.buttons]
            [i.update_all() for i in self.inside.buttons]
            [self.universe.screen_surface.blit(i.image,i.pos) for i in self.inside.items if i.queue]
            [i.update_all() for i in self.inside.items]
        if self.bar_speed < 20:
            self.bar_speed += self.bar_speed

    def update_outsidebar(self):
        self.universe.screen_surface.blit(self.down_bar.image,(0,self.down_bar_y))
        self.universe.screen_surface.blit(self.up_bar.image,(0,self.up_bar_y))

        if self.down_bar_y < self.universe.height:
            self.down_bar_y += self.bar_speed
        if self.up_bar_y > -self.bar_height:
            self.up_bar_y -= self.bar_speed
        if self.white.alpha_value > 0:
            self.universe.screen_surface.blit(self.princesses[0].image, ((self.universe.width/2)-(self.princesses[0].image_size[0]/2),
                                             (self.universe.height/2)-(self.princesses[0].image_size[1]/2)))
        if self.bar_speed < 20:
            self.bar_speed += self.bar_speed

    def BathhouseSt(self):
        self.gates = []
        self.directory = self.maindir+'bathhouse_st/'
        self.background= [scenarios.Background(110,self,self.maindir+'ballroom/ballroom_day/')]
        self.scenarios_prep  = [scenarios.Scenario(0,    self.directory+'left_corner_house/base/',self,index=0),
                                scenarios.Scenario(2350, self.directory+'left_house/base/',       self,index=0),
                                scenarios.Scenario(2920, self.directory+'small_house/base/',      self,index=0),
                                scenarios.Scenario(4700, self.directory+'right_house/base/',      self,index=0),
                                scenarios.Scenario(550,  self.directory+'bathhouse/bathhouse/',self,index =0),
                                scenarios.Scenario(3400,self.directory+'home/castelo/',self,index =0),
                                scenarios.Scenario(5850,self.directory+'magic_beauty_salon/base/',self,index=0),
                                scenarios.Flower(0,     'data/images/scenario/omni/flower_0/',self,8),
                                scenarios.Flower(350,   'data/images/scenario/omni/flower_1/',self,12),
                                scenarios.Flower(3135,  'data/images/scenario/omni/flower_3/',self,10),
                                scenarios.Flower(3126,  'data/images/scenario/omni/colorful_tree_1/',self,8),]
        self.scenarios_prep.extend([scenarios.Scenario(i,self.directory+'light_post/post/',self) for i in [2300,3350,4700,5470,5770]])

        self.gates =   [scenarios.BuildingDoor((620,490),self.directory+'bathhouse/door/',self),
                        scenarios.BuildingDoor((3820,490),self.directory+'home/door/',self),
                        scenarios.BuildingDoor((6000,465),self.directory+'magic_beauty_salon/door/',self),
                        scenarios.Gate(300, self.maindir+'omni/gate/',self,self.DressSt,index = 0),
                        scenarios.Gate(5510,self.maindir+'omni/gate/',self,self.AccessorySt,index = 0)]

        self.scenarios = BigScenario(self),

        for i in self.scenarios_prep:
            self.scenarios[0].image.blit(i.image,i.pos)

        self.enemies    = [enemy.Carriage(3,self.enemy_dir+'carriage/',3000,self),
                           enemy.OldLady(2,self.enemy_dir+'old_lady/',4000,self),
                           enemy.Schnauzer(10,self.enemy_dir+'schnauzer/',2600,self,[22,22,22,22],dirty=True),
                           enemy.Butterfly(4,self.enemy_dir+'butterflies/',6000,self)]

        self.floor_image= [floors.Floor(c,self.directory+'floor/tile/',self) for c in range(18)]
        floors.Bridge(self.directory+'floor/japanese_bridge/',4,self)

        self.sky             = [skies.Sky(self.maindir+'skies/daytime/daytime.png',self,self.universe.clock_pointer)]
        self.clouds     = [clouds.Cloud(self) for cl in range(3)]
        [self.sky[0].image.blit(i.image,i.pos) for i in self.clouds]

        self.moving_scenario = [moving_scenario.MovingScenario(1,self,self.directory+'billboard_city/billboard/')]

        self.scenarios_front = [scenarios.FrontScenario(6440,self.directory+'magic_beauty_salon/portal/',self,index=0)]

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

    def DressSt(self):
        self.gates = []                       
        self.directory = self.maindir+'dress_st/'
        self.background =  [scenarios.Background(110,self,'data/images/scenario/ballroom/ballroom_day/')]
        self.scenarios_prep  =  [scenarios.Scenario(0,self.directory+'Dress_Tower/',self,index =0),
                            scenarios.Scenario(0,self.directory+'Dress_Tower/flag/',self,index=0),
                            scenarios.Scenario(700,self.directory+'fachwerk_2/',self,index=0),
                            scenarios.Scenario(1400,self.directory+'fachwerk_3/',self,index=0),
                            scenarios.Scenario(2150,self.directory+'apple_pillar/',self,index=0),
                            scenarios.Scenario(2500,self.directory+'knight_statue/',self,index=0),
                            scenarios.Scenario(2850,self.directory+'chair/',self,index=0),
                            scenarios.Scenario(2250,self.directory+'flowers/',self,index=0),
                            scenarios.Scenario(3100,self.directory+'fachwerk_1/',self,index=0),
                            scenarios.Scenario(4300,self.directory+'snow_white_castle/',self,index=0)]

        self.scenarios = BigScenario(self),
        for i in self.scenarios_prep:
            self.scenarios[0].image.blit(i.image,i.pos)

        self.enemies    = [ enemy.Carriage(3,self.enemy_dir+'carriage/',3000,self),
                            enemy.OldLady(2,self.enemy_dir+'old_lady/',4000,self),
                            enemy.Schnauzer(10,self.enemy_dir+'schnauzer/',2600,self,[22,22,22,22],dirty=True),
                            enemy.Butterfly(4,self.enemy_dir+'butterflies/',6000,self)]

        self.gates = [scenarios.BuildingDoor((155,300),self.directory+'Dress_Tower/door/',self),
                      scenarios.BuildingDoor((4577,300),self.directory+'snow_white_castle/door/',self),
                      scenarios.Gate(1100,'data/images/scenario/omni/gate/',self,self.BathhouseSt,index = 0),
                      scenarios.Gate(3840,'data/images/scenario/omni/gate/',self,self.AccessorySt,index = 0)]

        self.floor_image= [floors.Floor(c,self.directory+'floor/',self) for c in range(30)]
        self.sky        = [skies.Sky('data/images/scenario/skies/daytime/daytime.png',self,self.universe.clock_pointer)]
        self.clouds     = [clouds.Cloud(self) for cl in range(3)]
        [self.sky[0].image.blit(i.image,i.pos) for i in self.clouds]
        self.moving_scenario = [moving_scenario.MovingScenario(1,self,'data/images/scenario/bathhouse_st/billboard_city/billboard/')]
        self.scenarios_front = [scenarios.Scenario(2050,self.directory+'fence/',self,index=0),]
        pygame.mixer.music.load("data/NeMedohounkou.ogg")
        try:       pygame.mixer.music.play()
        except:    print "Warning: no music loaded."
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
        self.background =  [scenarios.Background(110,self,'data/images/scenario/ballroom/ballroom_day/')]
        self.scenarios_prep  =  [scenarios.Scenario(i[0],self.directory+i[1],self) for i in 
                               ((-3,'accessory_tower/'),
                                (800,'accessory_tower/banner/'),
                                (1350,'cathedral/base/'),
                                (2500,'hut/base/'),
                                (3400,'house/base/'),
                                (4400,'statue/base/'),
                                (5700,'viking_house/base/'),
                                (7500,'castle/base/'))]
        self.scenarios = BigScenario(self),
        for i in self.scenarios_prep:
            self.scenarios[0].image.blit(i.image,i.pos)

        self.enemies    = [ enemy.Carriage(3,self.enemy_dir+'carriage/',3000,self),
                            enemy.OldLady(2,self.enemy_dir+'old_lady/',4000,self),
                            enemy.Schnauzer(10,self.enemy_dir+'schnauzer/',2600,self,[22,22,22,22],dirty=True),
                            enemy.Butterfly(4,self.enemy_dir+'butterflies/',6000,self)]
        self.gates.extend([scenarios.Gate(1100,'data/images/scenario/omni/gate/',self,self.DressSt,index = 0),
                          scenarios.Gate(5510,'data/images/scenario/omni/gate/',self,self.BathhouseSt ,index = 0)])
        self.floor_image= [floors.Floor(fl,self.directory+'floor/tile/',self) for fl in range(30)]
        self.floor_image.extend([floors.Water(wat,self.directory+'water/tile/',self) for wat in range(5)])
        self.floor_image.extend([floors.Water2(wat,self.directory+'water/tile/',self) for wat in range(5)])

        self.sky        = [skies.Sky('data/images/scenario/skies/daytime/daytime.png',self,self.universe.clock_pointer)]
        self.clouds     = [clouds.Cloud(self) for cl in range(3)]
        [self.sky[0].image.blit(i.image,i.pos) for i in self.clouds]

        self.moving_scenario = [moving_scenario.MovingScenario(1,self,'data/images/scenario/bathhouse_st/billboard_city/billboard/')]
        self.scenarios_front = [scenarios.Scenario(178,self.directory+'accessory_tower/front/',self,index=0),
                                scenarios.Scenario(3400,self.directory+'house/front/',self)]
        self.scenarios_front.extend([scenarios.Scenario(3000+i,'data/images/scenario/omni/grass_'+str(random.randint(1,4))+'/',self) for i in (2,50,80,120,180,210,300)])

#        os.popen4('ogg123 ~/Bazaar/Glamour/glamour/data/NeMedohounkou.ogg')
        pygame.mixer.music.load("data/NeMedohounkou.ogg")
        try:       pygame.mixer.music.play()
        except:    print "Warning: no music loaded."
        self.princesses = self.princesses or [princess.Princess(self,save=self.universe.file),None]
        panel.Data('', self.princesses[0].glamour_points, (300, 0), self,0,size=120)

        ### Set Floor ###
        self.floor_heights = {}


class Foreground():
    def __init__(self,universe):
        self.pos = 0,0
        self.image = pygame.Surface((universe.width,universe.height)).convert()
        self.image.fill((255,255,255))
        self.alpha_value = 0
        self.inside = False
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
        self.image      = pygame.Surface((7000,level.universe.height),pygame.SRCALPHA).convert_alpha()
        self.pos = [self.level.universe.center_x,0]

    def update_all(self):
        self.pos[0]         = self.level.universe.center_x

