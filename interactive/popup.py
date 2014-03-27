import pygame
import utils
from utils import text
import settings.directory as directory
from settings.directory import j
from settings import p
from string import Template


class Message():
	button = None
	def __init__(self, universe,font_size = 16, message = "Oops! I just forgot what I had to say... One of us should have a conversation with the programmer."):
		self.message	= message
		self.universe = universe
		self.image	  = utils.img.image(j(fairy_dir,'balloon','0.png'))
		self.size	   = self.image.get_size()
		self.pos		= ((self.universe.width - self.size[0])/2, self.universe.height - self.size[1])
		self.text_box   = self.size[0]*.8,self.size[1]*.8
		self.image.blit(text.in_box('FreeSans.ttf',font_size, self.text_box, self.image, message, margin={'left':150,'top':40,'right':150,'bottom':40}, alignment = "center"), self.pos)

	def update_all(self):
		pass
	
class Unlocking_Message():
	def __init__(self, universe,unlocking, font_size = 16):
		self.image = utils.img.image(j(directory.fairy_tips,'balloon','0.png'))
		self.universe	= universe
		self.size		= self.image.get_size()
		self.pos		= ((self.universe.width - self.size[0])/2, self.universe.height - self.size[1])
		self.text_box	= self.size[0]*.8,self.size[1]*.8
		unlock_template	= Template("you unlocked $garment_type $name")
		unlock_message	= unlock_template.substitute(garment_type=unlocking['type'],name=unlocking['name'])
		self.image.blit(text.in_box('FreeSans.ttf',font_size, self.text_box, self.image, unlock_message , margin={'left':150,'top':60,'right':150,'bottom':40}, alignment = "center"), self.pos)
	def update_all(self):
		pass

class Unlocking_Icon():
	growing = utils.img.OneSided(directory.unlocking_grow)
	running = utils.img.OneSided(directory.unlocking_run)
	def __init__(self, universe, message, unlocking):
		self.image_size = (p(212),p(212))
		self.image	  = pygame.Surface(self.image_size, pygame.SRCALPHA).convert_alpha()
		self.pos		= message.pos[0]+p(10),message.pos[1]+p(10)
		self.icon	   = utils.img.image(j(directory.princess,unlocking['type']+'_'+unlocking['name'],"big_icons","0.png"))
		self.step	   = "growing"
	def update_all(self):
		self.image	  = pygame.Surface(self.image_size, pygame.SRCALPHA).convert_alpha()
		if self.step =="growing":
			if self.growing.number <= len(self.growing.list)-1:
				self.image.blit(self.growing.list[self.growing.number],(0,0))
				self.growing.number+=1
			else:
				self.step = "running"
				self.growing.number = 0
		if self.step=="running":
			self.image.blit(self.running.list[self.running.number],(0,0))
			self.running.update_number()
			self.image.blit(self.icon,(p(41),p(41)))

