# -*- coding: utf-8 -*-
import random
import pygame
import os
from . import db
import sqlite3
from settings import *

def unlocked(universe, clothe_type=None, field = None, limit_n_random = False):
	type_to_select = ""
	if clothe_type:
		type_to_select = "type = '"+clothe_type+"' AND "
	sql = """
		SELECT * 
			FROM unlock 
			WHERE   """+type_to_select+""" status  = 'unlocked'
		"""
	row				 = universe.db_cursor.execute(sql).fetchall()
	if field:
		row = [i[field] for i in row]
		if limit_n_random:
			if len(row)>=4:
				row = random.sample(row,limit_n_random)
			else:
				row = random.sample(row,len(row))
	return row

def street(universe, street, table):
	db = sqlite3.connect(os.path.join(directory.data,street+'.db'))
	db.row_factory = sqlite3.Row
	cursor = db.cursor()
	result = cursor.execute("SELECT * FROM "+table+" ORDER BY id ASC").fetchall()
	return result

def message(universe, name, one = False):
	cursor = universe.db_cursor
	if not one:
		result = cursor.execute("SELECT * FROM messages WHERE name = '"+name+"'").fetchall()
	else:
		result = cursor.execute("SELECT * FROM messages WHERE name = '"+name+"'").fetchone()
	return result

def is_locked(universe,clothe_type,garment):
	row				 = universe.db_cursor.execute("""
	SELECT * 
		FROM unlock 
		WHERE   type = '"""+clothe_type+"""'
		AND	 garment = '"""+garment+"""'
	""").fetchone()
	if row['status'] == 'locked':
		return True
	else:
		return False
		
def is_beaten(universe,enemy):
	cursor = universe.db_cursor
	result = cursor.execute("SELECT "+enemy+" FROM stage_enemies WHERE stage = 'Beaten'").fetchone()
	if int(result[0])>0:
		return True
	else:
		return False

def last_balls(universe):
	cursor  = universe.db_cursor
	sql	 = "SELECT * FROM princess_garment ORDER BY id DESC LIMIT 3 OFFSET 1"
	result = cursor.execute(sql).fetchall()
	return result
	
def my_outfit(universe, princess, previous=0):
	cursor  = universe.db_cursor
	sql	 = "SELECT * FROM "+princess+" WHERE id = (SELECT MAX(id) FROM "+princess+")-"+str(previous)
	result  = cursor.execute(sql).fetchone()
	return result

def am_i_dirt(universe):
	cursor  = universe.db_cursor
	result  = cursor.execute("SELECT * FROM save").fetchone()['dirt']
	return result

def different_hairs_used(universe):
	cursor	= universe.db_cursor
	sql		= "SELECT DISTINCT hair FROM princess_garment"
	result	= cursor.execute(sql).fetchall()
	return len(result)

def beaten_enemies(universe):
	cursor 	= universe.db_cursor
	sql 	= "SELECT * FROM stage_enemies WHERE stage = 'Beaten'"
	result	= cursor.execute(sql).fetchone()
	count = 0
	for i in ('schnauzer','old_lady', 'lion', 'viking_ship','footboy'):
		if result[i]:
			count += 1
	return count

def won(universe):
	cursor	= universe.db_cursor
	sql		= "SELECT won FROM save LIMIT 1"
	result	= cursor.execute(sql).fetchone()
	if int(result[0])>0:
		return True
	else:
		return False

