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
#import itertools
import camera
import mousepointer
import inside
import ball
from settings import *
#TODO Insert every rect that is moving in stage class self.all and use main display.update to update only the different rects.
#TODO substitute all these lists by a single list, blitting on the screen using the class to estipulate the order.

def p(positions):
    return [int(i*scale) for i in positions ]
###Gate Positions###
bathhousegate = p([480, 8138])
dressgate =     p([800,4142, 8471])
accessorygate = p([1497, 4174, 7836])
makeupgate =    p([1200, 4661, 8231])
shoegate =      p([1198, 4690, 8140])


class Stage():
    enemy_dir = 'data/images/enemies/'
    maindir        = 'data/images/scenario/'
    princesses = None
    def __init__(self,size,universe):
        self.universe       = universe
        self.cameras=[camera.GameCamera(self,-4220*scale)]
        self.gates          = []
        self.clock          = []
        self.floor_heights  = {}
        self.floor          = universe.floor-186*scale
        self.menus          = []
        self.panel          = []
        self.pointer        = []
        self.scenarios_front= []
        self.animated_scenarios =[]
        self.size = size
        self.blitlist = ('sky', 'background', 'moving_scenario', 'scenarios', 'animated_scenarios' ,'gates', 'lights', 'enemies', 'menus', 'princesses')
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
        self.inside = self.dress_castle()
        self.fairy = True
        self.omni_directory = 'data/images/scenario/omni/'
        self.ball = None
        self.endmusic = pygame.event.Event(pygame.USEREVENT,{'music':'finished'})
        self.enemies_list = {
                'BathhouseSt':'Schnauzer'   ,
                'DressSt': 'Bird'           ,
                'AccessorySt': 'Schnauzer'  ,
                'MakeupSt': 'OldLady'       ,
                'ShoesSt' : 'FootBoy'
                }

    def dress_castle(self):
        return inside.Inside(self,'dress',('pink','plain','red','yellow'))
    def accessory_castle(self):
        return inside.Inside(self,'accessory',('crown','purse','ribbon','shades'))
    def makeup_castle(self):
        return inside.Inside(self,'face',('eyelids','eyeshades','lipstick','simple'))
    def hair_castle(self):
        return inside.Inside(self,'hair',('black','brown','cinderella','rapunzel','rastafari', 'red', 'short', 'sleeping', 'snowwhite', 'yellow'))
    def shoes_castle(self):
        return inside.Inside(self,'shoes',('crystal','red','slipper','white'))
    def bathhouse_castle(self):
        return inside.Inside(self,'shower', [])



    def what_is_my_height(self,object):
        try:        y_height = self.floor_heights[int(object.center_distance+(object.size[0]/2))]
        except:     y_height = self.floor
        return      y_height

    def update_all(self):
        self.game_mouse.update()
        act = self.act = self.universe.action
        dir = self.direction = self.universe.dir
        if self.universe.clock_pointer.count > 160:
            if self.background[0] == self.ballroom['day']:
                self.background = [self.ballroom['night']]
        else:
            if self.background[0] == self.ballroom['night']:
                self.background = [self.ballroom['day']]
        if self.universe.clock_pointer.time == 'ball':
            self.ball = self.ball or ball.Ball(self, self.universe, self.princesses[0])
            self.ball.update_all    ()
        else:
            if self.ball:
                self.ball = None
            self.cameras[0].update_all()
            self.universe.movement(self.direction)
            for att in self.blitlist:
                if att == 'lights':
                    if self.universe.clock_pointer.time == 'night':
                        for i in self.lights:
                            if i['status'] == 'on':
                                self.universe.screen_surface.blit(i['images'].list[i['images'].itnumber.next()],i['position'].pos)
                                i['position'].update_pos()
                            if i['status'] == 'off' and random.randint(0,10) == 0:
                                i['status'] = 'on'
                                i['position'].update_pos()
                else:
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
                i.update((self.princesses[0].center_distance,self.princesses[0].pos[1]))
            for i in self.pointer:
                self.universe.screen_surface.blit(i.image,i.pos)
                i.update_all()
            if self.fairy:
                for i in self.fae:
                    self.universe.screen_surface.blit(i.image,i.pos)
                    i.update_all()

    def update_insidebar(self):
        self.universe.screen_surface.blit(self.white.image,(0,0))
        if self.inside.status[:4] == 'bath': #Bath Castle
            if self.inside.status == 'bath':
                self.white.alpha_value = 0
                self.inside.status = 'bath_loading'
            elif self.inside.status == 'bath_loading':
                self.white.image.set_alpha(self.white.alpha_value)
                if self.white.alpha_value < 200:
                    self.white.alpha_value += 10
                if self.white.alpha_value >= 200:
                    self.inside.status = 'bath_choosing'
            elif self.inside.status == 'bath_choosing':
                self.princesses[0].dirt = 0
                self.princesses[1] = None
                self.inside.status = 'bath_done'
            elif self.inside.status == 'bath_done':
                if self.white.alpha_value > 0:
                    self.white.alpha_value -= 10
                    self.white.image.set_alpha(self.white.alpha_value)
                else:
                    self.white.alpha_value = 0
                    self.inside.status = 'bath_openning'
                self.white.image.set_alpha(self.white.alpha_value)
            elif self.inside.status == 'bath_openning':
                for i in self.gates:
                    if i.rect.colliderect(self.princesses[0].rect):
                        i.open = True
                        if i.images.number >= i.images.lenght -1:
                            self.inside.status = 'bath_closing'
            elif self.inside.status == 'bath_closing':
                for i in self.gates:
                    if i.rect.colliderect(self.princesses[0].rect):
                        i.outside()
                self.princesses[0].inside = False
        else: #Choosing Clothes Castles
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


    def BathhouseSt(self,goalpos = None):
        if goalpos:
            self.princesses[0].center_distance = goalpos
            self.universe.center_x = -goalpos+(self.universe.width/2)
        self.gates = []
        self.directory = self.maindir+'bathhouse_st/'
        self.ballroom = {   'day': scenarios.Background(110,self,self.maindir+'ballroom/ballroom_day/'),
                            'night': scenarios.Background(110,self,self.maindir+'ballroom/ballroom_night/')}
        self.background = [self.ballroom['day']]
        self.scenarios_prep  = [scenarios.Scenario(i[0],i[1],self) for i in (
                                (100*scale, self.omni_directory+'tree_2/'),
                                (200*scale, self.omni_directory+'bush/'),
                                (0  *scale,    self.directory+'left_corner_house/base/'),
                                (793*scale,  self.directory+'bathhouse/bathhouse/'),
                                (3280*scale, self.omni_directory+'tree_2/'),
                                (2810*scale, self.directory+'left_house/base/'),
                                (2795*scale, self.omni_directory+'small_bush_1/'),
                                (3384*scale, self.omni_directory+'small_bush_1/'),
                                (3499*scale, self.omni_directory+'small_bush_1/'),
                                (3948*scale, self.omni_directory+'tree_2/'),
                                (3677*scale, self.directory+'small_house/base/'),
                                (4060*scale, self.omni_directory+'small_bush_2/'),
                                (4479*scale, self.omni_directory+'tree_1/'),
                                (4671*scale,self.directory+'home/base/'),
                                (3948*scale, self.omni_directory+'tree_2/'),
                                (7014*scale, self.omni_directory+'tree_1/'),
                                (7826*scale, self.omni_directory+'tree_1/'),
                                (7147*scale, self.directory+'right_house/base/',),
                                (5975*scale, self.omni_directory+'tree_2/'),
                                (6354*scale, self.omni_directory+'bush/'),
                                (6584*scale, self.omni_directory+'tree_2/'),
                                (6917*scale, self.omni_directory+'bush/'),
                                (7552*scale, self.omni_directory+'small_bush_1/'),
                                (7828*scale, self.omni_directory+'small_bush_2/'),
                                (8517*scale,self.directory+'magic_beauty_salon/base/'),
                                (8562*scale,self.omni_directory+'small_bush_2/'),
                                (8696*scale,self.omni_directory+'small_bush_1/'))]
        self.scenarios_prep.extend([scenarios.Scenario(i,self.directory+'light_post/post/',self)
                                for i in p([405,2730,4217,6041,8469])])
        self.gates =   [scenarios.BuildingDoor(p((1063,453)),self.directory+'bathhouse/door/',self,self.bathhouse_castle(),bath = True),
                        scenarios.BuildingDoor(p((5206,500)),self.directory+'home/door/',self,self.hair_castle()),
                        scenarios.BuildingDoor(p((9305,503)),self.directory+'magic_beauty_salon/door/',self,self.shoes_castle()),
                        scenarios.Gate(bathhousegate[0], self.maindir+'omni/gate/',self,self.ShoesSt, goalpos = shoegate[2],),
                        scenarios.Gate(bathhousegate[1],self.maindir+'omni/gate/',self,self.AccessorySt,goalpos = accessorygate[0])]
        self.scenarios = BigScenario(self),
        for i in self.scenarios_prep:
            self.scenarios[0].image.blit(i.image,i.pos)
        self.enemies    = [enemy.Carriage(3,self.enemy_dir+'carriage/',     3000*scale,self),
                           enemy.OldLady(2,self.enemy_dir+'old_lady/',      4000*scale,self),
                           enemy.Schnauzer(10,self.enemy_dir+'schnauzer/',  2600*scale,self,p([22,22,22,22]),dirty=True),
                           enemy.Butterfly(4,self.enemy_dir+'butterflies/', 6000*scale,self),
                            ]
        self.enemies.append(enemy.FootBoy(9000*scale,self))
        self.floor_image= [floors.Floor(c,self.directory+'floor/tile/',self) for c in range(24)]
        floors.Bridge(self.directory+'floor/japanese_bridge/',5,self)

        self.sky             = [skies.Sky(self.maindir+'skies/daytime/daytime.png',self,self.universe.clock_pointer)]
        self.clouds     = [clouds.Cloud(self) for cl in range(3)]
        [self.sky[0].image.blit(i.image,i.pos) for i in self.clouds]
        self.moving_scenario = [moving_scenario.Billboard(self)]
        self.scenarios_front = [
                                scenarios.Scenario(3535*scale,self.omni_directory+'fence_1/',self),
                                scenarios.Scenario(4322*scale,self.omni_directory+'fence_1/',self),
                                scenarios.Flower(  4161*scale,     self.omni_directory+'flower_9/',self,8),
                                scenarios.Flower(  4243*scale,     self.omni_directory+'flower_6/',self,8),
                                scenarios.Flower(  4389*scale,     self.omni_directory+'flower_4/',self,8),
                                scenarios.Flower(  4332*scale,     self.omni_directory+'flower_7/',self,8),
                                scenarios.Flower(  6303*scale,     self.omni_directory+'flower_9/',self,8),
                                scenarios.Flower(  6218*scale,     self.omni_directory+'flower_6/',self,8),
                                scenarios.Flower(  6528*scale,     self.omni_directory+'flower_4/',self,8),
                                scenarios.Flower(  6665*scale,     self.omni_directory+'flower_4/',self,8),
                                scenarios.Flower(  6620*scale,     self.omni_directory+'flower_7/',self,8),
                                scenarios.Flower(  7123*scale,     self.omni_directory+'grass_2/',self,8),
                                scenarios.Flower(  7197*scale,     self.omni_directory+'grass_1/',self,8),
                                scenarios.Scenario(6058*scale,self.omni_directory+'grass_1/',self),
                                scenarios.Scenario(6754*scale,self.omni_directory+'fence_1/',self),
                                scenarios.FrontScenario(9168*scale,self.directory+'magic_beauty_salon/portal/',self,index=0)]
        self.fae = ([fairy.Fairy(20,self)])

        self.music = "data/sounds/music/bathhouse_day.ogg"
        pygame.mixer.music.load("data/sounds/music/bathhouse_day_intro.ogg")
        pygame.mixer.music.queue(self.music)
        pygame.mixer.music.queue(self.music)
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

        self.princesses = self.princesses or [princess.Princess(self,save=self.universe.file),None]
        panel.Data('', self.princesses[0].center_distance, p((300, 0)), self,0,size=120)
        ### set_floor ###
        self.floor_heights = [186*scale]*int((9400*scale))
        count   = 0
        FDICT   = [
                p((955,970,199  )),
                p((970,1200,212 )),
                p((1200,1220,199)),
                p((1730,1875,201)),
                p((1780,1905,221)),
                p((1850,1860,231)),
                p((1860,1880,241)),
                p((1880,1985,251)),
                p((1910,1995,261)),
                p((1970,2245,271)),
                p((2245,2305,261)),
                p((2305,2365,251)),
                p((2365,2415,231)),
                p((2415,2445,221)),
                p((2445,2475,211)),
                p((2475,2500,201)),
                p((9200,9360,198))]
        for i in FDICT:
            for r in range(i[0],i[1]):
                self.floor_heights[r]=i[2]
        self.animated_scenarios =[]
        self.lights = []
        for i in self.scenarios_prep:
            try:
                if i.lights:
                    self.lights.append(i.lights)
            except:
                pass

    def DressSt(self,goalpos = None):
        self.universe.center_x = -goalpos+(self.universe.width/2)
        self.princesses[0].center_distance = goalpos
        self.gates = []
        self.directory = self.maindir+'dress_st/'
        self.scenarios_prep  =  [scenarios.Scenario(scale*1086,self.omni_directory+'tree_2/',  self),
                                 scenarios.Scenario(scale*0,self.directory+'Dress_Tower/',     self),
                                 scenarios.Scenario(scale*1307,self.directory+'fachwerk_3/base/',self),
                                 scenarios.Scenario(scale*1127,'data/images/scenario/bathhouse_st/light_post/post/',self),
                                 scenarios.Scenario(scale*1992,self.omni_directory+'hydrant/',self),
                                 scenarios.Scenario(scale*2091,self.directory+'fachwerk_2/base/',self),
                                 scenarios.Scenario(scale*2538,'data/images/scenario/bathhouse_st/light_post/post/',self),
                                 scenarios.Scenario(scale*2901,self.omni_directory+'tree_2/',self),
                                 scenarios.Scenario(scale*2659,self.directory+'flowers/base/',self),
                                 scenarios.Scenario(scale*3085,self.directory+'chair/',self,invert = True),
                                 scenarios.Scenario(scale*3039,self.omni_directory+'grass_2/',self),
                                 scenarios.Scenario(scale*3605,self.directory+'knight_statue/',self),
                                 scenarios.Scenario(scale*4625,self.directory+'apple_pillar/',self),
                                 scenarios.Scenario(scale*4038,'data/images/scenario/bathhouse_st/light_post/post/',self),
                                 scenarios.Scenario(scale*4682,self.omni_directory+'tree_1/',self),
                                 scenarios.Scenario(scale*4878,self.directory+'chair/',self),
                                 scenarios.Scenario(scale*5128,self.omni_directory+'hydrant/',self),
                                 scenarios.Scenario(scale*5337,self.omni_directory+'tree_2/',self),
                                 scenarios.Scenario(scale*5600,self.omni_directory+'tree_1/',self),
                                 scenarios.Scenario(scale*5657,self.omni_directory+'grass_3/',self),
                                 scenarios.Scenario(scale*5220,self.directory+'flowers/base/',self),
                                 scenarios.Scenario(scale*6095,'data/images/scenario/bathhouse_st/light_post/post/',self),
                                 scenarios.Scenario(scale*6192,self.directory+'fachwerk_4/',self),
                                 scenarios.Scenario(scale*6148,self.omni_directory+'bush/',self),
                                 scenarios.Scenario(scale*6454,self.omni_directory+'flower_7/',self),
                                 scenarios.Scenario(scale*6393,self.omni_directory+'flower_8/',self),
                                 scenarios.Scenario(scale*6628,self.omni_directory+'flower_7/',self),
                                 scenarios.Scenario(scale*6724,self.omni_directory+'tree_2/',self),
                                 scenarios.Scenario(scale*6735,self.omni_directory+'bush/',self),
                                 scenarios.Scenario(scale*7310,self.omni_directory+'tree_2/',self),
                                 scenarios.Scenario(scale*7105,self.directory+'fachwerk_2/base/',self),
                                 scenarios.Scenario(scale*7536,self.directory+'fachwerk_1/',self),
                                 scenarios.Scenario(scale*8107,self.omni_directory+'tree_1/',self),
                                 scenarios.Scenario(scale*8398,'data/images/scenario/bathhouse_st/light_post/post/',self),
                                 scenarios.Scenario(scale*8917,self.directory+'snow_white_castle/',self)]

        self.scenarios = BigScenario(self),
        for i in self.scenarios_prep:
            self.scenarios[0].image.blit(i.image,i.pos)

        self.animated_scenarios = [scenarios.Scenario(0,self.directory+'Dress_Tower/flag/',self,index=0)]

        self.enemies    = [ enemy.Carriage(3,self.enemy_dir+'carriage/',    3000*scale,self),
                            enemy.OldLady(2,self.enemy_dir+'old_lady/',     4000*scale,self),
                            enemy.Schnauzer(10,self.enemy_dir+'schnauzer/', 2600*scale,self,[22*scale,22*scale,22*scale,22*scale],dirty=True),
                            enemy.Butterfly(4,self.enemy_dir+'butterflies/',6000*scale,self)]

        self.gates = [scenarios.BuildingDoor(p((100,450)),self.directory+'Dress_Tower/door/',self,self.dress_castle()),
                      scenarios.BuildingDoor(p((9092,430)),self.directory+'snow_white_castle/door/',self),
                      scenarios.Gate(dressgate[0], 'data/images/scenario/omni/gate/',self,self.AccessorySt,goalpos = accessorygate[2]),
                      scenarios.Gate(dressgate[1], 'data/images/scenario/omni/gate/',self,self.ShoesSt,goalpos = shoegate[1]),
                      scenarios.Gate(dressgate[2], 'data/images/scenario/omni/gate/',self,self.MakeupSt,goalpos = makeupgate[0])]

        self.floor_image= [floors.Floor(c,self.directory+'floor/',self) for c in range(30)]
        self.sky        = [skies.Sky('data/images/scenario/skies/daytime/daytime.png',self,self.universe.clock_pointer)]
        self.clouds     = [clouds.Cloud(self) for cl in range(3)]
        [self.sky[0].image.blit(i.image,i.pos) for i in self.clouds]
        self.scenarios_front = [scenarios.Scenario(i[0],i[1],self) for i in (
                                (557*scale,self.directory+'fence/base/'),
                                (719*scale,self.omni_directory+'grass_4/'),
                                (1200*scale,self.omni_directory+'grass_3/'),
                                (1905*scale,self.omni_directory+'grass_3/'),
                                (2098*scale,self.omni_directory+'grass_4/'),
                                (2464*scale,self.omni_directory+'grass_2/'),
                                (3408*scale,self.directory+'fence/base/'),
                                (3665*scale,self.omni_directory+'grass_3/'),
                                (4408*scale,self.directory+'fence/base/'),
                                (4606*scale,self.omni_directory+'grass_2/'),
                                (5855*scale,self.directory+'fence/base/'),
                                (7004*scale,self.omni_directory+'grass_3/'),
                                (7576*scale,self.omni_directory+'grass_3/'),
                                (8416*scale,self.omni_directory+'grass_3/'),
                                (8822*scale,self.omni_directory+'grass_3/')
                                )]
        self.music = "data/sounds/music/dress_day_intro.ogg"
        pygame.mixer.music.load("data/sounds/music/dress_day_intro.ogg")
        pygame.mixer.music.queue(self.music)
        pygame.mixer.music.queue(self.music)
        pygame.mixer.music.play()

        self.princesses = self.princesses or [princess.Princess(self,save=self.universe.file),None]
        self.lights = []
        for i in self.scenarios_prep:
            try:
                if i.lights:
                    self.lights.append(i.lights)
            except:
                pass
        ### Set Floor ###
        self.floor_heights = [185*scale]*(9400*scale)
        count   = 0
        n       = 1120
        a       = 15
        FDICT   = [p((50,189,252)),p((190,219,232)),p((220,260,210)),p((261,260,194))]
        for i in FDICT:
            for r in range(i[0],i[1]):
                self.floor_heights[r]=i[2]



    def AccessorySt(self,goalpos = None):
        self.universe.center_x = -goalpos+(self.universe.width/2)
        self.princesses[0].center_distance = goalpos
        self.gates = []
        self.directory = self.maindir+'accessory_st/'
        self.scenarios_prep  =  [scenarios.Scenario(i[0],i[1],self) for i in
                               ((scale*-3,self.directory+'accessory_tower/'),
                                (scale*800,self.directory+'accessory_tower/banner/'),
                                (scale*2575,self.omni_directory+'tree_2/'),
                                (scale*1795,self.directory+'statue/base/'),
                                (scale*1757,self.omni_directory+'small_bush_2/'),
                                (scale*1852,self.omni_directory+'small_bush_1/'),
                                (scale*2800,self.omni_directory+'small_bush_2/'),
                                (scale*2871,self.omni_directory+'small_bush_1/'),
                                (scale*2896,self.directory+'cathedral/base/'),
                                (scale*3336,self.omni_directory+'small_bush_1/'),
                                (scale*4400,self.omni_directory+'tree_2/'),
                                (scale*4497,self.directory+'hut/base/'),
                                (scale*6405,self.omni_directory+'tree_2/'),
                                (scale*5470,self.directory+'house/base/'),
                                (scale*3903,self.omni_directory+'fence_1/'),
                                (scale*5249,self.omni_directory+'small_bush_1/'),
                                (scale*5499,self.omni_directory+'small_bush_1/'),
                                (scale*6560,self.directory+'viking_house/base/'),
                                (scale*6420,self.omni_directory+'small_bush_1/'),
                                (scale*6512,self.omni_directory+'small_bush_2/'),
                                (scale*7446,self.omni_directory+'small_bush_2/'),
                                (scale*7531,self.omni_directory+'small_bush_1/'),
                                (scale*7644,self.omni_directory+'bush/'),
                                (scale*8218,self.directory+'castle/base/'),
                                (scale*9000,self.omni_directory+'grass_1/'),
                                (scale*9114,self.omni_directory+'grass_4/'),
                                (scale*9200,self.omni_directory+'grass_1/'),
                                (scale*9313,self.omni_directory+'small_bush_2/'),
                                (scale*9374,self.omni_directory+'flower_8/'),
                                (scale*9476,self.omni_directory+'small_bush_1/'),
                            )]
        self.scenarios_prep.extend([
                                scenarios.Scenario(scale*(2*400),self.directory+'floor/left_bank_back/',self, height = 4),
                                scenarios.Scenario(scale*(3*400),self.directory+'floor/right_bank_back/',self,height = 4)])
        self.scenarios = BigScenario(self),


        for i in self.scenarios_prep:
            self.scenarios[0].image.blit(i.image,i.pos)

        self.enemies    = [ enemy.Carriage(3,self.enemy_dir+'carriage/',    scale*3000,self),
                            enemy.OldLady(2,self.enemy_dir+'old_lady/',     scale*4000,self),
                            enemy.Schnauzer(10,self.enemy_dir+'schnauzer/', scale*2600,self,p([22*scale,22*scale,22*scale,22*scale]),dirty=True),
                            enemy.Butterfly(4,self.enemy_dir+'butterflies/',scale*6000,self)]
        self.gates.extend([
                            scenarios.Gate(accessorygate[0], 'data/images/scenario/omni/gate/',self,self.BathhouseSt,goalpos = bathhousegate[1]),
                            scenarios.Gate(accessorygate[1], 'data/images/scenario/omni/gate/',self,self.MakeupSt,goalpos = makeupgate[1]),
                            scenarios.Gate(accessorygate[2], 'data/images/scenario/omni/gate/',self,self.DressSt , goalpos = dressgate[0])])
        self.floor_image= [floors.Floor(fl,self.directory+'floor/tile/',self) for fl in range(30)]
        self.floor_image.extend([floors.Water(wat,self.directory+'water/tile/',self) for wat in range(11)])
        self.floor_image.extend([enemy.VikingShip(9000*scale,self)])
        self.floor_image.extend([floors.Water2(wat,self.directory+'water/tile/',self) for wat in range(11)])

        floors.Drain(self.directory+'floor/left_bank_front/',2,self)
        floors.Drain(self.directory+'floor/right_bank_front/',3,self)
        floors.Drain(self.directory+'floor/left_bank_front/',20,self)
        floors.Drain(self.directory+'floor/right_bank_front/',21,self)

        self.sky        = [skies.Sky('data/images/scenario/skies/daytime/daytime.png',self,self.universe.clock_pointer)]
        self.clouds     = [clouds.Cloud(self) for cl in range(3)]
        [self.sky[0].image.blit(i.image,i.pos) for i in self.clouds]

        self.scenarios_front = [
                                scenarios.Scenario(scale*3903,self.omni_directory+'fence_1/',self),
                                scenarios.Scenario(scale*178,self.directory+'accessory_tower/front/',self),
                                scenarios.Scenario(scale*5470,self.directory+'house/front/',self),
                                scenarios.Scenario(scale*1048,self.directory+'floor/main/',self, height = 10*scale),
                                scenarios.Scenario(scale*1180,self.directory+'floor/main/',self, height = 10*scale),
                                scenarios.Scenario(scale*1333,self.directory+'floor/main/',self, height = 10*scale),
                                scenarios.Scenario(scale*8248,self.directory+'floor/main/',self, height = 10*scale),
                                scenarios.Scenario(scale*8382,self.directory+'floor/main/',self, height = 10*scale),
                                scenarios.Scenario(scale*8534,self.directory+'floor/main/',self, height = 10*scale),
]
        self.music = "data/sounds/music/accessory_day.ogg"
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.queue(self.music)
        pygame.mixer.music.queue(self.music)
        pygame.mixer.music.play()

        self.princesses = self.princesses or [princess.Princess(self,save=self.universe.file),None]


        ### Set Floor ###
        self.floor_heights = [194*scale]*int((9400*scale))
        count   = 0
        n       = 1120
        a       = 15
        FDICT   = [
                p((850,950,92)),
                p((950,1010,180)),
                p((1010,1080,92)),
                p((1080,1150,180)),
                p((1150,1230,92)),
                p((1230,1300,180)),
                p((1300,1360,92)),
                p((5550,5610,202)),
                p((5610,5700,199)),
                p((5700,5810,197)),
                p((6170,6280,197)),
                p((6280,6350,199)),
                p((6350,6410,202)),
                p((8057,8146,92)),
                p((8147,8196,180)),
                p((8197,8286,92)),
                p((8287,8336,180)),
                p((8337,8436,92)),
                p((8437,8486,180)),
                p((8487,8547,92))
                ]

        for i in FDICT:
            for r in range(i[0],i[1]):
                self.floor_heights[r]=i[2]

        self.lights = []

        for i in self.scenarios_prep:
            try:
                if i.lights:
                    self.lights.append(i.lights)
            except:
                pass

    def MakeupSt(self,goalpos = None):
        self.universe.center_x = -goalpos+(self.universe.width/2)
        self.princesses[0].center_distance = goalpos
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
        self.gates.extend([ scenarios.Gate(makeupgate[x],'data/images/scenario/omni/gate/',self,y,goalpos = z)
                            for x,y,z in
                            ((0, self.DressSt, dressgate[2]),
                             (1, self.AccessorySt, accessorygate[1]),
                             (2, self.ShoesSt ,shoegate[0]))
                            ])
        self.gates.extend([scenarios.BuildingDoor((100,450),self.directory+'make-up_castle/door/',self,self.makeup_castle())])


        self.floor_image= [floors.Floor(fl,self.directory+'floor/',self) for fl in range(30)]

        self.sky        = [skies.Sky('data/images/scenario/skies/daytime/daytime.png',self,self.universe.clock_pointer)]
        self.clouds     = [clouds.Cloud(self) for cl in range(3)]
        [self.sky[0].image.blit(i.image,i.pos) for i in self.clouds]
        self.scenarios_front = [scenarios.Scenario(0,self.directory+'make-up_castle/front/',self)]
        self.princesses = self.princesses or [princess.Princess(self,save=self.universe.file),None]
        self.animated_scenarios = [ enemy.Lion(3200,self),
                                    enemy.Monkey(3500,self),
                                    scenarios.Scenario(2923,self.directory+'zoo/base/',self)]
        self.animated_scenarios.insert(1,self.animated_scenarios[0].tail)

        self.lights = []
        for i in self.scenarios_prep:
            try:
                if i.lights:
                    self.lights.append(i.lights)
            except:
                pass

        ### Set Floor ### (x1,x2,y)
        self.floor_heights = [190]*9400
        count   = 0
        n       = 1120
        a       = 15
        FDICT   = [ (0,90,3000),
                (90,130,330), (130,140,325),(140,150,320),(150,160,315),(160,170,310), (170,180,305), (180,190,300),
                (190,200,295), (200,210,290), (210,220,285), (220,230,280), (230,240,275), (240,250,270), (250,260,265),
                (260,270,260), (270,280,255), (280,290,250), (290,300,245), (300,310,240), (310,320,235), (320,330,230),
                (330,350,220), (350,360,210), (360,380,200)
                ]

        for i in FDICT:
            for r in range(i[0],i[1]):
                self.floor_heights[r]=i[2]
        self.music = "data/sounds/music/makeup_day.ogg"
        pygame.mixer.music.load("data/sounds/music/makeup_day_intro.ogg")
        pygame.mixer.music.queue(self.music)
        pygame.mixer.music.queue(self.music)
        pygame.mixer.music.play()

    def ShoesSt(self,goalpos=None):
        self.universe.center_x = -goalpos+(self.universe.width/2)
        self.princesses[0].center_distance = goalpos
        self.gates = []
        self.directory = self.maindir+'shoes_st/'
        self.scenarios_prep =  [scenarios.Scenario(i[0],i[1],self) for i in (
                                (0,  self.directory+'shoes_tower/base/'),
                                (649,self.omni_directory+'colorful_tree_2/'),
                                (649,self.omni_directory+'colorful_bush/'),
                                (1035,'data/images/scenario/bathhouse_st/light_post/post/'),
                                (1033,self.omni_directory+'flower_9/'),
                                (1098,self.omni_directory+'flower_9/'),
                                (1497,self.omni_directory+'colorful_tree_2/'),
                                (2368,self.omni_directory+'colorful_tree_2/'),
                                (2242,self.omni_directory+'colorful_tree_1/'),
                                (1670,self.directory+'temple/base/'),
                                (2548,self.omni_directory+'hydrant/'),
                                (2676,'data/images/scenario/bathhouse_st/light_post/post/'),
                                (3000,self.omni_directory+'colorful_bush/'),
                                (2876,self.omni_directory+'colorful_bush/'),
                                (3276,self.directory+'poor_house/base/'),
                                (3172,self.omni_directory+'colorful_tree_2/'),
                                (4086,self.omni_directory+'colorful_tree_2/'),
                                (4516,self.omni_directory+'flower_9/'),
                                (4594,self.omni_directory+'flower_9/'),
                                (4506,'data/images/scenario/bathhouse_st/light_post/post/'),
                                (5054,self.omni_directory+'flower_9/'),
                                (4992,self.omni_directory+'flower_9/'),
                                (4956,self.omni_directory+'hydrant/'),
                                (5588,self.omni_directory+'colorful_tree_2/'),
                                (5104,self.directory+'house_1/base/'),
                                (5846,self.directory+'library/base/'),
                                (5770,self.omni_directory+'colorful_bush/'),
                                (6750,'data/images/scenario/bathhouse_st/light_post/post/'),
                                (6918,self.omni_directory+'flower_9/'),
                                (7026,self.omni_directory+'flower_9/'),
                                (6918,self.omni_directory+'flower_9/'),
                                (7758,self.omni_directory+'flower_9/'),
                                (7666,self.omni_directory+'flower_9/'),
                                (7602,self.omni_directory+'flower_9/'),
                                (7778,self.omni_directory+'colorful_tree_1/'),
                                (7940,'data/images/scenario/dress_st/fence/base/'),
                                (8476,'data/images/scenario/bathhouse_st/light_post/post/'),
                                (8574,self.omni_directory+'colorful_tree_2/'),
                                (8570,self.omni_directory+'flower_9/'),
                                (8762,self.omni_directory+'flower_9/'),
                                (8682,self.omni_directory+'flower_9/'),
                                (8860,self.directory+'rapunzel_castle/base/'))]

        self.scenarios = BigScenario(self),
        for i in self.scenarios_prep:
            self.scenarios[0].image.blit(i.image,i.pos)

        self.animated_scenarios = [scenarios.Scenario(7137,self.directory+'fountain/base/',self)]

        self.enemies    = [ enemy.Carriage(3,self.enemy_dir+'carriage/',3000,self),
                            enemy.OldLady(2,self.enemy_dir+'old_lady/',4000,self),
                            enemy.Schnauzer(10,self.enemy_dir+'schnauzer/',2600,self,[22,22,22,22],dirty=True),
                            enemy.Butterfly(4,self.enemy_dir+'butterflies/',6000,self)]

        self.gates = [scenarios.Gate(shoegate[0],'data/images/scenario/omni/gate/',self,self.MakeupSt, goalpos = makeupgate[0]),
                      scenarios.Gate(shoegate[1],'data/images/scenario/omni/gate/',self,self.DressSt, goalpos = dressgate[1]),
                      scenarios.Gate(shoegate[2],'data/images/scenario/omni/gate/',self,self.BathhouseSt, goalpos = bathhousegate[0]),
]

        self.floor_image= [floors.Floor(c,self.directory+'floor/',self) for c in range(30)]
        self.sky        = [skies.Sky('data/images/scenario/skies/daytime/daytime.png',self,self.universe.clock_pointer)]
        self.clouds     = [clouds.Cloud(self) for cl in range(3)]
        [self.sky[0].image.blit(i.image,i.pos) for i in self.clouds]
        self.scenarios_front = [scenarios.Scenario(i[0],i[1],self) for i in (
                                (2754,'data/images/scenario/dress_st/fence/base/'),
                                (3936,'data/images/scenario/dress_st/fence/base/'),
                                (4434,self.omni_directory+'flower_9/'),
                                (4362,self.omni_directory+'flower_9/'),
                                (6544,self.omni_directory+'colorful_tree_2/'),
                                (6500,'data/images/scenario/dress_st/fence/base/'),
                                (6800,self.omni_directory+'colorful_tree_1/'),
                                (8860,self.directory+'rapunzel_castle/front/'),
                                )]

        self.music = "data/sounds/music/shoes_day.ogg"
        pygame.mixer.music.load("data/sounds/music/shoes_day_intro.ogg")
        pygame.mixer.music.queue(self.music)
        pygame.mixer.music.queue(self.music)
        pygame.mixer.music.play()
        self.princesses = self.princesses or [princess.Princess(self,save=self.universe.file),None]


        ### set floor ### (x1,x2,y)
        self.floor_heights = [190]*9400
        count   = 0
        n       = 1120
        a       = 15
        FDICT   = [ (250,350,242), (350,390,217), (390,430,195),(430,450,190)]

        for i in FDICT:
            for r in range(i[0],i[1]):
                self.floor_heights[r]=i[2]

        self.lights = []
        for i in self.scenarios_prep:
            try:
                if i.lights:
                    self.lights.append(i.lights)
            except:
                pass

    def define_enemies(self):
        stages = ['shoes','makeup','accessory','dress','bathhouse']
        enemies = ['OldLady', 'Schnauzer','Butterfly', 'FootBoy','Bird']

    def choose_enemies(self):
        try:
            self.file = save.readlines()
        except:
            self.file = open(save).readlines()
        #Interpret the save file
        for line in self.file:
            linha = line.split()
#            if linha[0] == self.name:
#               for enemy in linha[1:]:
#                    exec("self.enemies.append(enemy."+enemy+"(SPEED,self.enemy_dir+'"enemy.lower()+"/', int(randint(0,900)*scale),self))")

    def set_enemies(self):
        pass        


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
        tile = pygame.image.load('data/images/interface/omni/small_bar/0.png').convert_alpha()
        if up_or_down == 'up':
            tile = pygame.transform.flip(tile,0,1)
        screen_size = 1440,900 #level.universe.width, level.universe.height
        tile_size   = tile.get_size()
        image_prep  = pygame.Surface((screen_size[0],tile_size[1]),pygame.SRCALPHA).convert_alpha()
        bar_positions = range(0,(screen_size[0]/tile_size[0]+1))
        [image_prep.blit(tile,(i*tile_size[0],0)) for i in bar_positions]
        self.tile   = obj_images.scale_image(tile)
        self.tile_size = self.tile.get_size()
        self.image  = obj_images.scale_image(image_prep)


class BigScenario():
    def __init__(self,level):
        self.level      = level
        self.image      = pygame.Surface((9600*scale,level.universe.height),pygame.SRCALPHA).convert_alpha()
        self.pos        = [self.level.universe.center_x,0]

    def update_all(self):
        self.pos[0]         = self.level.universe.center_x
