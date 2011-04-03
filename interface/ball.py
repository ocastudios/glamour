import pygame
import os
import random
import itertools

import utils
import interface.widget as widget
import utils.save as save
import settings
import database
import mousepointer
from settings import directory
from settings import scale
from settings import t
from settings import p
from settings import d



class Ball():
	def __init__(self, universe, princess):
		self.universe = universe
		self.delay = 150
		self.universe.level.changing_stages_darkenning()
		self.universe.level.loading()
		#reset boyfriend list - so that the list can be managed by the instances
		NewDancer.boyfriend_list = ["gentleman_decent", 
				  "knight_reliable", 
				  "baron_serious", 
				  "count_loving", 
				  "marquess_attractive", 
				  "duke_intelligent"]
		self.position = 0,0
		self.universe   = universe
		self.boyfriend  = None
		universe.level.loading()
		self.texts	  = []
		self.texts+= [StarBall()]
		universe.level.loading()
		self.compute_glamour_points(universe)
		universe.level.loading()
		self.background	  = pygame.Surface((universe.width,universe.height),pygame.SRCALPHA).convert_alpha()
		universe.level.loading()
		for file in (os.path.join(directory.ball,'base.png'),os.path.join(directory.ball,'back-bubbles.png')):
			self.background.blit(utils.img.scale_image(pygame.image.load(file).convert_alpha()), (0,0))
			universe.level.loading()
		self.princess   = princess
		self.Bar		= VerticalBar(self)
		universe.level.loading()
		self.Frame	  = BallFrame(self)
		universe.level.loading()
		self.buttons = [widget.Button(self.universe, directory.button_ok,(1050,700), [0,0],self.return_to_game)]
		universe.level.loading()
		pygame.mixer.music.load(os.path.join(directory.music,"strauss_waltz_wedley.ogg"))
		universe.level.loading()
		pygame.mixer.music.set_volume(.9)
		pygame.mixer.music.play()
		universe.level.loading()
		princesses_list	  = ['Cinderella', 'Snow_White', 'Sleeping_Beauty','Rapunzel']
		garment_list		 = ['Accessory', 'Dress', 'Shoes','Makeup']
		Accessory_list	   = ['crown', 'purse','ribbon','shades']
		Dress_list		   = ['pink','plain','red','yellow']
		Shoes_list		   = ['crystal','red','slipper','white']
		Makeup_list		  = ['eyelids','eyeshades','lipstick','simple']
		self.counter		 = 0
		self.bigprincess = BigPrincess(self)
		universe.level.loading()
		self.dancers = []
		if self.boyfriend:
			self.dancers.append(NewDancer(universe, self.bigprincess,self.boyfriend.hard_name))
		universe.level.loading()
		for a in self.Frame.princesses:
			self.dancers.append(NewDancer(universe, a))
			universe.level.loading()
		self.foreground = pygame.Surface((universe.width,universe.height)).convert()
		self.foreground.fill((226,226,148))
		universe.level.loading()
		self.alpha = 0
		self.foreground.set_alpha(self.alpha)
		universe.level.loading()
		self.locked = database.query.is_locked(universe,'accessory','mask')
		self.universe = universe

	def update_all(self):
		if self.universe.level.black.alpha_value > 0:
			self.universe.level.changing_stages_darkenning(-1)
		for i in self.dancers:
			i.update_all()
		if self.counter > self.delay:
			if self.alpha < 150:
				self.alpha += 10
				self.foreground.set_alpha(self.alpha)
		self.Frame.update_all()
		self.Bar.update_all()
		if self.counter > self.delay:
			self.bigprincess.update_all()
		if self.counter > self.delay+20:
			for i in self.texts:
				i.update_all()
		if self.boyfriend:
			if self.counter == self.delay+50:
				self.texts+= [widget.GameText(self.universe, t("and won the heart of")+" ", (1090,237), [0,0],font_size = 40)]
			if self.counter == self.delay+60:
				self.texts+= [widget.GameText(self.universe, ".", (1300,237), [0,0],font_size = 40)]
			if self.counter == self.delay+70:
				self.texts+= [widget.GameText(self.universe, " .", (1300,237), [0,0],font_size = 40)]
			if self.counter == self.delay+80:
				self.texts+= [widget.GameText(self.universe, "  .", (1300,237), [0,0],font_size = 40)]
			if self.counter > self.delay+110:
				self.boyfriend.update_all()
		if self.counter > self.delay+130:
			for i in self.buttons:
				i.update_all()

		if self.counter == self.delay+130:
			if self.boyfriend:
				self.texts += [widget.GameText(self.universe, self.boyfriend.name,(1156,280),[0,0], font_size = 60,color=(58,56,0))]

		if self.counter <= self.delay+130:
			self.counter += 1

	def compute_glamour_points(self,universe):
		garments= ('face','shoes','dress','accessory')
		cursor = universe.db_cursor
		princess_rows = cursor.execute("SELECT * FROM princess_garment").fetchall()
		fairy_tale_rows = [
				cursor.execute("SELECT * FROM "+princess_name).fetchall() for princess_name in ("cinderella","rapunzel","sleeping_beauty","snow_white")
						]
		save_row	 = cursor.execute("SELECT * FROM save").fetchone()
		accumulated_points = int(save_row["points"])
		princess_garments   = {
					"this_ball":[princess_rows[len(princess_rows)-1][item] for item in garments],
					"last_ball":[princess_rows[len(princess_rows)-2][item] for item in garments]
							}
		others_garments	 = {
					"this_ball":[],
					"last_ball":[]
							}
		for row in fairy_tale_rows:
			for item in garments:
				others_garments["this_ball"].append(row[len(row)-1][item])
				others_garments["last_ball"].append(row[len(row)-2][item])


		print "Others Garments "+str(others_garments["this_ball"])
		print "Princess Garments"+str(princess_garments["this_ball"])

		present_repetitions = sum([others_garments["this_ball"].count(i) for i in princess_garments["this_ball"]])
		last_ball_garments  = others_garments["last_ball"]+princess_garments["last_ball"]
		past_repetitions	= sum([last_ball_garments.count(i) for i in princess_garments["this_ball"]])
		garments_history	= princess_rows[:-1]+fairy_tale_rows
		number_of_balls	 = len(princess_rows)
		history_repetitions = sum([garments_history.count(i) for i in princess_garments["this_ball"]])

		print "The total repetition points for the garments in this ball is "+ str(present_repetitions)
		print "The total repetition points for the garments last ball is "+ str(past_repetitions)
		print "Fashion points is equal to 34 - 3*repetition_points - past_repetition_points"
		fashion = 34-(3*present_repetitions)-(past_repetitions)
		print "Your total Fashion points is " + str(fashion)
		dirty   = (fashion * save_row['dirt'])/3
		print "Your total Dirt points is "+ str(dirty)
		creativity = fashion*(.5-(history_repetitions/number_of_balls))
		print "Youtr total creativity points is " + str(creativity)
		glamour_points = fashion-dirty+creativity
		print "YOUR TOTAL GLAMOUR POINTS THIS BALL IS "+ str(glamour_points)+" !!!!"
		print "Now I am going to save your points"
		print "YOU HAVE ACCUMULATED A TOTAL OF " +str(accumulated_points+glamour_points)+" glamour points."
		save_table = cursor.execute("SELECT * FROM save").fetchone()
		past_glamour_points = save_table['points']
		new_glamour_points = int(past_glamour_points)+int(glamour_points)

		universe.level.princesses[0].points = new_glamour_points
		cursor.execute("UPDATE save SET points = "+str(new_glamour_points))

		stage_list		   = ['BathhouseSt', 'DressSt', 'AccessorySt', 'MakeupSt','ShoesSt']
		print "Preparing the new set of enemies for each stage"
		for stage in stage_list:
			general_enemies_list = ['schnauzer', 'carriage','butterfly','old_lady','viking_ship','footboy','bird']
			print "Removing enemies from "+stage
			for i in general_enemies_list:
				sql = 'update stage_enemies set '+i+'= 0 where stage = "'+stage+'"'
				cursor.execute(sql)
			print "New Enemies List for "+stage
			max_enemies = 1
			if new_glamour_points >= 30:
				max_enemies = 2
			if new_glamour_points >= 65:
				max_enemies = 3
			if new_glamour_points >= 105:
				max_enemies = 4
			if new_glamour_points >= 175:
				max_enemies = 5
			if new_glamour_points >= 255:
				max_enemies = 6
			if new_glamour_points >= 345:
				max_enemies = 7
			if new_glamour_points >= 465:
				max_enemies = 8
			if new_glamour_points >= 685:
				max_enemies = 10
			enemy_number = random.randint(1,max_enemies)
			for i in range(enemy_number):
				chosen_enemy = random.choice(general_enemies_list)
				print chosen_enemy
				sql = 'update stage_enemies set '+chosen_enemy+' = 1 where stage = "'+stage+'"'
				cursor.execute(sql)

		universe.db.commit()
		save.save_thumbnail(universe)
		self.texts += [
				#TRANSLATORS: consider the whole sentence, which is divided in four parts as follows: (You've) (got) X (glamour) (points). Depending on the idiom you may need to consider a non literal translation.
				widget.GameText(universe, t("You've"),	(1064,81),		[0,0],font_size = 40),
				#TRANSLATORS: consider the whole sentence, which is divided in four parts as follows: (You've) (got) X (glamour) (points). Depending on the idiom you may need to consider a non literal translation.
				widget.GameText(universe, t("got"),		(1100,128),		[0,0],font_size = 40),
				#TRANSLATORS: consider the whole sentence, which is divided in four parts as follows: (You've) (got) X (glamour) (points). Depending on the idiom you may need to consider a non literal translation.
				widget.GameText(universe, t("glamour"),	(1309,151),		[0,0],font_size = 40),
				#TRANSLATORS: consider the whole sentence, which is divided in four parts as follows: (You've) (got) X (glamour) (points). Depending on the idiom you may need to consider a non literal translation.
				widget.GameText(universe, t("points"),	(1309,185),		[0,0],font_size = 40),
				widget.GameText(universe, str(int(glamour_points)), (1200,120),[0,0],font_size=80)
		]
		total_points = int(glamour_points+accumulated_points)
		if total_points >= 30:
			self.boyfriend = BoyFriend(universe, total_points)
		universe.level.panel[1]  = widget.GameText(universe, str(total_points), (1000,30), [0,0],font_size = 80, color=(58,56,0))

	def return_to_game(self):
		if self.universe.level.princesses[0].points >=1000 and not database.query.won(self.universe):
			self.universe.level = self.universe.menu
			database.update.won(self.universe)
			self.universe.stage.white.alpha_value = 0
			utils.save.save_file(self.universe)
			self.universe.stage.princesses = None
			self.universe.menu.action = 'open'
			self.universe.action[2] = 'open' 
			self.universe.menu.watching_ending()
#			self.universe.menu.STEP = self.universe.menu.STEP_arrive_bar
			self.universe.LEVEL= "menu"
			self.universe.pointer = mousepointer.MousePointer(self,type = 2)
			pygame.mixer.music.fadeout(1500)
		else:
			self.universe.level.princesses[0].visited_streets = []
			self.universe.level.BathhouseSt(goalpos = round(5220*scale), clean_princess = True)
			if self.locked:
				if database.query.different_hairs_used(self.universe)>=3:
					self.universe.level.unlocking = {'type':'accessory','name':'mask'}
					self.locked = False
			self.universe.stage.clock[1].count = 0
			self.universe.stage.clock[1].time = "morning"


class VerticalBar():
	def __init__(self, ball, right_or_left = 'left'):
		self.image = utils.img.image(os.path.join(directory.ball,'goldenbar.png'))
		if right_or_left == 'right':
			self.image = pygame.transform.flip(self.image, 1,0)
		self.size = self.image.get_size()
		self.position = [-self.size[0],0]
		self.speed = 5*scale
		self.ready = False
		self.countdown = 60

	def update_all(self):
		if self.countdown == 0:
			if self.position[0] < p(90):
				self.position[0] += self.speed
				self.speed += 5
			else:
				self.position[0] = p(90)
				self.ready = True
		else:
			self.countdown -= 1

class BallFrame():
	def __init__(self, ball):
		self.universe = ball.universe
		self.image = pygame.Surface(p((677,673)),pygame.SRCALPHA).convert_alpha()
		background = utils.img.image(os.path.join(directory.ball,'back-frame.png'))
		self.size = self.image.get_size()
		self.position = [p(30), -self.size[1]]
		self.speed = 5
		self.ball = ball
		princesses = [FairyTalePrincess(self, i[0], i[1], i[2], i[3], iconpos= i[5], name = i[4]) for i in (
				[(130,150), 'hair_snowwhite', 'pink', 'princess-icon-apple.png', 'Snow_White',   220],
				[(240,150), 'hair_cinderella','tan',  'princess-icon-shoe.png',	'Cinderella', 335],
				[(350,150), 'hair_rapunzel',  'pink', 'princess-icon-brush.png', 'Rapunzel'  ,   440],
				[(460,150), 'hair_sleeping',  'pink', 'princess-icon-spindle.png','Sleeping_Beauty', 560])]
		past_princesses= [FairyTalePrincess(self,i[0],i[1],i[2], name=i[3],ball=1) for i in (
				[(130,400), 'hair_snowwhite', 'pink', 'Snow_White'],
				[(240,400), 'hair_cinderella','tan',  'Cinderella'],
				[(350,400), 'hair_rapunzel',  'pink', 'Rapunzel'],
				[(460,400), 'hair_sleeping',  'pink', 'Sleeping_Beauty']) ]
		frametexts = [
				widget.GameText(self.universe, t("Tonight's ball"),		(0,0), [0,0], rotate = 90),
				widget.GameText(self.universe, t("Yesterday's ball"),	(0,0), [0,0], rotate = 90)
					]
		self.princesses = princesses
		for i in past_princesses:
			self.image.blit(i.image,i.pos)
		self.image.blit(background,(0,0))
		self.image.blit(frametexts[0].image, p((0, 130)))
		self.image.blit(frametexts[1].image, p((0, 360)))
		for i in princesses:
			self.image.blit(i.image,i.pos)
			if i.symbol:
				self.image.blit(i.symbol,(i.symbolpos,round(i.pos[1]-p(100) )))
		self.set_next_ball_clothes()
		self.ready = False

	def update_all(self):
		if self.ball.Bar.ready:
			if self.ball:
				if self.position[1] + (self.size[1]/2) < (self.ball.universe.height/2):
					self.speed +=2
				else:
					self.speed = 0
					self.ready = True
				self.position[1] += self.speed

	def set_next_ball_clothes(self):
		cursor = self.ball.universe.db_cursor
		faces   = ("face_eyelids", "face_eyeshades","face_lipstick","face_simple")
		dresses = ("dress_pink","dress_plain", "dress_red", "dress_yellow")
		arm_dresses = (0,0,1,1)
		accessories = ("accessory_crown","accessory_purse","accessory_ribbon","accessory_shades")
		shoes   = ("shoes_crystal","shoes_red","shoes_slipper","shoes_white")
		for p in ("rapunzel","cinderella","sleeping_beauty","snow_white"):
			dress_no = random.randint(0,len(dresses)-1)
			row = cursor.execute("SELECT * FROM "+p+" WHERE id = (SELECT MAX(id) FROM "+p+")").fetchone()
			cursor.execute("INSERT INTO "+p+" VALUES ("+str(row['id']+1)+" , "+str(row["hair_back"])+" , '"+row["skin"]+"', '"+random.choice(faces)+"' , '"+row['hair']+"' , '"+random.choice(shoes)+"' , '"+dresses[dress_no]+"', '"+row['arm']+"', "+str(arm_dresses[dress_no])+", '"+random.choice(accessories)+"')")
		row = cursor.execute("SELECT * FROM princess_garment WHERE id = (SELECT MAX(id) FROM princess_garment)").fetchone()
		cursor.execute("INSERT INTO princess_garment VALUES ("+str(row['id']+1)+" , '"+str(row["hair_back"])+"' , '"+row["skin"]+"', '"+row['face']+"' , '"+row['hair']+"' , '"+row['shoes']+"' , '"+row['dress']+"', '"+row['arm']+"', '"+str(row['armdress'])+"', '"+row['accessory']+"')")
		self.ball.universe.db.commit()


class FairyTalePrincess():
	def __init__(self, frame, position, hair, skin, icon=None, iconpos=None, name = "princess_garment", ball = 0):
		"""Creates Thumbnail of Princesses to remember past balls

		   The parameters are self, frame (or level), position, hair, skin, icon, name (name of the princess in the database, if no name, than player), ball (number of the ball to show - counted backwards).
		   """
		skin_body	   = 'skin_'+skin
		skin_arm		= 'arm_'+skin
		self.frame	  = frame
		self.file	   = frame.ball.universe.file
		self.image	  = utils.img.scale_image(pygame.Surface((200,200),pygame.SRCALPHA).convert_alpha())
		name_lower = name.lower()
		self.position   = p(position)
		self.symbol = None
		self.name = name
		if name != "princess_garment":
			if icon:
				self.symbol	 =  utils.img.image(os.path.join(directory.ball,icon))
				self.symbolpos  = int(round(iconpos*scale  - (float(self.symbol.get_width())/2)))
		sql				 = "SELECT * FROM "+name_lower+" WHERE id = (SELECT MAX(id)-"+str(ball)+" FROM "+name_lower+")"
		self.pos			= [self.position[0],self.position[1]]
		cursor = self.frame.ball.universe.db_cursor
		row	= cursor.execute(sql).fetchone()
		if row:
			if row['hair_back'] > 0:
				self.image.blit(utils.img.image(os.path.join(directory.princess,row['hair']+"_back",'stay','0.png')),(0,0))
			for i in  ('skin', 'hair', 'face', 'dress', 'accessory', 'arm', 'shoes'):
				self.__dict__[i] = row[i]
				self.image.blit(utils.img.image(os.path.join(directory.princess,row[i],'stay','0.png')),(0,0))
			self.image = pygame.transform.flip(self.image,1,0)
		

	def update_all(self):
		self.pos		= [self.frame.position[0]+self.position[0],
						   self.frame.position[1]+self.position[1]]



class StarBall():
	def __init__(self):
		self.images = utils.img.MultiPart([os.path.join(directory.ball,'star-score','backlight'),
										   os.path.join(directory.ball,'star-score','star')
											],onesided = True)
		self.image = self.images.left[0]
		self.pos = p([1025,-50])

	def update_all(self):
		self.image = self.images.left[self.images.itnumber.next()]


class BoyFriend():
	def __init__(self, universe, points):
		print "Oh my! You are so beautiful that most certainly someone will fall for you tonight!"
		boyfriend = None
		if points >= 30:
			boyfriend = "gentleman_decent"
			self.name = t('Gentleman Decent')
		if points >= 65:
			boyfriend = "knight_reliable"
			self.name = t('Knight Reliable')
		if points >= 105:
			boyfriend = "baron_serious"
			self.name = t('Baron Serious')
		if points >= 175:
			boyfriend = "count_loving"
			self.name = t('Count Loving')
		if points >= 255:
			boyfriend = "marquess_attractive"
			self.name = t('Marquess Attractive')
		if points >= 345:
			boyfriend = "duke_intelligent"
			self.name = t('Duke Intelligent')
		if points >= 465:
			boyfriend = "prince_charming"
			self.name = t('Prince Charming')
		if points >= 685:
			boyfriend = "king_kindhearted"
			self.name = t('King Kindhearted')
		if points >= 1000:
			if database.query.won(universe):
				boyfriend = "fabrizio"
				self.name = "Fabrizio"
			else:
				boyfriend = "emperor_awesome"
				self.name = t('Emperor Awesome')
		print "The heart of "+boyfriend+" is yours!"
		self.hard_name = boyfriend
		self.image= utils.img.image(os.path.join(directory.boyfriends,boyfriend,'0.png'))
		self.pos = p([1000,298])

	def update_all(self):
		pass


class BigPrincess():
	def __init__(self, ball):
		big_image	  = pygame.Surface((400,400),pygame.SRCALPHA).convert_alpha()
		self.pos		= p([ 670,398])
		cursor = ball.universe.db_cursor
		sql = "SELECT * FROM princess_garment WHERE id=(SELECT MAX(id) FROM princess_garment)"
		row = cursor.execute(sql).fetchone()
		for part in ["hair_back","skin","face","hair","shoes","dress","arm","armdress","accessory"]:
			self.__dict__[part] = row[part]
			if row[part] and row[part]!="None":
				img = pygame.image.load(os.path.join(directory.princess,row[part],"big.png")).convert_alpha()
				big_image.blit(img, (0,0))
		dirt	 = int(cursor.execute("SELECT * FROM save").fetchone()['dirt'])
		if dirt >0:
			big_image.blit(pygame.image.load(os.path.join(directory.princess,"dirt"+str(dirt),"big.png")).convert_alpha(),(0,0))
		self.image = utils.img.scale_image(big_image,invert=True)

	def update_all(self):
		pass



class Dancer():
	def __init__(self, position):
		self.images = utils.img.There_and_back_again(directory.dancers, exclude_border = True)
		self.image  = self.images.list[self.images.itnumber.next()]
		self.position = position
		self.images.number = random.randint(0,20)
		if random.randint(0,9) < 4:
			self.list = self.images.left
		else:
			self.list = self.images.right

	def update_all(self):
		self.image  = self.images.list[self.images.number]
		self.images.update_number()

class NewDancer():
	square = (p([400,800],r=False),p([100,500],r=False))
	steps = itertools.cycle(['a','b','c','d'])
	boyfriend_list = ["gentleman_decent", 
				  "knight_reliable", 
				  "baron_serious", 
				  "count_loving", 
				  "marquess_attractive", 
				  "duke_intelligent"]
	
	def __init__(self,universe, big_princess= None, boyfriend = None):
		princess_directory  = directory.princess
		if big_princess.__class__ == BigPrincess:
			self.player = True
		else:
			self.player = False
		if not boyfriend and not self.player:
			boyfriend = random.choice(self.boyfriend_list)
		try:
			self.boyfriend_list.remove(boyfriend)
		except:
			print Exception
		ordered_directory_list = [os.path.join(directory.boyfriends,boyfriend,'dance','body')]
		for i in ('skin','dress','hair','accessory'):
			part = None
			if not big_princess.__dict__[i] in ('dress_pink', 'dress_plain', 'accessory_purse'):
					part = big_princess.__dict__[i]
			if part:
				ordered_directory_list.append(os.path.join(directory.princess,big_princess.__dict__[i],'dance'))
		ordered_directory_list.append(os.path.join(directory.boyfriends,boyfriend,'dance','head'))
		self.images	= utils.img.MultiPart(ordered_directory_list, loading = universe.level.loading)
		self.image  = self.images.left[self.images.number]
		self.images.number = random.randint(0,20)
		self.speed = p(5,r=False)

		self.my_step = self.steps.next()
		if not self.player:
			if self.my_step == 'a':
				self.position = [self.square[0][0],self.square[1][1]]
			elif self.my_step == 'b':
				self.position = [self.square[0][1],self.square[1][1]]
			elif self.my_step == 'c':
				self.position = [self.square[0][1],self.square[1][0]]
			elif self.my_step == 'd':
				self.position = [self.square[0][0],self.square[1][0]]
		else:
			self.position = (self.square[0][0]+(200*scale),self.square[1][0]+(200*scale))

	def update_all(self):
		self.image  = self.images.left[self.images.number]
		self.images.update_number()
		if not self.player:
			translate = {'right':1,'left':-1,'up':-1,'down':1}
			a = -0.0035; b = 0; c = 140
			if self.my_step == 'a':
				self.position[0]+= self.speed
				x = d(self.position[0]) - d(self.square[0][0]) - 200
				arc = (a*(x*x))+(b*x)+c 
				self.position[1] = self.square[1][1]+(arc*scale)
				if self.position[0] >= self.square[0][1]:
					self.my_step = 'b'
					self.position[0] = self.square[0][1]

			elif self.my_step == 'b':
				self.position[1]-= self.speed
				x = (self.position[1]/scale) - (self.square[1][0]/scale) - 200
				arc = (a*(x*x))+(b*x)+c
				self.position[0] = self.square[0][1]+(arc*scale)
				if self.position[1]<= self.square[1][0]:
					self.my_step = 'c'
					self.position[1] = self.square[1][0]

			elif self.my_step == 'c':
				self.position[0] -= self.speed
				x = (self.position[0]/scale) - (self.square[0][0]/scale) - 200
				arc = (a*(x*x))+(b*x)+c
				self.position[1] = self.square[1][0]-(arc*scale)
				if self.position[0]<= self.square[0][0]:
					self.my_step = 'd'
					self.position[0] = self.square[0][0]

			elif self.my_step == 'd':
				self.position[1]+= self.speed
				x = (self.position[1]/scale) - (self.square[1][0]/scale) -200
				arc = (a*(x*x))+(b*x)+c
				self.position[0] = self.square[0][0]-(arc*scale)
				if self.position[1] >= self.square[1][1]:
					self.my_step = 'a'
					self.position[1] = self.square[1][1]
