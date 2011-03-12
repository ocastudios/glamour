import pygame
import itertools
import utils
import utils.save as save
import interactive.princess as princess
import os
import random


import interface.widget as widget
import interactive.messages as messages
import database
import settings
from settings import directory
p = settings.p
d = settings.d
t = settings.t

class Inside():
	def __init__(self, universe, item_type, item_list):
		self.status = 'outside'
		self.universe  = universe
		self.type_of_items = item_type
		self.items = []
		self.buttons = []
		self.menu = []
		counter = itertools.count()
		if item_type != 'shower':
			self.items = [Item(self, i,counter.next()) for i in item_list]
			self.menu.extend([(i.pos[0]+(i.size[0]/4),i.pos[1]+(i.size[1]/4)) for i in self.items])
			self.chosen_glow = Chosen_Glow(self, pos = [-200,500], degree = 90)
			self.buttons	= (
				 widget.Button(self.universe, directory.button_ok,(410,530),[0,0],self.all_set),
				 self.chosen_glow
								)
			self.menu.extend([(i.pos[0]+(i.size[0]/4),i.pos[1]+(i.size[1]/4)) for i in self.buttons if i.__class__==widget.Button])
			self.big_princess = BigPrincess(self)
		else:
			self.items = []
			shower	  = widget.GameText(self.universe, t('Take a shower'),(360,400))
			ok_pos	  = d(shower.pos[0]+(shower.size[0]/2)),d(shower.pos[1]+(shower.size[1]))+50
			ok_button   = widget.Button(self.universe, directory.button_ok,ok_pos,[0,0],self.clean_up)
			quit		= widget.GameText(self.universe, t('Leave'),(1080,400))
			cancel_pos  = d(quit.pos[0]+(quit.size[0]/2)),d(quit.pos[1]+(quit.size[1]))+50
			cancel_button = widget.Button(self.universe, directory.button_cancel,cancel_pos,[0,0],self.all_set)
			title	   = widget.GameText(self.universe, t('Would you like to take a shower?'),(720,100))
			self.buttons	= (shower, ok_button, quit, cancel_button, title)
			self.menu = [(i.pos[0]+(i.size[0]/4),i.pos[1]+(i.size[1]/4)) for i in self.buttons if i.__class__== widget.Button]
			self.big_princess = BigPrincess(self, pos = "center")
		self.locked = {'geisha': database.query.is_locked(self.universe,'face','geisha'),
						'indian': database.query.is_locked(self.universe,'dress','indian'),
						'crystal': database.query.is_locked(self.universe,'shoes','crystal')
		}
		self.chosen_item = None
		self.chosen_number = 0
		self.music = os.path.join(directory.music,'menu.ogg')

	def all_set(self):
		self.status = 'done'
		if self.chosen_item:
			exec('save.save_file(self.universe,'+self.type_of_items+' = "'+self.type_of_items+"_"+self.chosen_item.name+'")')
		else:
			save.save_file(self.universe)
		self.universe.level.princesses[0] = princess.Princess(self.universe, INSIDE = True)
		if self.locked['indian']:
			my_outfit = database.query.my_outfit(self.universe,"princess_garment")
			geisha_garments = 0
			for i in my_outfit:
				if ("geisha" in str(i)) or ('kimono' in str(i)) or ("flower" in str(i)):
					geisha_garments+= 1
			if geisha_garments >= 3:
				self.universe.level.unlocking = {'type':'dress','name':'indian'}
				self.locked['indian'] = False
		if self.locked['crystal']:
			if my_outfit[9] == 'accessory_ribbon' and \
					my_outfit[6] == 'dress_red' and \
					my_outfit[3] == 'face_eyelids' and \
					my_outfit[5] == 'shoes_red':
				self.universe.level.unlocking = {'type':'shoes','name':'crystal'}
				self.locked['crystal'] = False



	def clean_up(self):
		self.status = 'done'
		if self.universe.level.princesses[0].dirt ==0:
			if self.locked['geisha']:
				self.universe.level.unlocking = {'type':'face','name':'geisha'}
				self.locked['geisha'] = False

		self.universe.level.princesses[0].dirt = 0
		database.update.clean_up(self.universe)
		print "You look lovely all cleaned up!"
		self.universe.level.princesses[1] = None
		save.save_file(self.universe)
		thumbnail = pygame.transform.flip(pygame.transform.smoothscale(self.universe.level.princesses[0].stay_img.left[0],(100,100)),1,0)
		pygame.image.save(thumbnail,os.path.join(directory.saves,self.universe.level.princesses[0].name.encode('utf-8'),'thumbnail.PNG'))



	def NOTSETYET(self):
		pass

 

class Item():
	def __init__(self, room, name,index):
		self.name   = name
		self.universe  = room.universe
		self.room   = room
		self.type   = room.type_of_items
		if self.type != 'shower':
			self.image  = utils.img.image(os.path.join(directory.princess,self.type+'_'+name,'big_icons','0.png'))
			self.size   = self.image.get_size()
			self.pos	= [p(500,r=0)+(index*(self.size[0])),(self.universe.height/2)-(self.size[1]/2)]
			self.speed  = 1
		self.rect	   = pygame.Rect((self.pos),(self.size))
		self.active	 = False

	def update_all(self):
		self.click_detection()
		if self.room.chosen_item==self:
			self.room.chosen_glow.update_all()

	def click_detection(self):
		if self.rect.colliderect(self.universe.pointer.rect):
			self.active = True
			if self.universe.click:
				self.room.chosen_item = self
				BP = self.room.big_princess
				j = os.path.join
				BP.images[BP.image_dict[self.type]] = utils.img.image(j(directory.princess,self.type+'_'+self.name,'big.png'), invert = True)
				self.room.chosen_glow.pos = self.pos[0]-p(40,r=0),self.pos[1]-p(40,r=0)
				if self.type == "hair":
					if self.name in ("black","brown","rapunzel", "rastafari","red"):
						BP.images[BP.image_dict["hair_back"]] = utils.img.image(j(directory.princess,self.type+'_'+self.name+"_back",'big.png'), invert = True)
					else:
						BP.images[BP.image_dict["hair_back"]] = None
				elif self.type == "dress":
					if self.name in ("yellow","red","kimono","indian"):
						BP.images[BP.image_dict["armdress"]] = utils.img.image(j(directory.princess, 'sleeve_' + self.name,'big.png'),invert = True)
					else:
						BP.images[BP.image_dict["armdress"]] = None

class BigPrincess():
	def __init__(self, room, pos = "left"):
		self.room			= room
		self.universe		= room.universe
		if pos == "left":
			self.pos		= p((20,270))
		elif pos == "center":
			self.pos		= p((room.universe.width/2,270))
		row = database.query.my_outfit(self.universe, 'princess_garment')
		self.image_dict = {
						"hair_back" :0,
						"skin"	  :1,
						"face"	  :2,
						"hair"	  :3,
						"shoes"	 :4,
						"dress"	 :5,
						"arm"	   :6,
						"armdress"  :7,
						"accessory" :8
							} 
		garments = ["hair_back", "skin" ,"face", "hair" , "shoes", "dress", "arm", "armdress", "accessory"]
		self.images = []
		for i in garments:
			if row[i] and row[i]!= "None":
				img = utils.img.image(os.path.join(directory.princess,row[i],'big.png'), invert = True)
			else:
				img = None
			self.images += [img]


	def update_all(self):
		pass

	def all_set(self):
		self.status = 'done'
		thumbnail = pygame.transform.smoothscale(self.universe.level.princesses[0].stay_img.left[0],(100,100))
		pygame.image.save(thumbnail,os.path.join(saves_dir,self.universe.level.princesses[0].name,'thumbnail.PNG'))

	def update_all(self):
		self.pos		= [self.frame.position[0]+self.position[0],
						   self.frame.position[1]+self.position[1]]


class Princess_Home():
	def __init__(self, universe, princess=None):
		print "Creating Princess Home: "+ princess['name'] 
		painting_screen = pygame.Surface((400,400), pygame.SRCALPHA).convert_alpha()
		if princess == settings.Rapunzel:
			painting_screen.blit(utils.img.image(os.path.join(directory.princess,'hair_rapunzel_back','big.png')),(0,0))
		images  = [utils.img.image(os.path.join(directory.princess,item,'big.png')) for item in ('skin_'+princess['skin'],princess['hair'])]
		for img in images:
			painting_screen.blit(img, (0,0))
		self.princess_image = painting_screen#utils.img.scale_image(painting_screen)
		self.princess_icon  = utils.img.image(os.path.join(directory.ball,princess['icon']))
		self.status = 'outside'
		self.universe  = universe
		mymessage = messages.princesses_phrases[random.randint(0,(len(messages.princesses_phrases)-1))]
		if '%s' in mymessage:
			self.message = mymessage %self.universe.level.princesses[0].name
		else:
			self.message = mymessage
		self.items = []
		self.menu = []
		self.buttons = []
		self.buttons	= (
					widget.Button(self.universe, directory.button_ok,(410,450), [0,0], self.all_set),
					widget.GameText(self.universe, self.message, (850,820), font_size = 40, box = (1100,400))
		)
		self.menu.extend([(i.pos[0]+(i.size[0]/4),i.pos[1]+(i.size[1]/4)) for i in self.buttons if i.__class__==widget.Button])
		princess_name = princess["name"].lower()
		row = database.query.my_outfit(self.universe,princess_name)
		[self.princess_image.blit(utils.img.image(os.path.join(directory.princess,row[i],'big.png')),(0,0)) for i in (
					'face', 'dress', 'arm', 'accessory', 'shoes')]
		self.name=princess_name
		if self.name =="sleeping_beauty":
			self.name="sleeping"
		elif self.name == "snow_white":
			self.name="snowwhite"
		self.locked = database.query.is_locked(self.universe,'hair',self.name)
		self.big_princess = BigPrincess(self)
		self.chosen_number = 0
		self.music = os.path.join(directory.music,'menu.ogg')

	def all_set(self):
		self.status = 'done'
		if self.locked:
			print "You have unlocked "+self.name+"'s hair"
			self.universe.level.unlocking = {'type':'hair','name':self.name}
			self.locked = False

		thumbnail = pygame.transform.smoothscale(self.universe.level.princesses[0].stay_img.left[0],(100,100))
		pygame.image.save(thumbnail,os.path.join(directory.saves,self.universe.level.princesses[0].name,'thumbnail.PNG'))


	def update_all(self):
		self.pos		= [self.frame.position[0]+self.position[0],
						   self.frame.position[1]+self.position[1]]

class Home():
	def __init__(self, universe):
		self.status = 'outside'
		self.music = os.path.join(directory.music,'menu.ogg')
		self.universe  = universe
		self.items = []
		self.buttons = []
		self.buttons	= (widget.Button(self.universe, directory.button_ok,(410,450),[0,0],self.all_set),
						   widget.Button(self.universe, t('Go to the Ball'),(1240,550),[0,0], self.to_the_ball),
						   widget.GameText(self.universe, t("It is not very cute to repeat your outfits. Check out what you wore at past Balls and try to find something different."), (720,750), box=(600,300)),
						   widget.GameText(self.universe, t("Last Ball"),		(600,350), font_size = 25),
						   widget.GameText(self.universe, t("Great Past Ball"),	(800,350), font_size = 25),
						   widget.GameText(self.universe, t("3 Balls Ago"),		(1000,350),font_size = 25)
							)
		self.big_princess = BigPrincess(self)
		self.past_balls = []
		last_balls = database.query.last_balls(universe)
		if len(last_balls)>=1:
			for i in last_balls:
				image_dict = {  "hair_back" :0,
								"skin"	  :1,
								"face"	  :2,
								"hair"	  :3,
								"shoes"	 :4,
								"dress"	 :5,
								"arm"	   :6,
								"armdress"  :7,
								"accessory" :8
									} 
				garments = ["hair_back", "skin" ,"face", "hair" , "shoes", "dress", "arm", "armdress", "accessory"]
				image = pygame.Surface(p((200,200)), pygame.SRCALPHA).convert_alpha()
				for ii in garments:
					if i[ii] and i[ii]!= "None":
						image.blit(utils.img.image(os.path.join(directory.princess,i[ii],'stay','0.png')),(0,0))
				self.past_balls += [image]
		else:
			print "You haven't attended any Balls yet"
		self.locked = database.query.is_locked(self.universe,'face','lipstick')
		self.chosen_number = 0
		self.menu = [(i.pos[0]+(i.size[0]/4),i.pos[1]+(i.size[1]/4)) for i in self.buttons if i.__class__== widget.Button]
		
	def all_set(self):
		self.status = 'done'
		if self.locked:
			self.universe.level.unlocking={'type':'face','name':'lipstick'}
			self.locked = False

	def to_the_ball(self):
		self.universe.level.clock[1].count = 175
		self.universe.level.clock[1].time = 'night'
		self.status = 'done'


class Chosen_Glow():
	def __init__(self,room, pos = [0,0], degree = 0):
		self.room = room
		self.images =  utils.img.OneSided(os.path.join(directory.interface,'select'))
		self.image = self.images.list[0]
		self.pos   = p(pos)

	def update_all(self):
		self.image = self.images.list[self.images.itnumber.next()]
