
import pygame
import obj_images
from pygame.locals import *
import itertools
import random

class Enemy():
    """This class defines an enemy with no movement and no update to position or image. It is used to be extended by other classes of enemies that should define the functions for movements"""
    def __init__(self,speed,directory, pos, level,margin=[10,10,10,10],dirty=False):
        self.center_distance = pos
        for i in ['kissed','walk','stay']:
            exec("self."+i+"= obj_images.TwoSided(directory+'"+i+"/',margin)")
        self.image = self.walk.left[0]
        self.size = (self.image.get_width()/2, self.image.get_height())
        self.alive = True
        self.level = level
        self.speed = speed
        self.floor = self.level.universe.floor-self.level.what_is_my_height(self)
        self.margin = margin
        self.pos = [self.level.universe.center_x+self.center_distance,self.floor+self.margin[2]-(self.size[1])]
        self.decide = False
        self.count = 0
        self.move = True
        self.direction = 'left'
        self.rect = Rect(((self.pos[0]+(self.size[0]/2)),(level.floor-self.pos[1])),(self.size))
        self.gotkissed = 0
        self.image_number = 0
    def set_pos(self):
        self.floor = self.level.universe.floor - self.level.what_is_my_height(self)
        self.pos = [self.level.universe.center_x + self.center_distance,
                    self.floor+self.margin[2]-(self.size[1])]
        if self.move:
            if self.direction == 'right' :
                self.center_distance += self.speed
            else:
                self.center_distance -= self.speed
        self.rect = Rect(((self.pos[0]+(self.size[0]/2)),self.pos[1]),(self.size))

class Schnauzer(Enemy):
    barfing = 0
    bow = pygame.mixer.Sound('data/sounds/enemies/dog2.ogg')
    lookside = 0
    def barf(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.barfing == 1:
            self.bow.play()
        if self.rect.collidepoint(mouse_pos)and self.barfing == 0 or self.barfing:
            self.barfing += 1
        if self.barfing > 100:
            self.barfing = 0

    def update_all(self):
        self.look_around(self.level.princesses[0])
        self.set_pos()
        self.set_image()
        self.got_kissed(self.level.princesses[0])

#        self.level.rects.extend(pygame.mask.from_surface(self.image).get_bounding_rects())
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
    def update_all(self):
        self.move = True
        self.set_pos()
        self.set_image()

    def set_image(self):
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


class Butterfly(Enemy):
    height = 100
    up_direction = 'going_down'
    up = 5
    def update_all(self):
        self.set_pos()
        self.set_image()
    def set_pos(self):
        if self.pos[1] < 300:
            self.up = +5
        elif self.pos[1] > 500:
            self.up = -5
        self.height += self.up
        self.pos = (self.level.universe.center_x + self.center_distance, self.height)
        if self.move:
            if self.direction == 'right' :
                self.center_distance += self.speed
            else:
                self.center_distance -= self.speed
        self.rect = Rect(((self.pos[0]+(self.size[0]/2)),self.height),(self.size))
    def set_image(self):
#choose list
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
    def __init__(self,speed,directory, pos, level,margin=[10,10,10,10],dirty=False):
        self.center_distance = pos
        self.walk   = obj_images.TwoSided(directory+'/walk/',margin)
        self.wave   = obj_images.There_and_back_again(directory+'/hover/',margin)
        self.broom  = obj_images.There_and_back_again(directory+'/act/',margin)
        self.image  = self.walk.left[0]
        self.mouseovercount = 0
        self.size   = (self.image.get_width()/2, self.image.get_height())
        self.alive  = True
        self.level  = level
        self.speed  = speed
        self.floor  = self.level.universe.floor-self.level.what_is_my_height(self)
        self.margin = margin
        self.pos = [self.level.universe.center_x+self.center_distance,self.floor+self.margin[2]-(self.size[1])]
        self.decide = False
        self.count = 0
        self.direction = 'left'
        self.action = 'walk'
        self.rect = Rect(((self.pos[0]+(self.size[0]/2)),(level.floor-self.pos[1])),(self.size))
        self.image_number = 0

    def update_all(self):
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
        elif self.count > 33:
            self.action = 'walk'
            self.count = 0

    def brooming(self):
        if self.action != 'broom' and self.count == 60:
            self.action = 'broom'
            self.image_number = 0
        elif self.count == 105:
            self.direction = random.choice(['left','right'])
            self.action = 'walk'
            self.count = 0
        self.count +=1

    def set_pos(self):
        self.floor = self.level.universe.floor - self.level.what_is_my_height(self)
        self.pos = [self.level.universe.center_x + self.center_distance, self.floor+self.margin[2]-(self.size[1])]
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



class Lion():
    def __init__(self, pos, level):
        directory = level.enemy_dir+'lion/'
        self.center_distance = pos
        for i in ['base','growl','kissed']:
            exec("self."+i+"= obj_images.There_and_back_again(directory+'"+i+"/',exclude_border = True)")
        self.image = self.base.left[0]
        self.level = level
        self.pos = [self.level.universe.center_x+self.center_distance, 380]
        self.direction = 'left'
        self.gotkissed = 0
        self.image_number = 0
        self.tail = Tail(directory,self)

    def update_all(self):
        self.image = self.base.left[self.base.itnumber.next()]
        self.pos[0] = self.tail.pos[0]= self.level.universe.center_x + self.center_distance


class Tail():
    def __init__(self, directory, lion):
        self.lion = lion
        self.pos  = self.lion.pos
        self.images = obj_images.There_and_back_again(directory+'tail/')
        self.image = self.images.list[self.images.itnumber.next()]

    def update_all(self):
        self.pos  = self.lion.pos
        self.image = self.images.list[self.images.itnumber.next()]


class Elephant():
    def __init__(self, pos, level, dirty=False):
        directory = level.enemy_dir+'elephant/'
        self.center_distance = pos
        for i in ['base','hover']:
            exec("self."+i+"= obj_images.TwoSided(directory+'"+i+"/')")
        self.image = self.base.left[0]
        self.level = level
        self.pos = [self.level.universe.center_x+self.center_distance, (self.level.floor - self.image.get_height()) +15 ]
        self.direction = 'left'
        self.gotkissed = 0
        self.image_number = 0

    def update_all(self):
        self.image = self.base.left[self.base.itnumber.next()]
        self.pos[0] = self.level.universe.center_x + self.center_distance


class Monkey():
    def __init__(self, pos, level, dirty=False):
        directory = level.enemy_dir+'monkey/'
        self.center_distance = pos
        for i in ['stay','hover','happy','throw','attack']:
            exec("self."+i+"= obj_images.TwoSided(directory+'"+i+"/')")
        self.image = self.stay.left[0]
        self.level = level
        self.pos = [self.level.universe.center_x+self.center_distance, 150 ]
        self.direction = 'left'
        self.gotkissed = 0
        self.image_number = 0

    def update_all(self):
        self.image = self.stay.left[0]
        self.pos[0] = self.level.universe.center_x + self.center_distance

class VikingShip():
    def __init__(self, pos, level, dirty=False):
        directory = level.enemy_dir+'viking_ship/'
        self.center_distance = pos
        for i in ['base']:
            exec("self."+i+"= obj_images.TwoSided(directory+'"+i+"/')")
        self.image = self.base.left[0]
        self.level = level
        self.height = itertools.cycle(range(20)+ range(20)[-1:0:-1])
        self.image_height = self.image.get_height()
        self.pos = [self.level.universe.center_x+self.center_distance, self.level.floor - self.image_height + 200 +self.height.next()]
        self.direction = 'left'
        self.gotkissed = 0
        self.image_number = 0
        self.speed = -3

    def update_all(self):
        self.image = self.base.left[0]
        self.center_distance += self.speed
        self.pos[0] = self.level.universe.center_x + self.center_distance
        self.pos[1] = self.level.floor - self.image_height + 200 + self.height.next()


class Splash():
    def __init__(self, pos, level, ship, dirty=False):
        directory = level.enemy_dir+'viking_ship/wave/'
        self.distance = 20
        self.ship = ship
        self.level = level
        self.images = obj_images.TwoSided(directory)
        self.image = self.images.left[0]
        self.height = 200
        self.image_height = self.image.get_height()
        self.pos = [self.ship.pos[0]+self.distance, self.ship.height + self.height]
        self.direction = 'left'

    def update_all(self):
        self.image = self.images.left[self.images.itnumber.next()]
        self.pos[0] = self.ship.pos[0]+self.distance
        self.pos[1] = self.ship.height + self.height


class FootBoy():
    def __init__(self, pos, level, dirty=False):
        directory = level.enemy_dir+'footboy/'
        self.center_distance = pos
        self.running = obj_images.There_and_back_again(directory+'walk_body/first_cycle/', second_dir = directory+'walk_body/second_cycle/', extra_part = directory+'happy_face/')
        self.standing_body = obj_images.TwoSided(directory+'walk_body/stand/')
        self.body = self.running
        self.image = self.body.left[0]
        self.level = level
        self.image_height = self.image.get_height()
        self.pos = [self.level.universe.center_x+self.center_distance, self.level.floor-self.image_height+20]
        self.direction = 'left'
        self.gotkissed = 0
        self.image_number = 0
        self.speed = -12

    def update_all(self):
        self.image = self.body.left[self.body.itnumber.next()]
        self.center_distance += self.speed
        self.pos[0] = self.level.universe.center_x + self.center_distance

