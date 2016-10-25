import utils
import os
import random
import interactive.enemy as enemy
import pygame
import database
import settings
from settings import directory
p = settings.p


class Princess():
	"""Creates the princess.

	Princess is a rather complex class in comparison with the enemies for princess has many atributes called 'Princess Parts'.
	That's because princess instance is not build with a single group of images, but a bunch of groups of images that may or not be blitted to the screen.

	Princess Parts are her dress, her hair, her eyes, arms and everything that may move or change.
"""
	directory = directory.princess
	def __init__(self,universe,INSIDE = False,xpos=None):
		print "Creating Princess"
		self.first_frame = True
		self.universe = universe
		self.effects	= []
		self.size	   = (2,p(180))
		print "	retrieving data"
		row	 = self.universe.db_cursor.execute("SELECT * FROM save").fetchone()
		self.name = row['name']
		self.center_distance = p(row['center_distance'])
		if xpos:
			self.center_distance = p(xpos)
		self.dirt			= int(row['dirt'])
		self.points			= int(row['points'])
		self.pos = [int(universe.center_x)+self.center_distance, universe.floor-universe.level.what_is_my_height(self)-self.size[1]]
		print "	creating images:"
		print "		princess images"
		for act in ['walk','stay','kiss','fall','jump','ouch','celebrate']:
			self.__dict__[act+"_img"] = utils.img.MultiPart(self.ordered_directory_list(act))
		self.run_away_img = utils.img.Ad_hoc(self.walk_img.left[::2],self.walk_img.right[::2])
		print "		dirt images"
		self.dirties = [Dirt(self.universe,directory.princess+'/'+d,self.pos) for d in ('dirt1','dirt2','dirt3')]
		self.images = None
		self.open_door_img  = self.stay_img
		print "		kisses and dust images"
		self.lips = utils.img.TwoSided(directory.kiss)
		self.dirt_cloud = utils.img.TwoSided(directory.dirt)
		self.gravity = {'force':0, 'accel':p(3)}
		self.speed = p(14)
		self.rect = pygame.Rect(self.pos,self.size)
		self.direction = 'right'
		self.status = {"hurt":0,"excited":0,"scared":0,'move':False}
		self.jump = 0
		self.kiss = {
			'count':0,
			'ongoing':False,
			'direction':'right',
			'rect': ((0,0),(0,0)),
			'height':None
		}
		self.floor = self.universe.floor - self.universe.level.what_is_my_height(self)
		self.last_height = p(186)
		self.action = [None,'stay']
		self.image = self.stay_img.right[self.stay_img.itnumber.next()]
		self.image_size	= self.image.get_size()
		self.inside = INSIDE
		print "	creating sounds"
		print "		steps sounds"
		self.steps = [pygame.mixer.Sound(os.path.join(directory.princess_sounds,'steps','spike_heel','street',str(i)+'.ogg')) for i in range(0,5)]
		print "		jump sounds"
		self.jumpsound		= pygame.mixer.Sound(os.path.join(directory.princess_sounds,'pulo.ogg'))
		self.kisssound		= pygame.mixer.Sound(os.path.join(directory.princess_sounds,'kiss.ogg'))
		self.channel1		= pygame.mixer.Channel(0)
		self.channel2		= pygame.mixer.Channel(1)
		self.channel3		= pygame.mixer.Channel(2)
		self.past_choice	= None
		self.debuginside	=   0
		self.visited_streets = []
		self.locked = database.query.is_locked(self.universe,'shoes','boots')

	def ordered_directory_list(self, action):
		odl = []
		cursor = self.universe.db_cursor
		row = cursor.execute("SELECT * FROM princess_garment WHERE id=(SELECT MAX(id) FROM princess_garment)").fetchone()
		for part in ["hair_back","skin","face","hair","shoes","dress","arm","armdress","accessory"]:
			if row[part] != 'None':
				name = part.replace('_','')
				odl.extend([os.path.join(self.directory,row[part],action)])
		return odl

	def update_all(self):
		if self.first_frame:
			if self.dirt > 0:
				self.universe.level.princesses[1] = self.dirties[self.dirt -1]
		if not self.inside:
			self.direction  = self.universe.level.universe.dir
			self.action	 = self.universe.action
			self.effects = []
			self.soundeffects(self.action)
			self.jumping(self.action)
			self.update_pos(self.action)
			self.hurting(self.action)
			self.kissing()
			self.update_image(self.action,self.direction)
			if self.status['hurt'] > 5:
				if self.status['hurt']%2 == 0:
					self.image = None
		else:
			self.pos[0] = self.universe.center_x+self.center_distance
			self.update_image(self.action,'right')

	def dirt_cloud_funciton(self):
		if 0 < self.status['hurt'] < 24:
			if self.status['hurt'] > len(self.dirt_cloud.left):
				dirt_cloud_image = (self.dirt_cloud.left[self.status['hurt']-1-len(self.dirt_cloud.left)])
			else:
				dirt_cloud_image = (self.dirt_cloud.left[self.status['hurt']-1])
			self.effects.append(Effect(dirt_cloud_image,(self.pos)))

	def jumping(self,action):
		feet_position = self.pos[1]+self.size[1]
		if action[0]!= 'jump' and action[0]!= 'jump2' :
			self.jump = 0
		if feet_position == self.floor and not self.jump :
			if action[0]== 'jump':
				self.jump = 1
				self.channel3.play(self.jumpsound)
				self.images.number = 0
		if self.jump > 0 and self.jump <20:
			self.pos[1] -= p(30)
			if self.jump > 5:
				if self.images.lenght-1 > self.images.number:
					self.images.number += 1
			if self.jump > 10:
				self.images.number = 0
				action[0]= 'fall'
			self.jump +=1
		if action[0]=='fall' and feet_position == self.floor:
			action[0]=None
		if feet_position < self.floor and not self.jump:
			action[0]='fall'

	def hurting(self,action):
		self.speed = p(14) #reset speed eventually changed by Carriage
		if not self.inside:
			if not self.status['hurt']:
				for e in self.universe.level.enemies:
					if (e.__class__ in ( enemy.Schnauzer, enemy.FootBall, enemy.Hawk, enemy.BroomingDust, enemy.Banana) and self.rect.colliderect(e.rect)):
						self.get_dirty()
					if e.__class__ == enemy.Carriage:
						if self.rect.colliderect(e.rect):
							self.speed = 0
							self.action[1]= "stay"
					if e.__class__ == enemy.Butterfly:
						if self.rect.colliderect(e.rect) and self.status['excited'] == 0:
							self.status['excited']+=1
				if self.universe.level.viking_ship and self.rect.colliderect(self.universe.level.viking_ship.talk_balloon_rect):
						self.get_dirty()
				if self.universe.level.name == "accessory":
					if self.pos[1]+self.size[1]-p(20) > self.universe.level.water_level:
						self.get_dirty()
			else:
				self.status['hurt'] +=1
				if self.status['hurt'] == 40:
					self.status['hurt'] = 0
			if self.status['excited']:
				self.status['excited'] +=1
				action[0] = 'celebrate'
				if self.status['excited'] == 60:
					self.status['excited'] = 0
			if self.status['scared']:
				self.status['scared'] +=1
				action[1] = 'run_away'
				if self.status['scared'] == 60:
					self.status['scared'] = 0
			if self.status['hurt'] and self.status['hurt'] <6:
				action[0]='ouch'
				self.status['excited'] =0
				self.status['scared'] = 0
			if self.status['hurt'] >=6 and action[0] == 'ouch':
				action[0]= None

	def get_dirty(self):
		if self.dirt <= 2:
			self.status['hurt'] += 1
			self.dirt += 1
			self.universe.db_cursor.execute("UPDATE save SET dirt = "+str(self.dirt)+" WHERE name = '"+self.name+"'")
			print "Oh Dear, you've got all dirty! I need to take a record on that..."
			self.universe.level.princesses[1] = self.dirties[self.dirt -1]

	def kissing(self):
		if self.action[0] == 'kiss' and not self.kiss['ongoing']:
			self.kiss['count'] = 'start'
			self.kiss['ongoing'] = True
		if self.kiss['ongoing']:
			if self.kiss['count'].__class__ == str:
				self.kiss['count'] = 1
			else:
				self.kiss['count'] +=1
			if self.kiss['count'] == 1:
				self.kiss_img.number = 0
				self.channel3.play(self.kisssound)
			if self.kiss['count'] < 4:
				if self.action[0] != 'jump':
					self.action[0] = 'kiss'
			else:
				if self.action[0] == 'kiss':
					self.action[0] = None
			if self.kiss['count'] <9:
				self.throwkiss()
			else:
				self.kiss['ongoing'] = False
				self.kiss['count'] = 0
				self.kiss['rect'] = ((0,0),(0,0))

	def update_pos(self,action):
		"""update the position of the princesses on both axis.
		self.center_distance is the absolute distance to the point 0 of the stage.
		self.pos is the position relative to the screen, necessary for blitting
		
		receives universe.action
		no return
		"""
		feet_position= self.pos[1]+self.size[1]
		towards	= {'right':1,'left':-1}
		#Set center distance (relative to the point 0)
		#	move if walking or scared
		if action[1]=='walk' and action[0] != 'celebrate':
			self.center_distance += (self.speed*towards[self.direction])
		elif action[1] == 'run_away':
			boost = p(6)
			if self.center_distance < self.status['danger']:
				self.direction = 'left'
			else:
				self.direction = 'right'
			self.center_distance += ((boost+self.speed)*towards[self.direction])
		#don't move if there is an obstacle
		obstacle = self.universe.floor - self.universe.level.what_is_my_height(self)
		if obstacle <= int(round(feet_position - p(30))):
			if action[1] =='walk':
				self.center_distance -= (self.speed*towards[self.direction])
			elif action[1] == 'run_away':
				self.center_distance -= ((self.speed+boost)*towards[self.direction])
		#Set pos[0] (relative to the screen)
		self.pos[0] = self.universe.center_x+self.center_distance
		#Set y pos
		new_height = self.universe.level.what_is_my_height(self)
		self.floor = self.universe.floor - new_height
		#fall
		if feet_position < self.floor:
			new_y = self.pos[1]+self.gravity['force']
			if new_y+self.size[1] >= self.floor:
				new_y = self.floor-self.size[1]
			self.pos[1] = new_y
			self.gravity['force'] += self.gravity['accel']
		feet_position   = self.pos[1]+self.size[1]
		#do not stay lower than floor
		if feet_position > self.floor:
			self.pos[1]= self.floor-self.size[1]
		if feet_position == self.floor:
			self.gravity['force'] = 0
		
		#Unlocking event
		#TODO: agregate all unlocking events in one spot to ease mainteinance
		if self.universe.stage.name == 'accessory':
			if self.center_distance < p(840) or self.center_distance > p(8550):
				if not self.dirt:
					if self.locked:
						self.universe.level.unlocking = {'type':'shoes','name':'boots'}
					self.locked = False
		
	def soundeffects(self,action):
		"""Control the princess sound effects"""
		if not self.jump and (self.pos[1]+self.size[1]) == self.floor:
			if action[1]=='walk' or action[0] == 'pos[0]celebrate':
				if self.images.number % 6 == 0:
					self.channel1.play(self.steps[random.randint(0,1)])
				if (self.images.number + 3)% 6 == 0:
					self.channel2.play(self.steps[random.randint(2,3)])

	def throwkiss(self):
		"""Control the kiss, its direction, duration, position and so on"""

		#The first frame of the kiss sets its direction and height
		if self.kiss['count'] == 1:
			self.kiss['direction'] = self.direction
			self.kiss['height'] = self.pos[1]

		#D is the differences betwwen left and right
		D = {	'right':{'rect_correction':0,'effect_correction':0},
				'left':	{'rect_correction': p(200)-((self.kiss['count'])*p(44)),'effect_correction':p(200)}}

		#Setting the images and rect. Using D (differences)
		kissimage = self.lips.__dict__[self.kiss['direction']][self.kiss['count']-1]
		self.effects.append(Effect(kissimage, (self.pos[0]-D[self.kiss['direction']]['effect_correction'],self.kiss['height'])))
		self.kiss['rect'] = pygame.Rect(
								(self.pos[0]+D[self.kiss['direction']]['rect_correction'],self.kiss['height']),
								(self.kiss['count']*p(44),self.size[1])
							)

	def update_image(self,action,direction):
		"""Controls the princess images
		
		Princess images changes according to the action.
		Not all the universe actions affects the princess.
		The name of the image correspond to the name of the action plus '_img'.
		self.past_choice keeps the previous action in order to use it if there is no action to use in the present frame.
		"""

		self.rect = pygame.Rect((self.pos[0]+(self.image_size[0]/2),self.pos[1]-1), self.size)

		#filter actions that does not affects the princess
		if action[0] != 'OK':
			chosen = action[0] or action[1]
		else:
			chosen = self.past_choice
		if direction.__class__ != str:
			direction = "right"
		self.images = 		self.__dict__[chosen+'_img']
		actual_images =		self.__dict__[chosen+'_img'].__dict__[direction]
		self.image = actual_images[self.images.number]
		if chosen != self.past_choice:
			self.__dict__[chosen+'_img'].number = 0
		self.past_choice = chosen
		if not self.jump:
			self.images.update_number()

	def change_clothes(self,part,dir):
		self.parts.pop(part.index)
		part = PrincessPart(self,directory.princess+str(dir),part.index)


class Dirt():
	image_number = 0
	def __init__(self, universe, directory,pos):
		self.universe = universe
		self.directory = directory
		for act in ['walk','stay','kiss','fall','jump','ouch','celebrate']:
			self.__dict__[act] = utils.img.TwoSided(directory+'/'+act+'/')
		self.run_away = utils.img.Ad_hoc(self.walk.left[::2],self.walk.right[::2])
		self.open_door = self.stay
		self.list = self.stay
		self.actual_list = self.list.left
		self.pos = pos
		self.image = self.actual_list[self.image_number]
		self.past_choice = None

	def update_all(self):
		P = self.universe.level.princesses[0]
		self.pos = P.pos
		direction = P.direction
		if P.action[0] != 'OK':
			chosen = P.action[0] or P.action[1]
		else:
			chosen = self.past_choice
		if direction.__class__ != str:
			direction = "right"
		
		self.images = self.__dict__[chosen]
		actual_images = self.__dict__[chosen].__dict__[direction]
		if chosen != self.past_choice:
			self.__dict__[chosen].number = 0
		self.past_choice = chosen
		self.image = actual_images[self.images.number]
		if not P.jump:
			self.images.update_number()

class Effect():
	def __init__(self,image,position):
		self.image	  = image
		self.position   = self.pos = position
