# -*- coding: utf-8 -*-

import interactive.princess as princess
import os
import datetime
import pygame
import settings
from settings import scale
from settings import directory

def save_file(level, hairback = None, skin = None, face = None, hair = None, shoes = None, dress = None, arm = None, armdress = None, accessory = None, past_ball = None, great_past_ball = None, position = None, Ball = None):
	print "Saving progress into Database"
	universe = level.universe
	princess = level.princesses[0]
	#avoid errors in case there are no saved files
	try:
		os.mkdir(os.path.join(directory.saves,princess.name))
	except:
		pass
	dir = os.path.join(directory.saves,princess.name)
	day = datetime.datetime.today()

	if dress == "dress_yellow":
		armdress = "sleeve_yellow"
	elif dress == "dress_red":
		armdress = "sleeve_red"
	elif dress == "dress_kimono":
		armdress = "sleeve_kimono"
	elif dress == "dress_indian":
		armdress = "sleeve_indian"
	else:
		armdress = "None"
	hair_backs = ['hair_black','hair_brown','hair_rastafari','hair_rapunzel','hair_red']
	if hair in hair_backs:
		hairback = hair+'_back'
	else:
		hairback = "None"
	cursor = level.universe.db_cursor
	cursor.execute("UPDATE save SET center_distance = '"+str(int(princess.center_distance/scale))+"' WHERE name = '"+princess.name+"'")
	if hair:
		cursor.execute("UPDATE princess_garment SET hair_back = '"+str(hairback)+"' WHERE id = (SELECT max(id) FROM princess_garment)")
	if skin:
		cursor.execute("UPDATE princess_garment SET skin	 = '"+str(skin)+"' WHERE id =  (SELECT max(id) FROM princess_garment)")
		cursor.execute("UPDATE princess_garment SET arm	  = '"+str(arm)+"'   WHERE id =  (SELECT max(id) FROM princess_garment)")
	if face:
		cursor.execute("UPDATE princess_garment SET face	 = '"+str(face)+"' WHERE id =  (SELECT max(id) FROM princess_garment)")
	if hair:
		cursor.execute("UPDATE princess_garment SET hair	 = '"+str(hair)+"' WHERE id =  (SELECT max(id) FROM princess_garment)")
	if shoes:
		cursor.execute("UPDATE princess_garment SET shoes	= '"+str(shoes)+"' WHERE id =  (SELECT max(id) FROM princess_garment)")
	if dress:
		cursor.execute("UPDATE princess_garment SET dress	= '"+str(dress)+"' WHERE id =  (SELECT max(id) FROM princess_garment)")
		cursor.execute("UPDATE princess_garment SET armdress = '"+str(armdress)+"' WHERE id =  (SELECT max(id) FROM princess_garment)")
	if accessory:
		cursor.execute("UPDATE princess_garment SET accessory= '"+str(accessory)+"' WHERE id =  (SELECT max(id) FROM princess_garment)")
	cursor.execute("UPDATE save SET dirt	 = '"+str(princess.dirt)+"' WHERE name = '"+princess.name+"'")
	cursor.execute("UPDATE save SET points   = '"+str(princess.points)+"' WHERE name = '"+princess.name+"'")
	universe.db.commit()
	print "Save Database saved "
#	if Ball:
#		backupfile.close()
	return os.path.join(directory.saves,princess.name,princess.name+'.glamour')
