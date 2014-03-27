from settings import *
import pygame
import fairy
import random
import database
import database.update
import interactive
import interactive.popup

def pn(some_number):
	return round(some_number*scale)

def choose_event(universe,starting_game=False):
#	if level.event_counter:
#		level.event_counter += 1
#		if level.event_counter > 600:
#			level.event_counter = 0
#	else:
	if universe.level.clock[1].count > 2:
		princess = universe.level.princesses[0]
		princess_pos = princess.center_distance
		name = universe.level.name
		intro = database.query.message(universe, 'first day a')
		if intro[0]['count']==0:
			#princess.center_distance = pn(5220)
			universe.level.event_counter += 1
			create_message(universe, 'first day a')
			database.update.use_message(universe, 'first day a')
			#intro_first_day = database.query.message(universe, 'first day a')
			#if intro_first_day[0]['count'] == 0:
			#	universe.level.Fairy = 'loading'
			#	message_text = random.choice(intro_first_day)['message']
			#	universe.level.fae[0] = fairy.Message(universe, message = message_text)
			#	database.update.use_message(universe,'intro')
		elif name == "bathhouse":
			if pn(4700) < princess_pos < pn(5000):
				create_message(universe,'maddelines house')
			elif pn(8700) < princess_pos < pn(9000):
				create_message(universe,'magic beauty parlor')
			elif pn(850) <princess_pos < pn(1050):
				create_message(universe,"bathhouse")
		elif name == "accessory":
			if princess_pos < pn(360):
				create_message(universe,"accessory hall")
			elif pn(8300) < princess_pos:
				create_message(universe,"cinderellas castle")
		elif name == "dress":
			if princess_pos < pn(300):
				create_message(universe,"dress tower")
			elif pn(8900) < princess_pos:
				create_message(universe,"snow-whites castle")
		elif name == "makeup":
			if princess_pos <pn(300):
				create_message(universe,"make-up tower")
			elif pn(8900) < princess_pos:
				create_message(universe,"sleeping beautys palace")
		elif name == "shoes":
			if princess_pos < pn(300):
				create_message(universe,"shoes shop")
			if princess_pos > pn(8900):
				create_message(universe,"rapunzels villa")
		if universe.level.unlocking:
			unlock(universe,universe.level.unlocking)


def create_message(universe, name, unique=True):
	universe.level.event_counter +=1
	row = database.query.message(universe, name, one = True)
	if row['count'] == 0 or unique==False:
		print "Here comes the Fairy "+name
		universe.level.fairy = 'loading'
		pygame.mixer.Channel(0).play(universe.level.fae[1].whistle)
		universe.level.fae[0] = fairy.Message(universe, message = row['message'])
		database.update.use_message(universe, name)

def unlock(universe, unlocking):
	if database.query.is_locked(universe,unlocking['type'],unlocking['name']):
		popup = interactive.popup.Unlocking_Message(universe, unlocking)
		universe.level.unlocking['list'] = [popup, interactive.popup.Unlocking_Icon(universe,popup,unlocking)]
		database.update.unlock(universe, unlocking['type'],unlocking['name'])
		database.update.use_message(universe,unlocking['name'])
