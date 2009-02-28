from globals import *
from obj_images import *
import random
from random import randint
from getscreen import os_screen
from stage import *

class Princess():
    """Creates the princess. Princess is a rather complex class in comparison with the enemies, for princess has many atributes called 'Princess Parts'. That's because princess instance is not build with a single group of images, but a bunch of groups of images that may or not be blitted to the screen.
Princess Parts are her dress, her hair, her eyes, arms and everything that may move or change.
This class uses obj_images module for retrieving images from directories.
It is one of the first classes written, whitch means that it is somewhat old and may contain som old and useless code that was not well cleaned. This will be corrected soon, I hope.
You need only a 'self' as a parameter for this class. The other atributes are default.
Problems to be fixed in this class are:
Princess controls are not good enough, probably because of the clock tick;
Princess movement determines the camera, and this may not continue for Princess needs to move in the camera more freely;
Princess shoes are moving weirdly while she jumps.
The code is not yet well commented
"""
    def __init__(self):
        self.parts = []
        self.size = (80,180)
        self.distance_from_center = (os_screen.current_w/2)-100
        self.pos = (universe.center_x+self.distance_from_center,universe.floor - 186 -self.size[1])

        self.skin = PrincessPart(self,'data/images/princess/skin_pink',0)
        self.face = PrincessPart(self,'data/images/princess/face_simple',1)
        self.hair = PrincessPart(self,'data/images/princess/hair_yellow',2)
        self.shoes = PrincessPart(self,'data/images/princess/shoes_slipper',3)
        self.dress = PrincessPart(self,'data/images/princess/dress_plain',4)
        self.arm = PrincessPart(self,'data/images/princess/arm_pink',5)
        self.accessory = PrincessPart(self,'data/images/princess/accessory_ribbon',6)
        self.lips = ObjectImages('data/images/effects/kiss/')
        self.dirty = PrincessPart(self,'data/images/princess/dirt1',7)
        self.glamour_points = 0
        self.life = 1000
        self.gforce = 0
        self.speed = 10
        self.effects = []
        self.rect = Rect(self.pos,self.size)
        self.move = False
        self.direction = 'left'
        self.half_the_movement = False
        self.got_hitten = 0
        self.alive = True
        Level_01.princesses.append(self)
        self.jump = 0
        self.celebrate = 0
        self.kiss = 0        
        self.parts.remove(self.dirty)
        self.floor = universe.floor - 186
    def control(self, dir, act):
        self.effects = []
        #update rect        
        if action[0] == 'change':
            self.change_clothes((self.accessory),'accessory_shades',6)
        if action[0] == 'changedress':
            self.change_clothes((self.dress),'dress_pink',4)
        if action[0] == 'changehair':
            self.change_clothes((self.hair),'hair_cinderella',2)


        if self.direction == 'right':
            self.rect   = Rect(self.pos,self.size)
        else:
            self.rect = Rect((self.pos[0]+100,self.pos[1]),self.size)
        #fall
        if self.pos[1]+self.size[1] < self.floor:
            self.pos = (self.pos[0], self.pos[1]+self.gforce)
            self.gforce += universe.gravity
        #do not fall beyond the floor
        if self.pos[1]+self.size[1] > self.floor:
            self.pos= (self.pos[0],(self.floor-self.size[1]))
        if self.pos[1]+self.size[1] == self.floor:
            self.gforce = 0
        self.direction = dir
        once = False
        if act[0]!= 'jump' and act[0]!= 'jump2':
            self.jump = 0
        if self.pos[1]+self.size[1] == self.floor and self.jump == 0:
            if act[0]== 'jump':
                self.jump = 1
        if self.jump > 0 and self.jump <20:
            self.pos = (self.pos[0],self.pos[1]-30)
            self.jump +=1
            if self.jump > 5:
                for part in self.parts:
                    part.image_number = len(part.actual_list)-2
            if self.jump > 10:
                act[0]= 'fall'
        if act[0]=='fall':
            if self.pos[1]+self.size[1]== self.floor:
                act[0]=None
        if act[0]!='jump' and act[0]!='jump2' and self.pos[1]+self.size[1]<self.floor:
            act[0]='fall'
        if self.celebrate > 0:
            act[0]=['celebrate']
            self.celebrate +=1
            if self.celebrate>12:
                self.celebrate = 0
        if self.got_hitten > 0 and self.got_hitten <6:
            act[0]='ouch'
        elif self.got_hitten >=6:
            act[0]='stand'
        if act[0] == 'kiss':
            self.kiss +=1
            if self.kiss == 1:
                for part in self.parts:
                    part.reset_count = 0
        if self.kiss > 0:
            act[0] = 'kiss'
            if self.kiss > 3:
                act[0] = 'stand'
            if act[0]!= 'kiss':
                self.kiss +=1
            if self.kiss <9:
                self.throwkiss(dir)
            else:
                self.kiss = 0

        #for images to restart reset must be true
        self.choose_parts(act,dir)

        for part in self.parts:
            part.update_image(self,dir,once=True,reset=True,invert=part.invert)
        self.syncimages(act)
            
            
    def change_clothes(princess,part,dir,index):
        princess.parts.remove(part)
        part = PrincessPart(princess,'data/images/princess/'+str(dir),index)
        
    def ive_been_caught(self):
        if self.got_hitten == 0:
            for e in enemies:
                if e.dirty == True:
                    if self.dirty not in self.parts:
                        if self.rect.colliderect(e.rect):
                            self.life -= 10
                            self.got_hitten +=1
                            self.parts.insert(7,self.dirty)
                #Insert elif dirty2 not in self.parts and elif dirty3 not in self.parts to introduce differente levels of dirt.
        else:
            self.got_hitten +=1
            if self.got_hitten == 75:#75 at 25 frames per second
                self.got_hitten = 0
    def update_pos(self,act,direction):
        self.floor = universe.floor-Level_01.what_is_my_height(self)
        self.pos = (universe.center_x+self.distance_from_center, self.pos[1])
        if act[1]=='move':
           if direction == 'right':
               self.distance_from_center += self.speed
           else:
               self.distance_from_center -= self.speed
    def choose_parts(self,act,direction):
        for part in self.parts:
            if act[0] == 'ouch':
                part.list = part.ouch
            elif act[1] == 'move':
                part.list = part.walk
            elif act[1] == 'stand':
                part.list = part.stand
            if act[0] =='jump':
                part.list = part.jump
            if act[0] == 'kiss':
                part.list = part.kiss
            elif act[0] == 'fall':
                part.list = part.fall
            elif act[0] == 'celebrate':
                part.list = part.celebrate
                
            if direction == 'left':
                part.actual_list = part.list.right
            else:
                part.actual_list = part.list.left
    def syncimages(self,act):
        if act[1]=='move':
            for part in self.parts:
                part.image_number = self.skin.image_number

        if act[0]=='celebrate':
            self.face.image_number=self.skin.image_number
    def throwkiss(self,direction):
        if direction == 'right':
            kissimage = self.lips.left[self.kiss-1]
            self.effects.append((kissimage,(self.pos[0],self.pos[1])))          
        else:
            kissimage = self.lips.right[self.kiss-1]
            self.effects.append((kissimage,(self.pos[0]-200,self.pos[1])))          
            
            
class PrincessPart():
    def __init__(self, princess, directory,index,invert=0):
        self.walk = ObjectImages(str(directory)+'/walk/')
        self.stand = ObjectImages(str(directory)+'/stay/')
        self.kiss = ObjectImages(str(directory)+'/kiss/')
        self.fall = ObjectImages(str(directory)+'/fall/')
        self.jump = ObjectImages(str(directory)+'/jump/')
        self.ouch = ObjectImages(str(directory)+'/ouch/')
        self.celebrate = ObjectImages(str(directory)+'/celebrate/')
        self.image_number = 0
        self.list = self.stand
        self.actual_list = self.list.left
        self.reset_count = 0
        self.once = 0
        self.pos = princess.pos
        princess.parts.insert(index,self)
        self.image = self.actual_list[self.image_number]
        self.invert = invert

    def update_image(self,princess,direction,once = False,reset = False,invert = 0):
        if reset == True:
            if self.reset_count == 0:
                self.image_number = 1
                self.reset_count = 1
        number_of_files = len(self.actual_list)

        if direction == 'left':
            self.pos = (princess.pos[0]-invert,princess.pos[1])
        else:
            self.pos = princess.pos
        if self.image_number >= number_of_files:
            self.image_number=0
        self.image_number+=1
        self.image = self.actual_list[self.image_number-2]
