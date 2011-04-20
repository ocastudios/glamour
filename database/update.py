# -*- coding: utf-8 -*-

from settings import *

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
	if universe.stage.princesses[0].points >= 1000:
		universe.db_cursor.execute("UPDATE save SET won=1")
		universe.db.commit()

