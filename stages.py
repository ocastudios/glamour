import game_globals
import pygame
import princess
import obj_images
import enemy
import scenarios
import skies
import glamour_stars
import panel
import floor
import clouds
import random
import mousepointer


class Stage():
    """This class is meant to create the levels of the game. One of its most importante features is to blit everything on the screen and define what should be in each of the stages.
It is still in its early development"""
    def __init__(self,level,size,universe):
        self.music = None
        self.background = []
        self.cameras = []
        self.clock = []
        self.clouds = []
        self.enemies = []
        self.floor_heights = {}
        self.floor_image = []
        self.floor = universe.floor-186
        self.gates = []
        self.level = level
        self.menus = []
        self.moving_scenario = []
        self.night = []
        self.objects = []
        self.panel = []
        self.pointer = []
        self.princesses = []
        self.scenarios = []
        self.set_floor()
        self.size = size
        self.sky = []
        self.gamepointer = None
        #self.floor_list = {0:186,620:186}
    def what_is_my_height(self,object):
        try:        y_height = self.floor_heights[object.distance_from_center+(object.size[0]/2)]
        except:     y_height = 186 
        return      y_height
    def blit_all(self,surface,act,dir,universe,clock_pointer):
        for i in self.cameras:
            i.update_pos(universe,self.princesses[0])
        universe.movement(dir)
        for i in self.sky:
            surface.blit(i.background,(0,0))
#            i.set_light(clock_pointer)
        for i in self.clouds:
            surface.blit(i.image,i.pos)
            i.update_all(dir,act)
        for i in self.background:
            surface.blit(i.image,i.pos)
            i.update_image()
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
            i.update_all(self.princesses[0])
            if self.princesses[0].rect.colliderect(i.rect)== True:
                surface.blit(i.arrow_image,i.arrow_pos)
        for i in self.enemies:
            surface.blit(i.image,i.pos)
            i.update_all((self.princesses[0]))
            if i.dirty == True:
                i.barf()
        for i in self.objects:
            if i.alive == True:
                surface.blit(i.image,i.pos)
        for i in self.menus:
            surface.blit(i.image,i.pos)
        for i in self.princesses:
            for part in i.parts:
                if i.got_hitten > 5:
                    if i.got_hitten%2 == 0:
                        surface.blit(part.image,part.pos)
                else:
                    surface.blit(part.image,part.pos)
            for effect in i.effects:
                surface.blit(effect[0],effect[1])
            i.control(dir,act)
        for i in self.floor_image:
            surface.blit(i.image,i.pos)
            i.update_pos()
#        for i in self.sky:
#            surface.blit(i.night_front_image,(0,0))
        for i in self.clock:
            surface.blit(i.image,i.pos)
        for i in self.panel:
            surface.blit(i[0],i[1])
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
            if count >= 730+10:
                self.floor_heights[n+count] = 246 + a
            if count >= 790+10:                self.floor_heights[n+count] = 236 + a
            if count >= 840+10:                self.floor_heights[n+count] = 226 + a
            if count >= 880+10:                self.floor_heights[n+count] = 216 + a
            if count >= 910+10:                self.floor_heights[n+count] = 206 + a
            if count >= 940+10:                self.floor_heights[n+count] = 196 + a
            if count >= 969+10:
                self.floor_heights[n+count] = 186
            count += 1
    def create_instances(self,universe,number_of_clouds=120,number_of_posts=120,number_of_floor=120):
        self.music = 'data/NeMedohounkou.ogg'
        provisory_count = 0
        while provisory_count <= number_of_clouds:
            game_cloud = clouds.Cloud((random.randint(100,25000),random.randint(0,300)),self)
            provisory_count += 1
        provisory_count = 0
        while provisory_count <= number_of_posts:
            game_posts = scenarios.Scenario((provisory_count,0),'data/images/scenario/bathhouse_st/light_post/post/',self)
            provisory_count +=1
        provisory_count
        while provisory_count <= number_of_floor:
            game_floor = floor.Floor(provisory_count,'data/images/scenario/bathhouse_st/floor/tile',self)
            provisory_count += 1
        del provisory_count

        #Instancing Stuff
        bilboard = scenarios.MovingScenario(1,self,'data/images/scenario/bathhouse_st/billboard_city/billboard/')
        gate1 = scenarios.Gate((300,0),'data/images/scenario/omni/gate/',self,index = 0)
        bathhouse = scenarios.Scenario((550,0),'data/images/scenario/bathhouse_st/bathhouse/bathhouse/',self,index =0)
        smallhouse = scenarios.Scenario((3400,100),'data/images/scenario/bathhouse_st/small_house/base/',self,index =0)
        home = scenarios.Scenario((3800,100),'data/images/scenario/bathhouse_st/home/castelo/',self,index =0)
        #bathhouse_door = scenarios.Scenario((920,90),'data/images/scenario/bathhouse_st/bathhouse/door_close/',self)
        carriage = enemy.Carriage(3,'data/images/enemies/carriage/',3000,self,[10,10,10,10],[10,10,10,10],[10,10,10,10])
        oldlady = enemy.OldLady(2,'data/images/enemies/old_lady/',4000,self)
        schnauzer = enemy.Schnauzer(10,'data/images/enemies/schnauzer/',2600,self,[22,22,22,22],[22,22,22,22],[22,22,22,22],dirty=True)
        butterflies = enemy.Butterfly(4,'data/images/enemies/butterflies/',6000,self)
        fundo = skies.Sky('data/images/scenario/skies/daytime/daytime.png',self,game_globals.clock_pointer)
        Main_Star= glamour_stars.Glamour_Stars((0,0),self,True)

        try:       pygame.mixer.music.play()
        except:    print "Warning: no music loaded."

        player = princess.Princess(self)
        info_glamour_points = panel.Data('', player.glamour_points, (300, 0), self,0,size=120)
        castle = scenarios.Background((110,0),self,0,'data/images/scenario/ballroom/ballroom_day/')

#        japanese_bridge = floor.Bridge('data/images/scenario/bathhouse_st/floor/japanese_bridge/',4,self)

        mouse_pos = pygame.mouse.get_pos()
        self.gamepointer = mousepointer.MousePointer(mouse_pos,self)


