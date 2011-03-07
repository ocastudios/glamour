# -*- coding: utf-8 -*-

from settings import *


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
