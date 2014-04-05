import scenario.scenarios   as scenarios
import utils
import interactive.enemy as enemy
import scenario.skies as skies
import interactive.fairy as fairy
import scenario.floors as floors
import interface.widget as widget
import random
import scenario.moving_scenario as moving_scenario
import interface.glamour_stars as glamour_stars
import interactive.princess as princess
import os
import interface.game_clock as game_clock
import pygame
import interactive.camera as camera
import interface.inside as inside
import interface.ball as ball
import database
import database.query
import database.update
import interactive.events   as events
import settings
from settings import directory
import gc
p = settings.p
d = settings.d
j = os.path.join
from settings import t

###Gate Positions###
bathhousegate = p([480, 8138])
dressgate =	 p([800, 4142,8471])
accessorygate = p([1497,4174,7836])
makeupgate =	p([1200,4661,8231])
shoegate =	  p([1198,4690,8140])


class Stage():
	princesses = None
	def __init__(self,universe):
		self.name = None
		self.size = p(9600)
		self.universe = universe
		self.cameras=[camera.GameCamera(universe,p(-4220))]
		self.gates= []
		self.clock= [game_clock.GameClock(universe),game_clock.ClockPointer(universe)]
		self.floor_heights= {}
		self.floor= universe.floor-p(186)
		self.menus= []
		self.panel= [None,None,glamour_stars.Glamour_Stars(universe)]
		self.pointer= [self.universe.pointer]
		self.scenarios_front= []
		self.animated_scenarios =[]
		self.blitlist= ('sky', 'background', 'moving_scenario', 'scenarios', 'animated_scenarios' ,'gates',  'lights', 'princesses','enemies', 'menus')
		self.foreground	 = []
		self.white = Foreground(universe)
		self.black = Foreground(universe, color=(0,0,0), path= j(directory.loading,'back.png'))
		self.bar = {'down': Bar(universe,'down'), 'up': Bar(universe,'up'), 'left': Bar(universe,'left'), 'right': Bar(universe,'right')}
		self.bar_goal	   = self.universe.height/3
		self.bar_speed	  = 1
		self.inside		 = None
		self.princess_castle= None
		self.fairy		  = False
		self.omni_directory = directory.omni
		self.ball		   = None
		self.ballroom = {'day': scenarios.Background(110,universe,j(directory.scenario,'ballroom','ballroom_day')),
						'night':scenarios.Background(110,universe,j(directory.scenario,'ballroom','ballroom_night'))}
		self.event_counter  = 0
		self.starting_game  = True
		self.fae = [None,fairy.Fairy(20,universe)]
		self.pause			= Pause(universe)
		self.paused			= False
		self.water_level	= p(1440)
		self.exit_sign		= None
		self.loading_icons  = (utils.img.OneSided(j(directory.loading,'sun_n_moon_shadow')),
							   utils.img.OneSided(j(directory.loading,'sun_n_moon')),
							   utils.img.OneSided(j(directory.loading,'carriage'))
							   )
		self.margin = utils.img.image(j(directory.images,'shadow-B.png'))
		self.enemy_channel = pygame.mixer.Channel(6)
		self.unlocking = False
		self.big_princess = None

	def pause_game(self):
		return inside.Pause(self.universe)

	def what_is_my_height(self,object,pos_x = None):
		try:
			y_height = self.floor_heights[(pos_x or int(object.center_distance+round(object.size[0]/2)) )]
		except:
			y_height = self.floor
		return	  y_height

	def update_all(self):
		events.choose_event(self.universe)
		self.act = self.universe.action
		self.direction = self.universe.dir
		self.blit_all()
		if self.black.alpha_value > 0:
			self.changing_stages_darkenning(-1)
		if self.paused:
			self.update_pause()
		elif self.fairy and not self.princesses[0].inside and not self.ball:
			self.update_fairytip()
		else:
			if self.clock[1].count > 160:
				if self.background[0] == self.ballroom['day']:
					self.background = [self.ballroom['night']]
			else:
				if self.background[0] == self.ballroom['night']:
					self.background = [self.ballroom['day']]
			if self.clock[1].time == 'ball' and not self.princesses[0].inside:
				if self.enemy_channel.get_sound():
					self.enemy_channel.fadeout(1500)
				self.enemy_channel
				self.ball = self.ball or ball.Ball(self.universe, self.princesses[0])
				self.ball.update_all()
			else:
				if self.ball:
					self.ball = None
				self.cameras[0].update_all()
				self.universe.movement(self.direction)
				self.update_unlocking()

				if not self.inside or (self.inside.status != "choosing") or not self.princesses[0].inside:
					for att in self.blitlist:
						if att == 'lights':
							if self.clock[1].time == 'night':
								for i in self.lights:
									if i['status'] == 'on':
										i['position'].update_pos()
									if i['status'] == 'off' and random.randint(0,10) == 0:
										i['status'] = 'on'
										i['position'].update_pos()
						else:
							for i in self.__dict__[att]:
								if i:
									i.update_all()
					self.enemy_music()
				for i in self.scenarios_front+self.floor_image+self.foreground:
					i.update_all()
				if self.princesses[0].inside:
					self.update_insidebar()
				if not self.inside or (not self.inside.status == "choosing") or not self.princesses[0].inside:
					for i in self.clock:
						i.update_all()
				[i.update_all() for i in self.panel if i]
				self.exit_sign.update_all()
		if not pygame.mixer.music.get_busy():
			if self.music:
				pygame.mixer.music.load(self.music)
				pygame.mixer.music.play(-1)
		for i in self.pointer:
			i.update_all()

	def update_unlocking(self):
		if self.unlocking:
			if not self.princesses[0].inside:
				for i in self.unlocking['list']:
					i.update_all()
				self.event_counter += 1
				if self.event_counter > 210:
					self.unlocking = False
					self.event_counter = 0
		else:
			self.event_counter = 0

	def blit_all(self):
		screen = self.universe.screen_surface
		if not self.ball:
			for att in self.blitlist:
				if att == 'lights':
					if self.clock[1].time == 'night':
						for i in self.lights:
							if i['status'] == 'on':
								screen.blit(i['images'].list[i['images'].itnumber.next()],i['position'].pos)
				else:
					for i in self.__dict__[att]:
						if i and i.image:
							screen.blit(i.image,i.pos)
			for i in self.princesses[0].effects :
				screen.blit(i.image,i.pos)
			for i in self.scenarios_front:
				screen.blit(i.image,i.pos)
			if self.exit_sign.image:
				screen.blit(self.exit_sign.image, self.exit_sign.pos)
			for i in self.floor_image:
				screen.blit(i.image,i.pos)
			for i in self.foreground:
				screen.blit(i.image,i.pos)
			if self.sky[0].night_image:
				screen.blit(self.sky[0].night_image,(0,0))
			for i in self.clock:
				screen.blit(i.image,i.pos)
			for i in self.panel:
				if i:
					screen.blit(i.image,i.pos)
			if self.fairy:
				for i in self.fae:
					screen.blit(i.image,i.pos)
			if self.unlocking:
				if 'list' in self.unlocking:
					for i in self.unlocking['list']:
						screen.blit(i.image,i.pos)
			if self.princesses[0].inside:
				self.blit_inside(screen)
			if self.paused:
				self.blit_paused(screen)
			elif self.fairy and not self.princesses[0].inside and not self.ball:
				screen.blit(self.white.image,(0,0))
				if self.fairy == "speaking":
					for i in self.fae:
						screen.blit(i.image,i.pos)
		else:
			self.blit_ball(screen)
		for i in self.pointer:
			screen.blit(i.image,i.pos)
		screen.blit(self.margin,(0,0))

	def blit_inside(self, screen):
		screen.blit(self.white.image,(0,0))
		screen.blit(self.bar['down'].image,(0,self.bar['down'].pos))
		screen.blit(self.bar['up'].image,(0,self.bar['up'].pos))
		if self.inside.status == 'choosing':
			[screen.blit(i.image,i.pos) for i in self.inside.items]
			if self.big_princess:

				if self.inside.type_of_items == "shower":
					position = ((self.universe.width/2)-p(200),p(270))
				else:
					position = p((20,270))
				screen.blit(self.big_princess, position)

				[screen.blit(i.image,i.pos) for i in self.inside.buttons]
			if self.inside.__class__== inside.Inside:
				if self.inside.chosen_item:
					screen.blit(self.inside.chosen_item.image,self.inside.chosen_item.pos)

			elif self.inside.__class__==inside.Home:
				pos  = 500
				for img in self.inside.past_balls:
					screen.blit(img, p([pos,400]))
					pos +=200
			try:
				x = p(880,r=False)
				y = p(270,r=False)
				screen.blit(self.inside.princess_image, (x,y))
			except:
				pass
			self.keyboard_selection(self.inside)

	def blit_paused(self,screen):
		u = self.universe
		princess=self.princesses[0]
		screen.blit(self.white.image,(0,0))
		screen.blit(self.bar['down'].image,(0,self.bar['down'].pos))
		screen.blit(self.bar['up'].image,(0,self.bar['up'].pos))
		if self.pause.status == 'choosing' and not self.pause.closet:
			for i in self.pause.buttons :
				screen.blit(i.image, i.pos)
				if princess.image:
					screen.blit(princess.image, ((u.width/2)-(princess.image_size[0]/2),(u.height/2)-(princess.image_size[1]/2)))
		if self.pause.closet:
			screen.blit(self.pause.closet, (0,0))
			for i in self.pause.unlocked_items:
				screen.blit(i.image,i.pos)
				if i.__class__ == Closet_Icon and i.imagetxt:
					screen.blit(i.imagetxt.image,i.imagetxt.pos)
			screen.blit(self.pause.close_closet.image,self.pause.close_closet.pos)

	def blit_ball(self,screen):
		screen.blit(self.ball.background,(0,0))
		for i in self.ball.dancers:
			screen.blit(i.image,i.position)
		if self.ball.counter > self.ball.delay:
			screen.blit(self.ball.foreground, (0,0))
		screen.blit(self.ball.Frame.image,self.ball.Frame.position)
		screen.blit(self.ball.Bar.image,self.ball.Bar.position)
		if self.ball.counter > self.ball.delay:
			screen.blit(self.ball.bigprincess.image,self.ball.bigprincess.pos)
		if self.ball.counter > self.ball.delay+20:
			for i in self.ball.texts:
				screen.blit(i.image,i.pos)
		if self.ball.boyfriend:
			if self.ball.counter > self.ball.delay+110:
				screen.blit(self.ball.boyfriend.image,self.ball.boyfriend.pos)
		if self.ball.counter > self.ball.delay+130:
			for i in self.ball.buttons:
				screen.blit(i.image,i.pos)
		screen.blit(self.ball.universe.level.margin,(0,0))
		screen.blit(self.ball.universe.level.black.image,(0,0))

	def update_insidebar(self):
		if self.inside.status == 'inside':
			self.bar['up'].pos = -self.bar['up'].size[1]
			self.bar['down'].pos = self.universe.height
			self.white.alpha_value = 0
			self.inside.status = 'loading'
		elif self.inside.status == 'loading':
			pygame.mixer.music.fadeout(1500)
			self.white.image.set_alpha(self.white.alpha_value)
			if self.white.alpha_value < 200:
				self.white.alpha_value += 10
			if self.bar['down'].pos > 2*self.bar_goal:
				self.bar['down'].pos -= self.bar_speed
			if self.bar['up'].pos + self.bar['up'].size[1]< self.bar_goal:
				self.bar['up'].pos += self.bar_speed
			if self.bar_speed < p(20,r=False):
				self.bar_speed += self.bar_speed
			if self.white.alpha_value > 150:
				self.inside.status = 'choosing'
				pygame.mixer.music.load(self.inside.music)
				pygame.mixer.music.play(-1)
		elif self.inside.status == 'choosing':
			self.princesses[0].update_all()
			[i.update_all() for i in self.inside.items]
			[i.update_all() for i in self.inside.buttons if i.__class__ == widget.Button]

		elif self.inside.status == 'done':
			pygame.mixer.music.fadeout(1500)
			self.princesses[0].update_all()
			self.bar['down'].pos += self.bar_speed
			self.bar['up'].pos -= self.bar_speed
			if self.bar_speed < p(20,r=False):
				self.bar_speed += self.bar_speed
			if self.white.alpha_value > 0:
				self.white.alpha_value -= 10
				self.white.image.set_alpha(self.white.alpha_value)
			else:
				self.white.alpha_value = 0
			self.white.image.set_alpha(self.white.alpha_value)
			if self.bar['down'].pos > self.universe.height and self.bar['up'].pos < -self.bar['up'].size[1] and self.white.alpha_value == 0:
				pygame.mixer.music.load(self.music)
				pygame.mixer.music.play(-1)
				self.inside.status = 'openning'
		elif self.inside.status == 'openning':
			self.princesses[0].update_all()
			for i in self.gates:
				if i.rect.colliderect(self.princesses[0].rect):
					i.open = True
					if i.images.number >= i.images.lenght -1:
						self.inside.status = 'closing'
		elif self.inside.status == 'closing':
			print 'Getting out of the door'
			for i in self.gates:
				if i.rect.colliderect(self.princesses[0].rect):
					i.outside()
			self.inside.status = 'outside'
			self.princesses[0].inside = False


	def enemy_music(self):
		enemies_arround = []
		classes_arround = []
		now_playing = self.enemy_channel.get_sound()
		weight = 0
		actual_class = None
		for i in self.enemies:
			if i.music:
				if d(i.pos[0]) > 1440:
					distance = d(i.pos[0])-1440
				elif d(i.pos[0]) < d(i.real_size[0]):
					distance = (d(i.pos[0])+d(i.real_size[0]))*-1
				else:
					distance = 0
				if distance < 500:
					enemies_arround.append(i)
					if i.__class__ not in classes_arround:
						classes_arround.append(i.__class__)
		for i in classes_arround:
			if i.music:
				if i.music['weight'] > weight or i.music['sound'] == now_playing:
					weight = i.music['weight']
					actual_class = i
		for i in classes_arround:
			distance = 1100
			for ii in enemies_arround:
				if ii.__class__ == i:
					if d(ii.pos[0]) > 1440:
						thisdistance = d(ii.pos[0])-1440
					elif d(ii.pos[0])< -d(ii.real_size[0]):
						thisdistance = (d(ii.pos[0])+d(ii.real_size[0]))*-1
					else:
						thisdistance = 0
					if thisdistance < distance:
						distance = thisdistance
			if distance < 500 and i == actual_class:
				if now_playing != i.music['sound']:
					self.enemy_channel.play(i.music['sound'])
				if distance > 0:
					volume = 1-(distance/500)
				else:
					volume = 1
				if volume<=1:
					present_volume = self.enemy_channel.get_volume()
					if volume-present_volume > 0.05:
						self.enemy_channel.set_volume(present_volume+0.05)
					elif volume-present_volume<-0.05:
						self.enemy_channel.set_volume(present_volume-0.05)
					else:
						self.enemy_channel.set_volume(volume)
				if 1-volume < 0.6:
					present_volume = pygame.mixer.music.get_volume()
					if (1-volume)-present_volume > .05:
						pygame.mixer.music.set_volume(present_volume +.05)
					elif (1-volume)-present_volume< -.05:
						pygame.mixer.music.set_volume(present_volume -.05)
					else: 
						pygame.mixer.music.set_volume(1-volume)
		for i in self.enemies:
			if i.music and i.music['sound'] == now_playing:
				if i.__class__ != actual_class:
					i.music['sound'].stop()

	def keyboard_selection(self, inside):
		if self.universe.action[1] == 'walk':
			if self.universe.dir == 'right':
				inside.chosen_number+=1
			elif self.universe.dir == 'left':
				inside.chosen_number-=1
			if inside.chosen_number>=len(inside.menu):
				inside.chosen_number = 0
			elif inside.chosen_number<0:
				inside.chosen_number = len(inside.menu)-1
			pygame.mouse.set_pos(inside.menu[inside.chosen_number])

	def choice_screen(self, screen,condition):
		if screen.status == 'inside':
			pygame.mixer.music.fadeout(1500)
			self.bar['up'].pos = -self.bar['up'].size[1]
			self.bar['down'].pos = self.universe.height
			self.white.alpha_value = 0
			screen.status = 'loading'
		elif screen.status == 'loading':
			self.white.image.set_alpha(self.white.alpha_value)
			if self.white.alpha_value < 200:
				self.white.alpha_value += 10
			if self.bar['down'].pos > 2*self.bar_goal:
				self.bar['down'].pos -= self.bar_speed
			if self.bar['up'].pos + self.bar['up'].size[1]< self.bar_goal:
				self.bar['up'].pos += self.bar_speed
			if self.bar_speed < p(20,r=False):
				self.bar_speed += self.bar_speed
			if self.white.alpha_value > 150:
				screen.status = 'choosing'
				pygame.mixer.music.load(screen.music)
				pygame.mixer.music.play(-1)
		elif screen.status == 'choosing':
			pass
		elif screen.status == 'done':
			pygame.mixer.music.fadeout(1500)
			self.bar['down'].pos += self.bar_speed
			self.bar['up'].pos -= self.bar_speed
			if self.bar_speed < p(20,r=False):
				self.bar_speed += self.bar_speed
			if self.white.alpha_value > 0:
				self.white.alpha_value -= 10
				self.white.image.set_alpha(self.white.alpha_value)
			else:
				self.white.alpha_value = 0
			self.white.image.set_alpha(self.white.alpha_value)
			if self.bar['down'].pos > self.universe.height and self.bar['up'].pos < -self.bar['up'].size[1] and self.white.alpha_value == 0:
				pygame.mixer.music.load(self.music)
				pygame.mixer.music.play(-1)
				screen.status = 'finished'

	def update_pause(self):
		princess = self.princesses[0]
		self.choice_screen(self.pause,self.paused)
		if self.enemy_channel.get_sound():
			self.enemy_channel.fadeout(1500)
		if self.pause.closet:
			for i in self.pause.unlocked_items:
				i.update_all()
			self.pause.close_closet.update_all()
		else:
			if self.pause.status == 'choosing':
				for i in self.pause.buttons:
					i.update_all()
				if self.fairy:
					for i in self.fae:
						i.update_all()
				self.keyboard_selection(self.pause)
			elif self.pause.status == 'done':
				pass
			elif self.pause.status == 'finished':
				self.pause.status = 'outside'
				self.paused = False

	def update_fairytip(self):
		pymusic = pygame.mixer.music
		if self.fairy == 'loading':
			self.white.image.set_alpha(self.white.alpha_value)
			if self.white.alpha_value < 200:
				self.white.alpha_value += 50
				volume = pymusic.get_volume()
				if 0.6 >= volume > 0.1:
					volume -= .01
					pymusic.set_volume(volume)
			if self.white.alpha_value > 150:
				self.fairy = 'speaking'
		elif self.fairy == "speaking":
			if self.universe.action[0] == 'OK':
				self.fae[0].end_message()
			for i in self.fae:
				i.update_all()
		elif self.fairy == 'done':
			self.princesses[0].update_all()
			if self.bar_speed < p(20):
				self.bar_speed += self.bar_speed
			if self.white.alpha_value > 0:
				volume = pymusic.get_volume()
				if .6 >= volume >= 0: 
					volume += .01
					if volume >.6:
						volume=.6
					pymusic.set_volume(volume)
				self.white.alpha_value -= 50
				self.white.image.set_alpha(self.white.alpha_value)
			else:
				self.white.alpha_value = 0
				self.fairy = None
			self.white.image.set_alpha(self.white.alpha_value)

	def select_enemies(self, allowed_enemies, street):
		self.enemies = []
		universe_cursor = self.universe.db_cursor
		row	 = universe_cursor.execute("SELECT * FROM stage_enemies WHERE stage = '"+street+"'").fetchone()
		enemy.Butterfly._registry = []
		for e in allowed_enemies:
			if int(row[e]):
				name = e.replace('_',' ').title()
				name = name.replace(' ','')
				if name == 'Footboy':
					name = 'FootBoy'
				maximum = 1
				if name in ("Butterfly" , "Bird") :
					maximum = 2+int(self.princesses[0].points/50)
					if maximum > 20:
						maximum = 20
				for i in range(0,random.randint(1,maximum)):
					pos_x = p(random.randint(1400,7000),r=False)
					self.enemies.append(enemy.__dict__[name](pos_x,self.universe))
			self.loading()

	def loading(self):
		if self.black.alpha_value > 100:
			self.universe.screen_surface.blit(self.black.image,(0,0))
			shadow = self.loading_icons[0]
			world = self.loading_icons[1]
			carriage = self.loading_icons[2]
			world_pos =   ((self.universe.width/2)-(world.size[0]/2), (self.universe.height/2)-(world.size[1]/2))
			carriage_pos = (world_pos[0]+p(182,r=False),world_pos[1]+p(75,r=False))
			for i in self.loading_icons:
				i.update_number()
			self.universe.screen_surface.blit(shadow.list[world.number],(world_pos[0],(world_pos[1]+p(60,r=False))))
			self.universe.screen_surface.blit(world.list[world.number],world_pos)
			self.universe.screen_surface.blit(carriage.list[carriage.number],carriage_pos)
			self.universe.screen_surface.blit(self.bar['left'].image,(self.bar['left'].pos,0))
			self.universe.screen_surface.blit(self.bar['right'].image,(self.bar['right'].pos,0))
			pygame.display.flip()

	def bring_side_bars(self,darkenning):
		self.universe.screen_surface.blit(self.black.image,(0,0))
		self.universe.screen_surface.blit(self.bar['left'].image,(self.bar['left'].pos,0))
		self.universe.screen_surface.blit(self.bar['right'].image,(self.bar['right'].pos,0))
		if self.bar['left'].pos < 0-(self.bar['left'].size[0]/5):
			self.bar['left'].pos += self.bar_speed
		else:
			self.bar['left'].pos = 0-(self.bar['left'].size[0]/5)
		if self.bar['right'].pos > self.universe.width-(self.bar['right'].size[0]-(self.bar['right'].size[0]/5) ):
			self.bar['right'].pos -= self.bar_speed
		else:
			self.bar['right'].pos = self.universe.width-(self.bar['right'].size[0]-(self.bar['right'].size[0]/5) )
		if self.bar_speed < p(20,r=False):
			self.bar_speed += self.bar_speed
		self.black.alpha_value += (5*darkenning)
		self.black.image.set_alpha(self.black.alpha_value)
		self.universe.clock.tick(self.universe.fps)
		pygame.display.flip()

	def changing_stages_darkenning(self,darkenning=1):
		self.bar['left'].pos = -self.bar['left'].size[0]
		self.bar['right'].pos = self.universe.width
		self.universe.screen_surface.blit(self.black.image,(0,0))
		if darkenning > 0:
			pygame.display.flip()
			while self.black.alpha_value<255:
				self.bring_side_bars(darkenning)
		if self.black.alpha_value > 255:
			self.black.alpha_value = 255
		elif self.black.alpha_value < 0:
			self.black.alpha_value = 0
		self.black.image.set_alpha(self.black.alpha_value)
		self.black.alpha_value += (10*darkenning)

	def create_scenario(self,street):
		self.bar['up'].pos = -self.bar['up'].size[1]
		self.bar['down'].pos = self.universe.height
		self.loading()
		self.viking_ship = None
		self.loading()
		self.scenarios_prep = []
		#while creating Big Scenario, the list above is filled so that it is possible to include the lights
		self.scenarios = (BigScenario(self.universe, street),)
		self.lights = []
		for i in self.scenarios_prep:
			try:
				if i.lights:
					self.lights.append(i.lights)
			except:
				pass
			self.loading()
		self.scenarios_prep = []
		self.sky			 = [skies.Sky(self.universe)]
		self.clouds			=   [scenarios.Cloud(self.universe) for cl in range(3)]
		self.loading()
		[self.sky[0].image.blit(i.image,i.pos) for i in self.clouds]
		self.clouds = []
		self.loading()
		gc.collect()

	def create_front_scenario(self,street):
		front_row = database.query.street(self,street,'front_scenario')
		self.scenarios_front = []
		for i in front_row:
			if i['type'] == 'scenario':
				if i['height'] == 0:
					self.scenarios_front.append(scenarios.Scenario(p(i['xpos'],r=0),j(directory.main,i['directory']),self.universe))
				else:
					self.scenarios_front.append(scenarios.Scenario(p(i['xpos'],r=0),j(directory.main,i['directory']),self.universe,height = p(i['height'])))
			elif i['type'] == 'flower':
				self.scenarios_front.append(scenarios.Flower(p(i['xpos'],r=0),j(directory.main,i['directory']),self.universe,i['frames']))
			elif i['type'] == 'frontscenario':
				self.scenarios_front.append(scenarios.Scenario(p(i['xpos'],r=0),j(directory.main,i['directory']),self.universe,i['ind']))
			self.loading()

	def set_floor_heights(self,height,width,street):
		self.floor_heights = [p(height)]*int(p(width))
		for row in database.query.street(self.universe, street, 'floor'):
			for r in range(int(p(int(row['start']))),int(p(int(row['end'])))):
				self.floor_heights[r]=p(row['value'],r=False)
		self.loading()

	def stage_music(self, music=None,intro=None):
		pygame.mixer.music.fadeout(4000)
		self.music = j(directory.music,music)
		if not intro:
			pygame.mixer.music.load(j(directory.music,music))
		else:
			pygame.mixer.music.load(j(directory.music,intro))
			self.loading()
			pygame.mixer.music.queue(j(directory.music,music))
		pygame.mixer.music.set_endevent(pygame.USEREVENT)
		pygame.mixer.music.set_volume(.6)
		self.loading()
		pygame.mixer.music.play()

	def create_stage(self,translatable_name,goalpos,hardname):
		if self.enemy_channel.get_sound():
			self.enemy_channel.fadeout(1500)
		self.changing_stages_darkenning()
		self.loading()
		self.name = hardname
		self.princesses = self.princesses or [princess.Princess(self.universe),None]
		if self.name not in self.princesses[0].visited_streets:
			self.princesses[0].visited_streets.append(self.name)
			if len(self.princesses[0].visited_streets)==5:
				if database.query.is_locked(self.universe,'shoes','flower'):
					self.unlocking = {'type':'shoes','name':'flower'}
		self.animated_scenarios = []
		self.loading()
		if goalpos:
			self.princesses[0].center_distance = goalpos
			self.universe.center_x = -goalpos+(self.universe.width/2)
		self.gates = []
		self.directory = j(directory.scenario,hardname+'_st/')
		self.background = [self.ballroom['day']]
		self.loading()
		self.moving_scenario = [moving_scenario.Billboard(self.universe)]
		self.loading()
		self.animated_scenarios =[]
		self.exit_sign  = self.exit_sign or scenarios.ExitSign(self.universe)
		self.loading()
		self.create_scenario(hardname)
		self.create_front_scenario(hardname)
		self.panel = [widget.GameText(self.universe, t(translatable_name), (300,20)),
			None,
			glamour_stars.Glamour_Stars(self.universe),
			widget.GameText(self.universe, self.princesses[0].name, (660,47),main_font=settings.second_font),
			glamour_stars.Lil_Star_Back(self.universe,(1020,0)),
			glamour_stars.Lil_Stars(self.universe, (1030,10)),
			widget.GameText(self.universe, str(self.princesses[0].points), (1000,20))
		]


	def BathhouseSt(self,goalpos = None, clean_princess = False):
		self.set_floor_heights(186,9400,'bathhouse')
		self.create_stage(t('Bathhouse St'),goalpos,'bathhouse')
		gates = ( [(1063,453),'bathhouse/door/',	inside.Inside(self.universe,'shower', []),True],
			  [(5206,500),'home/door/', 		inside.Home(self.universe), False], 
			  [(9305,503),'magic_beauty_salon/door/',inside.Inside(self.universe,'hair',database.query.unlocked(self.universe,'hair','garment',4)),False])
		self.loading()
		doors = (   [bathhousegate[0], self.ShoesSt,shoegate[2]],
					[bathhousegate[1], self.AccessorySt, accessorygate[0]])
		self.loading()
		self.gates = [scenarios.BuildingDoor(p(i[0]),j(self.directory,i[1]),self.universe,i[2],bath=i[3]) for i in gates]
		self.loading()
		self.gates.extend([scenarios.Gate(i[0], self.universe,i[1], goalpos = i[2]) for i in doors])
		self.loading()
		self.select_enemies(('schnauzer', 'butterfly', 'old_lady', 'footboy', 'bird'),'BathhouseSt')
		self.floor_image= [floors.Floor(c,j(self.directory,'floor','tile'),self.universe) for c in range(24)]
		self.loading()
		floors.Bridge(j(self.directory,'floor','japanese_bridge'),5,self.universe)
		self.loading()
		self.stage_music("bathhouse.ogg")
		self.loading()
		if self.starting_game:
			events.choose_event(self.universe,starting_game=True)
			self.starting_game = False
		if clean_princess:
			self.princesses[0].dirt = 0
			database.update.clean_up(self.universe)
			print "You look lovely all cleaned up!"
			self.princesses[1] = None

	def DressSt(self,goalpos = None):
		self.create_stage(t('Dress St'), goalpos,'dress')
		self.animated_scenarios = [scenarios.Scenario(0,j(self.directory,'Dress_Tower','flag'),self.universe)]
		self.loading()
		self.select_enemies(('schnauzer', 'butterfly', 'old_lady', 'footboy', 'bird','carriage'),'DressSt')
		self.gates = [scenarios.BuildingDoor(p((155,318)),j(self.directory,'Dress_Tower','door'),self.universe,inside.Inside(self.universe,'dress',database.query.unlocked(self.universe, 'dress', 'garment',4))),
					  scenarios.BuildingDoor(p((9180,430)),j(self.directory,'snow_white_castle','door'),self.universe, inside.Princess_Home(self.universe,settings.Snow_White)),
					  scenarios.Gate(dressgate[0], self.universe, self.AccessorySt,goalpos = accessorygate[2]),
					  scenarios.Gate(dressgate[1], self.universe, self.ShoesSt,goalpos = shoegate[1]),
					  scenarios.Gate(dressgate[2], self.universe, self.MakeupSt,goalpos = makeupgate[0])]
		self.loading()
		self.floor_image= [floors.Floor(c,j(self.directory,'floor'),self.universe) for c in range(30)]
		self.loading()
		self.stage_music("snow-white.ogg")
		self.set_floor_heights(185,9400,'dress')

	def AccessorySt(self,goalpos = None):
		self.create_stage(t('Accessory St'), goalpos,'accessory')
		self.select_enemies(('schnauzer', 'butterfly', 'old_lady', 'bird'),'AccessorySt')
		self.viking_ship = enemy.VikingShip(self.universe)
		self.loading()
		self.gates = ([
			scenarios.BuildingDoor(p((330,428)),j(self.directory,'accessory_tower','door'),self.universe,inside.Inside(self.universe,'accessory',database.query.unlocked(self.universe,'accessory','garment',4))),
			scenarios.BuildingDoor(p((8809,425)),j(self.directory,'castle','door'),self.universe,inside.Princess_Home(self.universe, settings.Cinderella)),
			scenarios.Gate(accessorygate[0], self.universe,self.BathhouseSt,goalpos = bathhousegate[1]),
			scenarios.Gate(accessorygate[1], self.universe,self.MakeupSt,goalpos = makeupgate[1]),
			scenarios.Gate(accessorygate[2], self.universe,self.DressSt , goalpos = dressgate[0])
						])
		self.loading()
		self.floor_image= [floors.Floor(fl,j(self.directory,'floor','tile'),self.universe) for fl in range(30)]
		self.loading()
		self.floor_image.extend([floors.Water(wat,j(self.directory,'water','tile'),self.universe) for wat in range(11)])
		self.loading()
		self.floor_image.extend([self.viking_ship])
		self.loading()
		self.floor_image.extend([floors.Water2(wat,j(self.directory,'water','tile'),self.universe) for wat in range(11)])
		self.loading()
		[floors.Drain(j(self.directory,'floor',i[0]+'_bank_front'),i[1],self.universe) for i in [('left',2),('right',3),('left',20),('right',21)]]
		self.loading()
		self.stage_music("cinderella.ogg")
		self.set_floor_heights(194,9400,'accessory')

	def MakeupSt(self,goalpos = None):
		self.create_stage(t('Makeup St'),goalpos,'makeup')
		self.select_enemies(('carriage','schnauzer', 'butterfly', 'old_lady', 'footboy', 'bird'),'MakeupSt')
		self.gates.extend([ scenarios.Gate(makeupgate[x],self.universe,y,goalpos = z)
							for x,y,z in
							((0, self.DressSt, dressgate[2]),
							 (1, self.AccessorySt, accessorygate[1]),
							 (2, self.ShoesSt ,shoegate[0]))
							])
		self.loading()
		self.gates.extend([scenarios.BuildingDoor(p((130,225)),j(self.directory,'make-up_castle','door'),self.universe,inside.Inside(self.universe,'face',database.query.unlocked(self.universe,'face','garment',4))),
					 scenarios.BuildingDoor(p((9082,301)),j(self.directory,'sleeping_castle','door'),self.universe,inside.Princess_Home(self.universe,settings.Sleeping_Beauty))])
		self.loading()
		self.floor_image= [floors.Floor(fl,j(self.directory,'floor'),self.universe) for fl in range(30)]
		self.loading()
		available_animals = random.sample( (enemy.Lion, enemy.Monkey, enemy.Elephant, enemy.Penguin, enemy.Giraffe), 3 )
		self.animated_scenarios = [ i(self.universe) for i in available_animals]
		self.loading()
		self.animated_scenarios.append(scenarios.Scenario(p(2923,r=0),j(self.directory,'zoo','base'),self.universe))
		self.loading()
		tail = None
		if enemy.Lion in available_animals:
			for i in self.animated_scenarios:
				if i.__class__ == enemy.Lion:
					tail = True
				break
		if tail:
			self.animated_scenarios.insert(1,i.tail)
		self.loading()
		self.set_floor_heights(192,9400,'makeup')
		self.loading()
		self.stage_music("sleeping-beauty.ogg")

	def ShoesSt(self,goalpos=None):
		self.create_stage(t('Shoes St'),goalpos,'shoes')
		self.animated_scenarios = [scenarios.Scenario(p(7137,r=0),j(self.directory,'fountain','base'),self.universe)]
		self.loading()
		self.select_enemies(('carriage','schnauzer', 'butterfly', 'old_lady', 'footboy', 'bird'),'ShoesSt')
		self.gates = [scenarios.BuildingDoor(p((372,273)),j(self.directory,'shoes_tower','door'),self.universe,inside.Inside(self.universe,'shoes',database.query.unlocked(self.universe,'shoes','garment',4))),
		scenarios.BuildingDoor(p((9440,374)),j(self.directory,'rapunzel_castle','door'),self.universe,inside.Princess_Home(self.universe, settings.Rapunzel)),
		scenarios.Gate(shoegate[0],self.universe,self.MakeupSt, goalpos = makeupgate[2]),
		scenarios.Gate(shoegate[1],self.universe,self.DressSt,  goalpos = dressgate[1]),
		scenarios.Gate(shoegate[2],self.universe,self.BathhouseSt, goalpos = bathhousegate[0]),]
		self.floor_image= [floors.Floor(c,j(self.directory,'floor'),self.universe) for c in range(30)]
		self.loading()
		self.stage_music("rapunzel.ogg")
		self.set_floor_heights(192,9601,'shoes')
		self.loading()

class Foreground():
	def __init__(self,universe, color=(255,255,255), path=None):
		self.pos = 0,0
		if path:
			self.image = utils.img.image(path, alpha = False)
		else:
			self.image = pygame.Surface((universe.width,universe.height)).convert()
			self.image.fill(color)
		self.alpha_value = 0
		self.image.set_alpha(self.alpha_value)
		self.status = None

	def update_all(self):
		pass

class Bar():
	def __init__(self,universe, up_or_down):
		if up_or_down in ('left','right'):
			if up_or_down == 'left':
				self.image = utils.img.image(j(directory.left_bar,'0.png'))
				self.size = self.image.get_size()
				self.pos = -self.size[0]
			else:
				self.image = utils.img.image(j(directory.left_bar,'0.png'),invert=True)
				self.size = self.image.get_size()
				self.pos = universe.width
		else:
			tile = utils.img.image(j(directory.omni_interface,'small_bar','0.png'))
			if up_or_down == 'up':
				tile = pygame.transform.flip(tile,0,1)
				self.pos = -tile.get_height()
			else:
				self.pos = universe.height
			screen_size = 1440,900 #universe.width, universe.height
			tile_size   = tile.get_size()
			image_prep  = pygame.Surface((screen_size[0],tile_size[1]),pygame.SRCALPHA).convert_alpha()
			bar_positions = range(0,(screen_size[0]/tile_size[0]+1))
			[image_prep.blit(tile,(i*tile_size[0],0)) for i in bar_positions]
			self.tile   = utils.img.scale_image(tile)
			self.tile_size = self.tile.get_size()
			self.image  = utils.img.scale_image(image_prep)
			self.size = self.image.get_size()


class BigScenario():
	def __init__(self,universe,street):
		self.universe		= universe
		scenario_row	= database.query.street(universe, street, 'scenario')
		cached_images = os.listdir(os.path.join(directory.cache, 'images'))

		if street+str(p(1440,900)) in cached_images:
			self.image = pygame.image.load(os.path.join(directory.cache, 'images',street+str(p([1440,900]))+'.png')).convert_alpha()
		else:
			self.universe.stage.scenarios_prep = []
			self.image			= pygame.Surface((p(9600,r=0),universe.height), pygame.SRCALPHA).convert_alpha()
			for i in scenario_row:
				if i['invert'] == 1:
					if i['height'] != 0:
						img = scenarios.Scenario(p(i['xpos'],r=False),j(directory.main,i['directory']),self.universe, invert=True, height= p(i['height']))
					else:
						img = scenarios.Scenario(p(i['xpos'],r=False),j(directory.main,i['directory']),self.universe, invert=True)
				else:
					if i['height'] != 0:
						img = scenarios.Scenario(p(i['xpos'],r=False),j(directory.main,i['directory']),self.universe, height= p(i['height']))
					else:
						img = scenarios.Scenario(p(i['xpos'],r=False),j(directory.main,i['directory']),self.universe)
				self.universe.stage.loading()
				self.universe.stage.scenarios_prep.append(img)
			for i in self.universe.stage.scenarios_prep:
				self.image.blit(i.image,i.pos)
			pygame.image.save(self.image,os.path.join(directory.cache, 'images',street+str(p([1440,900]))+'.png') )
		self.pos			= [self.universe.center_x,0]

	def update_all(self):
		self.pos[0]		 = self.universe.center_x


class Pause():
	def __init__(self, universe):
		self.status = 'outside'
		self.universe = universe
		resume	  = widget.GameText(self.universe, t('Resume'),(360,400),  main_font=settings.second_font)
		ok_pos	  = d(resume.pos[0]+(resume.size[0]/2)),d(resume.pos[1]+(resume.size[1]))+50
		ok_button   = widget.Button(self.universe, directory.button_ok,ok_pos, [0,0],self.resume)
		leave		= widget.GameText(self.universe, t('Quit'),(1080,400),  main_font=settings.second_font)
		cancel_pos  = d(leave.pos[0]+(leave.size[0]/2)),d(leave.pos[1]+(leave.size[1]))+50
		cancel_button = widget.Button(self.universe, directory.button_cancel,cancel_pos,[0,0], self.exit_game)
		title	   = widget.GameText(self.universe, t('Game Paused'),(720,100), main_font=settings.second_font)
		check_closet = widget.Button(self.universe, t('Check your closet'), (720,700), [0,0], self.set_closet)
		toggle = widget.Button(self.universe, t('Toggle Fullscreen'), (710,760), [0,0], self.toggle_fullscreen)
		self.buttons	= (resume, ok_button, leave, cancel_button, title, check_closet, toggle)
		self.music  = j(directory.music,'1stSnowfall.ogg')
		self.menu = [(i.pos[0]+(i.size[0]/4),i.pos[1]+(i.size[1]/4)) for i in self.buttons if i.__class__== widget.Button]
		self.chosen_number = 0
		self.closet = None
		self.close_closet = None
		self.unlocked_items= []
		self.unlocked_boyfriends = []
		self.icons = {
			'accessory_beret':	[p((240, 82)),	t("The beret accessory, earnd for jumping with the penguin.")],
			'accessory_crown':	[p((350, 82)),	t("The crown accessory, unlocked from the start.")],
			'accessory_shades':	[p((460, 82)),	t("The shades accessory, earned after trampling 20 chicks.")],
			'accessory_mask':	[p((570, 82)),	t("The mask, earned for debuting three hairstyles in balls.")],
			'accessory_purse':	[p((680, 82)),	t("The purse accessory, unlocked from the start.")],
			'accessory_ribbon':	[p((790, 82)),	t("The ribbon accessory, unlocked from the start.")],
			'dress_indian':		[p((900, 82)),	t("The indian dress, earned for dressing as a geisha.")],
			'dress_kimono':		[p((1010,82)),	t("The kimono, earned for being crossed by the carriage.")],
			'dress_pink':		[p((1120,82)),	t("The pink dress, unlocked from the start.")],
			'dress_red':		[p((240, 192)),	t("The red dress, unlocked from the start.")],
			'dress_plain':		[p((350, 192)),	t("The simple dress, unlocked from the start.")],
			'dress_yellow':		[p((460, 192)),	t("The yellow dress, earned for beating all kinds of enemies.")],
			'face_eyelids':		[p((570, 192)),	t("The eyelids make-up, unlocked from the start.")],
			'face_eyeshades':	[p((680, 192)),	t("The eyeshades make-up, unlocked from the start.")],
			'face_geisha':		[p((790, 192)),	t("The geisha look, earned for bathing while clean.")],
			'face_indian':		[p((900, 192)),	t("The indian look, earned for kissing the lion.")],
			'face_lipstick':	[p((1010,192)),	t("The lipstick make-up, earned for entering your own castle.")],
			'face_simple':		[p((1120,192)),	t("The simple make-up, unlocked from the start.")],
			'hair_black':		[p((240, 302)),	t("The black hairstyle, unlocked from the start.")],
			'hair_braid_and_tail':	[p((350, 302)),	t("The braid and tail hairstyle, unlocked from the start.")],
			'hair_brown':		[p((460, 302)),	t("The brown hairstyle, unlocked from the start.")],
			'hair_cinderella':	[p((570, 302)),	t("Cinderella's hairstyle, earned for visiting her.")],
			'hair_geisha':		[p((680, 302)),	t("The geisha hairstyle, unlocked from the start.")],
			'hair_rapunzel':	[p((790, 302)),	t("Rapunzel's hairstyle, earned for visiting her.")],
			'hair_rastafari':	[p((900, 302)),	t("The rastafari hairstyle, unlocked from the start.")],
			'hair_red':		[p((1010,302)),	t("The red hairstyle, unlocked from the start.")],
			'hair_short':		[p((1120,302)),	t("The short hairstyle, unlocked from the start.")],
			'hair_sleeping':	[p((240, 412)),	t("Sleeping Beauty's hairstyle, earned for visiting her.")],
			'hair_snowwhite':	[p((350, 412)),	t("Snow White's hairstyle, earned for visiting her.")],
			'hair_yellow':		[p((460, 412)),	t("The blonde hairstyle, unlocked from the start.")],
			'shoes_boots':		[p((570, 412)),	t("The go-go boots, earned by crossing the drains clean.")],
			'shoes_crystal':	[p((680, 412)),	t("The glass slippers, earned for wearing the dream outfit.")],
			'shoes_flower':		[p((790, 412)),	t("The flower sandals, earned for visiting all streets in one day.")],
			'shoes_red':		[p((900, 412)),	t("The red shoes, unlocked from the start.")],
			'shoes_slipper':	[p((1010,412)),	t("The slippers, unlocked from the start.")],
			'shoes_white':		[p((1120,412)),	t("The white shoes, unlocked from the start.")]
			}


	def toggle_fullscreen(self):
		size = (self.universe.width, self.universe.height)
		if self.universe.screen_surface.get_flags() & pygame.FULLSCREEN:
			pygame.display.set_mode(size)
		else:
			pygame.display.set_mode(size, pygame.FULLSCREEN)

	def resume(self):
		self.status = 'done'

	def set_closet(self):
		self.closet = utils.img.image(os.path.join(directory.closet,'background.png'))
		unlocked = database.query.unlocked(self.universe)
		unlocked_names = [i['type']+'_'+i['garment'] for i in unlocked]
		self.unlocked_items = [Closet_Icon(self.universe, i['type'],i['garment'],self.icons[i['type']+'_'+i['garment']]) for i in unlocked]

		for i in self.icons:
			if i not in unlocked_names:
				self.unlocked_items.append(Closet_Icon(self.universe, None,None,self.icons[i], locked = True))
		self.unlocked_items.extend([Dearhearts(self.universe.stage.princesses[0].points)])
		self.close_closet = widget.Button(self.universe, directory.button_cancel,(1300,800),[0,0], self.clear_closet)

	def clear_closet(self):
		self.closet = None
		self.unlocked_items = None
		self.close_closet = None

	def update_all(self):
		pass

	def exit_game(self):
		self.universe.level.white.alpha_value = 0
		utils.save.save_file(self.universe)
		self.universe.level.princesses = None
		self.universe.menu.vertical_bar['position'] = -self.universe.menu.vertical_bar['size'][0]
		self.universe.menu.vertical_bar['side'] = 'left'
		self.universe.menu.vertical_bar['call_bar'] = 'left'
		self.universe.menu.vertical_bar['image'] = pygame.transform.flip(self.universe.menu.vertical_bar['image'],1,0)
		self.universe.menu.STEP = self.universe.menu.STEP_arrive_bar
		self.universe.LEVEL= "menu"


class Closet_Icon():
	def __init__(self, universe, garment_type, garment, icon, locked=None):
		self.pos = icon[0]
		self.locked = locked

		if self.locked:
			self.name = "?"
			text	= t('This garment is locked')
			self.medium = utils.img.image(os.path.join(directory.interface,'closet','blocked.png'))
			self.big	= None
		else:
			self.name = garment_type + '_' + garment
			text = icon[1]
			self.medium = utils.img.image(os.path.join(directory.princess,self.name,'medium','0.png'))
			self.big = utils.img.image(os.path.join(directory.princess,self.name,'big_icons','0.png'))

		self.text = widget.GameText(universe, text, [720,550])
		self.image = self.medium
		self.rect  = pygame.Rect(self.pos, self.medium.get_size())
		self.universe = universe
		self.imagetxt = None
		self.hover		= None

	def update_all(self):
		if self.rect.colliderect(self.universe.pointer.rect):
			if not self.hover:
				self.hover = True
				if not self.locked:
					self.pos[0]-= p(26)
					self.pos[1]-= p(26)
					self.image = self.big
			self.imagetxt = self.text
		elif self.hover == True:
			self.hover = None
			if not self.locked:
				self.pos[0]+= p(26)
				self.pos[1]+= p(26)
			self.image = self.medium
			self.imagetxt = None

class Dearhearts():
	def __init__(self, points):
		image_size = p((1200,350))
		self.pos = p((140,527))
		self.image = pygame.Surface(image_size, pygame.SRCALPHA).convert_alpha()
		boyfriends_ranking = (
			('gentleman_decent',(0,0),30),
			('knight_reliable',(82,0),65),
			('baron_serious',(162,0),105),
			('count_loving',(230,0),175),
			('marquess_attractive',(331,0),255),
			('duke_intelligent',(411,0),345),
			('prince_charming',(504,0),465),
			('king_kindhearted',(560,0),685),
			('emperor_awesome',(664,0),1000),
			)
		for i in boyfriends_ranking:
			if points >= i[2]:
				self.image.blit(utils.img.image(os.path.join(directory.boyfriends,i[0],'medium','0.png')),p(i[1]))
	
	def update_all(self):
		pass

