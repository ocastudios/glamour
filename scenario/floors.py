import utils
import pygame
import settings
import os
p = settings.p

class Floor():
	images = None

	def __init__(self,index,dir,universe,height=0):
		height = {'all':p(186+height)}
		self.universe = universe
		self.images = self.images or utils.img.OneSided(dir)
		self.image = self.images.list[self.images.number]
		self.size = self.image.get_size()
		self.center_distance = round((self.size[0])*index)
		self.set_pos()

	def set_pos(self):
		self.pos = [self.universe.center_x+(self.center_distance),self.universe.floor-self.size[1]]


	def update_all(self):
		self.pos[0] = self.universe.center_x+(self.center_distance)


class Water(Floor):
	height = p(101,r=False)
	max	= p(125,r=False)
	min	= p(95,r=False)
	speed = [2,1]
	direction = 'up'

	def set_pos(self):
		self.pos = [self.universe.center_x+(self.center_distance),self.universe.floor-self.size[1]]
	def update_all(self):
		self.center_distance += self.speed[0]
		if self.direction == 'up':
			self.height += self.speed[1]
		else:
			self.height -= self.speed[1]

		if self.height > self.max:		  self.direction = 'down'
		if self.height < self.min:		  self.direction = 'up'

		self.pos = (self.universe.center_x+(self.center_distance),self.universe.floor-self.height)
		if self.pos[0] > self.universe.width:
			self.center_distance -= self.universe.width+(self.size[0]*2)
		if self.pos[0] < -self.size[0]:
			self.center_distance += self.universe.width+(self.size[0]*2)
		if self.__class__ != Water2:
			self.universe.level.water_level = self.universe.floor-self.height


class Water2(Water):
	height = p(81)
	max =	p(90)
	min =	p(80)
	direction = 'up'
	speed = [6,1]

class Bridge():
	def __init__(self,dir,index,universe,main=True):
		if main:			self.images = utils.img.OneSided(os.path.join(dir,'main'))
		else:			   self.images = utils.img.OneSided(dir) 

		if main:
			self.left_bank = Bridge(os.path.join(str(dir),'left_bank'),index-1,universe,main = False)
			self.right_bank= Bridge(os.path.join(str(dir),'right_bank'),index+1,universe,main = False)

		self.image_number = 0
		self.image = self.images.list[0]
		self.size = self.image.get_size()
		self.universe = universe
		width = p(400,r=False)
		if main:			self.center_distance = round((width*index)-width)
		else:			   self.center_distance = round(width*index)

		self.pos = [self.universe.center_x+(self.center_distance),self.universe.floor-self.size[1]]
		if main:
			del universe.level.floor_image[index]
			universe.level.floor_image.insert(0,self)
		else:
			universe.level.floor_image[index]= self

	def update_all(self):
		self.update_pos()
	def update_pos(self):
		self.pos[0] = self.universe.center_x+self.center_distance


class Drain():
	def __init__(self,directory,index,universe):
		self.images = utils.img.OneSided(directory) 
		self.image_number = 0
		self.image = self.images.list[0]
		self.size = self.image.get_size()
		self.universe = universe
		self.center_distance = p(400)*index
		self.pos = [self.universe.center_x+(self.center_distance),int(p(900))-self.size[1]]
		universe.level.floor_image[index]= self

	def update_all(self):
		self.pos[0] = self.universe.center_x+(self.center_distance)
