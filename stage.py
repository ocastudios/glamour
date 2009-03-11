import scenarios
import obj_images
import enemy
import skies
import globals
import floors
import clouds
import random
import moving_scenario
import glamour_stars
import princess
import panel
import pygame


class Stage():
    """This class is meant to create the levels of the game. One of its most importante features is to blit everything on the screen and define what should be in each of the stages.
It is still in its early development"""
    enemy_dir = 'data/images/enemies/'
    def __init__(self,level,size,universe,directory):
        self.all = []
        self.directory      = directory
        self.background     = []
        self.cameras        = []
        self.clock          = []
        self.clouds         = []
        self.enemies        = []
        self.floor_heights  = {}
        self.floor_image    = []
        self.floor          = universe.floor-186
        self.gates          = []
        self.level          = level
        self.menus          = []
        self.moving_scenario= []
        self.night          = []
        self.objects        = []
        self.panel          = []
        self.pointer        = []
        self.princess       = None
        self.princesses     = []
        self.scenarios      = []
        self.scenarios_front= []
        self.set_floor()
        self.size = size
        self.sky = []
        #self.floor_list = {0:186,620:186}


    def bathhouse_street(self):
        pygame.mixer.music.load("data/NeMedohounkou.ogg")
        def create_clouds(number):
            count = 0
            while count <= number:
                nuvem = clouds.Cloud((random.randint(100,25000),random.randint(0,300)),[self])
                count += 1
        def create_posts(number):
            posts = [2300,3350,4700, 5470,5770]
            for i in posts:
                post = scenarios.Scenario((i,0),self.directory+'light_post/post/',self)
        def create_floor(number):
            count = 0
            while count <= number:
                tile = floors.Floor(count,self.directory+'floor/tile/',self)
                count +=1
    #Instancing Stuff
        lef_corner_house = scenarios.Scenario((0,100),self.directory+'left_corner_house/base/',self,index=0)
        gate1 = scenarios.Gate((300,0),'data/images/scenario/omni/gate/',self,index = 0)
        bathhouse = scenarios.Building((550,0),self.directory+'bathhouse/bathhouse/',self,{'pos':(270,540),'directory':self.directory+'bathhouse/door_shut/'},index =0)

        left_house = scenarios.Scenario((2350,100),self.directory+'left_house/base/',self,index = 0)
        smallhouse = scenarios.Scenario((2920,100),self.directory+'small_house/base/',self,index =0)
        home = scenarios.Building((3400,100),self.directory+'home/castelo/',self,{'pos':(537,490),'directory':self.directory+'home/door_shut/'},index =0)
        right_house = scenarios.Scenario((4700,100),self.directory+'right_house/base/',self,index=0)
        gate2 = scenarios.Gate((5510,0),'data/images/scenario/omni/gate/',self,index = 0)
        magic_beauty_salon = scenarios.Building((5790,100),self.directory+'magic_beauty_salon/base/',self,{'pos':(787,513),'directory':self.directory+'magic_beauty_salon/door/'},index=0)
        magic_beauty_salon_portal = scenarios.FrontScenario((5790,100),self.directory+'magic_beauty_salon/portal/',self,index=0)
        carriage = enemy.Carriage(3,self.enemy_dir+'carriage/',3000,self,[10,10,10,10],[10,10,10,10],[10,10,10,10])
        oldlady = enemy.OldLady(2,self.enemy_dir+'old_lady/',4000,self)
        schnauzer = enemy.Schnauzer(10,self.enemy_dir+'schnauzer/',2600,self,[22,22,22,22],[22,22,22,22],[22,22,22,22],dirty=True)
        butterflies = enemy.Butterfly(4,self.enemy_dir+'butterflies/',6000,self)
        fundo = skies.Sky('data/images/scenario/skies/daytime/daytime.png',self,globals.clock_pointer)
        create_posts(15)
        create_floor(30)
        create_clouds(50)
        bilboard = moving_scenario.MovingScenario(1,self,self.directory+'billboard_city/billboard/')
        Main_Star= glamour_stars.Glamour_Stars((0,0),self,True)

        try:       pygame.mixer.music.play()
        except:    print "Warning: no music loaded."
        self.princess = princess.Princess(self)

        info_glamour_points = panel.Data('', self.princess.glamour_points, (300, 0), self,0,size=120)
        castle = scenarios.Background((110,0),self,0,'data/images/scenario/ballroom/ballroom_day/')

        japanese_bridge = floors.Bridge(self.directory+'floor/japanese_bridge/',4,self)
    def what_is_my_height(self,object):
        try:        y_height = self.floor_heights[object.distance_from_center+(object.size[0]/2)]
        except:     y_height = 186 
        return      y_height

    def update_all(self,surface,act,dir,universe,clock_pointer):
        for i in self.cameras:
            i.update_all(self.princess)
        universe.movement(dir)
        for i in self.sky:
            surface.blit(i.background,(0,0))
#            i.set_light(clock_pointer)
        for i in self.clouds:
            surface.blit(i.image,i.pos)
            i.update_all(dir,act)
        for i in self.background:
            surface.blit(i.image,i.pos)
            i.update_all()
        for i in self.moving_scenario:
            surface.blit(i.image,i.pos)
            i.update_all(act,dir)
#        for i in self.sky:
#            surface.blit(i.night_back_image,(0,0))
        for i in self.scenarios:
            surface.blit(i.image,i.pos)
            i.update_all()
        for i in self.gates:
            surface.blit(i.image,i.pos)
            i.update_all(self.princess)
        for i in self.enemies:
            surface.blit(i.image,i.pos)
            i.update_all((self.princess))
            if i.dirty == True:
                i.barf()
        for i in self.objects:
            if i.alive == True:
                surface.blit(i.image,i.pos)
        for i in self.menus:
            surface.blit(i.image,i.pos)

        for part in self.princess.parts:
            if self.princess.got_hitten > 5:
                if self.princess.got_hitten%2 == 0:
                    surface.blit(part.image,part.pos)
            else:
                surface.blit(part.image,part.pos)
        for effect in self.princess.effects:
            surface.blit(effect[0],effect[1])
        self.princess.control(dir,act)

        for i in self.scenarios_front:
            surface.blit(i.image,i.pos)
            i.update_all()
        for i in self.gates:
            if self.princesses[0].rect.colliderect(i.rect)== True:
                surface.blit(i.arrow_image,i.arrow_pos)
        for i in self.floor_image:
            surface.blit(i.image,i.pos)
            i.update_pos()
#        for i in self.sky:
#            surface.blit(i.night_front_image,(0,0))
        for i in self.clock:
            surface.blit(i.image,i.pos)
        for i in self.panel:
            surface.blit(i.label,i.pos)
            i.update(self.princesses[0].glamour_points)
        for i in self.pointer:
            surface.blit(i.image,i.pos)

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
            if count >= 800:                self.floor_heights[n+count] = 236 + a
            if count >= 850:                self.floor_heights[n+count] = 226 + a
            if count >= 890:                self.floor_heights[n+count] = 216 + a
            if count >= 920:                self.floor_heights[n+count] = 206 + a
            if count >= 950:                self.floor_heights[n+count] = 196 + a
            if count >= 979:
                self.floor_heights[n+count] = 186
            count += 1
    def dress_st(self):
        pygame.mixer.music.load("data/NeMedohounkou.ogg")
        def create_floor(number):
            count = 0
            while count <= number:
                tile = floors.Floor(count,self.directory+'floor/',self)
                count +=1
        dress_tower =  scenarios.Building((0,100),self.directory+'Dress_Tower/',self,{'pos':(155,350),'directory':self.directory+'Dress_Tower/door/'},index =0)
        fachwerk1   = scenarios.Scenario((1000,100),self.directory+'fachwerk_1/',self,index=0)
        fachwerk2   = scenarios.Scenario((2000,100),self.directory+'fachwerk_2/',self,index=0)
        fachwerk3   = scenarios.Scenario((3000,100),self.directory+'fachwerk_3/',self,index=0)
        fence       = scenarios.Scenario((4000,100),self.directory+'fence/',self,index=0)
        knightstatue= scenarios.Scenario((5000,100),self.directory+'knight_statue/',self,index=0)
        gate1 = scenarios.Gate((400,0),'data/images/scenario/omni/gate/',self,index = 0)
        gate2 = scenarios.Gate((5510,0),'data/images/scenario/omni/gate/',self,index = 0)
        bilboard = moving_scenario.MovingScenario(1,self,'data/images/scenario/bathhouse_st/billboard_city/billboard/')

        carriage = enemy.Carriage(3,self.enemy_dir+'carriage/',3000,self,[10,10,10,10],[10,10,10,10],[10,10,10,10])
        oldlady = enemy.OldLady(2,self.enemy_dir+'old_lady/',4000,self)
        schnauzer = enemy.Schnauzer(10,self.enemy_dir+'schnauzer/',2600,self,[22,22,22,22],[22,22,22,22],[22,22,22,22],dirty=True)
        butterflies = enemy.Butterfly(4,self.enemy_dir+'butterflies/',6000,self)
        fundo = skies.Sky('data/images/scenario/skies/daytime/daytime.png',self,globals.clock_pointer)

        create_floor(30)


        Main_Star= glamour_stars.Glamour_Stars((0,0),self,True)

        try:       pygame.mixer.music.play()
        except:    print "Warning: no music loaded."
        self.princess = princess.Princess(self)

        info_glamour_points = panel.Data('', self.princess.glamour_points, (300, 0), self,0,size=120)
        castle = scenarios.Background((110,0),self,0,'data/images/scenario/ballroom/ballroom_day/')
