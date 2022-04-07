import interactive.princess as princess
import utils
import os
from pygame.locals import *
from settings import directory
from settings import *


def p(positions):
	return [int(i*scale) for i in positions ]
	
class Glamour_Stars():
	def __init__(self,universe):
		self.universe = universe
		self.image_lists = [utils.img.OneSided(os.path.join(directory.star, 'star'+i)) for i in ('0','1','2','3')]
		self.image = self.image_lists[0].list[0]
		self.size = self.image.get_size()
		self.pos = p((195,45))

	def update_all(self):
		actual_list = self.image_lists[self.universe.level.princesses[0].dirt]
		self.image = actual_list.list[next(actual_list.itnumber)]
		
class Lil_Stars():
	def __init__(self,universe, pos):
		self.universe = universe
		self.rotating = utils.img.There_and_back_again(os.path.join(directory.interface, 'lil_star','right'), second_dir = os.path.join(directory.interface,'lil_star','left'))
		self.image = self.rotating.list[0]
		self.size = self.image.get_size()
		self.pos = p(pos)

	def update_all(self):
		self.image = self.rotating.list[next(self.rotating.itnumber)]
		
class Lil_Star_Back():
	def __init__(self,universe,pos):
		self.universe =universe
		self.image = utils.img.image(os.path.join(directory.interface,'lil_star','back.png'))
		self.pos = p(pos)
	def update_all(self):
		pass
