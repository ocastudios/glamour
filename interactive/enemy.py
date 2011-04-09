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
	music   = {'sound':pygame.mixer.Sound(os.path.join(directory.music,'schnauzer.ogg')), 'weight':5}
	bow	 = pygame.mixer.Sound(os.path.join(directory.enemies,'Schnauzer_bark.ogg'))
	def __init__(self, pos, universe,margin=p([20,20,20,20]),dirty=False):
		print "Creating Schnauzer..."
		self.center_distance = pos
		for i in ['kissed','walk','stay']:
			self.__dict__[i] = utils.img.TwoSided(os.path.join(directory.enemies,'Schnauzer',i))
		self.image = self.walk.left[0]
		self.size = self.image.get_size()#(self.image.get_width()/2, self.image.get_height())
		self.real_size = self.size
		self.universe = universe
		self.speed = p(16)
		self.floor = self.universe.floor-self.universe.level.what_is_my_height(self)
		self.margin = margin
		self.pos = [self.universe.center_x+self.center_distance,self.floor+self.margin[2]-(self.size[1])]
		self.count = 0
		self.move = True
		self.direction = 'left'
		self.rect = pygame.Rect(((self.pos[0]+int(self.size[0]/2.8)),self.pos[1]),(self.size[0]-int(self.size[0]/2.8),self.size[1]))
		self.gotkissed = 0
		self.image_number = 0
		self.barfing = 0
		self.lookside = 0
		self.beaten = database.query.is_beaten(self.universe,'schnauzer')
		print "Done."

	def barf(self):
		if self.barfing == 1:
			self.bow.play()
		if self.rect.collidepoint(self.universe.pointer.mouse_pos) and self.barfing == 0 or self.barfing:
			self.barfing += 1
		if self.barfing > 100:
			self.barfing = 0

	def set_pos(self,cross = 30):
		towards = {'right':1,'left':-1}
		if self.move:
			if self.direction == 'left':
				new_y = self.universe.level.what_is_my_height(self,pos_x=int(self.center_distance+(self.speed*towards[self.direction])))
			else:
				new_y = self.universe.level.what_is_my_height(self,pos_x=int(self.center_distance+(self.speed*towards[self.direction])+self.size[0]))
			actual_y = self.universe.level.what_is_my_height(self)
			obstacle = max(new_y,actual_y)-min(new_y,actual_y)
			if obstacle >= cross:
				print "obstacle found"
				print obstacle
				print new_y
				print cross
				self.direction = utils.reverse(self.direction)
			self.center_distance += (self.speed*towards[self.direction])
		self.floor = self.universe.floor - self.universe.level.what_is_my_height(self)
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

		if -p(400) < self.pos[0] < p(1500):
			self.set_image()
			if princess.kiss['rect'] \
			and self.rect.colliderect(princess.kiss['rect']):
				self.gotkissed += 1
				self.move = False
				if not self.beaten:
					database.update.beat_enemy(self.universe, 'schnauzer')
					self.beaten = True
					if database.query.beaten_enemies(self.universe)>=5:
						self.universe.level.unlocking={'type':'dress','name':'yellow'}
		if self.gotkissed != 0:
			self.gotkissed += 1
			if self.gotkissed > 250:
				self.gotkissed = 0
				self.move = True

	def set_image(self):
		if self.gotkissed >=1:
			images = self.kissed
			self.move = False
			self.image = self.kissed.__dict__[self.direction][images.number]
		else:
			images = self.walk
			if self.move:
				self.image = images.__dict__[self.direction][images.number]
			else:
				if self.lookside % 2 == 0:
					self.image = images.right[0]
				else:
					self.image = images.left[0]
		images.update_number()



class Carriage():
	music = {'sound':pygame.mixer.Sound(os.path.join(directory.music,'carriage.ogg')),
			'weight':6,
			'playing':False}

	def __init__(self, pos, universe,margin=p([10,10,10,10]),dirty=False):
		print "Creating Carriage..."
		self.center_distance = pos
		for i in ['walk','stay']:
			self.__dict__[i] = utils.img.TwoSided(os.path.join(directory.enemies,'Carriage',i), margin)
		self.image = self.walk.left[0]
		full_width = self.image.get_width()
		self.correction = full_width/5
		self.size = (full_width-self.correction, self.image.get_height())
		self.real_size = self.image.get_size()
		self.universe = universe
		self.speed = p(3)
		self.floor = self.universe.floor-p(192,r=0)
		self.margin = margin
		self.pos = [self.universe.center_x+self.center_distance,self.floor+self.margin[2]-(self.size[1])]
		self.count = 0
		self.move = True
		self.direction = random.choice(['left','right'])
		self.rect = pygame.Rect((self.pos[0]+self.correction,(self.universe.level.floor-self.pos[1])),(self.size))
		self.gotkissed = 0
		self.image_number = 0
		self.locked = database.query.is_locked(self.universe,'dress','kimono')
		print "done."

	def update_all(self):
		self.move = True
		self.set_pos()
		self.set_image()

	def set_pos(self):
		self.pos = [self.universe.center_x + self.center_distance,
					self.floor+self.margin[2]-(self.size[1])]
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
	music = {'sound':pygame.mixer.Sound(os.path.join(directory.music,'butterfly.ogg')),
			'weight':1,
			'playing':False}
	walk = utils.img.TwoSided(os.path.join(directory.enemies,'Butterfly','walk'))
	_registry = []
	def __init__(self, pos, universe,margin=p([10,10,10,10]),dirty=False):
		print "Creating Butterfly"
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
		self.pos = [self.center_distance,self.height+(self.size[1]/4)]
		self.direction = random.choice(['left','right'])
		self.rect = pygame.Rect(((self.pos[0]+(self.size[0]/4)),(self.universe.level.floor-self.pos[1]+(self.size[1]/4))),(self.size))
		self.gotkissed = 0
		print "done."

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
		self.image = self.walk.__dict__[self.direction][self.walk.number]
		if self._registry[0] == self:
			self.walk.update_number()
		if self.pos[0] > p(10000):
			self.direction = 'left'
		elif self.pos[0] < 0:
			self.direction = 'right'


class OldLady():
	music = {'sound':pygame.mixer.Sound(os.path.join(directory.music,'old_lady.ogg')),
			 'weight':3}
	
	def __init__(self, pos, universe,margin=p([10,10,10,10]),dirty=False):
		print "Creating Old Lady"
		self.center_distance = pos
		self.walk   = utils.img.TwoSided(os.path.join(directory.enemies,'OldLady','walk'),margin)
		self.wave   = utils.img.There_and_back_again(os.path.join(directory.enemies,'OldLady','hover'),margin)
		self.broom  = utils.img.There_and_back_again(os.path.join(directory.enemies,'OldLady','act'),margin)
		self.image  = self.walk.left[0]
		self.mouseovercount = 0
		self.size   = (self.image.get_width()/2, self.image.get_height())
		self.real_size = self.image.get_size()
		self.universe  = universe
		self.speed  = p(2)
		self.floor  = self.universe.floor-self.universe.level.what_is_my_height(self)
		self.margin = margin
		self.pos = [self.universe.center_x+self.center_distance,self.floor+self.margin[2]-(self.size[1])]
		self.decide = False
		self.count = 0
		self.direction = 'left'
		self.action = 'walk'
		self.rect = pygame.Rect(((self.pos[0]+(self.size[0]/2)),(self.universe.level.floor-self.pos[1])),(self.size))
		self.image_number = 0
		self.universe.level.enemies.append(BroomingDust(self))
		self.beaten = database.query.is_beaten(self.universe,'old_lady')
		print "done."

	def update_all(self):
		if -p(400) < self.pos[0] < p(1490):
			self.wave_to_princess()
			self.brooming()
			self.set_image()
		self.set_pos()

	def wave_to_princess(self):
		if self.action != 'wave':
			if self.rect.collidepoint(self.universe.pointer.mouse_pos):
				self.action = 'wave'
				self.image_number = 0
				self.count = 0
				if not self.beaten:
					database.update.beat_enemy(self.universe, 'old_lady')
					self.beaten = True
					if database.query.beaten_enemies(self.universe)>=5:
						self.universe.level.unlocking={'type':'dress','name':'yellow'}
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
		self.floor = self.universe.floor - self.universe.level.what_is_my_height(self)
		self.pos = [self.universe.center_x + self.center_distance, self.floor+self.margin[2]-(self.size[1])]

		if self.action == 'walk':
			if self.direction == 'right':
				self.center_distance += self.speed
				next_height = self.universe.level.what_is_my_height(self)
				if (self.universe.floor - next_height)  <= (self.floor-self.size[1])-30:
					self.center_distance += self.speed
			else:
				self.center_distance -= self.speed
				next_height = self.universe.level.what_is_my_height(self)
				if (self.universe.floor - next_height)  <= (self.floor-self.size[1]) -30:
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
		print 'Creating the Brooming Dust'
		self.lady		   = lady
		self.universe	  = lady.universe
		self.center_distance= lady.center_distance
		self.images		 = utils.img.TwoSided(os.path.join(directory.enemies,'OldLady','dirt'))
		self.image		  = self.images.left[0]
		self.size		   = (self.images.left[0].get_width(),self.images.left[0].get_height())
		self.real_size	  = self.images.left[0].get_size()
		self.pos			= [self.lady.pos[0]-p(194), self.lady.pos[1]+p(38)]
		self.direction	  = lady.direction
		self.rect_list	  = ( 
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
				self.pos		 = [self.lady.pos[0]-p(194), self.lady.pos[1]+p(38)]
				self.image = self.images.left[self.images.number]
				rect_pos = (self.pos[0]+self.rect_list[self.images.number]['pos'][0],  self.pos[1]+self.rect_list[self.images.number]['pos'][1])
			else:
				self.pos		 = [self.lady.pos[0]+p(144), self.lady.pos[1]+p(38)]
				self.image = self.images.right[self.images.number]
				rect_pos = (self.pos[0]+p(144)-self.rect_list[self.images.number]['pos'][0],  self.pos[1]+self.rect_list[self.images.number]['pos'][1])
			rect_rect		= self.rect_list[self.images.number]['size']
			self.rect		   = pygame.Rect(rect_pos, rect_rect)
			self.images.update_number()
		else:
			self.direction  = self.lady.direction
			self.rect	   = ((0,0),(0,0))
			self.image	  = None


class Lion():
	music = None
	def __init__(self, universe):
		print "Creating Lion"
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
		self.channel4	   = pygame.mixer.Channel(4)
		self.locked = database.query.is_locked(self.universe,'face','indian')
		self.beaten = database.query.is_beaten(self.universe,'lion')
		print "done."

	def update_all(self):
		if -p(400) < self.pos[0] < p(1490):
			if self.action == "dance":
				self.base.update_number()
				self.image = self.base.left[self.base.number]
				if self.base.number == 0:
					if random.randint(1,6) == 1:
						self.action = 'growl'
			if self.action == 'growl':
				if self.growl.number == 2:
					self.universe.level.princesses[0].status["scared"] = 1
					self.universe.level.princesses[0].status["danger"] = self.center_distance
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

			if self.universe.level.princesses[0].kiss['rect']\
			and self.rect.colliderect(self.universe.level.princesses[0].kiss['rect']):
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
		print "Creating Lion's tail"
		self.lion = lion
		self.pos  = self.lion.pos
		self.images = utils.img.There_and_back_again(os.path.join(directory.enemies,'Lion','tail'))
		self.image = self.images.list[self.images.itnumber.next()]

	def update_all(self):
		if 0 < self.pos[0] < p(700):
			self.image = self.images.list[self.images.itnumber.next()]
		self.pos  = self.lion.pos

class Elephant():
	music = None
	def __init__(self, universe):
		print "Creating Elephant"
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
		print "done."

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
		self.pos
		self.pos[0] = self.universe.center_x + self.center_distance


class Giraffe():
	music = None
	def __init__(self,universe):
		print "Creating Giraffe"
		self.center_distance = p(3800,r=0)
		ordered_directory_list = (os.path.join(directory.enemies,'giraffe','base'),
								  os.path.join(directory.enemies,'giraffe','chew'))
		self.chewing_images = utils.img.MultiPart(ordered_directory_list)
		self.hover_images   = utils.img.TwoSided(os.path.join(directory.enemies,'giraffe','hover'))
		self.image		  = self.chewing_images.left[0]
		self.universe		  = universe
		self.pos			= [self.universe.center_x+self.center_distance, (self.universe.level.floor - self.image.get_height())]
		self.direction = random.choice(['left','right'])
		self.image_number = 0
		self.count = 0
		print "done."

	def update_all(self):
		if -p(400) < self.pos[0] < p(1490):
			if self.count   == 2:
				self.image  = self.chewing_images.left[self.chewing_images.itnumber.next()]
				self.count  = 0
			self.count	  += 1
		self.pos[0]	 = self.universe.center_x + self.center_distance



class Penguin():
	music = None
	def __init__(self, universe):
		print "Creating Penguin"
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
		print "done."

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
						print "That's it"
					else:
						self.count['jumps']=0
						print "C'mon, jump with me..."
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
		print "Creating Monkey"
		self.center_distance = p(3500,r=0)
		for i in ['stay','hover','happy','throw','attack']:
			self.__dict__[i] = utils.img.TwoSided(os.path.join(directory.enemies,'Monkey',i))
		self.direction = random.choice(['right','right'])
		self.image = self.stay.__dict__[self.direction][0]
		self.size = self.stay.size
		self.real_size = self.size
		self.universe = universe
		self.pos = [self.universe.center_x+self.center_distance, p(150)]

		self.gotkissed = 0
		self.image_number = 0
		self.action = 'stay'
		self.banana = Banana(universe,self)
		self.universe.level.enemies.append(self.banana)
		print "done."

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
		print "Creating banana"
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
				self.image = self.images['throwing'].__dict__[self.monkey.direction][self.images['throwing'].number]
				self.images['throwing'].update_number()
				if self.images['throwing'].number == 3 or self.monkey.throw.number == 10:
					self.status = 'thrown'
					self.images['throwing'].number = 0
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
			if self.speed['actual'] < 0:
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

	music = {'sound':pygame.mixer.Sound(os.path.join(directory.enemies,'viking_ship.ogg')),
			 'weight':5}
	def __init__(self, pos, universe):
		print "Creating Viking Ship"
		self.universe = universe
		self.base = utils.img.TwoSided(os.path.join(directory.enemies,'VikingShip','base'))
		sailor_body = utils.img.image(os.path.join(directory.enemies,'VikingShip','viking_sailor','body','0.png'))
		left_sailor = utils.img.invert_images([sailor_body])

		for i in self.base.left:
			i.blit(sailor_body,(p(253),p(635)))
		for i in self.base.right:
			i.blit(left_sailor[0], (p(490),p(639)))
		del sailor_body, left_sailor

		D = {
			'right':{
				'center_distance': p(40, r=0),
				'flag_pos': 650,
				'wave_pos': 200,
				'head':  (476,518),
				'talk':  (650,400),
				'shout': (650,400)
			},
			'left':{
				'center_distance':p(9000, r=0),
				'flag_pos':400,
				'wave_pos':200,
				'head':  (262,518),
				'talk':  (-90,400),
				'shout': (-90,400)
			}
		}

		self.direction = random.choice(['right','left'])
		self.center_distance = D[self.direction]['center_distance']
		self.image = self.base.__dict__[self.direction][0]
		self.height = itertools.cycle(range(20)+ range(20)[-1:0:-1])
		self.image_height = self.image.get_height()
		self.pos = [self.universe.center_x+self.center_distance, self.universe.level.floor - self.image_height + p(200) +self.height.next()]
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
		self.talk_balloon = VikingPart(self, 'talk_balloon',
										pos_x = D[self.direction]['talk'][0],
										pos_y = D[self.direction]['talk'][1])
		self.shout_balloon= VikingPart(self, 'shout_balloon',
										pos_x = D[self.direction]['shout'][0],
										pos_y = D[self.direction]['shout'][1])

		self.mood  = "normal"
		self.head  = self.head_list[self.mood]
		self.count = 0
		self.curses  = [Curse(self,i) for i in range(7)]
		self.curse_number = [random.randint(0,6),random.randint(0,6),random.randint(0,6)]
		self.sailor_rect = pygame.Rect(self.head.pos,self.head.size)
		self.talk_balloon_rect = pygame.Rect(self.talk_balloon.pos,self.talk_balloon.size)
		self.balloon_curses = []
		self.beaten = database.query.is_beaten(self.universe,'viking_ship')
		print "done."

	def update_all(self):
		#take the balloon off the way, for it hurts the princess
		#if self.mood is talk it will be reset below
		self.talk_balloon.pos = p(-1000),p(-1000)
		self.talk_balloon_rect	= pygame.Rect(self.talk_balloon.pos,self.talk_balloon.size)
	
		if -p(1000) < self.pos[0] < p(1800): #check if Viking is on screen
			if self.wave not in self.universe.level.floor_image:
			
				self.universe.level.floor_image.extend([self.flag,self.wave,self.head])
			else:
				self.head = self.head_list[self.mood] # change faces acording to the mood
				self.universe.level.floor_image[-1] = self.head
			self.count += 1

			if self.mood == "normal":
				#on normal mood Viking does nothing
				#check if mood should be changed
				self.check_mood_talking()
				self.check_mood_hover()
				self.check_mood_angry()

			elif self.mood == "hover":
				if self.count > 40:
					self.mood = "normal"
					self.count = 0

			elif self.mood == "talk":
				self.talk_balloon_rect	= pygame.Rect(self.talk_balloon.pos,self.talk_balloon.size)
				self.talk_balloon.pos	= self.pos[0]+self.talk_balloon.pos_x,self.pos[1]+self.talk_balloon.pos_y
				#The balloon and the curses must appear over the boat
				#But the last floor listing position is used by the sailor head
				#That is why the ballon and curses will be placed on the panel list
				for i in self.universe.level.panel:
					if i.__class__ == Curse:
						if self.direction == 'left':
							i.pos = (self.pos[0]+i.position[0],self.pos[1]+i.position[1])
						else:
							i.pos = (self.pos[0]+p(800)+i.position[0],self.pos[1]+i.position[1])
						if i not in self.balloon_curses:
							self.universe.level.panel.remove(i)
							i.pos = (-p(100),i.position[1])
				if self.count > 60:
					for i in self.balloon_curses:
						self.universe.level.panel.remove(i)
						i.pos = p([-400,-400])
					self.balloon_curses = []
					self.curse_number = (random.randint(0,6),random.randint(0,6),random.randint(0,6))
					self.mood = "normal"
					self.count = 0

			elif self.mood == "angry":
				self.shout_balloon.pos = self.pos[0]+self.shout_balloon.pos_x,self.pos[1]+self.shout_balloon.pos_y
				for i in self.universe.level.panel:
					if i.__class__ == Curse:
						for i in self.universe.level.panel:
							if i.__class__ == Curse:
								if self.direction == 'left':
									i.pos = (self.pos[0]+i.position[0]-p(80),self.pos[1]+i.position[1]+p(70))
								else:
									i.pos = (self.pos[0]+p(800)+i.position[0]+p(80),self.pos[1]+i.position[1]+p(70))
						if i not in self.balloon_curses:
							self.universe.level.panel.remove(i)
							i.pos = (-p(100),i.position[1])
				if self.count > 60:
					for i in self.balloon_curses:
						self.universe.level.panel.remove(i)
						i.pos = p([-400,-400])
					self.balloon_curses = []
					self.curse_number = (random.randint(0,6),random.randint(0,6),random.randint(0,6))
					self.mood = "normal"
					self.count = 0
		#while not on screen Viking should only update position.
		self.moving()


	def moving(self):
		if self.direction == "left":
			self.center_distance -= self.speed
		else:
			self.center_distance += self.speed
		self.pos[0] = self.universe.center_x + self.center_distance
		self.pos[1] = self.universe.level.floor - self.image_height + p(200) + self.height.next()
		self.sailor_rect = pygame.Rect(self.head.pos,self.head.size)
		self.flag.pos = self.pos[0]+(self.flag.pos_x-self.flag.size[0]),self.pos[1]+self.flag.pos_y
		self.wave.pos = self.pos[0]+(self.wave.pos_x-self.wave.size[0]),self.universe.level.floor_image[-5].pos[1]-(self.wave.size[1]-p(20))
		self.head.pos = self.pos[0]+self.head.pos_x,self.pos[1]+self.head.pos_y

	def check_mood_talking(self):
		if self.count > 100 \
		and random.randint(0,20) == 0:
			self.mood = "talk"
			self.balloon_curses = [self.talk_balloon]+[self.curses[self.curse_number[i]] for i in (0,1,2)]
			self.universe.level.panel.extend(self.balloon_curses)
			for i,pos in [(0,-70), (1,10), (2,90)]:
				self.curses[self.curse_number[i]].position[0] = p(pos)
			self.talk_balloon.pos = self.pos[0]+self.talk_balloon.pos_x,self.pos[1]+self.talk_balloon.pos_y
			for i in self.universe.level.panel:
				if i.__class__ == Curse:
					if self.direction == 'left':
						i.pos = (self.pos[0]+i.position[0],self.pos[1]+i.position[1])
					else:
						i.pos = (self.pos[0]+p(800)+i.position[0],self.pos[1]+i.position[1])
			self.count = 0

	def check_mood_hover(self):
		if self.sailor_rect.collidepoint(self.universe.pointer.mouse_pos):
			if not self.beaten:
				database.update.beat_enemy(self.universe, 'viking_ship')
				self.beaten = True
				if database.query.beaten_enemies(self.universe)>=5:
					self.universe.level.unlocking={'type':'dress','name':'yellow'}
			self.mood = "hover"
			self.count = 0

	def check_mood_angry(self):
		if self.universe.level.princesses[0].kiss \
		and self.sailor_rect.colliderect(self.universe.level.princesses[0].kiss['rect']):
			self.universe.stage.princesses[0].get_dirty()
			print "got you"
			self.mood = "angry"
			self.balloon_curses = [self.shout_balloon]+[self.curses[self.curse_number[i]] for i in (0,1,2)]
			self.universe.level.panel.extend(self.balloon_curses)
			for i,pos in [(0,-70), (1,10), (2,90)]:
				self.curses[self.curse_number[i]].position[0] = p(pos)
			self.shout_balloon.pos = self.pos[0]+self.shout_balloon.pos_x,self.pos[1]+self.shout_balloon.pos_y
			for i in self.universe.level.panel:
				if i.__class__ == Curse:
					if self.direction == 'left':
						i.pos = (self.pos[0]+i.position[0],self.pos[1]+i.position[1])
					else:
						i.pos = (self.pos[0]+p(800)+i.position[0],self.pos[1]+i.position[1])
			self.count = 0
			
class VikingPart():
	music = None
	def __init__(self, ship, part, pos_x = 0, pos_y = 0):
		print "Creating Viking part: "+part
		self.pos_x  = p(pos_x,r=False)
		self.pos_y  = p(pos_y,r=False)
		self.ship = ship
		self.pos  = self.ship.pos[0]+pos_x,self.ship.pos[1]+pos_y
		self.images = utils.img.TwoSided(os.path.join(directory.enemies,'VikingShip',part))
		if self.ship.direction == 'left':
			self.actual_images = self.images.left
		else:
			self.actual_images = self.images.right
		self.image = self.actual_images[self.images.itnumber.next()]
		self.size = self.image.get_size()
		self.real_size = self.size

	def update_all(self):
		self.image = self.actual_images[self.images.itnumber.next()]

class Curse():
	music = None
	def __init__(self,ship,index):
		print "Creating new curse"
		self.image  = utils.img.image(os.path.join(directory.enemies,'VikingShip','curses',str(index)+'.png'))
		if ship.direction =='left':
			self.pos	= p([-70,440])
			self.position = p([-70,440])
		else:
			self.pos	= p([500,440])
			self.position= p([500,440])
		print "done"

	def update_all(self):
		pass


class FootBoy():
	music = {'sound':pygame.mixer.Sound(os.path.join(directory.music,'fabrizio.ogg')),
			'weight':4,
			'playing':False}
	def __init__(self, pos, universe, dirty=False):
		print 'Creating Fabrizio'
		self.center_distance = pos
		self.running = utils.img.There_and_back_again(
						os.path.join(directory.enemies,'FootBoy','walk_body','first_cycle'),
						second_dir = os.path.join(directory.enemies,'FootBoy','walk_body','second_cycle'),
						extra_part = os.path.join(directory.enemies,'FootBoy','happy_face','first_cycle'),
						second_extra_part = os.path.join(directory.enemies,'FootBoy','happy_face','second_cycle'))
		self.running_mad = utils.img.There_and_back_again(
					os.path.join(directory.enemies,'FootBoy','walk_body','first_cycle'),
					second_dir = os.path.join(directory.enemies,'FootBoy','walk_body','second_cycle'),
					extra_part = os.path.join(directory.enemies,'FootBoy','mad_face','first_cycle'),
					second_extra_part = os.path.join(directory.enemies,'FootBoy','mad_face','second_cycle'))
		self.running_kissed = utils.img.There_and_back_again(os.path.join(directory.enemies,'FootBoy','kissed'))
		self.standing_body = utils.img.TwoSided(os.path.join(directory.enemies,'FootBoy','walk_body','stand'))
		self.body = self.running_mad
		self.image = self.body.left[0]
		self.universe = universe
		self.size = [(self.image.get_width()/3),self.image.get_height()]
		self.real_size = self.size
		self.pos = [self.universe.center_x+self.center_distance, self.universe.level.floor-self.size[1]+20]
		self.direction = random.choice(['left','right'])
		self.got_kissed = 0
		self.image_number = 0
		self.speed = -p(14)
		self.rect = pygame.Rect((self.pos[0]+self.size[0],self.pos[1]),self.size)
		self.universe.level.enemies.append(FootBall(random.randint(int(p(4000)),int(p(6000))), self))
		self.beaten = database.query.is_beaten(self.universe,'footboy')
		print "done."

	def update_all(self):
		if self.direction == 'left':
			self.speed = -p(12)
			self.image = self.body.left[self.body.number]
		else:
			self.speed = p(12)
			self.image = self.body.right[self.body.number]
		if not self.got_kissed \
		and self.universe.level.princesses[0].kiss['rect']\
		and self.rect.colliderect(self.universe.level.princesses[0].kiss['rect']):
			self.got_kissed = 1
			if not self.beaten:
				database.update.beat_enemy(self.universe, 'footboy')
				self.beaten = True
				if database.query.beaten_enemies(self.universe)>=5:
					self.universe.level.unlocking={'type':'dress','name':'yellow'}
		if self.got_kissed > 0:
			if self.got_kissed == 1:
				self.body = self.running_kissed
				print "Ooops! He, he!"
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
		print 'Creating the Ball'
		self.footboy		= footboy
		self.universe		  = footboy.universe
		self.center_distance= center_distance
		self.images		 = utils.img.TwoSided(os.path.join(directory.enemies,'FootBoy','ball'))
		self.image		  = self.images.left[0]
		self.size		   = (self.images.left[0].get_width(),self.images.left[0].get_height()-p(7))
		self.real_size	  = self.size
		self.pos			= [self.footboy.universe.center_x + self.center_distance, self.footboy.universe.level.floor - self.size[1]]
		self.speed		  = 0
		self.rect		   = pygame.Rect(self.pos, self.size)
		self.lowlist		= p((3,4,5,12,13,14))
		self.movetype	   = 'high'
		ballheights	= p([80,120,170,210,240,260,270,275])
		ballheights	+= list(reversed(ballheights))
		ballheights	 += p([1,40,70,90,95,90,70,40,1])
		ballheights	+= p([20,10,15,10,20,0])
		self.ballheights = itertools.cycle(ballheights)
		self.direction = self.footboy.direction

#itertools.cycle([i*20 for i in range(7)+list(reversed(range(6)))])


	def update_all(self):
		speed = self.speed
		if self.footboy.body != self.footboy.running:
			if self.rect.colliderect(self.footboy.rect):
				if self.footboy.body.number in self.lowlist:
					self.movetype = 'low'
				else:
					self.movetype = 'high'
					self.pos[1] += 1
				if self.footboy.direction == "left":
					self.speed = -p(50)
				else:
					self.speed = p(50)
				self.pos[1] += 1
			if self.footboy.direction == 'right' and self.pos[0] < self.footboy.pos[0]:
				self.footboy.direction = 'left'
			if self.footboy.direction == 'left' and self.pos[0]-p(400) > self.footboy.pos[0]:
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
		self.pos[0] =  self.footboy.universe.center_x + self.center_distance
		floor = (self.universe.floor - self.universe.level.what_is_my_height(self)) - (self.size[1])
		if self.pos[1] != floor:
			self.pos[1] = floor - self.ballheights.next()
		self.rect   = pygame.Rect(self.pos, self.size)

class Bird():
	music = None
	disturbed   = {'ongoing':False, 'count':0,'spot':(0,0),'count_all':0}
	flying	  = utils.img.There_and_back_again(os.path.join(directory.enemies,'Birdy','fly'))
	walking	 = utils.img.There_and_back_again(os.path.join(directory.enemies,'Birdy','walk'))
	standing	= utils.img.TwoSided(os.path.join(directory.enemies,'Birdy','stay'))
	def __init__(self, pos, universe, dirty=False, margin=p([5,5,5,5])):
		print 'Creating Bird'
		self.center_distance = int(pos+p(random.randint(3,50)))
		self.margin = margin
		self.body	   = self.walking
		self.image	  = self.body.left[0]
		self.universe	  = universe
		self.size	   = [(self.image.get_width()/3),self.image.get_height()]
		self.real_size  = self.image.get_size()
		#adjusting self.size
		self.size[1] -= p(8)
		self.pos		= [self.universe.center_x+self.center_distance, self.universe.level.floor+self.margin[2]-self.size[1]+p(10)]
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
			self.universe.level.enemies.append(Hawk((self.universe.width+int(p(600)), int(-p(300))), self.universe, self))
			self.original = True
		else:
			self.original = False
		self.gforce		 = 0
		self.g_acceleration = p(3)
		self.floor = self.universe.floor - self.universe.level.what_is_my_height(self)
		self.disturbed['count_all'] = 0
		self.locked = database.query.is_locked(self.universe,'accessory','shades')


	def update_all(self, cross = 30):
		floor = self.universe.floor - self.universe.level.what_is_my_height(self)
		if self.body	== self.walking:
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
		obstacle = self.universe.level.floor - self.universe.level.what_is_my_height(self,self.center_distance+(round(self.size[0])*towards[self.direction]))
		new_y = self.universe.level.what_is_my_height(self,pos_x = int(self.center_distance + (self.speed*towards[self.direction]))+int(round(self.size[0]/2)))
		actual_y = self.universe.level.what_is_my_height(self)
		obstacle = max(new_y,actual_y)-min(new_y,actual_y)
		if obstacle >= cross:
#				self.center_distance -= (self.speed*towards[self.direction])
			print "obstacle found"
			print obstacle
			print cross
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
			self.disturbed['spot'] = (self.pos[0],(self.universe.floor - (self.universe.level.princesses[0].size[1]/2)))
			self.body = self.flying
		if self.rect.colliderect(self.universe.level.princesses[0].rect):
			if not self.disturbed['ongoing']:
				self.disturbed['count'] += 1
				if self.disturbed['count_all']>=0:
					self.disturbed['count_all']+=1
				self.disturbed['ongoing'] = True
				print 'The little bird was disturbed ' + str(self.disturbed['count']) + ' times'
		else:
			self.disturbed['ongoing'] = False
		if self.original:
			self.body.update_number()
		self.floor = self.universe.floor - self.universe.level.what_is_my_height(self)
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
				self.universe.level.unlocking = {'type':'accessory','name':'shades'}



class Hawk():
	music = {'sound': pygame.mixer.Sound(os.path.join(directory.music,'hawk.ogg')),
			'weight': 2,
			'playing':False}
	def __init__(self, pos, universe, bird):
		print 'Creating Hawk'
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
		princess = self.universe.level.princesses[0]
		if self.direction == 'left':
			self.speed = -p(30)
			self.image = self.body.left[self.body.number]
		else:
			self.speed = p(30)
			self.image = self.body.right[self.body.number]

		if self.bird.disturbed <= 3:
			self.body = self.attack
		else:
			self.body = self.flying

		if self.bird.disturbed['count'] == 3:
			self.mood = 'angry'
			print "Hawk is now angry with you!!"

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
				print "Hawk fells revanged now..."
			if self.pos[1] > self.bird.pos[1] - (self.universe.level.princesses[0].size[1]/2):#self.level.universe.floor - int(round(350*scale)):
#			elif self.rect.collidepoint(self.bird.disturbed['spot']):
				self.mood = 'calm'
				self.bird.disturbed['count'] = 0
				print "Poor howk! It missed the attack."

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
