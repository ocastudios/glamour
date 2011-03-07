# -*- coding: utf-8 -*-
import pygame
import random
import interface.random_names as random_names
import os
import re
import utils
import settings.directory as directory
from settings import *


channel = pygame.mixer.Channel(0)
class Button():
	click = pygame.mixer.Sound(main_dir+'/data/sounds/click.ogg')
	def __init__(self,universe,dirtxt,position, level_pos,function,parameter = None,invert = False,fonte='Domestic_Manners.ttf', second_font = 'Chopin_Script.ttf', font_size=40, color=(0,0,0)):
		"""Creates a clickable button

		dirtxt: if image button than directory, if text button, than text.
		function: a button function is necessary.
		parameter: a string or tuple with the needed parameters for the button function.
		fonte, font_size and color: only useful to image buttons.
		"""
		self.universe = universe
		self.level_pos = level_pos
		self.font_size  = int(font_size*scale)
		try:
			os.listdir(dirtxt)
			self.type_of_button = 'image'
		except:
			self.type_of_button = 'text'

		if self.type_of_button == 'image':
			self.images	 = utils.img.Buttons(dirtxt,5)
			if invert:
				self.images.list = self.invert_images(self.images.list)
			self.list_of_images = self.images.list
		if self.type_of_button == 'text':
			font_size  = int(font_size*scale)
			font	   = fonte
			self.text	   = dirtxt
			self.color	  = color
			self.fontA	  = pygame.font.Font(os.path.join(directory.fonts,fonte),self.font_size)
			self.fontB	  = pygame.font.Font(os.path.join(directory.fonts,second_font),self.font_size+(self.font_size/3))
			self.list_of_images= [self.fontA.render(self.text,1,self.color)]

		self.image	  = self.list_of_images[0]
		self.size	   = self.image.get_size()
		self.position   = p(position)
		self.pos		= [(self.position[0]-(self.image.get_size()[0]/2)),
						   (self.position[1]-(self.image.get_size()[1])/2)]
		self.rect	   = pygame.Rect(self.pos,self.size)
		self.function   = function
		self.parameter  = parameter

	def update_all(self):
		self.size	   = self.image.get_size()
		try:
			self.pos		= [self.level_pos[0]+self.position[0]-(self.size[0]/2),
							   self.level_pos[1]+self.position[1]-(self.size[1]/2)]
		except:
			pass
		self.rect	   = pygame.Rect(self.pos,self.size)
		self.click_detection()

	def invert_images(self,list):
		inv_list=[]
		for img in list:
			inv = pygame.transform.flip(img,1,0)
			inv_list.append(inv)
		return inv_list

	def click_detection(self):
		if (self.rect.collidepoint(self.universe.pointer.mouse_pos) and self.universe.pointer.type == 2) or (self.rect.colliderect(self.universe.pointer.rect) and self.universe.pointer.type == 1):
			try:
				self.image = self.list_of_images[self.images.itnumber.next()]
			except:
				pass
			if self.type_of_button=="text":
				self.image = self.fontB.render(self.text,1,self.color)
			if self.universe.click:
				channel.play(self.click)
				if self.parameter:
					if self.parameter.__class__ in (tuple, list):
						exec("self.function("+str(self.parameter)[1:-1]+")")
				else:
					self.function()
		else:
			if self.image != self.list_of_images[0]:
				try:
					self.image = self.images.list[self.images.itnumber.next()]
				except: pass
			if self.type_of_button=="text":
				self.image = self.fontA.render(self.text,1,self.color)


class GameText():
	def __init__(self, universe, text,pos,frame_pos =None,fonte='Domestic_Manners.ttf', font_size=40, color=(58,56,0),second_font = 'Chopin_Script.ttf',var = False, rotate = None, box = None):
		font_size  = int(round(font_size*scale))
		pos = p(pos)
		self.font	   = fonte
		
		if frame_pos:
			self.frame_pos	= frame_pos
		else:
			self.frame_pos = None
		self.text	   = text
		self.color	  = color
		self.fontA	  = pygame.font.Font(main_dir+'/data/fonts/'+fonte,font_size)
		self.fontB	  = pygame.font.Font(main_dir+'/data/fonts/'+second_font,font_size+(font_size/3))
		self.position   = pos
		if box:
			self.box	= pygame.Surface(p(box), pygame.SRCALPHA).convert_alpha()
			self.adjusting_fonts()
			self.image  = self.box
			self.size	   = self.image.get_size()
			self.pos		= [self.position[0]-(self.size[0]/2),
							   self.position[1]-(self.size[1]/2)]


		else:
			self.image	  = self.fontA.render(self.text,1,self.color)
			if rotate:
				try:
					self.image = pygame.transform.rotate(self.image,rotate)
				except:
					print "the rotate parameter must be a number"
			self.size	   = self.image.get_size()
			if self.frame_pos:
				self.pos		= [self.frame_pos[0]+self.position[0]-(self.size[0]/2),
								   self.frame_pos[1]+self.position[1]-(self.size[1]/2)]
			else:
				self.pos = pos

		self.variable_text = var
		self.text_box   = self.size[0]*.8,self.size[1]*.8

	def update_all(self):
		if self.frame_pos:
			self.pos		= [self.frame_pos[0]+self.position[0]-(self.size[0]/2),
							   self.frame_pos[1]+self.position[1]-(self.size[1]/2)]
		if self.variable_text:
			self.image = self.fontA.render(self.text,1,self.color)

	def adjusting_fonts(self):
#		print "Adjusting text: "+u(str(self.text))
		fix_x	   = int(0*scale)
		fix_y	   = int(0*scale)
		font_object = self.fontA
		box = self.box
		text_box	= self.box.get_size()
		text_list = self.text.split()
		number_of_words = len(text_list)
		count = 0
		height = fix_y
		first = True
		line = ""
		line_break  = False
		while count < number_of_words:
			line		+= text_list[count]
			line_size   = font_object.size(line)
			line_pos = int((text_box[0]+fix_x-line_size[0])/2)
			if line_size[0] < text_box[0]:
				if count+1 < number_of_words:
					temporary_line = line + ' '+ text_list[count+1]
					if font_object.size(temporary_line)[0] >= text_box[0]:
						line_image = font_object.render(line,1, self.color)
						height += int((line_size[1]*.8))
						box.blit(line_image, (line_pos,height))
						line = ""
					else:
						line += ' '
				elif count+1 == number_of_words:
					height += int((line_size[1]*.8))
					box.blit(font_object.render(line, 1, self.color), (line_pos,height))
			else:
				line = text_list[count]
				height += int(line_size[1]*.8) #If line height is perfect it does not seem that it is the same text
			count += 1



class Letter(GameText):
	hoover = False
	def __init__(self,universe,text,pos,frame_pos,hoover_size,fonte='Domestic_Manners.ttf',font_size=20, color=(83,0,0)):
		self.universe = universe
		font_size = int(font_size*scale)
		GameText.__init__(self,universe, text,pos,frame_pos,fonte,font_size,color)
		self.hoover_size = hoover_size
		self.size = p((30,30))
		
		self.rect = (self.pos,self.size)

	def update_all(self):
		self.size	   = self.image.get_size()
		self.pos		= [self.frame_pos[0]+self.position[0]-(self.size[0]/2),
						   self.frame_pos[1]+self.position[1]-(self.size[1]/2)]
		self.rect	   = pygame.Rect(self.pos,self.size)
		self.type	   = type
		self.click_detection()

	def click_detection(self):
		if -.5< self.universe.level.speed < .5:
			mouse_pos = pygame.mouse.get_pos()
			if self.rect.collidepoint(mouse_pos):
				self.hoover = True
####################################### BUTTON ACTION ########################################
				if self.universe.click:
					self.universe.level.princess.name.text += self.text
			else:
				self.hoover = False


class Key(GameText):
	hoover = False
	def __init__(self,universe, text,pos,frame_pos,key_type):
		self.universe = universe
		GameText.__init__(self,universe, text,pos,frame_pos,fonte='GentesqueRegular.otf',font_size=30, color=(83,0,0))
		self.key = key_type


	def update_all(self):
		self.size	   = self.image.get_size()
		self.pos		= [self.frame_pos[0]+self.position[0]-(self.size[0]/2),
						   self.frame_pos[1]+self.position[1]-(self.size[1]/2)]
		self.rect	   = pygame.Rect(self.pos,self.size)
		self.click_detection()

	def click_detection(self):
		menu = self.universe.level
		if -.5< menu.speed < .5:
			mouse_pos = pygame.mouse.get_pos()
			if self.rect.collidepoint(mouse_pos):
				self.hoover = True
				if self.universe.click:
					if   self.key == 'Spacebar':
						menu.princess.name.text += ' '
					elif self.key == 'Backspace':
						menu.princess.name.text = menu.princess.name.text[:-1]
					elif self.key == 'Cleanup':
						menu.princess.name.text = ""
						
						
#Alteracao nao testada
					elif self.key == 'Random':
						menu.princess.name.text = random.choice(random_names.names)
						saved_games = os.listdir(main_dir+'/data/saves')
						counting = 0
						while menu.princess.name.text in saved_games:
							print "Oh, oh, this name is taken. I'd better choose another one for u"
							counting += 1
							menu.princess.name.text = random.choice(random_names.names)
							if counting >500:
								break
			else:
				self.hoover = False



