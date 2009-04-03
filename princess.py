import globals
import obj_images
import os
import random
import enemy

from pygame.locals import *

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
    directory = 'data/images/princess/'
    def __init__(self,level,save = None):
        self.file = open(save or 'data/saves/default').readlines()
        self.parts = []
        self.part_keys=["hair_back","skin","face","hair","shoes","dress","arm","arm_dress","accessory","dirty","dirty2","dirty3"]
        self.size       = (80,180)
        self.center_distance = 4200
        self.pos        = (globals.universe.center_x+self.center_distance,
                           globals.universe.floor - 186 -self.size[1])
        for part in self.part_keys:
            for line in self.file:
                if part in line:
                    l = line.split()
                    if part == l[0]:
                        if l[1] != 'None':
                            exec('self.'+l[0]+'= PrincessPart(self, self.directory+"'+l[1]+'",'+l[2]+")") 
                        else:
                            exec('self.'+l[0]+'= None')
                            exec('self.parts.insert('+l[2]+',self.'+l[0]+')')
        self.parts.remove(self.dirty)
        self.parts.remove(self.dirty2)
        self.parts.remove(self.dirty3)
        self.lips       = obj_images.TwoSided('data/images/effects/kiss/')
        self.dirt_cloud= obj_images.TwoSided('data/images/effects/dirt/')
        self.glamour_points = 0
        self.gforce     = 0
        self.speed      = 10
        self.effects    = []
        self.rect       = Rect(self.pos,self.size)
        self.move       = False
        self.direction  = 'left'
        self.got_hitten = 0
        self.alive      = True
        self.level      = level
        level.princesses.append(self)
        self.jump       = 0
        self.celebrate  = 0
        self.kiss       = 0
        self.kiss_direction = 'left'

        self.kiss_rect = ((0,0),(0,0))
        self.floor = globals.universe.floor - 186
    def control(self, dir, action):
        self.effects = []
        self.direction = dir
        self.update_pos(action)
        self.update_rect()
        self.new_clothes(action)
        self.ive_been_caught()
        self.jumping(action)
        self.falling(action)
        self.celebrating(action)
        self.hurting(action)
        self.kissing(action,dir)
        self.dirt_cloud_funciton()
        self.choose_parts(action,dir)
        for part in self.parts:
            if part != None:
                part.update_image(self,dir,reset=True,invert=part.invert)
        self.syncimages(action)

    def dirt_cloud_funciton(self):
        if self.got_hitten > 0 and self.got_hitten < 24:
            if self.got_hitten > len(self.dirt_cloud.left):
                dirt_cloud_image = (self.dirt_cloud.left[self.got_hitten-1-len(self.dirt_cloud.left)])
            else:
                dirt_cloud_image = (self.dirt_cloud.left[self.got_hitten-1])
            self.effects.append((dirt_cloud_image,(self.pos)))
    def new_clothes(self,action):
        if action[0] == 'changeskin':
            self.change_clothes((self.arm),         'arm_black')
        if action[0] == 'changeshoes':
            self.change_clothes((self.shoes),       'shoes_crystal')
        if action[0] == 'changeshoes2':
            self.change_clothes((self.shoes),       'shoes_slipper')
        if action[0] == 'change':
            self.change_clothes((self.accessory),'accessory_shades')
        if action[0] == 'changedress':
            self.change_clothes((self.dress),     'dress_pink')
        if action[0] == 'changehair':
            self.change_clothes((self.hair),       'hair_cinderella')
            self.parts[0] = None
        if action[0] == 'changehair2':
            self.change_clothes((self.hair),       'hair_rapunzel')
            self.parts.pop(0)
            self.hair_back = PrincessPart(self,'data/images/princess/hair_rapunzel_back',0)
    def change_clothes(self,part,dir):
        self.parts.pop(part.index)
        part = PrincessPart(self,'data/images/princess/'+str(dir),part.index)

    def update_rect(self):
        #Correct rect position when turned left
        if self.direction == 'right':
            self.rect   = Rect(self.pos,self.size)
        else:
            self.rect = Rect((self.pos[0]+100,self.pos[1]),self.size)

    def jumping(self,action):
        if action[0]!= 'jump' and action[0]!= 'jump2':
            self.jump = 0
        if self.pos[1] + self.size[1] == self.floor and self.jump == 0:
            if action[0]== 'jump':
                self.jump = 1
                os.popen4('ogg123 ~/Bazaar/Glamour/glamour/data/sounds/princess/pulo.ogg')
                for part in self.parts:
                    if part != None:
                        part.reset_count = 0
        if self.jump > 0 and self.jump <20:
            self.pos = (self.pos[0],self.pos[1]-30)
            if self.jump > 5:
                for part in self.parts:
                    if part != None:
                        part.image_number = len(part.actual_list)-1
            if self.jump > 10:
                action[0]= 'fall'
            self.jump +=1
            
    def falling(self,action):
        if action[0]=='fall':
            if self.pos[1]+self.size[1]== self.floor:
                action[0]=None
                os.popen4('ogg123 ~/Bazaar/Glamour/glamour/data/sounds/princess/fall/spike_heel/street/'+str(random.randint(0,0))+'.ogg')
        if action[0]!='jump' and action[0]!='jump2' and self.pos[1]+self.size[1]<self.floor and self.jump==0:
            action[0]='fall'
    def celebrating(self,action):
        if self.celebrate > 0:
            action[0]=['celebrate']
            self.celebrate +=1
            if self.celebrate>12:
                self.celebrate = 0
    def hurting(self,action):
        if self.got_hitten > 0 and self.got_hitten <6:
            action[0]='ouch'
        elif self.got_hitten >=6:
            action[0]='stand'
    def kissing(self,action,dir):
        if action[0] == 'kiss' or self.kiss > 0:
            self.kiss +=1
            if self.kiss == 1:
                for part in self.parts:
                    if part != None:
                        part.reset_count = 0
        if self.kiss > 0:
            if self.kiss< 4:
                action[0] = 'kiss'
            else:
                action[0] = 'stand'
            if self.kiss <9:
                self.throwkiss(dir)
            else:
                self.kiss = 0
                self.kiss_rect = Rect ((0,0),(0,0))
    def ive_been_caught(self):
        if self.got_hitten == 0:
            for e in self.level.enemies:
                if e.__class__ == enemy.Schnauzer:
                    if self.dirty not in self.parts:
                        if self.rect.colliderect(e.rect):
                            self.got_hitten +=1
                            self.parts.insert(7,self.dirty)
                    elif self.dirty2 not in self.parts:
                        if self.rect.colliderect(e.rect):
                            self.got_hitten+=1
                            self.parts.insert(7,self.dirty2)
                    elif self.dirty3 not in self.parts:
                        if self.rect.colliderect(e.rect):
                            self.got_hitten += 1
                            self.parts.insert(7,self.dirty3)
                #Insert elif dirty2 not in self.parts and elif dirty3 not in self.parts to introduce differente levels of dirt.
        else:
            self.got_hitten +=1

            if self.got_hitten == 30:#75 at 25 frames per second
                self.got_hitten = 0
    def update_pos(self,action):
        #fall
        if self.pos[1]+self.size[1] < self.floor:
            self.pos = (self.pos[0], self.pos[1]+self.gforce)
            self.gforce += globals.universe.gravity
        #do not fall beyond the floor
        if self.pos[1]+self.size[1] > self.floor:
            self.pos= (self.pos[0],(self.floor-self.size[1]))
        if self.pos[1]+self.size[1] == self.floor:
            self.gforce = 0
        self.floor = globals.universe.floor-self.level.what_is_my_height(self)
        self.pos = (globals.universe.center_x+self.center_distance, self.pos[1])
        if action[1]=='walk':
           if self.direction == 'right':
               self.center_distance += self.speed
           else:
               self.center_distance -= self.speed
    def choose_parts(self,action,direction):
        for part in self.parts:
            if part != None:
                chosen = action[0] or action[1]
                exec('part.list = part.'+ chosen)
#                if action[0] == 'ouch':
#                    part.list = part.ouch
#                elif action[1] == 'walk':
#                    part.list = part.walk
#                elif action[1] == 'stand':
#                    part.list = part.stand
#                if action[0] =='jump':
#                    part.list = part.jump
#                if action[0] == 'kiss':
#                    part.list = part.kiss
#                elif action[0] == 'fall':
#                    part.list = part.fall
#                elif action[0] == 'celebrate':
#                    part.list = part.celebrate
                if direction == 'left':
                    part.actual_list = part.list.right
                else:
                    part.actual_list = part.list.left
    def syncimages(self,action):
        if action[1]=='walk':
            for part in self.parts:
                if part != None:
                    part.image_number = self.skin.image_number

            if self.skin.image_number == 3:
                os.popen4('ogg123 ~/Bazaar/Glamour/glamour/data/sounds/princess/steps/spike_heel/street/'+str(random.randint(0,1))+'.ogg')
            if self.skin.image_number == 6:
                os.popen4('ogg123 ~/Bazaar/Glamour/glamour/data/sounds/princess/steps/spike_heel/street/'+str(random.randint(2,3))+'.ogg')

        if action[0]=='celebrate':
            self.face.image_number=self.skin.image_number
    def throwkiss(self,direction):
        if self.kiss == 1:
            self.kiss_direction = direction
        if self.kiss_direction == 'right':
            kissimage = self.lips.left[self.kiss-1]
            self.effects.append((kissimage,(self.pos[0],self.pos[1])))
            self.kiss_rect = Rect((self.pos[0],self.pos[1]),((self.kiss)*44,self.size[1]))
        else:
            kissimage = self.lips.right[self.kiss-1]
            self.effects.append((kissimage,(self.pos[0]-200,self.pos[1])))

            self.kiss_rect = Rect((self.pos[0]-((self.kiss)*44),self.pos[1]),((self.kiss)*44,self.size[1]))
    def save(self):
        self.save_number = 0
        save_file = open('data/saves/'+str(self.save_number),'w')
        save_file.write('Position: '+str(self.pos)+'\n'
                        'Glamour_Points: '+str(self.glamour_points)+'\n'
                        'Self_parts: '
                        )
        for part in self.parts:
            try:            save_file.write(str(part.index or 0))
            except:         save_file.write(str(Exception))
class PrincessPart():
    def __init__(self, princess, directory,index,invert=0):
        self.index = index
        self.walk = obj_images.TwoSided(str(directory)+'/walk/')
        self.stand = obj_images.TwoSided(str(directory)+'/stay/')
        self.kiss = obj_images.TwoSided(str(directory)+'/kiss/')
        self.fall = obj_images.TwoSided(str(directory)+'/fall/')
        self.jump = obj_images.TwoSided(str(directory)+'/jump/')
        self.ouch = obj_images.TwoSided(str(directory)+'/ouch/')
        self.celebrate = obj_images.TwoSided(str(directory)+'/celebrate/')
        self.image_number = 0
        self.list = self.stand
        self.actual_list = self.list.left
        self.reset_count = 0
        self.once = 0
        self.pos = princess.pos
        princess.parts.insert(index,self)
        self.image = self.actual_list[self.image_number]
        self.invert = invert
    def update_image(self,princess,direction,reset = False,invert = 0):
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
