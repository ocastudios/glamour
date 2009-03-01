from globals import *

class Stage():
    """This class is meant to create the levels of the game. One of its most importante features is to blit everything on the screen and define what should be in each of the stages.
It is still in its early development"""
    def __init__(self,level,size,universe):
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
            i.movement(dir,act)
            i.set_image()

        for i in self.background:
            surface.blit(i.image,i.pos)
            i.update_image()
        for i in self.moving_scenario:
            surface.blit(i.image,i.pos)
            i.set_pos(act,dir)

#        for i in self.sky:
#            surface.blit(i.night_back_image,(0,0))
            

        for i in self.scenarios:
            surface.blit(i.image,i.pos)
            i.update_pos()

        for i in self.gates:
            surface.blit(i.image,i.pos)
            i.update_pos()
            i.indicate_exit(self.princesses[0])
            if self.princesses[0].rect.colliderect(i.rect)== True:
                surface.blit(i.arrow_image,i.arrow_pos)

        for i in self.enemies:
            surface.blit(i.image,i.pos)
            i.movement((self.princesses[0]))
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

