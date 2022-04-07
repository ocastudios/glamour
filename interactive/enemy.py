"""Classes of the enemies used in glamour"""
import pygame
import utils
import itertools
import random
import database
import os
import settings
from settings import directory
p = settings.p

class Schnauzer():
	"""Schnauzer is a dog enemy. 
	It is kinda dirty, so the princess cannot let him touch her.
	It runs after the princess and should not be able to fall in the sewers"""
	music = None
	def __init__(self, pos, universe, margin=p([20,20,20,20])):
		self.music	= {'sound':pygame.mixer.Sound(os.path.join(directory.music,'schnauzer.ogg')), 'weight':5} 
		self.bow	= pygame.mixer.Sound(os.path.join(directory.enemies,'Schnauzer_bark.ogg')) 
		self.center_distance = pos
		for i in ['kissed', 'walk', 'stay']:
			self.__dict__[i] = utils.img.TwoSided(os.path.join(directory.enemies,'Schnauzer',i))
		self.image		= self.walk.left[0]
		self.size		= self.image.get_size()
		self.real_size	= self.size
		self.speed		= p(16)
		self.floor		= universe.floor-universe.level.what_is_my_height(self)
		self.margin		= margin
		self.pos		= [universe.center_x+pos,self.floor+self.margin[2]-(self.size[1])]
		self.count = self.gotkissed = self.barfing = self.lookside = 0
		self.move		= True
		self.direction	= random.choice(['left','right'])
		self.rect		= pygame.Rect(((self.pos[0]+int(self.size[0]/2.8)),self.pos[1]),(self.size[0]-int(self.size[0]/2.8),self.size[1]))
		self.beaten		= database.query.is_beaten(universe,'schnauzer')
		self.universe = universe

	def barf(self):
		if self.barfing == 1:
			self.bow.play()
		if self.rect.collidepoint(self.universe.pointer.mouse_pos) and self.barfing == 0 or self.barfing:
			self.barfing += 1
		if self.barfing > 100:
			self.barfing = 0

	def set_pos(self,cross = 30):
		towards = {'right':1,'left':-1}
		get_height = self.universe.level.what_is_my_height
		if self.move:
			modifier = 0 if self.direction == 'left' else self.size[0]
			new_y = get_height(self, pos_x = int(self.center_distance+(self.speed*towards[self.direction])+modifier))
			actual_y = get_height(self)
			obstacle = max(new_y,actual_y)-min(new_y,actual_y)
			if obstacle >= cross:
				self.direction = utils.reverse(self.direction)
			self.center_distance += (self.speed*towards[self.direction])
		self.floor = self.universe.floor - get_height(self)
		self.pos = [self.universe.center_x + self.center_distance,
					self.floor+self.margin[2]-(self.size[1])]
		self.rect = pygame.Rect(self.pos,self.size)

	def update_all(self):
		princess = self.universe.level.princesses[0]
		self.set_pos()
		self.count +=1
		if self.count > 130:
			self.move = False
		if not self.move and not self.gotkissed:
			self.direction = 'right' if  princess.pos[0]>self.pos[0] else 'left'
			if self.count % 2 == 1:
				self.lookside += 1
			if self.lookside == 6:
				self.move = True
				self.lookside = 0
				self.count = 0
		if -p(400) < self.pos[0] < p(1500):
			self.set_image()
			if princess.kiss['rect'] and self.rect.colliderect(princess.kiss['rect']):
				self.gotkissed += 1
				self.move = False
				if not self.beaten:
					database.update.beat_enemy(self.universe, 'schnauzer')
					self.beaten = True
					if database.query.beaten_enemies(self.universe)>=5:
						self.universe.level.unlocking={'type':'dress','name':'yellow'}
		if self.gotkissed:
			self.gotkissed += 1
			if self.gotkissed > 250:
				self.gotkissed = 0
				self.move = True

	def set_image(self):
		if self.gotkissed >=1:
			images = self.kissed
			self.move = False
			self.image = images.__dict__[self.direction][images.number]
		else:
			images = self.walk
			if self.move:
				self.image = images.__dict__[self.direction][images.number]
			else:
				self.image = images.right[0] if self.lookside%2==0 else images.left[0]
		images.update_number()

class Carriage():
	music = None
	def __init__(self, pos, universe,margin=p([10,10,10,10])):
		self.music = {
			'sound':pygame.mixer.Sound(os.path.join(directory.music,'carriage.ogg')),
			'weight':6,
			'playing':False} 
		self.speed = p(3)
		for i in ['walk','stay']:
			self.__dict__[i] = utils.img.TwoSided(os.path.join(directory.enemies,'Carriage',i), margin)
		self.image = self.walk.left[0]
		full_width = self.image.get_width()
		self.correction = full_width/5
		self.size = (full_width-self.correction, self.image.get_height())
		self.real_size = self.image.get_size()
		self.floor = universe.floor-p(192,r=0)
		self.margin = margin
		self.pos = [universe.center_x+pos,self.floor+self.margin[2]-(self.size[1])]
		self.count = 0
		self.move = True
		self.direction = random.choice(['left','right'])
		self.rect = pygame.Rect((self.pos[0]+self.correction,(universe.level.floor-self.pos[1])),(self.size))
		self.gotkissed = 0
		self.image_number = 0
		self.locked = database.query.is_locked(universe,'dress','kimono')
		self.universe = universe
		self.center_distance = pos

	def update_all(self):
		self.set_pos()
		self.set_image()

	def set_pos(self):
		self.pos = [self.universe.center_x + self.center_distance, self.floor+self.margin[2]-(self.size[1])]
		if self.move:
			if self.direction == 'right':
				self.center_distance += self.speed
				self.rect = pygame.Rect(self.pos,(self.size))
			else:
				self.center_distance -= self.speed
				self.rect = pygame.Rect((self.pos[0]+self.correction,self.pos[1]),(self.size))
		if self.rect.contains(self.universe.level.princesses[0].rect):
			if self.locked:
				self.universe.level.unlocking = {'type':'dress','name':'kimono'}
				self.locked = False

	def set_image(self):
		self.image = self.walk.__dict__[self.direction][self.walk.number]
		self.walk.update_number()


class Butterfly():
	music	= None
	walk	= None
	_registry = []
	def __init__(self, pos, universe):
		self.music = self.music or {'sound':pygame.mixer.Sound(os.path.join(directory.music,'butterfly.ogg')),
			'weight':1,
			'playing':False} 
		self.walk = self.walk or utils.img.TwoSided(os.path.join(directory.enemies,'Butterfly','walk'))
		self.walk_number=0
		self._registry.append(self)
		self.height = p(random.randint(300,600))
		self.up_direction = 'going_down'
		self.up = p(5)
		self.speed = p(4)
		self.center_distance = pos
		self.image = self.walk.left[0]
		self.size = (self.image.get_width()/2, self.image.get_height()/2)
		self.real_size = self.image.get_size()
		self.universe = universe
		self.pos = [pos,self.height+(self.size[1]/4)]
		self.direction = random.choice(['left','right'])
		self.rect = pygame.Rect(((self.pos[0]+(self.size[0]/4)),(universe.level.floor-self.pos[1]+(self.size[1]/4))),(self.size))
		self.gotkissed = 0

	def update_all(self):
		self.set_pos()
		self.set_image()

	def set_pos(self):
		if self.pos[1] < p(300):
			self.up = +p(5)
		elif self.pos[1] > p(500):
			self.up = -p(5)
		self.height += self.up
		self.pos = (self.universe.center_x + self.center_distance, self.height+(self.size[1]/4))
		if self.direction == 'right' :
			self.center_distance += self.speed
		else:
			self.center_distance -= self.speed
		self.rect = pygame.Rect(((self.pos[0]+(self.size[0]/4)),self.height+(self.size[1]/4)),(self.size))

	def set_image(self):
		if self.walk_number >= len(self.walk.__dict__[self.direction])-1:
			self.walk_number=0
		else:
			self.walk_number+=1
		self.image = self.walk.__dict__[self.direction][self.walk_number]
		if self.pos[0] > p(10000):
			self.direction = 'left'
		elif self.pos[0] < 0:
			self.direction = 'right'


class OldLady():
	music = None
	def __init__(self, pos, universe,margin=p([10,10,10,10])):
		self.music = {'sound':pygame.mixer.Sound(os.path.join(directory.music,'old_lady.ogg')), 'weight':3} 
		self.center_distance = pos
		self.walk   = utils.img.TwoSided(os.path.join(directory.enemies,'OldLady','walk'),margin)
		self.wave   = utils.img.There_and_back_again(os.path.join(directory.enemies,'OldLady','hover'),margin)
		self.broom  = utils.img.There_and_back_again(os.path.join(directory.enemies,'OldLady','act'),margin)
		self.kissed = utils.img.There_and_back_again(os.path.join(directory.enemies,'OldLady','kissed'),margin)
		self.image  = self.walk.left[0]
		self.mouseovercount = 0
		self.size   = (self.image.get_width()/2, self.image.get_height())
		self.real_size = self.image.get_size()
		self.universe  = universe
		self.speed  = p(2)
		self.floor  = universe.floor-universe.level.what_is_my_height(self)
		self.margin = margin
		self.pos = [universe.center_x+pos,self.floor+self.margin[2]-(self.size[1])]
		self.decide = False
		self.count = 0
		self.direction = 'left'
		self.action = 'walk'
		self.rect = pygame.Rect(((self.pos[0]+(self.size[0]/2)),(self.universe.level.floor-self.pos[1])),(self.size))
		self.image_number = 0
		self.universe.level.enemies.append(BroomingDust(self))
		self.beaten = database.query.is_beaten(self.universe,'old_lady')

	def update_all(self):
		if -p(400) < self.pos[0] < p(1490):
			self.got_kissed()
			self.wave_to_princess()
			self.brooming()
			self.count +=1
			self.set_image()
		self.set_pos()

	def got_kissed(self):
		princess = self.universe.stage.princesses[0]
		if self.action not in ('wave', 'kissed') and princess.kiss['rect'] and self.rect.colliderect(princess.kiss['rect']):
			self.action = 'kissed'
			self.image_number = 0
			self.count = 0
		if self.action == 'kissed':
			if 5 < self.count < 15:
				self.image_number -= 1
			elif self.count > 20:
				self.action = "walk"
				self.count = 0

	def wave_to_princess(self):
		if self.action not in  ('wave', 'kissed'):
			if self.rect.collidepoint(self.universe.pointer.mouse_pos):
				self.action = 'wave'
				self.image_number = 0
				self.count = 0
				if not self.beaten:
					database.update.beat_enemy(self.universe, 'old_lady')
					self.beaten = True
					if database.query.beaten_enemies(self.universe)>=5:
						self.universe.level.unlocking={'type':'dress','name':'yellow'}
		if self.action == 'wave':
			if self.count > 33:
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

	def set_pos(self):
		get_height = self.universe.level.what_is_my_height
		self.floor = self.universe.floor - get_height(self)
		self.pos = [self.universe.center_x + self.center_distance, self.floor+self.margin[2]-(self.size[1])]
		if self.action == 'walk':
			if self.direction == 'right':
				self.center_distance += self.speed
				next_height = get_height(self)
				if (self.universe.floor - next_height)  <= (self.floor-self.size[1])-p(5):
					self.center_distance += self.speed
			else:
				self.center_distance -= self.speed
				next_height = get_height(self)
				if (self.universe.floor - next_height)  <= (self.floor-self.size[1]) -p(5):
					self.center_distance -= self.speed
		self.rect = pygame.Rect(((self.pos[0]+(self.size[0]/2)),(self.universe.level.floor-self.size[1])),(self.size))

	def set_image(self):
		actual_list = self.__dict__[self.action].__dict__[self.direction]
		number_of_files = len(actual_list)-2
		if self.image_number <= number_of_files:
			self.image_number +=1
		else:
			self.image_number = 0
		self.image = actual_list[self.image_number]


class BroomingDust():
	music = None
	def __init__(self, lady):
		self.music 			= None
		self.lady			= lady
		self.universe		= lady.universe
		self.center_distance= lady.center_distance
		self.images			= utils.img.TwoSided(os.path.join(directory.enemies,'OldLady','dirt'))
		self.image			= self.images.left[0]
		self.size			= (self.images.left[0].get_width(),self.images.left[0].get_height())
		self.real_size		= self.images.left[0].get_size()
		self.pos			= [self.lady.pos[0]-p(194), self.lady.pos[1]+p(38)]
		self.direction		= lady.direction
		self.rect_list		= ( 
								{'pos':(0,0),'size':(0,0)},
								{'pos':(0,0),'size':(0,0)},
								{'pos':(0,0),'size':(0,0)},
								{'pos':(0,0),'size':(0,0)},
								{'pos':(121,87),'size':(92,94)},
								{'pos':(110,90),'size':(92,94)},
								{'pos':(97,85),'size':(103,97)},
								{'pos':(89,76),'size':(111,108)},
								{'pos':(85,70),'size':(113,111)},
								{'pos':(66,53),'size':(121,131)},
								{'pos':(53,45),'size':(130,140)},
								{'pos':(44,39),'size':(124,145)},
								{'pos':(50,30),'size':(108,151)},
								{'pos':(0,0),'size':(0,0)},
								{'pos':(0,0),'size':(0,0)}
								)
		rect_pos			= (self.pos[0]+self.rect_list[self.images.number]['pos'][0],
							   self.pos[1]+self.rect_list[self.images.number]['pos'][1])
		rect_rect		   = self.rect_list[self.images.number]['size']
		self.rect		   = pygame.Rect(rect_pos, rect_rect)
		self.active		 = False

	def update_all(self):
		if (self.lady.action == 'broom' and self.lady.image_number ==1) or (self.images.number != 0):
			if self.direction == 'left':
				self.pos = [self.lady.pos[0]-p(194), self.lady.pos[1]+p(38)]
				self.image = self.images.left[self.images.number]
				rect_pos = (self.pos[0]+self.rect_list[self.images.number]['pos'][0],  self.pos[1]+self.rect_list[self.images.number]['pos'][1])
			else:
				self.pos = [self.lady.pos[0]+p(144), self.lady.pos[1]+p(38)]
				self.image = self.images.right[self.images.number]
				rect_pos = (self.pos[0]+p(144)-self.rect_list[self.images.number]['pos'][0],  self.pos[1]+self.rect_list[self.images.number]['pos'][1])
			rect_rect = self.rect_list[self.images.number]['size']
			self.rect = pygame.Rect(rect_pos, rect_rect)
			self.images.update_number()
		else:
			self.direction = self.lady.direction
			self.rect = ((0,0),(0,0))
			self.image = None


class Lion():
	music = None
	def __init__(self, universe):
		self.music = None
		self.center_distance = p(3200,r=0)
		self.base  = utils.img.There_and_back_again(os.path.join(directory.enemies,'Lion','base'),exclude_border = True)
		self.growl = utils.img.There_and_back_again(os.path.join(directory.enemies,'Lion','growl'),exclude_border = True)
		self.kissed = utils.img.TwoSided(os.path.join(directory.enemies,'Lion','kissed'))
		self.image = self.base.left[0]
		self.universe = universe
		self.pos = [self.universe.center_x+self.center_distance, p(380)]
		self.rect =  pygame.Rect(self.pos, self.base.size)
		self.direction = random.choice(['right','right'])
		self.got_kissed = 0
		self.tail = Tail(self)
		self.action = "dance"
		self.growl_sound = pygame.mixer.Sound(os.path.join(directory.sounds,'enemies','lion3.ogg'))
		self.channel4 = pygame.mixer.Channel(4)
		self.locked = database.query.is_locked(self.universe,'face','indian')
		self.beaten = database.query.is_beaten(self.universe,'lion')

	def update_all(self):
		princess = self.universe.level.princesses[0]
		if -p(400) < self.pos[0] < p(1490):
			if self.action == "dance":
				self.base.update_number()
				self.image = self.base.left[self.base.number]
				if self.base.number == 0:
					if random.randint(1,6) == 1:
						self.action = 'growl'
			if self.action == 'growl':
				if self.growl.number == 2:
					princess.status["scared"] = 1
					princess.status["danger"] = self.center_distance
				if self.growl.number in (0,13):
					self.channel4.play(self.growl_sound)
				self.image = self.growl.left[self.growl.number]
				if self.growl.lenght-1 == self.growl.number:
					self.action = 'dance'
					self.base.number = 0
				self.growl.update_number()
			if self.action == 'kissed':
				self.image = self.kissed.left[self.kissed.number]
				self.got_kissed += 1
				if self.got_kissed < 60:
					self.kissed.number += 1
					if self.kissed.number >= 3:
						self.kissed.number = 3
				elif self.kissed.number > 0:
					self.kissed.number -= 1
				else:
					self.action = "dance"
					self.base.number = 0
			if princess.kiss['rect'] and self.rect.colliderect(princess.kiss['rect']):
				if self.action != "kissed":
					self.kissed.number = 0
					if not self.beaten:
						database.update.beat_enemy(self.universe, 'lion')
						self.beaten = True
						if database.query.beaten_enemies(self.universe)>=5:
							self.universe.level.unlocking={'type':'dress','name':'yellow'}
				self.action = "kissed"
				self.got_kissed = 0
				if self.locked:
					self.universe.level.unlocking = {'type':'face','name':'indian'}
					self.locked = False
			self.rect = pygame.Rect(self.pos, self.base.size) 
		self.pos[0] = self.tail.pos[0]= self.universe.center_x + self.center_distance


class Tail():
	music = None
	def __init__(self, lion):
		self.music = None
		self.lion = lion
		self.pos  = self.lion.pos
		self.images = utils.img.There_and_back_again(os.path.join(directory.enemies,'Lion','tail'))
		self.image = self.images.list[next(self.images.itnumber)]

	def update_all(self):
		if 0 < self.pos[0] < p(700):
			self.image = self.images.list[next(self.images.itnumber)]
		self.pos  = self.lion.pos

class Elephant():
	music = None
	def __init__(self, universe):
		self.music = None
		self.center_distance = p(3600)
		for i in ['base','hover']:
			self.__dict__[i] = utils.img.There_and_back_again(os.path.join(directory.enemies,'Elephant',i),exclude_border = True)
		self.image = self.base.left[0]
		self.size = self.base.size
		self.real_size = self.size
		self.universe = universe
		self.pos = [self.universe.center_x+self.center_distance, (self.universe.level.floor - self.image.get_height()) +15 ]
		self.direction = random.choice(['left','right'])
		self.gotkissed = 0
		self.image_number = 0
		self.action = 'dance'
		self.count = 0
		self.call = pygame.mixer.Sound(os.path.join(directory.sounds,'enemies','elephant9.ogg'))
		self.channel = pygame.mixer.Channel(3)
		self.rect = pygame.Rect((0,0),(0,0))

	def update_all(self):
		if -p(400) < self.pos[0] < p(1490):
			self.rect = pygame.Rect(self.pos, self.base.size)
			if self.action == "dance":
				self.base.update_number()
				self.image = self.base.left[self.base.number]
				if self.base.number == 0:
					if self.rect.collidepoint(self.universe.pointer.mouse_pos):
						self.action = 'call'
			if self.action == 'call':
				self.image = self.hover.left[self.hover.number]
				if self.hover.number in (5,11):
					self.channel.play(self.call)
				if self.hover.number in (6,12):
					self.count += 1
					if self.count > 60:
						self.count = 0
						self.hover.update_number()
				else:
					self.hover.update_number()
				if self.hover.number == 0:
					self.action = 'dance'
		self.pos[0] = self.universe.center_x + self.center_distance


class Giraffe():
	music = None
	def __init__(self,universe):
		self.music = None
		self.center_distance = p(3800,r=0)
		ordered_directory_list = (os.path.join(directory.enemies,'giraffe','base'),
								  os.path.join(directory.enemies,'giraffe','chew'))
		self.chewing_images = utils.img.MultiPart(ordered_directory_list)
		self.hover_images   = utils.img.TwoSided(os.path.join(directory.enemies,'giraffe','hover'))
		self.image		  = self.chewing_images.left[0]
		self.universe		  = universe
		self.pos			= [universe.center_x+self.center_distance, (self.universe.level.floor - self.image.get_height())]
		self.direction = random.choice(['left','right'])
		self.image_number = 0
		self.count = 0

	def update_all(self):
		if -p(400) < self.pos[0] < p(1490):
			if self.count == 2:
				self.image = self.chewing_images.left[next(self.chewing_images.itnumber)]
				self.count = 0
			self.count += 1
		self.pos[0] = self.universe.center_x + self.center_distance


class Penguin():
	music = None
	def __init__(self, universe):
		self.music = None
		self.images = utils.img.There_and_back_again(os.path.join(directory.enemies,'penguin','jump'),exclude_border=True)
		self.center_distance = p(3550,r=0)
		self.image = self.images.left[self.images.number]
		self.size = self.images.size
		self.real_size = self.size
		self.universe = universe
		self.pos = [self.universe.center_x+self.center_distance, (self.universe.level.floor - self.image.get_height())+p(15)]
		self.direction = 'left'
		self.gotkissed = 0
		self.image_number = 0
		self.gforce= {'accel':3,'max':10,'actual':0}
		self.action = 'dance'
		self.jump  = 0
		self.count = {'time':0,'jumps':0}
		self.floor = self.universe.floor - self.universe.level.what_is_my_height(self)
		self.locked = database.query.is_locked(self.universe,'accessory','beret')

	def update_all(self):
		self.pos[0] = self.universe.center_x + self.center_distance
		if -p(400) < self.pos[0] < p(1490):
			self.update_image()
			self.jumping()
			self.floor = self.universe.floor - self.universe.level.what_is_my_height(self)
			if self.action == 'dance':
				self.dancing()
				if self.count['time'] >= 50:
					self.count['time'] = 0
					self.action = 'jump'
					if self.universe.level.princesses[0].jump:
						self.count['jumps']+=1
					else:
						self.count['jumps']=0
					if self.count['jumps']==3:
						if self.locked:
							self.universe.level.unlocking = {'type':'accessory','name':'beret'}
							self.locked = False
			self.count['time'] += 1

	def dancing(self):
		if self.count['time'] %5 ==0:
			if self.image in self.images.left:
				self.direction = 'right'
			else:
				self.direction = 'left'

	def update_image(self):
		self.image = self.images.__dict__[self.direction][self.images.number]

	def jumping(self):
		feet_position = self.pos[1]+self.size[1]
		if self.action != 'dance':
			self.images.update_number()
		if self.action != 'jump':
			self.jump = 0
			if self.action=='fall':
				self.pos[1] += self.gforce['actual']
				self.gforce['actual']+= self.gforce['accel']
				if feet_position >= self.floor:
					self.action='dance'
					self.pos[1] = (self.universe.level.floor - self.image.get_height())+p(15)
			if feet_position < self.floor and not self.jump:
				self.action='fall'
		else:
			self.jump +=1
			if self.jump == 1:
				self.images.number = 0
				self.gforce['actual'] = 0
			if self.action == 'jump':
				if self.jump > 0 and self.jump <20:
					self.pos[1] -= p(30)
					if self.jump > 10:
						self.images.number = 0
						self.action= 'fall'


class Monkey():
	music = None
	def __init__(self, universe):
		self.music = None
		self.center_distance = p(3500,r=0)
		for i in ['stay','hover','happy','throw','attack']:
			self.__dict__[i] = utils.img.TwoSided(os.path.join(directory.enemies,'Monkey',i))
		self.direction = random.choice(['right','right'])
		self.image = self.stay.__dict__[self.direction][0]
		self.size  = self.stay.size
		self.real_size = self.size
		self.universe = universe
		self.pos = [universe.center_x+self.center_distance, p(150)]
		self.gotkissed = 0
		self.image_number = 0
		self.action = 'stay'
		self.banana = Banana(universe,self)
		self.universe.level.enemies.append(self.banana)
		self.rect = pygame.Rect((0, 0), (0, 0))

	def update_all(self):
		self.pos[0] = self.universe.center_x + self.center_distance
		if -p(400) < self.pos[0] < p(1490):
			if self.universe.level.princesses[0].pos[0] > self.pos[0]:
				self.direction= 'left'
			else:
				self.direction = 'right'
			self.image = self.stay.__dict__[self.direction][0]
			self.pos[0] = self.universe.center_x + self.center_distance
			self.rect = pygame.Rect(self.pos,self.size)
			if self.rect.collidepoint(self.universe.pointer.mouse_pos):
				self.image = self.hover.left[0]
			elif self.action == 'attack':
				self.image = self.throw.__dict__[self.direction][self.throw.number]
				self.throw.update_number()
				if self.throw.number == 0:
					self.action = 'stay'
			elif self.action == 'stay' and self.banana.status == 'held':
				if random.randint(0,50)== 0:
					self.action = 'attack'


class Banana():
	music = None
	def __init__(self, universe, monkey):
		self.monkey = monkey
		self.center_distance = self.monkey.center_distance
		self.images = {
					'throwing': utils.img.TwoSided(os.path.join(directory.enemies,'Monkey','banana','throwing')),
					'quiet':	utils.img.TwoSided(os.path.join(directory.enemies,'Monkey','banana','quiet')),
					'thrown':   utils.img.TwoSided(os.path.join(directory.enemies,'Monkey','banana','thrown')),
					}
		self.image = self.images['quiet'].__dict__[self.monkey.direction][0]
		self.size = self.images['quiet'].size
		self.real_size = self.size
		self.universe = universe
		self.pos = [self.monkey.pos[0],self.monkey.pos[1]]
		self.pos_correction = p([72,37],r=0)
		self.banana_size = p([29,51],r=0)
		self.image_number = 0
		self.status = 'held'
		self.direction = 'left'
		self.speed = {
						'max': p(40),
						'resistance': p(2,r=0),
						'actual': p(40),
						'gforce': p(0),
						'gaccel': p(3)
					 }
		self.rect = pygame.Rect(
						(self.pos[0]+self.pos_correction[0],self.pos[1]+self.pos_correction[1]),
						self.banana_size
						)

	def update_all(self):
		self.rect = pygame.Rect(
				(self.pos[0]+self.pos_correction[0],self.pos[1]+self.pos_correction[1]),
				self.banana_size
				)
		if self.status == 'held':
			self.pos = [self.monkey.pos[0],self.monkey.pos[1]]
			if self.monkey.action == 'stay':
				self.image = None
			if self.monkey.action == 'attack':
				images = self.images['throwing']
				self.image = images.__dict__[self.monkey.direction][images.number]
				images.update_number()
				if images.number == 3 or self.monkey.throw.number == 10:
					self.status = 'thrown'
					images.number = 0
					self.direction = self.monkey.direction
		if self.status == 'thrown':
			self.image = self.images['thrown'].__dict__[self.monkey.direction][0]
			self.pos[0] = self.universe.center_x + self.center_distance
			if self.direction == 'left':
				self.center_distance += self.speed['actual']
			else:
				self.center_distance -= self.speed['actual']
			if self.speed['actual'] > 0:
				self.speed['actual'] = round(self.speed['actual']-self.speed['resistance'])
			else:
				self.speed['actual'] = 0
			if self.pos[1] < self.universe.level.floor:
				self.pos[1] += self.speed['gforce']
				self.speed['gforce']+=self.speed['gaccel']
			if self.pos[1] > self.universe.level.floor:
				self.status = 'held'
				self.speed['gforce'] = 0
				self.speed['actual'] = self.speed['max']
				self.center_distance = self.monkey.center_distance


class VikingShip():
	"""Viking Ship is a special enemy. It is included in front of the floor, between two layers of water.
	It's base image is included between the waters by the function that places the waters.
	The other images are included here"""
	music = None 

	def __init__(self, universe):
		self.music = self.music or {'sound':pygame.mixer.Sound(os.path.join(directory.enemies,'viking_ship.ogg')),
			 'weight':5}
		self.universe = universe
		self.base = utils.img.TwoSided(os.path.join(directory.enemies,'VikingShip','base'))
		sailor_body = utils.img.image(os.path.join(directory.enemies,'VikingShip','viking_sailor','body','0.png'))
		left_sailor = utils.img.invert_images([sailor_body])
		for i in self.base.left:
			i.blit(sailor_body,(p(253),p(635)))
		for i in self.base.right:
			i.blit(left_sailor[0], (p(490),p(639)))
		del sailor_body, left_sailor
		D = self.D = {
			'right':{
				'center_distance': p(40, r=0),
				'flag_pos': 650,
				'wave_pos': 820,
				'head':  (476,518),
				'talk':  (650,400),
				'shout': (650,250)
			},
			'left':{
				'center_distance':p(9000, r=0),
				'flag_pos':400,
				'wave_pos':200,
				'head':  (262,518),
				'talk':  (-90,400),
				'shout': (-350,250)
			}
		}

		self.direction = random.choice(['right','left'])
		self.center_distance = D[self.direction]['center_distance']
		self.image = self.base.__dict__[self.direction][0]
		self.height = itertools.cycle(list(range(20))+ list(range(20))[-1:0:-1])
		self.image_height = self.image.get_height()
		self.pos = [universe.center_x+self.center_distance, universe.level.floor - self.image_height + p(200) +next(self.height)]
		self.gotkissed		= 0
		self.image_number	= 0
		self.speed = p(3)
		self.flag = VikingPart(self,'flag',pos_x = D[self.direction]['flag_pos'])
		self.wave = VikingPart(self,'wave',pos_x = D[self.direction]['wave_pos'])
		self.head_list = {
			"normal": VikingPart(self, os.path.join('viking_sailor','head_normal'),
					pos_x = D[self.direction]['head'][0],
					pos_y = D[self.direction]['head'][1]),
			"hover": VikingPart(self, os.path.join('viking_sailor','head_hover'),
					pos_x = D[self.direction]['head'][0],
			 		pos_y = D[self.direction]['head'][1]),
			"angry" : VikingPart(self,os.path.join('viking_sailor','head_angry'),
					pos_x = D[self.direction]['head'][0],
			 		pos_y = D[self.direction]['head'][1]),
			"talk"  : VikingPart(self,os.path.join('viking_sailor','head_talk'),
					pos_x = D[self.direction]['head'][0],
			 		pos_y = D[self.direction]['head'][1]),
		}
		self.mood  = "normal"
		self.head  = self.head_list[self.mood]
		self.count = 0
		self.sailor_rect = pygame.Rect(self.head.pos,self.head.size)
		self.talk_balloon_rect = pygame.Rect((0,0),(0,0))
		self.balloon = Balloon(self, brand = 'talk', pos_x = self.D[self.direction]['talk'][0], pos_y = self.D[self.direction]['talk'][1])
		self.beaten = database.query.is_beaten(self.universe,'viking_ship')


	def update_all(self):
		#take the balloon off the way, for it hurts the princess
		#if self.mood is talk it will be reset below
		if -p(1000) < self.pos[0] < p(1800): #check if Viking is on screen
			if self.wave not in self.universe.level.floor_image:
				self.universe.level.floor_image.extend([self.flag,self.wave,self.head])
			else:
				self.head = self.head_list[self.mood] # change faces acording to the mood
				self.universe.level.floor_image[-1] = self.head
			self.count += 1
			if self.mood == "normal":
				#on normal mood Viking resets balloon
				self.reset_talk()
				self.reset_shout()
				#check if mood should be changed
				self.check_mood_talking()
				self.check_mood_hover()
				self.check_mood_angry()
			elif self.mood == "hover":
				if self.count > 40:
					self.mood = "normal"
					self.count = 0
			elif self.mood == "talk":
				self.check_mood_angry()
				#The balloon must appear over the boat
				#But the last floor listing position is used by the sailor head
				#That is why the balloon will be placed on the panel list
				if self.count > 60:
					self.mood = "normal"
					self.count = 0
					self.reset_talk()
				self.talk_balloon_rect	= pygame.Rect(self.balloon.pos,self.balloon.size)
			elif self.mood == "angry":
				if self.count > 60:
					self.reset_shout()
					self.mood = "normal"
					self.count = 0
		#while not on screen Viking should only update position.
		self.moving()

	def reset_talk(self):
		self.talk_balloon_rect	= pygame.Rect((0,0),(0,0))
		self.remove_curses()

	def reset_shout(self):
		self.remove_curses()

	def remove_curses(self):
		to_remove = []
		for i in self.universe.level.panel:
			if i.__class__ == Balloon:
				to_remove.append(i)
		for i in to_remove:
			self.universe.level.panel.remove(i)
		del to_remove

	def moving(self):
		if self.direction == "left":
			self.center_distance -= self.speed
		else:
			self.center_distance += self.speed
		self.pos[0] = self.universe.center_x + self.center_distance
		self.pos[1] = self.universe.level.floor - self.image_height + p(200) + next(self.height)
		self.sailor_rect = pygame.Rect(self.head.pos,self.head.size)
		self.flag.pos = self.pos[0]+(self.flag.pos_x-self.flag.size[0]),self.pos[1]+self.flag.pos_y
		self.wave.pos = self.pos[0]+(self.wave.pos_x-self.wave.size[0]),self.universe.level.floor_image[-5].pos[1]-(self.wave.size[1]-p(20))
		self.head.pos = self.pos[0]+self.head.pos_x,self.pos[1]+self.head.pos_y

	def check_mood_talking(self):
		if self.count > 100 and random.randint(0,20) == 0:
			self.mood = "talk"
			self.balloon =  Balloon(self, pos_x = self.D[self.direction]['talk'][0], pos_y = self.D[self.direction]['talk'][1] )
			self.universe.level.panel.append(self.balloon)
			self.balloon.pos = self.pos[0]+self.balloon.pos_x,self.pos[1]+self.balloon.pos_y
			self.count = 0

	def check_mood_hover(self):
		if self.sailor_rect.collidepoint(self.universe.pointer.mouse_pos):
			if not self.beaten:
				database.update.beat_enemy(self.universe, 'viking_ship')
				self.beaten = True
				if database.query.beaten_enemies(self.universe)>=5:
					self.universe.level.unlocking={'type':'dress','name':'yellow'}
			self.mood = "hover"
			self.reset_talk()
			self.count = 0

	def check_mood_angry(self):
		D = self.D
		if self.universe.level.princesses[0].kiss and self.sailor_rect.colliderect(self.universe.level.princesses[0].kiss['rect']):
			self.universe.stage.princesses[0].get_dirty()
			self.mood = "angry"
			self.reset_talk()
			self.balloon = Balloon(self, brand='shout', pos_x=D[self.direction]['shout'][0], pos_y=D[self.direction]['shout'][1])
			self.universe.level.panel.append(self.balloon)
			self.balloon.pos = self.pos[0]+self.balloon.pos_x,self.pos[1]+self.balloon.pos_y
			self.count = 0


class VikingPart():
	music = None
	def __init__(self, ship, part, pos_x = 0, pos_y = 0):
		self.pos_x  = p(pos_x,r=False)
		self.pos_y  = p(pos_y,r=False)
		self.ship = ship
		self.pos  = self.ship.pos[0]+pos_x,self.ship.pos[1]+pos_y
		self.images = utils.img.TwoSided(os.path.join(directory.enemies,'VikingShip',part))
		if self.ship.direction == 'left':
			self.actual_images = self.images.left
		else:
			self.actual_images = self.images.right
		self.image = self.actual_images[next(self.images.itnumber)]
		self.size = self.image.get_size()
		self.real_size = self.size

	def update_all(self):
		self.image = self.actual_images[next(self.images.itnumber)]


class Balloon():
	talk_image_tpl = utils.img.image(os.path.join(directory.enemies, 'VikingShip', 'talk_balloon', '0.png'))
	shout_image_tpl = utils.img.image(os.path.join(directory.enemies, 'VikingShip', 'shout_balloon', '0.png'))
	curses = [os.path.join(directory.enemies,'VikingShip','curses',str(index)+'.png') for index in range(7)]
	music = None
	def __init__(self, ship, brand = 'talk', pos_x = 0, pos_y = 0):
		self.pos_x	= p(pos_x, r=False)
		self.pos_y	= p(pos_y, r=False)
		self.ship	= ship
		self.pos	= self.ship.pos[0]+pos_x, self.ship.pos[1]+pos_y
		if brand	==	'talk':
			image_size = p([341,223])
			self.image = pygame.Surface(image_size, pygame.SRCALPHA).convert_alpha()
			self.image.blit(self.talk_image_tpl, (0,0))
			self.image.blit(utils.img.image(random.choice(self.curses)), p([29,42]))
			self.image.blit(utils.img.image(random.choice(self.curses)), p([104,42]))
			self.image.blit(utils.img.image(random.choice(self.curses)), p([174,42]))
		else:
			image_size = p([605,364])
			self.image = pygame.Surface(image_size, pygame.SRCALPHA).convert_alpha()
			self.image.blit(self.shout_image_tpl, (0,0))
			self.image.blit(utils.img.image(random.choice(self.curses)), p([104,186]))
			self.image.blit(utils.img.image(random.choice(self.curses)), p([83,85]))
			self.image.blit(utils.img.image(random.choice(self.curses)), p([371,143]))
			self.image.blit(utils.img.image(random.choice(self.curses)), p([201,194]))
			self.image.blit(utils.img.image(random.choice(self.curses)), p([307,191]))
			self.image.blit(utils.img.image(random.choice(self.curses)), p([257,124]))
			self.image.blit(utils.img.image(random.choice(self.curses)), p([165,131]))
			self.image.blit(utils.img.image(random.choice(self.curses)), p([319,101]))
			self.image.blit(utils.img.image(random.choice(self.curses)), p([245,56]))
		if self.ship.direction == 'left':
			pass
		else:
			self.image = pygame.transform.flip(self.image,1,0)
		self.size = self.image.get_size()
		self.real_size = self.size

	def update_all(self):
		self.pos = self.ship.pos[0]+self.pos_x,self.ship.pos[1]+self.pos_y


class FootBoy():
	music = None
	def __init__(self, pos, universe):
		self.music = self.music or {'sound':pygame.mixer.Sound(os.path.join(directory.music,'fabrizio.ogg')),
			'weight':4,
			'playing':False}
		self.center_distance = pos
		walk1 = os.path.join(directory.enemies,'FootBoy','walk_body','first_cycle')
		walk2 = os.path.join(directory.enemies,'FootBoy','walk_body','second_cycle')
		self.running = utils.img.There_and_back_again(
						walk1, second_dir = walk2,
						extra_part = os.path.join(directory.enemies,'FootBoy','happy_face','first_cycle'),
						second_extra_part = os.path.join(directory.enemies,'FootBoy','happy_face','second_cycle'))
		self.running_mad = utils.img.There_and_back_again(
					walk1, second_dir = walk2,
					extra_part = os.path.join(directory.enemies,'FootBoy','mad_face','first_cycle'),
					second_extra_part = os.path.join(directory.enemies,'FootBoy','mad_face','second_cycle'))
		self.running_kissed = utils.img.There_and_back_again(os.path.join(directory.enemies,'FootBoy','kissed'))
		self.standing_body = utils.img.TwoSided(os.path.join(directory.enemies,'FootBoy','walk_body','stand'))
		self.body = self.running_mad
		self.image = self.body.left[0]
		self.universe = universe
		self.size = [(self.image.get_width()/3),self.image.get_height()]
		self.real_size = self.size
		self.pos = [universe.center_x+pos, universe.level.floor-self.size[1]+20]
		self.direction = random.choice(['left','right'])
		self.got_kissed = 0
		self.image_number = 0
		self.speed = -p(14)
		self.rect = pygame.Rect((self.pos[0]+self.size[0],self.pos[1]),self.size)
		self.universe.level.enemies.append(FootBall(random.randint(int(p(4000)),int(p(6000))), self))
		self.beaten = database.query.is_beaten(self.universe,'footboy')

	def update_all(self):
		if self.direction == 'left':
			self.speed = -p(12)
			self.image = self.body.left[self.body.number]
		else:
			self.speed = p(12)
			self.image = self.body.right[self.body.number]
		princess = self.universe.level.princesses[0]
		if not self.got_kissed and princess.kiss['rect'] and self.rect.colliderect(princess.kiss['rect']):
			self.got_kissed = 1
			if not self.beaten:
				database.update.beat_enemy(self.universe, 'footboy')
				self.beaten = True
				if database.query.beaten_enemies(self.universe)>=5:
					self.universe.level.unlocking={'type':'dress','name':'yellow'}
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
		self.floor = self.universe.floor - self.universe.level.what_is_my_height(self)
		self.pos = [self.universe.center_x + self.center_distance,
					self.floor-(self.size[1]-p(20))]
		self.rect = pygame.Rect((self.pos[0]+self.size[0],self.pos[1]),self.size)
		if -200 < self.center_distance <-100 and self.direction =='left':
			self.got_kissed +=.01
		elif 10200 < self.center_distance < 10300 and self.direction =='right':
			self.got_kissed +=.01

class FootBall():
	music = None
	def __init__(self, center_distance, footboy):
		self.footboy = footboy
		self.universe = footboy.universe
		self.center_distance= center_distance
		self.images = utils.img.TwoSided(os.path.join(directory.enemies,'FootBoy','ball'))
		self.image = self.images.left[0]
		self.size = (self.images.left[0].get_width(),self.images.left[0].get_height()-p(7))
		self.real_size = self.size
		self.pos = [self.footboy.universe.center_x + self.center_distance, self.footboy.universe.level.floor - self.size[1]]
		self.speed = 0
		self.rect = pygame.Rect(self.pos, self.size)
		self.lowlist = p((3,4,5,12,13,14))
		self.movetype = 'high'
		ballheights = p([80,120,170,210,240,260,270,275])
		ballheights += list(reversed(ballheights))
		ballheights += p([1,40,70,90,95,90,70,40,1])
		ballheights	+= p([20,10,15,10,20,0])
		self.ballheights = itertools.cycle(ballheights)
		self.direction = self.footboy.direction

#itertools.cycle([i*20 for i in range(7)+list(reversed(range(6)))])
	def update_all(self):
		direction = {'right':1,'left':-1}
		speed = self.speed
		if self.footboy.body != self.footboy.running:
			if self.rect.colliderect(self.footboy.rect):
				self.direction = self.footboy.direction
				if self.footboy.body.number in self.lowlist:
					self.movetype = 'low'
				else:
					self.movetype = 'high'
					self.pos[1] += 1
				self.speed = p(50)
				self.pos[1] += 1
			#call the boy back
			if self.footboy.direction == 'right' and self.pos[0] < self.footboy.pos[0]:
				self.footboy.direction = 'left'
			if self.footboy.direction == 'left' and self.pos[0]-p(400) > self.footboy.pos[0]:
				self.footboy.direction = 'right'
		if speed:
			self.speed -= 1
			backwards = True if (self.direction=='left') else False
			self.images.update_number(backwards)
			self.image = self.images.left[self.images.number]
		self.center_distance += speed*direction[self.direction]
		self.pos[0] =  self.footboy.universe.center_x + self.center_distance
		floor = (self.universe.floor - self.universe.level.what_is_my_height(self)) - (self.size[1])
		if self.pos[1] != floor:
			self.pos[1] = floor - next(self.ballheights)
		self.rect   = pygame.Rect(self.pos, self.size)


class Bird():
	music = None
	disturbed = {'ongoing':False, 'count':0,'spot':(0,0),'count_all':0}
	flying = utils.img.There_and_back_again(os.path.join(directory.enemies,'Birdy','fly'))
	walking = utils.img.There_and_back_again(os.path.join(directory.enemies,'Birdy','walk'))
	standing = utils.img.TwoSided(os.path.join(directory.enemies,'Birdy','stay'))
	def __init__(self, pos, universe):
		self.center_distance = int(pos+p(random.randint(3,50)))
		self.margin = p([5,5,5,5])
		self.body = self.walking
		self.image = self.body.left[0]
		self.universe = universe
		self.size = [(self.image.get_width()/3),self.image.get_height()]
		self.real_size = self.image.get_size()
		#adjusting self.size
		self.size[1] -= p(8)
		self.pos = [universe.center_x+self.center_distance, universe.level.floor+self.margin[2]-self.size[1]+p(10)]
		self.direction  = 'left'
		self.counter	= 0
		self.image_number = 0
		self.speed = p(5)
		self.rect = pygame.Rect((self.pos[0]+self.size[0],self.pos[1]),self.size)
		hawks = 0
		for i in self.universe.level.enemies:
			if i.__class__ == Hawk:
				hawks += 1
		if not hawks:
			universe.level.enemies.append(Hawk((universe.width+int(p(600)), int(-p(300))), universe, self))
			self.original = True
		else:
			self.original = False
		self.gforce		 = 0
		self.g_acceleration = p(3)
		self.floor = universe.floor - universe.level.what_is_my_height(self)
		self.disturbed['count_all'] = 0
		self.locked = database.query.is_locked(universe,'accessory','shades')

	def update_all(self, cross = 30):
		level = self.universe.level
		floor = self.universe.floor - level.what_is_my_height(self)
		if self.body == self.walking:
			speed = p(5)
			if self.size[1] + self.pos[1] < floor+self.margin[2]:
				self.gforce += self.g_acceleration
				self.pos[1] += self.gforce
			else:
				self.gforce = 0
			if self.pos[1]+self.size[1] > self.floor+self.margin[2]:
					self.pos[1] = self.floor+self.margin[2] - self.size[1]		 #do not fall beyond the floor
		elif self.body  == self.flying:
			speed = p(10)
		elif self.body  == self.standing:
			speed = 0
		self.counter += 1
		if self.counter >= random.randint(50,500):
			direction = random.choice(['left','right'])
			self.direction = direction
			self.counter =0
		towards = {'right':1,'left':-1}
		obstacle = level.floor - level.what_is_my_height(self,self.center_distance+(round(self.size[0])*towards[self.direction]))
		new_y = level.what_is_my_height(self,pos_x = int(self.center_distance + (self.speed*towards[self.direction]))+int(round(self.size[0]/2)))
		actual_y = level.what_is_my_height(self)
		obstacle = max(new_y,actual_y)-min(new_y,actual_y)
		if obstacle >= cross:
#				self.center_distance -= (self.speed*towards[self.direction])
			self.direction = utils.reverse(self.direction)
		if self.direction == 'left':
			self.speed = p(speed)*-1
			self.image = self.body.left[self.body.number]
		else:
			self.speed = p(speed)
			self.image = self.body.right[self.body.number]
		if self.disturbed['count'] < 3:
			self.body = self.walking
		if self.disturbed['count'] == 3:
			self.counter = 0
			self.disturbed['spot'] = (self.pos[0],(self.universe.floor - (level.princesses[0].size[1]/2)))
			self.body = self.flying
		if self.rect.colliderect(level.princesses[0].rect):
			if not self.disturbed['ongoing']:
				self.disturbed['count'] += 1
				if self.disturbed['count_all']>=0:
					self.disturbed['count_all']+=1
				self.disturbed['ongoing'] = True
		else:
			self.disturbed['ongoing'] = False
		if self.original:
			self.body.update_number()
		self.floor = self.universe.floor - level.what_is_my_height(self)
		self.center_distance += self.speed
		if self.body == self.flying:
			height = random.randint(-5,10)
			height = p(height)
			self.pos[1] -= height
		self.pos[0] = self.universe.center_x + self.center_distance
		self.rect = pygame.Rect((self.pos[0]+self.size[0],self.pos[1]),self.size)
		if self.disturbed['count_all']>20:
			self.disturbed['count_all']=-1
			if self.locked:
				level.unlocking = {'type':'accessory','name':'shades'}


class Hawk():
	music = None 
	def __init__(self, pos, universe, bird):
		self.music = self.music or {'sound': pygame.mixer.Sound(os.path.join(directory.music,'hawk.ogg')),
			'weight': 2,
			'playing':False} 
		self.bird = bird
		self.center_distance = pos[0]
		self.flying	 = utils.img.There_and_back_again(os.path.join(directory.enemies,'Hawk','fly'))
		self.attacking   = utils.img.TwoSided(os.path.join(directory.enemies,'Hawk','attack'))
		self.body	   = self.attacking
		self.image	  = self.body.left[0]
		self.universe	  = universe
		self.size	   = [(self.image.get_width()/3),(self.image.get_height())]
		self.real_size = self.image.get_size()
		self.pos		= [self.universe.center_x+ self.center_distance, p(20)]
		self.direction  = 'left'
		self.disturbed  = 0
		self.image_number = 0
		self.speed = p(15)
		self.rect = pygame.Rect((self.pos[0]+self.size[0],self.pos[1]),self.size)
		self.mood   = 'calm'

	def update_all(self):
		if self.direction == 'left':
			self.speed = -p(30)
			self.image = self.body.left[self.body.number]
		else:
			self.speed = p(30)
			self.image = self.body.right[self.body.number]
		self.body = self.attack if self.bird.disturbed <= 3 else self.flying
		if self.bird.disturbed['count'] == 3:
			self.mood = 'angry'
		if self.mood == 'angry':
			self.center_distance += self.speed
			if self.bird.disturbed['spot'][0] > self.pos[0]:
				self.direction='right'
			else:
				self.direction = 'left'
			if 0 < self.pos[0] < self.universe.width:
				if self.pos[1] <  self.bird.disturbed['spot'][1]:
					self.pos[1] += p(15)
			if self.rect.colliderect(self.universe.level.princesses[0].rect):
				self.mood = 'revanged'
				self.bird.disturbed['count'] = 0
			if self.pos[1] > self.bird.pos[1] - (self.universe.level.princesses[0].size[1]/2):#self.level.universe.floor - int(round(350*scale)):
#			elif self.rect.collidepoint(self.bird.disturbed['spot']):
				self.mood = 'calm'
				self.bird.disturbed['count'] = 0
		elif self.mood == 'revanged':
			self.center_distance += int(self.speed*0.6)
			if -self.size[1] < self.pos[1]:
				self.pos[1] -= p(6)
			else:
				self.mood = 'calm'
		if self.mood == 'calm':
			self.center_distance += (self.speed*.5)
			if self.center_distance > self.bird.center_distance + p(1000):
				self.direction = 'left'
			elif self.center_distance < self.bird.center_distance -p(1000):
				self.direction = 'right'
			if self.pos[1]>0:
				self.pos[1] -= p(30)
		self.pos[0] = self.universe.center_x + self.center_distance
		self.rect = pygame.Rect((self.pos[0]+self.size[0],self.pos[1]),self.size)
		self.body.update_number()
