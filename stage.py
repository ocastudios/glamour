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
    down_bar = pygame.image.load('data/images/interface/omni/small_bar/0.png')
    up_bar   = pygame.transform.flip(down_bar,0,1)

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
        self.blitlist = ('clouds','background','moving_scenario','scenarios','gates','enemies','menus','princesses')
        self.foreground = []

        self.white = Foreground(self.universe)


        self.bar_positions = range(0,self.universe.width+10,self.down_bar.get_width())
        self.bar_height = self.up_bar.get_height()
        self.down_bar_y = self.universe.height
        self.up_bar_y   = - self.bar_height
        self.bar_goal   = self.universe.height/3
        self.bar_speed  = 1
        self.pointer = [glamour_stars.Glamour_Stars(self)]

        self.dress_castle = Inside(self,'dress',('pink','plain','red','yellow'))
        self.accessory_castle = Inside(self,'accessory',('crown','purse','ribbon','shades'))
        self.makeup_castle = Inside(self,'face',('eyelids','eyeshades','lipstick','simple'))
        self.hair_castle = Inside(self,'hair',('black','brown','cinderella','rapunzel'))
        self.shoes_castle = Inside(self,'shoes',('crystal','red','slipper','white'))
        

        self.princesses = None
        self.inside = self.dress_castle
    def what_is_my_height(self,object):
        try:        y_height = self.floor_heights[object.center_distance+(object.size[0]/2)]
        except:     y_height = 186 
        return      y_height
    def update_all(self):
        try:
            surface
        except:
            surface = self.universe.screen_surface
        act = self.act = self.universe.action
        dir = self.direction = self.universe.dir
        [i.update_all(self.princess) for i in self.cameras]
        self.universe.movement(self.direction)
        [surface.blit(i.background,(0,0)) for i in self.sky]
        for att in self.blitlist:
            exec('[surface.blit(i.image,i.pos) for i in self.'+att+' if i.image ]')
            #and i.rect.colliderect(self.cameras[0].rect) DID NOT PROVIDE GREAT PERFORMANCE GAIN
            exec('[i.update_all() for i in self.'+att+']')
        for effect in self.princess.effects:
            surface.blit(effect[0],effect[1])
        for i in self.scenarios_front:
            surface.blit(i.image,i.pos)
            i.update_all()
        [surface.blit(i.arrow_image,i.arrow_pos) for i in self.gates if self.princess.rect.colliderect(i.rect) and i.arrow_image]
        for i in self.floor_image:
            if i.__class__ == floors.Floor or floors.Bridge:
                surface.blit(i.image,i.pos)
                i.update_all()
        for i in self.floor_image:
            if i.__class__ == floors.Water:
                surface.blit(i.image,i.pos)
                i.update_all()
        for i in self.floor_image:
            if i.__class__ == floors.Water2:
                surface.blit(i.image,i.pos)
                i.update_all()
        for i in self.foreground:
            surface.blit(i.image,i.pos)
            i.update_all()

        if self.princess.inside:
            self.update_insidebar()

        for i in self.clock:
            surface.blit(i.image,i.pos)
        for i in self.panel:
            surface.blit(i.label,i.pos)
            i.update(self.princess.glamour_points)
        for i in self.pointer:
            surface.blit(i.image,i.pos)
            i.update_all()

    def update_insidebar(self):
        try:
            surface, size
        except:
            surface = self.universe.screen_surface
            size = self.princess.image.get_size()
        for p in self.bar_positions:
            surface.blit(self.down_bar,(p,self.down_bar_y))
            surface.blit(self.up_bar,(p,self.up_bar_y))
        if self.down_bar_y > 2*self.bar_goal:
            self.down_bar_y -= self.bar_speed
        if self.up_bar_y + self.bar_height< self.bar_goal:
            self.up_bar_y += self.bar_speed
        elif self.white.alpha_value > 150:
            surface.blit(self.princess.image, ((self.universe.width/2)-(size[0]/2),
                                               (self.universe.height/2)-(size[1]/2)))

            [surface.blit(i.image,i.pos) for i in self.inside.items]
            [i.update_all() for i in self.inside.items]

        if self.bar_speed < 20:
            self.bar_speed += self.bar_speed

    def BathhouseSt(self):
        self.gates = []

        self.directory = self.maindir+'bathhouse_st/'
        self.background= [scenarios.Background(110,self,self.maindir+'ballroom/ballroom_day/')]

        self.clouds     = [clouds.Cloud(self) for cl in range(3)]

        self.scenarios  = [scenarios.Scenario(0,    self.directory+'left_corner_house/base/',self,index=0),
                           scenarios.Scenario(2350, self.directory+'left_house/base/',       self,index=0),
                           scenarios.Scenario(2920, self.directory+'small_house/base/',      self,index=0),
                           scenarios.Scenario(4700, self.directory+'right_house/base/',      self,index=0),

                           scenarios.Building(550,self.directory+'bathhouse/bathhouse/',self,
                                  {'pos':(270,540),'directory':self.directory+'bathhouse/door/'},index =0),
                           scenarios.Building(3400,self.directory+'home/castelo/',self,
                                  {'pos':(536,593),'directory':self.directory+'home/door/'},index =0),
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

        self.pointer.extend([fairy.Fairy(20,self)])

        try:       pygame.mixer.music.play()
        except:    print "Warning: no music loaded."

        self.princess = self.princess or princess.Princess(self)
        self.princesses = (self.princess,)
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
        self.clouds     = [clouds.Cloud(self) for cl in range(10)]
        self.scenarios  =  [scenarios.Building(0,self.directory+'Dress_Tower/',self,
                                {'pos':(155,390),'directory':self.directory+'Dress_Tower/door/'},index =0),
                            scenarios.Scenario(0,self.directory+'Dress_Tower/flag/',self,index=0),
                            scenarios.Scenario(700,self.directory+'fachwerk_2/',self,index=0),
                            scenarios.Scenario(1400,self.directory+'fachwerk_3/',self,index=0),
                            scenarios.Scenario(2150,self.directory+'apple_pillar/',self,index=0),
                            scenarios.Scenario(2500,self.directory+'knight_statue/',self,index=0),
                            scenarios.Scenario(2850,self.directory+'chair/',self,index=0),
                            scenarios.Scenario(2250,self.directory+'flowers/',self,index=0),
                            scenarios.Scenario(3100,self.directory+'fachwerk_1/',self,index=0),
                            scenarios.Building(4300,self.directory+'snow_white_castle/',self,
                                {'pos':(277,500),'directory':self.directory+'snow_white_castle/door/'},index=0)]
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
        self.background =  [scenarios.Background(110,self,'data/images/scenario/ballroom/ballroom_day/')]
        self.clouds     = [clouds.Cloud(self) for cl in range(10)]
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

#        os.popen4('ogg123 ~/Bazaar/Glamour/glamour/data/NeMedohounkou.ogg')
        pygame.mixer.music.load("data/NeMedohounkou.ogg")
        try:       pygame.mixer.music.play()
        except:    print "Warning: no music loaded."
        self.princess = self.princess or princess.Princess(self,distance = 5400)
        panel.Data('', self.princess.glamour_points, (300, 0), self,0,size=120)

        ### Set Floor ###
        self.floor_heights = {}
class Foreground():
    def __init__(self,universe):
        self.pos = 0,0
        self.image = pygame.Surface((universe.width,universe.height)).convert()
        self.image.fill((255,255,255))
        self.alpha_value = 0
        self.inside = True
        self.image.set_alpha(self.alpha_value)
    def update_all(self):
        if self.inside:
            if self.alpha_value < 200:
                self.alpha_value += 5
        else:
            if self.alpha_value > 50:
                self.alpha_value -= 5
        self.image.set_alpha(self.alpha_value)


class Inside():
    def __init__(self, level, item_type, item_list):
        self.level  = level
        self.type_of_items = item_type
        self.items = [Item(self, i) for i in item_list]
        self.buttons    = ()
        self.texts      = ()
class Item():
    def __init__(self, room, directory):
        self.level  = room.level
        self.type   = room.type_of_items
        self.image  = pygame.image.load('data/images/princess/'+self.type+'_'+directory+'/stay/0.png').convert_alpha()
        self.size   = self.image.get_size()
        self.pos    = [1300,(self.level.universe.width/2)-self.size[1]]
    def update_all(self):
        if self.pos[0] > (3*(self.level.universe.width/4))-(self.size[0]/2):
            self.pos[0] -= 5

