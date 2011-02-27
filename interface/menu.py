# -*- coding: utf-8 -*-
import utils.img
import interactive.princess as princess
import pygame
import scenario.drapes as drapes
import os	
import interface.mousepointer as mousepointer
import database.db as db
import sqlite3
import interface.widget as widget
import settings
from settings import directory
from pygame.locals import *
p = settings.p
d = settings.d # reverse of p
t = settings.t

items		  = ['texts', 'options', 'buttons']
name_taken	  = False

print "Initiating menu music."
pygame.mixer.music.load(os.path.join(directory.music,'menu.ogg'))
pygame.mixer.music.play()

class MenuScreen():
	color = [230,230,230]
	def __init__(self,universe):
		print "Creating MenuScreen"
		self.universe	   = universe
		self.bar_side	   = None
		self.bar_left	   = utils.img.image(os.path.join(directory.left_bar,'0.png'))
		self.bar_right	  = pygame.transform.flip(self.bar_left,1,0)
		self.bar			= self.bar_left
		self.bar_size	   = self.bar.get_size()
		self.bar_position   = -self.bar_size[0]
		self.menu		   = Menu(self)
		self.menu.main()
		self.speed		  = p(5,r=False)
		self.STEP		   = self.update_drape
		self.count		  = 0
		self.action		 = 'open'
		self.hoover_letter  = utils.img.image(os.path.join(directory.title_screen,'selection_letter','0.png'))
		self.hoover_letter_size = self.hoover_letter.get_size()
		self.hoover_large   = utils.img.image(os.path.join(directory.title_screen,'selection_back_space','0.png'))
		self.hoover_large_size = self.hoover_large.get_size()
		self.story_frames   = []
		self.drapes		 = drapes.Drape()
		self.upper_drapes   = drapes.UperDrape()
		self.screen		 = self.universe.screen_surface

#STEP SEQUENCE
## 1- update_drape
## 2- arrive_bar
## 3- update_menus


	def update_all(self):
		self.screen.fill(self.color)
		self.STEP(self.screen)
		self.count += 1

	def update_drape(self,surface):
		self.drapes.action=self.action
		self.drapes.update_all()
		surface.blit(self.drapes.image,(0,0))
		self.upper_drapes.action = self.action
		self.upper_drapes.update_all()
		surface.blit(self.upper_drapes.image,(0,self.upper_drapes.y))
		if self.upper_drapes.y < -self.upper_drapes.size_y+10:
			self.STEP = self.STEP_arrive_bar ## Change the STEP
			self.bar_side = 'left'
			del self.drapes
			del self.upper_drapes

	def STEP_arrive_bar(self,surface):
		if self.menu.back_background:
			surface.blit(self.menu.back_background,(0,0))
		if self.bar_side:
			surface.blit(self.bar,(self.bar_position,0))

			if self.bar_side == 'left':
				if self.bar_position < 0:
					self.bar_position += self.speed
					if self.bar_position > p(-200):
						self.speed -= .5
					else:
						self.speed += .5
				else:
					self.bar_position = 0
					self.STEP = self.update_menus ## Change the STEP
			elif self.bar_side == 'right':
				if self.bar_position <10:
					self.bar_position =  p(2000)
				if self.bar_position+p(516) > self.universe.width:
					self.bar_position -= self.speed
					if self.bar_position < int((self.universe.width-p(300))):
						self.speed += .5
					else:
						self.speed -= .5
				else:
					self.bar_position = p(924)
					self.STEP = self.update_menus ## Change the STEP

	def update_menus(self,surface):
		if self.menu.back_background:
			surface.blit(self.menu.back_background,(0,0))
		if self.menu.background:
			surface.blit(self.menu.background,self.menu.position)
		if self.bar_side:
			surface.blit(self.bar,(self.bar_position,0))
		if self.menu.story:
			self.menu.story.update_all()
			[surface.blit(i,(0,0)) for i in self.menu.story.images if i]
		if self.menu.tutorial:
			self.menu.tutorial.update_all()
			[surface.blit(i,(0,0)) for i in self.menu.tutorial.images if i]
		for item in items:
			for i in self.menu.__dict__[item]:
				i.update_all()
				surface.blit(i.image, i.pos)
		for i in self.menu.options:
			if i.__class__ == widget.Letter and i.hoover:
				surface.blit(self.hoover_letter,(i.pos[0]-((self.hoover_letter_size[0]-i.size[0])/2),
												 i.pos[1]-((self.hoover_letter_size[1]-i.size[1])/2) ))
			if (i.__class__ == widget.Key) and i.hoover:
				surface.blit(self.hoover_large,(i.pos[0]-((self.hoover_large_size[0]-i.size[0])/2),
												i.pos[1]-((self.hoover_large_size[1]-i.size[1])/2) ))
		if self.menu.print_princess:
			self.menu.princess.update_all()
			[surface.blit(i,self.menu.princess.pos) for i in self.menu.princess.images if i]
		self.menu.update_all()

		if self.action == 'open':
			self.menu.action = self.action
		else:
			if not self.menu.go_back:
				if self.menu.position[1]<p(1200):
					self.menu.action = 'close'
				else:
					self.action = 'open'
					self.STEP = self.close_bar ## Change the STEP
			else:
				if self.menu.position[1]>p(-600):
					self.menu.action = 'close'
				else:
					self.action = 'open'
					self.STEP = self.close_bar
		if self.menu.princess:
			self.menu.princess.name.text = self.menu.princess.name.text.title()

		if self.menu.credits:
			surface.blit(self.menu.credits.background,self.menu.credits.pos)
			self.menu.credits.update_all()

	def close_bar(self,surface, call_bar = 'right'):
		width = p(1440)
		if (p(-800) < self.bar_position <p(10)) or (width-self.bar_size[0] < self.bar_position < width +1):
			self.bar_position -= round(self.speed)
			self.speed += p(1,r=False)
		else:
			####### STEP #######
			if call_bar:
				self.STEP = self.STEP_arrive_bar
				if call_bar == 'right':
					self.bar_side   = "right"
				elif call_bar == 'left':
					self.bar_side = "left"
			self.action = 'open'
			self.menu.next_menu()
		if self.menu.back_background:
			surface.blit(self.menu.back_background,(0,0))
		surface.blit(self.bar,(self.bar_position,0))


class Menu():
	selection_canvas = utils.img.image(os.path.join(directory.title_screen,'selection_canvas','0.png'))
	def __init__(self,screen,position= [360,200]):
		print "Creating main menu"
		position = p([position[0],position[1]])
		self.universe	   = screen.universe
		self.screen		 = screen
		self.speed		  = p(2,r =False)
		self.goal_pos	   = position
		self.position= [position[0],p(-600)]
		self.background	 = self.selection_canvas
		self.size		   = self.background.get_size()
		self.action		 = None
		self.next_menu	  = self.select_princess
		self.print_princess = False
		self.princess	   = None
		self.story		  = None
		self.tutorial	   = None
		self.credits		= None
		self.go_back		= False
		self.back_background= None
		self.mouse_positions= []
		self.selector = 0
		self.game_mouse	 = mousepointer.MousePointer(self, type = 2)
		self.mouse_pos	  = pygame.mouse.get_pos()
		print "done."


	def main(self):
		self.print_princess = False
		self.background	 = self.selection_canvas
		self.back_background = None
		self.action = 'open'
		if not self.go_back:
			self.position[1] = p(-600)
		else:
			self.position	= [p(450),p(1000)]
		opt = ((t('New Game'),100,self.new_game),(t('Load Game'),180,self.load_game),(t('Play Story'),260,self.play_story),(t('Learn to play'),340,self.play_tutorial),(t('Credits'),420,self.play_credits))
		self.options = [ widget.Button(i[0], (300,i[1]), self, i[2], font_size=40,color = (255,84,84)) for i in opt]
		self.texts =   [ widget.GameText(t('select one'),(65,250),self, rotate=90,color = (58,56,0))]
		self.buttons = [ widget.Button(directory.arrow_right,(410,450),self,self.NOTSETYET),
						 widget.Button(directory.arrow_right,(200,450),self,self.NOTSETYET, invert = True)]

	def reset_menu(self, background = None, action = None, options = [], texts = [], buttons = []):
		self.story		  = None
		self.credits		= None
		self.screen.story_frames = []
		self.background	 = self.selection_canvas
		if background:
			self.back_background	= utils.img.image(background)
		self.action		 = action
		self.speed		  = 0
		if not self.go_back:
			print "Going Forward"
			self.position = p([450,-600])
		else:
			print "Going Back"
			self.position = p([450,1000])
		self.options		= options
		self.texts		  = texts
		self.buttons		= buttons

	def select_princess(self):
		self.screen.bar = self.screen.bar_right
		self.princess	   = MenuPrincess(self)
		self.print_princess = True
		txt=[(t('Choose your'),[-200,200]),(t('appearence...'),[-200,250]),(t('skin tone'),[250,420]),(t('previous'),[250,90]),(t('next'),[250,520])]
		self.reset_menu(
			background  = os.path.join(directory.story,'svg_bedroom.png'),
			action	  = 'open',
			texts = [widget.GameText(t(i[0]),i[1],self,color = (58,56,0)) for i in txt],
			buttons = [widget.Button(os.path.join(directory.title_screen,i[0]),i[1],self,i[2], parameter = i[3], invert = i[4]) for i in
					(["arrow_right",(380,430),self.change_princess,[(1,'skin')],False],
					 ["arrow_right",(120,430),self.change_princess,[(-1,'skin')],True],
					 ["arrow_up"   ,(250,-5),self.back_to_main,None,False],
					 ["arrow_down"  ,(250,620),self.to_select_hair,None,False])]
					)

	def select_hair(self):
		txt = [(t('Choose your'), (-200,200)), (t('appearence...'),(-200,250)), (t('hair style'),(250,420)), (t('previous'),(250,90)), (t('next'),(250,520))]
		self.print_princess = True
		self.reset_menu(
		  action  = 'open',
		  texts   =  [widget.GameText(t(i[0]),i[1],self,color = (58,56,0)) for i in txt],
		  buttons = [widget.Button(os.path.join(directory.title_screen,i[0]),i[1],self,i[2], parameter = i[3], invert = i[4]) for i in
				  (['arrow_right',(380,430),self.change_princess,[(1,'hair')],False],
				   ['arrow_right',(120,430),self.change_princess,[(-1,'hair')],True],
				   ['arrow_up'   ,(250,-5),self.back_to_select_princess,None,False],
				   ['arrow_down' ,(250,620),self.to_name_your_princess,None,False])])


	def name_your_princess(self):

		self.print_princess = False
		opt = [widget.Letter(i[0],i[1],self, self.screen.hoover_letter_size, 'GentesqueRegular.otf', 40) for i in zip(
				map(chr,xrange(97,123)),
				zip([x for n in xrange(9) for x in xrange(int(100),int(422),int(40))],
					[n for n in xrange(int(200),int(352),int(50)) for x in xrange(9)]))] 
		opt.extend([widget.Key(t('< back'),	   (140,350)  ,self, 'Backspace'),
					widget.Key(t('space >'),	  (360,350)  ,self, 'Spacebar'),
					widget.Key(t('clean up [  ]'),(140,400)  ,self, 'Cleanup'),
					widget.Key(t('random   ???'), (360,400)  ,self, 'Random')
		   ])

		buttom_list = [widget.Button(os.path.join(directory.title_screen,i[0]),i[1],self,i[2],parameter=i[3],invert=i[4]) for i in (
						 ['button_ok',   (250,620), self.start_game,	None,False],
						 ['arrow_up'   ,(250,-5),self.back_to_select_hair,None,False],
						)]
		if name_taken:
			txts = [	widget.GameText(t('Sorry, This name is taken.'),(-100,-150),self,color = (58,56,0)),
						widget.GameText(t('Please, choose another one'),(-100,-50),self,color = (58,56,0)),
						widget.GameText(t('_ _ _ _ _ _ _'),(230,130),self,color = (58,56,0)),
						self.princess.name
					]
			buttom_list.extend([widget.Button('or Overwrite it.',(-100,620), self, self.start_game,color = (58,56,0), parameter=[False,True]) ])
		else:
			txts =[	 widget.GameText(t('... and your name.'),(-200,200),self,color = (58,56,0)),
						widget.GameText('_ _ _ _ _ _ _', (230,130),self,color = (58,56,0)),
						self.princess.name]
		self.reset_menu(action  = 'open', options = opt, texts = txts, buttons = buttom_list)

	def update_all(self):
		self.game_mouse.update()
		self.mouse_pos  = self.game_mouse.mouse_pos
		self.mouse_positions = [i.rect.center for i in self.options+self.buttons]
		keyboard = self.screen.universe.action[0]
		if keyboard:
			if keyboard in ("up","left"):
				self.selector -=1
				if self.selector <0:
					self.selector = len(self.mouse_positions)-1
			elif keyboard in ("down","right"):
				self.selector +=1
				if self.selector > len(self.mouse_positions)-1:
					self.selector = 0
			pygame.mouse.set_pos(self.mouse_positions[self.selector])
		self.position[1] += round(self.speed)

		if '_ _ _ _ _ _ _' in [i.text for i in self.texts]:
			if keyboard in ("a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"):
				self.princess.name.text += keyboard
			if keyboard == 'space':
				self.princess.name.text += ' '
			if keyboard == 'backspace':
				self.princess.name.text = self.princess.name.text[:-1]
		accel = p(2,r=False)
		if self.action == 'open':
			if self.position[1] != self.goal_pos[1]:
				#Breaks
				if self.goal_pos[1]+(p(70,r=False)) > self.position[1] > self.goal_pos[1]-p(70,r=False):
					if self.speed > 0:
						self.speed -= self.speed*.25
					elif self.speed < 0:
						self.speed += -self.speed*.25
				elif self.position[1] < self.goal_pos[1]:
					if self.position[1] < self.goal_pos[1] - p(50,r=False):
						self.speed+=accel
				else:
					if self.position[1] > self.goal_pos[1] + p(50,r=False):
						self.speed-=accel
		elif self.action == 'close':
			if not self.go_back:
				if self.speed < p(85,r=False):
					self.speed += accel
			else:
				if self.speed > -p(85,r=False):
					self.speed -= accel
		self.universe.screen_surface.blit(self.game_mouse.image,self.game_mouse.pos)

	### Buttons functions ###
	def back_to_main(self):
		self.story		  = None
		self.credits		= None
		self.tutorial	   = None
		self.screen.story_frames = []
		self.go_back = True
		self.next_menu = self.main
		self.screen.action = 'close'

	def back_to_select_princess(self):
		self.go_back = True
		self.next_menu = self.select_princess
		self.screen.action = 'close'

	def back_to_select_hair(self):
		self.go_back = True
		self.next_menu = self.select_hair
		self.screen.action = 'close'

	def new_game(self):
		self.go_back = False
		self.next_menu = self.select_princess
		self.screen.action = 'close'

	def load_game(self):
		self.go_back = False
		self.next_menu = self.select_saved_game
		self.screen.action = 'close'

	def play_story(self):
		self.go_back = False
		self.next_menu = self.watching_story
		self.screen.action = 'close'

	def play_tutorial(self):
		self.go_back = False
		self.next_menu = self.watching_tutorial
		self.screen.action = 'close'

	def play_credits(self):
		self.credits = Credits(self)

	def choose_language(self):
		pass

	def start_game(self, using_saved_game=False, start_anyway= False):
		pygame.mixer.music.fadeout(4000)
		if self.princess and self.princess.name.text == "":
			self.princess.name.text = "			  "
		global name_taken
		if not using_saved_game:
			try:
				self.create_files()
				self.screen.universe.LEVEL= 'start'
				name_taken = False
			except Exception as  (errno, strerror):
				print "Maybe this name already existed"
				print strerror
				if errno == 17 and start_anyway:
					self.remove_save_directory(self.princess.name.text)
					self.create_files()
					self.screen.universe.LEVEL= 'start'
				else:
					name_taken = True
					self.to_name_your_princess()
		else:
			print "Using saved game "+ using_saved_game
			print "Connecting to Database"
			db.connect_db(using_saved_game, self.screen.universe)
			print "done."
			self.screen.universe.LEVEL = 'start'

	def create_files(self,):
		print "Starting a New Save"
		new_dir = os.path.join(directory.saves,self.princess.name.text)
		os.mkdir(new_dir)
		print "Directory Created"
		db.create_save_db(
				os.path.join(new_dir,self.princess.name.text+'.db'),
				name = self.princess.name.text,
				hairback = self.princess.hairs_back[self.princess.numbers['hair']],
				skin = self.princess.skins[self.princess.numbers['skin']],
				hair = self.princess.hairs[self.princess.numbers['hair']],
				arm = self.princess.arms[self.princess.numbers['skin']],
				universe = self.screen.universe)
		print "Database Created"

	def change_princess(self,list):#list of: int,part
		if list[1] == "hair":
			number = 4
		elif list[1] == 'skin':
			number = 2
		self.princess.numbers[list[1]] += list[0]
		if   self.princess.numbers[list[1]] < 0:
			 self.princess.numbers[list[1]] = number
		elif self.princess.numbers[list[1]] > number:
			 self.princess.numbers[list[1]] = 0

	def to_name_your_princess(self):
		self.go_back = False
		self.next_menu = self.name_your_princess
		self.screen.action = 'close'

	def to_select_hair(self):
		self.go_back = False
		self.next_menu = self.select_hair
		self.screen.action = 'close'

	def select_saved_game(self):
		print "Let's select a saved princess"
		self.screen.bar = self.screen.bar_right
		saved_games = []
		print "searching for saved games"
		for i in os.listdir(directory.saves):
			try:
				D = os.path.join(directory.saves,i)
				files = os.listdir(D)
				if 'thumbnail.PNG' in files:
					saved_games.extend([{'name':i, 'file': os.path.join(directory.saves,i,i+'.db')}])
					print "Saved game found: "+ i
				else:
					print t('The '+i+' file is not well formed. The thumbnail was probably not saved. The saved file will not work without a thumbnail. Please, check this out in '+ directory.saves+'/'+i)
					for f in files:
						file_to_remove = D+f
						print "Removing "+file_to_remove
						os.remove(file_to_remove)
					print "removing directory "+D
					os.rmdir(D)
			except:
				pass
		print "done."
		self.back_background = utils.img.image(os.path.join(directory.story,'svg_bedroom.png'))
		white_mask		   = pygame.Surface(self.back_background.get_size(),pygame.SRCALPHA).convert_alpha()
		white_mask.fill((255,255,255,150))
		self.back_background.blit(white_mask,(0,0))
		self.background = None
		self.action	 = 'open'
		self.speed	  = 0
		self.position = p([100,-600])
		self.options	= [widget.Button(t('Or go back to Main Menu'), (245,500),self,self.back_to_main,font_size=40,color = (58,56,0))]
		self.texts =	  [widget.GameText(t('Have you already saved a game?'),(250,-150),self,color = (58,56,0)),
						   widget.GameText(t('Then choose your saved princess:'),(250,-100),self,color = (58,56,0))]
		ypos = 0
		xpos = 0
		self.buttons = []
		for i in saved_games:
			print directory.saves+'/'+i['name']+'/'
			self.buttons.extend([widget.Button(os.path.join(directory.saves,i['name']),(xpos,ypos),self, self.start_game,color = (58,56,0), parameter=([i['file']]))])
			self.options.extend([
			  widget.Button(i['name'],  (xpos+100,ypos), self,self.start_game, font_size=30,color = (58,56,0), parameter=([i['file']])),
			  widget.Button(t('erase'), (xpos+300,ypos) ,self,self.remove_save_directory,font_size=30,color = (58,56,0), parameter=[i['name']])
								])
			ypos += d(self.buttons[0].size[1])
			if ypos > 450:
				ypos = 0
				xpos += 400

	def watching_story(self):
		print "Let's watch the story"
		self.screen.bar = self.screen.bar_right
		self.story = Story_Frame(self,directory.story_frames)
		self.action	 = 'open'
		self.speed	  = 0
		self.position = p([450,-600])
		self.options	= []
		self.buttons= [widget.Button(directory.arrow_left,(340,510), self, self.story.next_frame,color = (58,56,0)),
					   widget.Button(directory.arrow_right,(250,510), self, self.story.past_frame, invert = True,color = (58,56,0))]
		self.texts =   self.story.texts

	def watching_tutorial(self):
		print "Let's watch the tutorial"
		self.screen.bar = self.screen.bar_right
		self.tutorial   = Story_Frame(self,directory.tutorial_frames)
		self.action	 = 'open'
		self.speed	  = 0
		self.position   = p([450,-600])
		self.options	= []
		self.buttons	= [widget.Button(directory.arrow_right,(940,270), self, self.tutorial.next_frame,color = (58,56,0)),
						   widget.Button(directory.arrow_right,(-400,270), self, self.tutorial.past_frame, invert = True,color = (58,56,0))]
		self.texts	  = self.tutorial.texts

	def remove_save_directory(self, save_name):
		for root, dirs, files in os.walk(os.path.join(directory.saves,save_name), topdown=False):
			for name in files:
				os.remove(os.path.join(root, name))
			for name in dirs:
				os.rmdir(os.path.join(root, name))
		os.rmdir(os.path.join(directory.saves,save_name))
		self.select_saved_game()

	def NOTSETYET(self):
		pass


class MenuPrincess():
	def __init__(self,menu,thumbnail=None):
		dir = directory.princess
		self.menu = menu
		if not thumbnail:
			self.skins = ('skin_pink','skin_black','skin_tan')
			self.arms  = ('arm_pink','arm_black','arm_tan')
			self.hairs = ('hair_yellow', 'hair_short', 'hair_brown', 'hair_rastafari', 'hair_red')
			self.hairs_back= (None, None, 'hair_brown_back', 'hair_rastafari_back','hair_red_back')
			self.skin = [utils.img.image(os.path.join(dir,i,'stay','0.png')) for i in self.skins]
			self.arm  = [utils.img.image(os.path.join(dir,i,'stay','0.png')) for i in self.arms]
			self.hair = [utils.img.image(os.path.join(dir,i,'stay','0.png')) for i in self.hairs]
			self.hairback = [None,
							 None,
							 utils.img.image(os.path.join(dir,self.hairs_back[2],'stay','0.png')),
							 utils.img.image(os.path.join(dir,self.hairs_back[3],'stay','0.png')),
							 utils.img.image(os.path.join(dir,self.hairs_back[4],'stay','0.png'))]
			self.numbers = {'skin':1,'hair':1}
			self.images = [ self.hairback[self.numbers['hair']],
							self.skin[self.numbers['skin']],
							utils.img.image(os.path.join(dir,'face_simple','stay','0.png')),
							self.hair[self.numbers['hair']],
							utils.img.image(os.path.join(dir,'shoes_slipper','stay','0.png')),
							utils.img.image(os.path.join(dir,'dress_plain','stay','0.png')),
							self.arm[self.numbers['skin']]
							]
			self.size = self.skin[0].get_size()
		else:
			self.images = utils.img.image(thumbnail)
		self.goal_pos = p((250,250))
		self.name = widget.GameText('maddeline',(170,120),self.menu,var = True,color = (58,56,0))
		self.pos = [self.menu.position[0]+self.goal_pos[0]-(self.size[0]/2),
						   self.menu.position[1]+self.goal_pos[1]-(self.size[1]/2)]

	def update_all(self):
		self.images[0]  = self.hairback[self.numbers['hair']]
		self.images[1]  = self.skin[self.numbers['skin']]
		self.images[3]  = self.hair[self.numbers['hair']]
		self.images[6]  = self.arm[self.numbers['skin']]
		self.pos		= [self.menu.position[0]+self.goal_pos[0]-(self.size[0]/2),
						   self.menu.position[1]+self.goal_pos[1]-(self.size[1]/2)]


class Story_Frame():
	def __init__(self, menu, path):
		self.menu = menu
		self.texts = [widget.GameText(t('Use the arrows to go'),(220,150),menu,font_size = 25,color = (58,56,0)),
					  widget.GameText(t('forward and backward'),(220,200),menu,font_size = 25,color = (58,56,0))]
		image_frames = sorted(os.listdir(path))
		self.channel = pygame.mixer.Channel(0)
		self.available_images   = [utils.img.image(os.path.join(path,i)) for i in image_frames]
		if "tutorial" in path:
			sound_frames = sorted(os.listdir(os.path.join(directory.sounds,'tutorial','frames')))
			self.available_sounds = [pygame.mixer.Sound(os.path.join(directory.sounds,'tutorial','frames',i)) for i in sound_frames]
			GT = widget.GameText
			frame_texts = {

				0:[	GT(t('Hi!'),(800,250),font_size =30),
						GT(t("Hello, dear! I'm a fairy godmother and I asked for princess Madelline's help to give you a superb tutorial, okay?"),(757,790), box = (718,218), font_size=30)],

				1:[	GT(t('Yiipi!'),(764,495),font_size = 30),
						GT(t("As you'll soon find out, pressing left or right will move your princess around."),(730,790),box=(718,218), font_size = 30) ],

				2:[	GT(t('Yey!'),(650,110),font_size = 30),
						GT(t("And pressing the spacebar will allow you to jump."),(730,790),box=(718,218), font_size = 30)],

				3:[	GT(t('x'), (575,198), font_size = 30),
						GT(t("And the Control key will get you a kiss."),(730,790),box=(718,218), font_size = 30)],

				4:[	GT(t('Ooh!'), (500,210),font_size = 30),
						GT(t("If you kiss enemies, they will sometimes be sooo happy as to stop bothering you... for a while."),(730,790),box=(718,218), font_size = 30)],

				5:[	GT(t("But be aware that some enemies will respond only to your mouse cursor, and yet others can only be dodged!"),(730,790),box=(718,218), font_size = 30)],

				6:[	GT(t("You'll notice that on the upper right side there's a clock. When it points down, it will be time for the ball."),(730,790),box=(718,218), font_size = 30)],

				7:[	GT(t("Yeah!"),(510,210),font_size = 30),
				widget.GameText(t("But first we need to find you a beautiful and original look."),(730,790),box=(718,218), font_size = 30)],

				8:[	GT(t("And in order to do that, we must visit the castles that lie in the left part of most streets."),(730,790),box=(718,218), font_size = 30)],

				9:[	GT(t("That's because they are shops, and in them you'll find the most wonderful dresses, make-up, shoes and accessories!"),(730,790),box=(718,218), font_size = 30)],

				10:[GT(t("You got it!"),(580,495),font_size=26,box=(100,200)),
						GT(t("Oh! And remember you can switch streets by pressing up when in front of a gate."),(730,790),box=(718,218), font_size = 30)],

				11:[GT(t("Ookay..."),(630,445),font_size = 30),
						GT(t("Now, once you're at the ball, your look will be compared to those of other princesses, and even with the garments you girls used in previous balls."),(730,790),box=(718,218), font_size = 30)],

				12:[GT(t("Oh, no!..."),(560,450),font_size = 24),
						GT(t("If you wear the same outfit as others (or repeat it ball after ball), you'll earn little to no glamour points. It would be a shame."),(730,790),box=(718,218), font_size = 30)],

				13:[GT(t("All right!"),(600,500),font_size = 26,box=(100,200)),
						GT(t("But, on the other hand, if you show up with an original look, then you may earn lots of glamour points!"),(730,790),box=(718,218), font_size = 30)],

				14:[GT(t("Who's my True Love?"),(410,495),font_size = 22,box=(120,200)),
						GT(t("And as you gain glamour points, more and more boys will offer you their hearts. And some day, you may even catch the eyes of Prince Charming himself."),(730,780),box=(750,218), font_size = 30)],

				15:[GT(t("Oh, no!"),(480,205),font_size = 30),
						GT(t("Woof!"),(885,490),font_size=30),
						GT(t("But beware! The enemies on your way may not hurt you, but they can make you dirty. And THAT would certainly cost you lots of glamour points!"),(730,790),box=(718,218), font_size = 30)],

				16:[GT(t("So be careful."),(780,550),font_size = 24,box=(120,200)),
						GT(t("You can get even dirtier if you are caught a second time, and become dirtiest if hit yet again..."),(730,790),box=(718,218), font_size = 30)],

				17:[GT(t("Hooray!"),(740,490),font_size = 30),
						GT(t("...but event then there's hope. Go back and enter the Bathhouse, and you'll be clean and perfumed in no time!"),(730,790),box=(718,218), font_size = 30)],

				18:[GT(t("Neat!"),(765,470),font_size=30),
						GT(t("But before you go, I've got two more tips to you. First, stay alert to the music! By it you can tell not only what is the stronger enemy around, but how far it is from you."),(700,790),box=(830,218), font_size = 30)],

				19:[GT(t("Ooooh!"),(800,400),font_size=30),
						GT(t("And finally, there are many secret items in the game, and you should anlock them ASAP. To get you started, try kissing the lion on Make-up Street's zoo."), (710,790),box=(800,218), font_size = 30)],

				20:[GT(t("Have fun!"),(820,260),font_size=30,box=(120,200)),
						GT(t("Now you're good to go! Don't stay idle waiting your dreams come true - go get them, girl!"),(730,790),box=(718,218), font_size = 30)]
			}
		elif "story" in path:
			sound_frames = sorted(os.listdir(os.path.join(directory.sounds,'story','frames')))
			self.available_sounds   = [pygame.mixer.Sound(os.path.join(directory.sounds,'story','frames',i)) for i in sound_frames]
			frame_texts = {
				}

		for i in range(0,len(self.available_images)):
			if i in frame_texts and frame_texts[i]:
				for ii in frame_texts[i]:
					self.available_images[i].blit(ii.image,ii.pos)

		self.flip_sound = pygame.mixer.Sound(os.path.join(directory.sounds,'story','sflip.ogg'))
		self.frame_number   = 0


	def update_all(self):
		if self.frame_number:
			self.images = [self.available_images[self.frame_number-1]]
		else:
			self.images = []
		

	def next_frame(self):
		self.channel.play(self.flip_sound)
		if self.frame_number >= len(self.available_images):
			self.menu.back_to_main()
		else:
			self.channel.queue(self.available_sounds[self.frame_number])
			self.frame_number += 1
			if self.frame_number:
				self.menu.screen.bar_side = None
				self.menu.backgrounds = []
				self.menu.background = None
				if self.frame_number in self.texts:
					self.menu.texts = self.texts
				else:
					self.menu.texts = []


	def past_frame(self):
		self.channel.play(self.flip_sound)
		self.frame_number -= 1
		if self.frame_number == 0:
			self.menu.screen.bar_side = 'right'
			if self.frame_number in self.texts:
				self.menu.texts = self.texts
			else:
				self.menu.texts = []
			self.menu.background = utils.img.image(os.path.join(directory.title_screen,'selection_canvas','0.png'))
		if self.frame_number == -1:
			self.menu.back_to_main()



class Credits():
	def __init__(self,menu):
		self.background = utils.img.image(os.path.join(directory.credits,'fundo.png'))
		self.menu	   = menu
		self.pos		= p((0,100))
		developers = [
				('isac',	os.path.join(directory.credits,'isacvale.png')   ,(433,840)),
				('ndvo',	os.path.join(directory.credits,'ndvo.png'	)   ,(265,631)),
				('raquel',  os.path.join(directory.credits,'raquel.png'  )   ,(986,631)),
				('sergio',  os.path.join(directory.credits,'sergio.png'  )   ,(810,840))
							]
		rendered_texts	  = [
				('cilda & sara',	os.path.join(directory.credits,'text_cilda_e_sara.png' )  ,(590,462)),
				('isac & sergio',   os.path.join(directory.credits,'text_isac_e_sergio.png')  ,(614,950)),
				('ndvo',			os.path.join(directory.credits,'text_ndvo.png'		 )  ,(415,790)),
				('ndvo & isac',	 os.path.join(directory.credits,'text_ndvo_e_isac.png'  )  ,(601,1200)),
				('ocastudios',	  os.path.join(directory.credits,'text_ocastudios.png'   )  ,(514,1251)),
				('raquel',		  os.path.join(directory.credits,'text_raquel.png'	   )  ,(841,790))
							]
		texts_chopin = [
			(t('in loving memory of')  ,(713,436),44,(0,0,0,255)),
			(t('and')				  ,(701,520),24,(0,0,0,255)),
			(t('Credits')			  ,(693,711),75,(0,0,0,255)),
			(t('Programming')		  ,(485,769),34,(0,0,0,255)),
			(t('Support')			  ,(934,769),34,(0,0,0,255)),
			(t('Design')			   ,(682,930),34,(0,0,0,255)),
			(t('Music'),				(704,1400),54,(0,0,0,255)),
			(t('first snowfall'),	   (583,1448),44,(128,0,0,255)),
			(t('endless blue'),		 (650,1489),44,(128,0,0,255)),
			(t('celtic cappricio'),	 (762,1530),44,(128,0,0,255)),
			(t('the bee'),			  (488,1572),44,(128,0,0,255)),
			(t("lonesome man's dance"), (684,1612),44,(128,0,0,255)),
			(t('dragon dance'),		 (754,1657),44,(128,0,0,255)),
			(t('ship of fools'),		(829,1695),44,(128,0,0,255)),
			(t('sword fight'),		  (684,1733),44,(128,0,0,255)),
			(t('the foggy dew'),		(615,1778),44,(128,0,0,255)),
			(t('revolution on resoluti on'), (828,1820),44,(128,0,0,255)),
			(t('twilight on mountain'), (907,1858),44,(128,0,0,255)),
			(t('brian boru 2'),		 (770,1899),44,(128,0,0,255)),
			(t('ignition'),			 (830,1934),44,(128,0,0,255)),
			(t('first snowfall'),	   (750,1975),44,(128,0,0,255)),
			(t('cocci ci tini cocci'),  (780,2012),44,(128,0,0,255)),
			(t('first snowfall'),	   (826,2053),44,(128,0,0,255)),
			(t('waltz wedley'),		 (972,2100),44,(128,0,0,255))
		   ]
		texts_gentesque = [
			(t('All python & pygame code, written in gedit.'),(501,841),16,(180,60)),
			(t('Bureaucracy and et ceteras'),(909,837),16,(110,60)),
			(t('Almost all Inkscape, with a touch of Blender and Gimp.'), (704,1027),16,(200,60)),
			(t('based on the homonimous board game by'),(699,1179),22,None),
			(t('available at'),		(703,1237),22,None),
			(t('introduction'),		(427,1458),14,None),
			(t('by Torley on Piano'),  (754,1458),14,None),
			(t('menu'),				(540,1499),14,None),
			(t('by Armolithae'),	   (800,1499),14,None),
			(t('bathhouse st'),		(588,1540),14,None),
			(t('by armolithae'),	   (938,1540),14,None),
			(t('dress st'),			(400,1582),14,None),
			(t('by Ceili Moss'),	   (600,1582),14,None),
			(t("shoe's st"),		   (500,1622),14,None),
			(t("by Ceili Moss"),	   (900,1622),14,None),
			(t('accessory st.'),	   (600,1667),14,None),
			(t('by Butterfly Tea'),	(920,1667),14,None),
			(t('make-up st.'),		 (700,1705),14,None),
			(t('by Ceili Moss'),	   (961,1705),14,None),
			(t('schnauzer'),		   (550,1743),14,None),
			(t('by Armolithae'),	   (821,1743),14,None),
			(t('carriage'),			(470,1788),14,None),
			(t('by Ceili Moss'),	   (760,1788),14,None),
			(t('old lady'),			(610,1830),14,None),
			(t('by Torly on Piano'),   (1080,1830),14,None),
			(t('viking'),			  (720,1868),14,None),
			(t('by Armolithae'),	   (1100,1868),14,None),
			(t('butterffly'),		  (620,1909),14,None),
			(t('by Adragante'),		(920,1899),14,None),
			(t('hawk'),				(750,1944),14,None),
			(t('by Armolithae'),	   (950,1944),14,None),
			(t('birdie'),			  (600,1985),14,None),
			(t('by Torley on Piano'),  (950,1985),14,None),
			(t('fabrizio'),			(600,2022),14,None),
			(t('by Picari'),		   (960,2022),14,None),
			(t('zoo'),				 (700,2063),14,None),
			(t('by Torley on Piano'),  (980,2063),14,None),
			(t('ball'),				(831,2110),14,None),
			(t('by strauss'),		  (1095,2110),14,None),
			(t('Sad and unfortunate legal mambo jambo'),(830,2290),14,None),
			(t("All programming and art are public domain, released so by us, their authors."),(800,2335),14,None),
			(t("The musics, however, comes in a variety of free licenses. They can be used and altered, even commercially, but credit MUST be given. Special thanks to www.jamendo.com, from where most of our music came."),(850,2375),14,(720,90)),
			(t("( If you are an author and want your music out of this game, contact us and we'll promptly remove it. )"),(800,2385),13,None),
			(t("And then there are the fonts: Gentesque, by Paulo Silva, is in OpenFont License while Chopin Script, by Diogene, is in Public Domain (hurray!)."),(830,2415),13,(720,60)),
			(t("If you are a developer of free content, please consider the limitations the varying \"free licenses\" impose on derivative works. Tons (or better yet, Teras) of cultural content, as images, music and fonts that are \"free\" are quite unuseable due to legal and procedural restraints (we just cannot give credit to every bit of data we'll use). \"Free for personnal use, but not commercial\", \"free for use, but not to alter\" and/or \"free for use, but not to distribute\" hinders freedom, and equals \"free as in beer, not as in speech\". Giving credit to a music used is fair and doable, but not to the recording of step sounds, for example, or other minuscule but necessary files. Please help us spread and create upon your work by releasing it either in public domain or in GPL - avoid semi-free, non-standard and multiple-standard licenses. These just end up torturing developers with pages of sad and unfortunate license disclaimers... such as this."),(900,2525),13,(720,220)),
			(t("want to congratulate or complain? do it to glamour@ocastudios.com"), (1000,2540),14,None)
		   ]
		self.images = developers+rendered_texts
		self.texts = [ widget.GameText(i[0],i[1],self,fonte='Chopin_Script.ttf', font_size=i[2], color=i[3]) for i in texts_chopin]+[
					   widget.GameText(i[0],i[1],self,fonte='GentesqueRegular.otf', font_size=i[2], color=(0,0,0,255),box = i[3]) for i in texts_gentesque]
		for i in self.images:
			print i
			self.background.blit(utils.img.image(i[1]),p(i[2]))
		for i in self.texts:
			self.background.blit(i.image,i.pos)


	def update_all(self):
		if self.pos[1] > -p(3020):
			self.pos[1]-=p(1,r=False)
		else:
			self.pos[1] = p(1000)
			self.menu.credits = None
