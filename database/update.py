# -*- coding: utf-8 -*-
import random
from settings import *
from . import database.query as query

def princess_garment(universe, Princess, hairback, skin, arm, face, hair, shoes, dress, armdress, accessory):
	cursor = universe.db_cursor
	cursor.execute("UPDATE save SET center_distance = '"+str(int(Princess.center_distance/scale))+"' WHERE name = '"+Princess.name+"'")
	if hair:
		cursor.execute("UPDATE princess_garment SET hair_back = '"+str(hairback)+"' WHERE id = (SELECT max(id) FROM princess_garment)")
	if skin:
		cursor.execute("UPDATE princess_garment SET skin	= '"+str(skin)+"' WHERE id =  (SELECT max(id) FROM princess_garment)")
		cursor.execute("UPDATE princess_garment SET arm		= '"+str(arm)+"'   WHERE id =  (SELECT max(id) FROM princess_garment)")
	if face:
		cursor.execute("UPDATE princess_garment SET face	= '"+str(face)+"' WHERE id =  (SELECT max(id) FROM princess_garment)")
	if hair:
		cursor.execute("UPDATE princess_garment SET hair	= '"+str(hair)+"' WHERE id =  (SELECT max(id) FROM princess_garment)")
	if shoes:
		cursor.execute("UPDATE princess_garment SET shoes	= '"+str(shoes)+"' WHERE id =  (SELECT max(id) FROM princess_garment)")
	if dress:
		cursor.execute("UPDATE princess_garment SET dress	= '"+str(dress)+"' WHERE id =  (SELECT max(id) FROM princess_garment)")
		cursor.execute("UPDATE princess_garment SET armdress= '"+str(armdress)+"' WHERE id =  (SELECT max(id) FROM princess_garment)")
	if accessory:
		cursor.execute("UPDATE princess_garment SET accessory= '"+str(accessory)+"' WHERE id =  (SELECT max(id) FROM princess_garment)")
	cursor.execute("UPDATE save SET dirt	= '"+str(Princess.dirt)+"' WHERE name = '"	+Princess.name+"'")
	cursor.execute("UPDATE save SET points	= '"+str(Princess.points)+"' WHERE name = '"+Princess.name+"'")
	universe.db.commit()

def clean_up(universe):
	universe.db_cursor.execute("UPDATE save SET dirt = "+str(universe.level.princesses[0].dirt)+" WHERE name = '"+universe.level.princesses[0].name+"'")
	universe.db.commit()

def unlock(universe, type, garment):
	universe.db_cursor.execute("UPDATE unlock SET status = 'unlocked' WHERE type = '"+type+"' and garment = '"+garment+"'")
	universe.db.commit()

def use_message(universe, name):#, name):
	universe.db_cursor.execute("UPDATE messages SET count = 1 WHERE name = '"+name+"';")
	universe.db.commit()
	
def beat_enemy(universe, enemy):
	universe.db_cursor.execute("UPDATE stage_enemies SET "+enemy+" = 1 WHERE stage = 'Beaten'")
	universe.db.commit()

def won(universe):
	if universe.stage.princesses[0].points >= boyfriend_rank[-1][1]:
		universe.db_cursor.execute("UPDATE save SET won=1")
		universe.db.commit()

def set_next_ball_clothes(universe, fairy_tale_princess=None, avoid=[],update=False):
	cursor = universe.db_cursor
	if avoid:
		avoid = random.choice(avoid)
	faces 	= [i['type'] + "_" + i['garment'] for i in query.unlocked(universe,'face')]
	dresses = [i['type'] + "_" + i['garment'] for i in query.unlocked(universe,'dress')]
	accessories = [i['type'] + "_" + i['garment'] for i in query.unlocked(universe,'accessory')]
	shoes 	= [i['type']  + "_" + i['garment'] for i in query.unlocked(universe,'shoes')]
	for l in (faces,dresses,accessories,shoes):
		if avoid in l:
			l.remove(avoid)
	#TODO: the list below should be replaced by a definition of dresses in a database so that it would be easier to mantain.
	arm_dresses = { 
			"dress_indian": "sleeve_indian",
			"dress_kimono": "sleeve_kimono",
			"dress_red": "sleeve_red",
			"dress_yellow":"sleeve_yellow"
			}#('None','None','sleeve_red','sleeve_yellow')
#		accessories = ("accessory_crown","accessory_purse","accessory_ribbon","accessory_shades")
#		shoes   = ("shoes_crystal","shoes_red","shoes_slipper","shoes_white")
	if fairy_tale_princess:
		princesses_list = [fairy_tale_princess]
	else:
		princesses_list = ("rapunzel","cinderella","sleeping_beauty","snow_white")
	for p in princesses_list:
		face  = 	random.choice(faces)
		dress = 	random.choice(dresses)
		accessory =	random.choice(accessories)
		shoe = 		random.choice(shoes)
		sleeve = None
		if dress in arm_dresses:
			sleeve = arm_dresses[dress]
		if not update:
			row = cursor.execute("SELECT * FROM "+p+" WHERE id = (SELECT MAX(id) FROM "+p+")").fetchone()
			cursor.execute("INSERT INTO "+p+
				" VALUES ("+str(row['id']+1)+" , '"+
				str(row["hair_back"])+"' , '"+
				str(row["skin"])+"', '"	+
				str(face)+"' , '"+
				str(row['hair'])+"' , '"+
				str(shoe)+"' , '"+
				str(dress)+"', '"+
				str(row['arm'])+"', '"+
				str(sleeve)+"', '"+
				str(accessory)+"')")
		else:
			cursor.execute("UPDATE "+p+" SET face = '"+str(face)+"', shoes = '"+str(shoe)+"', dress = '"+str(dress)+"', armdress ='"+str(sleeve)+"', accessory='"+str(accessory)+"' WHERE id=(SELECT MAX(id) FROM "+p+")")
	if not update:
		row = cursor.execute("SELECT * FROM princess_garment WHERE id = (SELECT MAX(id) FROM princess_garment)").fetchone()
		cursor.execute("INSERT INTO princess_garment VALUES ("+str(row['id']+1)+" , '"+str(row["hair_back"])+"' , '"+row["skin"]+"', '"+row['face']+"' , '"+row['hair']+"' , '"+row['shoes']+"' , '"+row['dress']+"', '"+row['arm']+"', '"+str(row['armdress'])+"', '"+row['accessory']+"')")
	universe.db.commit()
