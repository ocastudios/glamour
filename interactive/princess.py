import utils.obj_images as obj_images
import os
import random
import interactive.enemy as enemy
import pygame
import sqlite3
from pygame.locals import *
from settings import *

class Princess():
    """Creates the princess.

    Princess is a rather complex class in comparison with the enemies, for princess has many atributes called 'Princess Parts'. That's because princess instance is not build with a single group of images, but a bunch of groups of images that may or not be blitted to the screen.
Princess Parts are her dress, her hair, her eyes, arms and everything that may move or change.
This class uses obj_images module for retrieving images from directories.
It is one of the first classes written, which means that it is somewhat old and may contain som old and useless code that was not well cleaned. This will be corrected soon, I hope.
Problems to be fixed in this class are:
Princess shoes are moving weirdly when she jumps.
"""
    directory = data_dir+'/images/princess/'
    def __init__(self,level,INSIDE = False,xpos=None):
        print "Creating Princess"
        self.first_frame = True
        self.level = level
        self.effects    = []
        self.size       = (2,180*scale)
        #Acess db save file
        print "    connecting to princess database"
        self.save_db     = level.universe.db
        self.save_cursor = level.universe.db_cursor
        print "    retrieving data"
        row     = self.save_cursor.execute("SELECT * FROM save").fetchone()
        self.name = row['name']
        self.center_distance = int(int(row['center_distance'])*scale)
        if xpos:
            self.center_distance = int(xpos*scale)
        self.dirt            = int(row['dirt'])
        self.points          = int(row['points'])
        self.pos = [int(self.level.universe.center_x) + self.center_distance,
                           self.level.universe.floor -  self.level.what_is_my_height(self) -self.size[1]]
        print "    creating images:"
        print "        princess images"
        for act in ['walk','stay','kiss','fall','jump','ouch','celebrate']:
            exec('self.'+act+'_img = obj_images.MultiPart(self.ordered_directory_list("'+act+'"))')
        self.run_away_img = obj_images.Ad_hoc(self.walk_img.left[::2],self.walk_img.right[::2])
        print "        dirt images"
        self.dirties = [Dirt(level,data_dir+'/images/princess/'+d,self.pos) for d in ('dirt1','dirt2','dirt3')]
        self.images = None
        self.open_door_img  = self.stay_img
        print "        kisses and dust images"
        self.lips           = obj_images.TwoSided(data_dir+'/images/effects/kiss/')
        self.dirt_cloud     = obj_images.TwoSided(data_dir+'/images/effects/dirt/')
        self.gforce         = 0
        self.g_acceleration = round(3*scale)
        self.speed          = round(14*scale)
        self.rect           = Rect(self.pos,self.size)
        self.move           = False
        self.direction      = 'left'
        self.situation      = {"hurt":0,"excited":0,"scared":0}
        self.jump           = 0
        self.kiss           = 0
        self.kiss_direction = 'left'
        self.kiss_rect      = ((0,0),(0,0))
        self.floor          = self.level.universe.floor - self.level.what_is_my_height(self)
        self.last_height    = round(186*scale)
        self.action         = [None,'stay']
        self.image          = self.stay_img.left[self.stay_img.itnumber.next()]
        self.image_size     = self.image.get_size()
        self.inside         = INSIDE
        print "    creating sounds"
        print "        steps sounds"
        self.steps = [pygame.mixer.Sound(data_dir+'/sounds/princess/steps/spike_heel/street/'+str(i)+'.ogg') for i in range(0,5)]
        print "        jump sounds"
        self.jumpsound      = pygame.mixer.Sound(data_dir+'/sounds/princess/pulo.ogg')
        self.channel1       = pygame.mixer.Channel(0)
        self.channel2       = pygame.mixer.Channel(1)
        self.channel3       = pygame.mixer.Channel(2)
        self.past_choice    = None
        self.debuginside    =   0
        print "princess created"
        print "done."

    def ordered_directory_list(self, action):
        odl = []
        cursor = self.level.universe.db_cursor
        row = cursor.execute("SELECT * FROM princess_garment WHERE id=(SELECT MAX(id) FROM princess_garment)").fetchone()
        for part in ["hair_back","skin","face","hair","shoes","dress","arm","armdress","accessory"]:
            if row[part] != 'None':
                name = part.replace('_','')
                odl.extend([str(self.directory+row[part]+"/"+action+"/")])
        return odl

    def update_all(self):
        if self.first_frame:
            if self.dirt > 0:
                self.level.princesses[1] = self.dirties[self.dirt -1]
        if not self.inside:
            self.direction  = self.level.universe.dir
            self.action     = self.level.universe.action
            self.effects = []
            self.soundeffects(self.action)
            self.jumping(self.action)
            self.update_pos(self.action)
            self.hurting(self.action)
            self.kissing()
            self.update_image(self.action,self.direction)
            if self.situation['hurt'] > 5:
                if self.situation['hurt']%2 == 0:
                    self.image = None
            self.debuginside = 0
        else:
            self.pos[0] = self.level.universe.center_x+self.center_distance
            if not self.debuginside:
                print 'Now changed to inside'
                self.debuginside += 1
            self.update_image(self.action,'right')

    def dirt_cloud_funciton(self):
        if 0 < self.situation['hurt'] < 24:
            if self.situation['hurt'] > len(self.dirt_cloud.left):
                dirt_cloud_image = (self.dirt_cloud.left[self.situation['hurt']-1-len(self.dirt_cloud.left)])
            else:
                dirt_cloud_image = (self.dirt_cloud.left[self.situation['hurt']-1])
            self.effects.append(Effect(dirt_cloud_image,(self.pos)))

    def jumping(self,action):
        feet_position = self.pos[1]+self.size[1]
        if action[0]!= 'jump' and action[0]!= 'jump2' :
            self.jump = 0
        if feet_position == self.floor and not self.jump :
            if action[0]== 'jump':
                self.jump = 1
                self.channel3.play(self.jumpsound)
                self.images.number = 0
        if self.jump > 0 and self.jump <20:
            self.pos[1] -= round(30*scale)
            if self.jump > 5:
                if self.images.lenght-1 > self.images.number:
                    self.images.number += 1
            if self.jump > 10:
                self.images.number = 0
                action[0]= 'fall'
            self.jump +=1
        if action[0]=='fall' and feet_position == self.floor:
            action[0]=None
        if feet_position < self.floor and not self.jump:
            action[0]='fall'

    def hurting(self,action):
        if not self.inside:
            if not self.situation['hurt']:
                for e in self.level.enemies:
                    if (e.__class__ in (enemy.Schnauzer , enemy.FootBall, enemy.Hawk, enemy.BroomingDust) and self.rect.colliderect(e.rect)):
                        print "Princess got hurt by an enemy of the "+ str(e.__class__)+"class"
                        self.get_dirty()
                    if e.__class__ == enemy.Carriage:
                        if self.rect.colliderect(e.rect):
                            print "Princess got stuck at the Carriage"
                            self.speed = 0
                            self.action[1]= "stay"
                        else:
                            self.speed = round(14*scale)
                    if e.__class__ == enemy.Butterfly:
                        if self.rect.colliderect(e.rect) and self.situation['excited'] == 0:
                            print "Princess got excited by the Butterflies"
                            self.situation['excited']+=1
                if self.level.viking_ship:
                    if self.rect.colliderect(self.level.viking_ship.talk_balloon_rect):
                        self.get_dirty()
                if self.level.name == "accessory":
                    if self.pos[1]+self.size[1]-round(20*scale) > self.level.water_level:
                        print "Princess feet are at "+str(self.pos[1]+self.size[1])
                        print "Water level is "+str(self.level.water_level)
                        self.get_dirty()
            else:
                self.situation['hurt'] +=1
                if self.situation['hurt'] == 40:
                    self.situation['hurt'] = 0
            if self.situation['excited']:
                self.situation['excited'] +=1
                action[0] = 'celebrate'
                if self.situation['excited'] == 60:
                    self.situation['excited'] = 0
            if self.situation['scared']:
                self.situation['scared'] +=1
                action[1] = 'run_away'
                if self.situation['scared'] == 60:
                    self.situation['scared'] = 0
            if self.situation['hurt'] and self.situation['hurt'] <6:
                action[0]='ouch'
                self.situation['excited'] =0
                self.situation['scared'] = 0
            if self.situation['hurt'] >=6 and action[0] == 'ouch':
                action[0]= None

    def get_dirty(self):
        if self.dirt <= 2:
            self.situation['hurt'] += 1
            self.dirt += 1
            self.save_cursor.execute("UPDATE save SET dirt = "+str(self.dirt)+" WHERE name = '"+self.name+"'")
            print "Oh Dear, you've got all dirty! I need to take a record on that..."
            self.level.princesses[1] = self.dirties[self.dirt -1]

    def kissing(self):
        if self.action[0] == 'kiss' or self.kiss > 0:
            self.kiss +=1
            if self.kiss == 1:
                self.kiss_img.number = 0
        if self.kiss > 0:
            if self.kiss< 4:
                self.action[0] = 'kiss'
            else:
                self.action[0] = None
            if self.kiss <9:
                self.throwkiss()
            else:
                self.kiss = 0
                self.kiss_rect = Rect ((0,0),(0,0))

    def update_pos(self,action):
#        last_height = self.level.what_is_my_height(self)
        feet_position   = self.pos[1]+self.size[1]
        towards = {'right':1,'left':-1}

        #set x pos
        if action[1]=='walk' and action[0] != 'celebrate':
            self.center_distance += (self.speed*towards[self.direction])
            obstacle = self.level.universe.floor - self.level.what_is_my_height(self)
            if obstacle <= int(feet_position -round(30*scale)):
                self.center_distance -= (self.speed*towards[self.direction])
        if action[1] == 'run_away':
            if self.center_distance < self.situation['danger']:
                self.direction = 'left'
            else:
                self.direction = 'right'
            self.center_distance += ((round(6*scale)+self.speed)*towards[self.direction])
        self.pos[0] = self.level.universe.center_x+self.center_distance

        #set y pos
        new_height = self.level.what_is_my_height(self)
        self.floor = self.level.universe.floor - new_height
        #fall
        if feet_position < self.floor:
            new_y = self.pos[1]+self.gforce
            if new_y+self.size[1] >= self.floor:
                new_y = self.floor-self.size[1]
            self.pos[1] = new_y
            self.gforce += self.g_acceleration
            
        feet_position   = self.pos[1]+self.size[1]
        #do not stay lower than floor
        if feet_position > self.floor:
            self.pos[1]= self.floor-self.size[1]
        if feet_position == self.floor:
            self.gforce = 0
                
    def soundeffects(self,action):
        if not self.jump and (self.pos[1]+self.size[1]) == self.floor:
            if action[1]=='walk' or action[0] == 'pos[0]celebrate':
                if self.images.number % 6 == 0:
                    self.channel1.play(self.steps[random.randint(0,1)])
                if (self.images.number + 3)% 6 == 0:
                    self.channel2.play(self.steps[random.randint(2,3)])

    def throwkiss(self):
        if self.kiss == 1:
            self.kiss_direction = self.direction
        if self.kiss_direction == 'right':
            kissimage = self.lips.left[self.kiss-1]
            self.effects.append(Effect(kissimage,(self.pos[0],self.pos[1])))
            self.kiss_rect = Rect((self.pos[0],self.pos[1]),((self.kiss)*44,self.size[1]))
        else:
            kissimage = self.lips.right[self.kiss-1]
            self.effects.append(Effect(kissimage,(self.pos[0]-round(200*scale),self.pos[1])))
            self.kiss_rect = Rect((self.pos[0]+round(200*scale)-((self.kiss)*round(44*scale)),self.pos[1]),((self.kiss)*round(44*scale),self.size[1]))

    def update_image(self,action,direction):
        self.rect   = Rect(     (self.pos[0]+(self.image_size[0]/2),self.pos[1]-1),
                                self.size)
        chosen = action[0] or action[1]
        if direction.__class__ != str:
            direction = "right"
        exec('self.images = self.'+chosen+'_img \n'+'actual_images = self.'+chosen+'_img.'+direction)
        self.image = actual_images[self.images.number]
        if chosen != self.past_choice:
            exec('self.'+chosen+'_img.number = 0')
        self.past_choice = chosen
        if not self.jump:
            self.images.update_number()

    def change_clothes(self,part,dir):
        self.parts.pop(part.index)
        part = PrincessPart(self,data_dir+'/images/princess/'+str(dir),part.index)


class Dirt():
    image_number = 0
    def __init__(self, level, directory,pos):
        self.level = level
        self.directory = directory
        for act in ['walk','stay','kiss','fall','jump','ouch','celebrate']:
            exec('self.'+act+' = obj_images.TwoSided(str(directory)+"/'+act+'/")')
        self.run_away = obj_images.Ad_hoc(self.walk.left[::2],self.walk.right[::2])
        self.open_door = self.stay
        self.list = self.stay
        self.actual_list = self.list.left
        self.pos = pos
        self.image = self.actual_list[self.image_number]
        self.past_choice = None

    def update_all(self):
        self.pos = self.level.princesses[0].pos
        direction = self.level.princesses[0].direction
        chosen = self.level.princesses[0].action[0] or self.level.princesses[0].action[1]
        if direction.__class__ != str:
            direction = "right"
        exec('self.images = self.'+chosen+' \n'+
             'actual_images = self.'+chosen+'.'+direction)
        if chosen != self.past_choice:
            exec('self.'+chosen+'.number = 0')
        self.past_choice = chosen
        self.image = actual_images[self.images.number]
        if not self.level.princesses[0].jump:
            self.images.update_number()

class Effect():
    def __init__(self,image,position):
        self.image      = image
        self.position   = self.pos = position
