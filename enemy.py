
import globals
import pygame
import obj_images
from pygame.locals import *
import random

class Enemy():
    """This class defines an enemy with no movement and no update to position or image. It is used to be extended by other classes of enemies that should define the functions for movements"""
    def __init__(self,speed,directory, pos, level,walk_margin=[10,10,10,10],stay_margin=[10,10,10,10],kissed_margin=[10,10,10,10],dirty=False):
        self.center_distance = pos
        try:        self.walk = obj_images.TwoSided(directory+'/walk/',walk_margin)
        except:     pass 
        try:        self.stay = obj_images.TwoSided(directory+'/stay/',stay_margin)
        except:     pass
        try:        self.kissed = obj_images.TwoSided(directory+'/kissed/',kissed_margin)
        except:     pass
        try:        self.image = self.walk.left[0]
        except:     self.image = self.stay.left[0]

        self.size = (self.image.get_width()/2, self.image.get_height())
        self.alive = True
        self.level = level
        self.speed = speed
        self.floor = globals.universe.floor-self.level.what_is_my_height(self)
        self.margin = walk_margin
        self.pos = (globals.universe.center_x+self.center_distance,self.floor+self.margin[2]-(self.size[1]))
        self.decide = False
        self.count = 0
        self.move = True
        self.direction = 'left'
        self.lookside = 0
        self.rect = Rect(((self.pos[0]+(self.size[0]/2)),(level.floor-self.pos[1])),(self.size))
        self.gotkissed = 0
        self.image_number = 0
        self.dirty = dirty
        self.level.enemies.append(self)
class Schnauzer(Enemy):
    barfing = 0
    bow = pygame.mixer.Sound('data/sounds/enemies/dog2.ogg')
    def barf(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.barfing == 1:
            self.bow.play()
        if self.rect.collidepoint(mouse_pos)and self.barfing == 0 or self.barfing:
            self.barfing += 1
        if self.barfing > 100:
            self.barfing = 0

    def update_all(self,princess):
        self.look_around(princess)
        self.set_pos()
        self.set_image()
        self.got_kissed(princess)
    def look_around(self,princess):
        self.count +=1
        if self.count > 130:
            self.move = False
        if not self.move and not self.gotkissed:
            if princess.pos[0] > self.pos[0]:
                self.direction='right'
            else:
                self.direction = 'left'
            if self.count % 2 == 1:
                self.lookside += 1
            if self.lookside == 6:
                self.move = True
                self.lookside = 0
                self.count = 0

    def got_kissed(self,princess):
        if self.rect.colliderect(princess.kiss_rect):
            self.gotkissed += 1
            self.move = False
        if self.gotkissed != 0:
            self.gotkissed +1
        if self.gotkissed >= 250:
            self.gotkissed = 0
            self.move = True
    def set_pos(self):
        self.floor = globals.universe.floor - self.level.what_is_my_height(self)
        self.pos = (globals.universe.center_x + self.center_distance,
                    self.floor+self.margin[2]-(self.size[1]))

        if self.move:
            if self.direction == 'right' :
                self.center_distance += self.speed
            else:
                self.center_distance -= self.speed
        self.rect = Rect(((self.pos[0]+(self.size[0]/2)),self.pos[1]),(self.size))
    def set_image(self):
        #choose list
        if self.move:
            exec('actual_list = self.walk.'+self.direction)
        else:
            if self.lookside % 2 ==0:
                actual_list = self.walk.right[0:1]
            else:
                actual_list = self.walk.left[0:1]
        if self.gotkissed >= 1:
            self.move =False
            exec('actual_list = self.kissed.'+self.direction)
        number_of_files = len(actual_list)-2

        if self.image_number <= number_of_files:
            self.image_number +=1
        else:
            self.image_number = 0
        
        self.image = actual_list[self.image_number]
class Carriage(Enemy):
    def update_all(self,princess):
        self.set_pos()
        self.set_image()
    def set_pos(self):
        self.floor = globals.universe.floor-self.level.what_is_my_height(self)
        self.pos = (globals.universe.center_x + self.center_distance, self.floor+self.margin[2]-(self.size[1]))
        self.direction = 'right'
        if self.move:
            if self.direction == 'right' :
                self.center_distance += self.speed
            else:
                self.center_distance -= self.speed
        self.rect = Rect(((self.pos[0]+(self.size[0]/2)),(self.level.floor-self.size[1])),(self.size))
    def set_image(self):
#choose list
        if self.move:   exec('actual_list = self.walk.'+self.direction)
        else:           exec('actual_list = self.stay.'+self.direction)

        number_of_files = len(actual_list)-2
        if self.image_number <= number_of_files:
            self.image_number +=1
        else:
            self.image_number = 0
        self.image = actual_list[self.image_number]
class Butterfly(Enemy):
    height = 100
    up_direction = 'going_down'
    def update_all(self,princess):
        self.set_pos()
        self.set_image()
    def set_pos(self):
        
        if self.pos[1] < 300:
            self.up_direction = 'going_down'
        elif self.pos[1] > 500:
            self.up_direction = 'going_up'
        if self.up_direction == 'going_down':
            self.height += 5
        if self.up_direction == 'going_up':
            self.height -= 5 
        self.pos = (globals.universe.center_x + self.center_distance, self.height)
        if self.move == True:
            if self.direction == 'right' :
                self.center_distance += self.speed
            else:
                self.center_distance -= self.speed
        self.rect = Rect(((self.pos[0]+(self.size[0]/2)),self.height),(self.size))
    def set_image(self):
#choose list
        self.count+=1
        if self.move:
            exec('actual_list = self.walk.'+self.direction)
        else:
            exec('actual_list = self.stay.'+self.direction)

        number_of_files = len(actual_list)-2
        if self.image_number <= number_of_files:
            self.image_number +=1
        else:
            self.image_number = 0
        self.image = actual_list[self.image_number]
class OldLady(Enemy):
    def __init__(self,speed,directory, pos, level,walk_margin=[10,10,10,10],stay_margin=[10,10,10,10],kissed_margin=[10,10,10,10],dirty=False):
        self.center_distance = pos
        self.walk   = obj_images.TwoSided(directory+'/walk/',walk_margin)
        self.hover  = obj_images.There_and_back_again(directory+'/hover/',stay_margin)
        self.broom  = obj_images.There_and_back_again(directory+'/act/',stay_margin)
        self.image  = self.walk.left[0]
        self.mouseovercount = 0
        self.size   = (self.image.get_width()/2, self.image.get_height())
        self.alive  = True
        self.level  = level
        self.speed  = speed
        self.floor  = globals.universe.floor-self.level.what_is_my_height(self)
        self.margin = walk_margin
        self.pos = (globals.universe.center_x+self.center_distance,self.floor+self.margin[2]-(self.size[1]))
        self.decide = False
        self.count = 0
        self.direction = 'left'
        self.action = 'walk'
        self.level.enemies.append(self)
        self.rect = Rect(((self.pos[0]+(self.size[0]/2)),(level.floor-self.pos[1])),(self.size))
        self.gotkissed = 0
        self.image_number = 0
        self.dirty = dirty

    def update_all(self,princess):
        self.wave_to_princess()
        self.brooming()
        self.set_pos()
        self.set_image()

    def wave_to_princess(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.action != 'wave':
            if self.rect.collidepoint(mouse_pos):
                self.action = 'wave'
                self.image_number = 0
                self.count = 0
        else:
            if self.count > 33:
                self.action = 'walk'
                self.count = 0

    def brooming(self):
        if self.action != 'broom':
            if self.count == 60:
                self.action = 'broom'
                self.image_number = 0
        else:
            if self.count == 105:
                if random.randint(0,1)>0:
                    self.direction = 'left'
                else:
                    self.direction = 'right'
                self.action = 'walk'
                self.count = 0
        self.count += 1
            

    def set_pos(self):
        self.floor = globals.universe.floor-self.level.what_is_my_height(self)
        self.pos = (globals.universe.center_x + self.center_distance, self.floor+self.margin[2]-(self.size[1]))
        if self.action == 'walk':
            if self.direction == 'right' :
                self.center_distance += self.speed
            else:
                self.center_distance -= self.speed
        self.rect = Rect(((self.pos[0]+(self.size[0]/2)),(self.level.floor-self.size[1])),(self.size))

    def set_image(self):

        exec('actual_list = self.'+self.action+'.'+self.direction)

        number_of_files = len(actual_list)-2
        if self.image_number <= number_of_files:
            self.image_number +=1
        else:
            self.image_number = 0
        self.image = actual_list[self.image_number]
