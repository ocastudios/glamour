import pygame
import utils
import utils.text
import random
import settings
from settings import directory
import interactive.messages as messages
import interface.widget	 as widget 
import os


p = settings.p
j = os.path.join
fairy_dir = j(directory.interface, 'fairy_tips')

class Fairy():
	"""This class defines the tip fairy, who helps the princess during the game."""
	whistle	 = pygame.mixer.Sound(j(directory.sounds,'story','frames','s03.ogg'))
	music	   = j(directory.music,'1stSnowfall.ogg')
	def __init__(self, pos, universe,margin=p([10,10,10,10]),dirty=False):
		self.size = p((10,10))
		self.universe = universe
		self.center_distance = pos
		self.pos =  p([-200,600])
		self.lists_of_images = {
			'mouth_speak': utils.img.TwoSided(j(fairy_dir,'fairy_speak'),margin),
			'mouth_smile': utils.img.There_and_back_again(j(fairy_dir,'fairy_smile'),margin),
			'eyes_eyes': utils.img.There_and_back_again(j(fairy_dir,'fairy_eyes'),margin),
			'eyes_blink': utils.img.There_and_back_again(j(fairy_dir,'fairy_blink'),margin),
			'wings_wings': utils.img.TwoSided(j(fairy_dir,'fairy_wings'),margin),
			'wings_fly': utils.img.TwoSided(j(fairy_dir,'fairy_fly_wings'),margin),
			'body_fly': utils.img.There_and_back_again(j(fairy_dir,'fairy_fly'),margin),
			'body_stand_right': utils.img.There_and_back_again(j(fairy_dir,'fairy_stand_right'),margin),
			'body_stand_left': utils.img.There_and_back_again(j(fairy_dir,'fairy_stand_left'),margin)
		}
		self.images_strings = ['wings_wings','body_stand_left','mouth_speak','eyes_eyes']
		self.parts	  = [self.lists_of_images[i].left[self.lists_of_images[i].number] for i in self.images_strings]
		self.size	   = self.parts[1].get_size()
		self.image	  = pygame.Surface(self.size,pygame.SRCALPHA).convert_alpha()
#		self.goalpos	= p([1200,700])
		self.direction  = "left"
		self.action	 = self.explain
		self.count	  = 0
		self.wand	   = utils.img.TwoSided(j(fairy_dir,'fairy_wand'),margin)
		self.enchant	= utils.img.TwoSided(j(fairy_dir,'fairy_enchant'),margin)
		self.spark	  = utils.img.OneSided(j(fairy_dir,'spark'),margin)
		self.reached_goal = False

	def update_all(self):
		for key,value in self.lists_of_images.items():
			value.update_number()
		self.action()

	def wait(self):
		pass

	def explain(self):
		self.select_images()
		self.image = self.update_image()
		if not self.reached_goal:
			self.fly_to_goal()
		else:
			if self.pos[0]>(self.universe.width/2):
				self.direction = "left"
				self.images_strings = ['wings_wings','body_stand_left','mouth_speak','eyes_eyes']
			else:
				self.direction = "right"
				self.images_strings = ['wings_wings','body_stand_left','mouth_speak','eyes_eyes']
	def select_images(self):
		if self.direction == "left":
			self.parts = [self.lists_of_images[i].left[self.lists_of_images[i].number] for i in self.images_strings]
		else:
			self.parts = [self.lists_of_images[i].right[self.lists_of_images[i].number] for i in self.images_strings]

	def update_image(self):
		image = pygame.Surface(self.size,pygame.SRCALPHA).convert_alpha()
		for i in self.parts:
			if i:
				image.blit(i,(0,0))
		return image

	def fly_to_goal(self):
		self.pos = p((1260,720))


class Message():
	button = None
	shut_up = None
	def __init__(self, universe, message = "Oops! I just forgot what I had to say... One of us should have a conversation with the programmer."):
		self.message	= message
		self.universe	= universe
		self.image = utils.img.image(j(fairy_dir,'balloon','0.png'))
		self.size = self.image.get_size()
		self.pos = ((universe.width - self.size[0])/2, universe.height-self.size[1])
		self.text_box = self.size[0]*.8,self.size[1]*.8
		self.text_font = pygame.font.Font(j(directory.fonts,settings.third_font),settings.fairy_font_size)
		self.color = (0,0,0,0)
		self.image.blit(utils.text.in_box(settings.third_font, settings.fairy_font_size, self.text_box, self.image, message, {'top':40,'left':80,'bottom':40,'right':80}),self.pos)
		self.button  = self.button or widget.Button(universe, directory.button_ok,(1200,820),[0,0],self.end_message)
		#self.shut_up = self.shut_up or widget.Button(universe, directory.button_cancel, (1200,850),[0,0],self.end_message)
		if self.button not in self.universe.level.fae:
			self.universe.level.fae.append(self.button)
			#self.universe.level.fae.append(self.shut_up)

	def update_all(self):
		pass

	def end_message(self):
		self.universe.level.fairy = 'done'
		self.universe.level.fae[1].pos =  p([-200,600])
		self.universe.level.fae.remove(self.button)
