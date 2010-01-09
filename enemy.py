import pygame
import obj_images
from pygame.locals import *
import itertools
import random
import os
from settings import *
def p(positions):
    return [i*scale for i in positions ]

enemy_dir = os.getcwd()+'/data/images/enemies/'

class Enemy():
    """This class defines an enemy with no movement and no update to position or image. It is used to be extended by other classes of enemies that should define the functions for movements"""
    def __init__(self,speed,directory, pos, level,margin=p([10,10,10,10]),dirty=False):
        self.center_distance = pos
        for i in ['kissed','walk','stay']:
            exec("self."+i+"= obj_images.TwoSided(directory+'"+i+"/',margin)")
        self.image = self.walk.left[0]
        self.size = (self.image.get_width()/2, self.image.get_height())
        self.level = level
        self.speed = speed*scale
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
            if self.direction == 'right':
                self.center_distance += self.speed
                next_height = self.level.what_is_my_height(self)
                if (self.level.universe.floor - next_height)  <= (self.floor-self.size[1])-(30*scale):
                    self.center_distance += self.speed
            else:
                self.center_distance -= self.speed
                next_height = self.level.what_is_my_height(self)
                if (self.level.universe.floor - next_height)  <= (self.floor-self.size[1]) -(30*scale):
                    self.center_distance -= self.speed

        self.rect = Rect(((self.pos[0]+(self.size[0]/2)),self.pos[1]),(self.size))

class Schnauzer(Enemy):
    def __init__(self, pos, level,margin=p([10,10,10,10]),dirty=False):
        directory  = enemy_dir+'Schnauzer/'
        self.center_distance = pos
        for i in ['kissed','walk','stay']:
            exec("self."+i+"= obj_images.TwoSided(directory+'"+i+"/',margin)")
        self.image = self.walk.left[0]
        self.size = (self.image.get_width()/2, self.image.get_height())
        self.level = level
        self.speed = 12*scale
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
        self.barfing = 0
        self.bow = pygame.mixer.Sound('data/sounds/enemies/dog2.ogg')
        self.lookside = 0

    def barf(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.barfing == 1:
            self.bow.play()
        if self.rect.collidepoint(mouse_pos)and self.barfing == 0 or self.barfing:
            self.barfing += 1
        if self.barfing > 100:
            self.barfing = 0

    def update_all(self):
        princess = self.level.princesses[0]
        self.set_pos()
        self.set_image()
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

        if self.rect.colliderect(princess.kiss_rect):
            self.gotkissed += 1
            self.move = False
        if self.gotkissed != 0:
            self.gotkissed += 1
        if self.gotkissed > 250:
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
    def __init__(self, pos, level,margin=p([10,10,10,10]),dirty=False):
        directory = enemy_dir+'Carriage/'
        self.center_distance = pos
        for i in ['kissed','walk','stay']:
            exec("self."+i+"= obj_images.TwoSided(directory+'"+i+"/',margin)")
        self.image = self.walk.left[0]
        self.size = (self.image.get_width(), self.image.get_height())
        self.level = level
        self.speed = 3 * scale
        self.floor = self.level.universe.floor-self.level.what_is_my_height(self)
        self.margin = margin
        self.pos = [self.level.universe.center_x+self.center_distance,self.floor+self.margin[2]-(self.size[1])]
        self.decide = False
        self.count = 0
        self.move = True
        self.direction = 'left'
        self.rect = Rect((self.pos[0],(level.floor-self.pos[1])),(self.size))
        self.gotkissed = 0
        self.image_number = 0

    def update_all(self):
        self.move = True
        self.set_pos()
        self.set_image()

    def set_pos(self):
        self.floor = self.level.universe.floor - self.level.what_is_my_height(self)
        self.pos = [self.level.universe.center_x + self.center_distance,
                    self.floor+self.margin[2]-(self.size[1])]
        if self.move:
            if self.direction == 'right':
                self.center_distance += self.speed
                next_height = self.level.what_is_my_height(self)
                if (self.level.universe.floor - next_height)  <= (self.floor-self.size[1])-30*scale:
                    self.center_distance += self.speed
            else:
                self.center_distance -= self.speed
                next_height = self.level.what_is_my_height(self)
                if (self.level.universe.floor - next_height)  <= (self.floor-self.size[1]) -30*scale:
                    self.center_distance -= self.speed

        self.rect = Rect((self.pos),(self.size))


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
    height = 100*scale
    up_direction = 'going_down'
    up = 5*scale
    def __init__(self, pos, level,margin=p([10,10,10,10]),dirty=False):
        directory = enemy_dir+'Butterfly/'
        self.speed = 4*scale
        self.center_distance = pos
        for i in ['kissed','walk','stay']:
            exec("self."+i+"= obj_images.TwoSided(directory+'"+i+"/',margin)")
        self.image = self.walk.left[0]
        self.size = (self.image.get_width()/2, self.image.get_height())
        self.level = level
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

    def update_all(self):
        self.set_pos()
        self.set_image()

    def set_pos(self):
        if self.pos[1] < 300*scale:
            self.up = +5*scale
        elif self.pos[1] > 500*scale:
            self.up = -5*scale
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
    def __init__(self, pos, level,margin=p([10,10,10,10]),dirty=False):
        directory = enemy_dir+'OldLady/'
        self.center_distance = pos
        self.walk   = obj_images.TwoSided(directory+'/walk/',margin)
        self.wave   = obj_images.There_and_back_again(directory+'/hover/',margin)
        self.broom  = obj_images.There_and_back_again(directory+'/act/',margin)
        self.image  = self.walk.left[0]
        self.mouseovercount = 0
        self.size   = (self.image.get_width()/2, self.image.get_height())
        self.level  = level
        self.speed  = 2*scale
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
            if self.direction == 'right':
                self.center_distance += self.speed
                next_height = self.level.what_is_my_height(self)
                if (self.level.universe.floor - next_height)  <= (self.floor-self.size[1])-30:
                    self.center_distance += self.speed
            else:
                self.center_distance -= self.speed
                next_height = self.level.what_is_my_height(self)
                if (self.level.universe.floor - next_height)  <= (self.floor-self.size[1]) -30:
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
        directory = level.enemy_dir+'Lion/'
        self.center_distance = pos
        for i in ['base','growl','kissed']:
            exec("self."+i+"= obj_images.There_and_back_again(directory+'"+i+"/',exclude_border = True)")
        self.image = self.base.left[0]
        self.level = level
        self.pos = [self.level.universe.center_x+self.center_distance, 380*scale]
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
        directory = level.enemy_dir+'Elephant/'
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
        directory = level.enemy_dir+'Monkey/'
        self.center_distance = pos
        for i in ['stay','hover','happy','throw','attack']:
            exec("self."+i+"= obj_images.TwoSided(directory+'"+i+"/')")
        self.image = self.stay.left[0]
        self.level = level
        self.pos = [self.level.universe.center_x+self.center_distance, 150*scale ]
        self.direction = 'left'
        self.gotkissed = 0
        self.image_number = 0

    def update_all(self):
        self.image = self.stay.left[0]
        self.pos[0] = self.level.universe.center_x + self.center_distance


class VikingShip():
    def __init__(self, pos, level, dirty=False):
        directory = level.enemy_dir+'VikingShip/'
        self.center_distance = pos
        for i in ['base']:
            exec("self."+i+"= obj_images.TwoSided(directory+'"+i+"/')")
        self.image = self.base.left[0]
        self.level = level
        self.height = itertools.cycle(range(20)+ range(20)[-1:0:-1])
        self.image_height = self.image.get_height()
        self.pos = [self.level.universe.center_x+self.center_distance, self.level.floor - self.image_height + (200*scale) +self.height.next()]
        self.direction = 'left'
        self.gotkissed = 0
        self.image_number = 0
        self.speed = -3*scale
        self.flag = VikingPart(self,'flag',pos_x = 400)
        self.wave = VikingPart(self,'wave',pos_x = 200)


    def update_all(self):
        try:
            wavesize
        except:
            wavesize = self.wave.size[1] -20*scale
        self.image = self.base.left[0]
        self.center_distance += self.speed
        self.pos[0] = self.level.universe.center_x + self.center_distance
        self.pos[1] = self.level.floor - self.image_height + (200*scale) + self.height.next()
        if self.wave not in self.level.floor_image:
            self.level.floor_image.extend([self.flag,self.wave])
        self.flag.pos = self.pos[0]+(self.flag.pos_x-self.flag.size[0]),self.pos[1]+self.flag.pos_y
        self.wave.pos = self.pos[0]+(self.wave.pos_x-self.wave.size[0]),self.level.floor_image[-5].pos[1]-wavesize


class VikingPart():
    def __init__(self, ship, part, pos_x = 0, pos_y = 0):
        directory = 'data/images/enemies/VikingShip/'+part+'/'
        self.pos_x  = pos_x
        self.pos_y  = pos_y
        self.ship = ship
        self.pos  = self.ship.pos[0]+pos_x,self.ship.pos[1]+pos_y
        self.images = obj_images.TwoSided(directory)
        if self.ship.direction == 'left':
            self.actual_images = self.images.left
        else:
            self.actual_images = self.images.right
        self.image = self.actual_images[self.images.itnumber.next()]
        self.size = self.image.get_size()

    def update_all(self):
        self.image = self.actual_images[self.images.itnumber.next()]


class Splash():
    def __init__(self, pos, level, ship, dirty=False):
        directory = level.enemy_dir+'VikingShip/wave/'
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
        directory = level.enemy_dir+'FootBoy/'
        self.center_distance = pos
        self.running = obj_images.There_and_back_again(directory+'walk_body/first_cycle/', second_dir = directory+'walk_body/second_cycle/', extra_part = directory+'happy_face/first_cycle/', second_extra_part = directory+'happy_face/second_cycle/')
        self.running_mad = obj_images.There_and_back_again(directory+'walk_body/first_cycle/',second_dir = directory+'walk_body/second_cycle/', extra_part = directory+'mad_face/first_cycle/', second_extra_part = directory+'mad_face/second_cycle/')
        self.running_kissed = obj_images.There_and_back_again(directory+'kissed/')
        self.standing_body = obj_images.TwoSided(directory+'walk_body/stand/')
        self.body = self.running_mad
        self.image = self.body.left[0]
        self.level = level
        self.size = [(self.image.get_width()/3),self.image.get_height()]
        self.pos = [self.level.universe.center_x+self.center_distance, self.level.floor-self.size[1]+20]
        self.direction = 'left'
        self.got_kissed = 0
        self.image_number = 0
        self.speed = -12*scale
        self.rect = pygame.Rect((self.pos[0]+self.size[0],self.pos[1]),self.size)
        self.level.enemies.append(FootBall(random.randint(int(4000*scale),int(6000*scale)), self))


    def update_all(self):
        if self.direction == 'left':
            self.speed = -12*scale
            self.image = self.body.left[self.body.number]
        else:
            self.speed = 12*scale
            self.image = self.body.right[self.body.number]
        if not self.got_kissed and self.rect.colliderect(self.level.princesses[0].kiss_rect):
            self.got_kissed = 1
        if self.got_kissed > 0:
            if self.got_kissed == 1:
                self.body = self.running_kissed
            self.got_kissed += 1
            if self.got_kissed < 8:
                self.speed = 0
                self.body.update_number()
            elif self.got_kissed < 200:
                self.body = self.running
                self.body.update_number()
            else:
                self.body = self.running_mad
                self.got_kissed = 0
        else:
            self.body.update_number()

        self.center_distance += self.speed


        self.floor = self.level.universe.floor - self.level.what_is_my_height(self)
        self.pos = [self.level.universe.center_x + self.center_distance,
                    self.floor-(self.size[1]-(20*scale))]

#        self.pos[0] = self.level.universe.center_x + self.center_distance



        self.rect = pygame.Rect((self.pos[0]+self.size[0],self.pos[1]),self.size)

class FootBall():
    def __init__(self, center_distance, footboy):
        self.footboy        = footboy
        self.level          = footboy.level
        self.center_distance= center_distance
        self.images         = obj_images.TwoSided('data/images/enemies/FootBoy/ball/')
        self.image          = self.images.left[0]
        self.size           = (self.images.left[0].get_width(),self.images.left[0].get_height()-7)
        self.pos            = [self.footboy.level.universe.center_x + self.center_distance, self.footboy.level.floor - self.size[1]]
        self.speed          = 0
        self.rect           = pygame.Rect(self.pos, self.size)
        self.lowlist        = p((3,4,5,12,13,14))
        self.movetype       = 'high'
        ballheights    = p([80,120,170,210,240,260,270,275])
        ballheights    += list(reversed(ballheights))
        ballheights     += p([1,40,70,90,95,90,70,40,1])
        ballheights    += p([20,10,15,10,20,0])
        self.ballheights = itertools.cycle(ballheights)
        self.direction = self.footboy.direction

#itertools.cycle([i*20 for i in range(7)+list(reversed(range(6)))])


    def update_all(self):
        speed = self.speed
        self.rect           = pygame.Rect(self.pos, self.size)
        if self.footboy.body != self.footboy.running:
            if self.rect.colliderect(self.footboy.rect):
                if self.footboy.body.number in self.lowlist:
                    self.movetype = 'low'
                else:
                    self.movetype = 'high'
                    self.pos[1] += 1
                if self.footboy.direction == "left":
                    self.speed = -50*scale
                else:
                    self.speed = 50*scale
                self.pos[1] += 1
            if self.footboy.direction == 'right' and self.pos[0] < self.footboy.pos[0]:
                self.footboy.direction = 'left'
            if self.footboy.direction == 'left' and self.pos[0]-(400*scale) > self.footboy.pos[0]:
                self.footboy.direction = 'right'
        if speed < 0:
            self.speed += 1
        elif speed > 0:
            self.speed -= 1
        self.direction = self.footboy.direction
        if speed > 0:
            if self.direction == 'left':
                self.image = self.images.right[self.images.itnumber.next()]
            else:
                self.image = self.images.left[self.images.itnumber.next()]
        self.center_distance += speed
        self.pos[0] =  self.footboy.level.universe.center_x + self.center_distance
        floor = (self.level.universe.floor - self.level.what_is_my_height(self)) - (self.size[1])
        if self.pos[1] != floor:
            self.pos[1] = floor - self.ballheights.next()
