# -*- coding: utf-8 -*-
import random
import pygame
import os
import db
import sqlite3

from settings import *



def unlocked(stage, clothe_type, field = None, limit_n_random = False):
	row				 = stage.universe.db_cursor.execute("""
		SELECT * 
			FROM unlock 
			WHERE   type = '"""+clothe_type+"""'
			AND	 status  = 'unlocked'
		""").fetchall()
	if field:
		row = [i[field] for i in row]
		if limit_n_random:
			if len(row)>=4:
				row = random.sample(row,limit_n_random)
			else:
				row = random.sample(row,len(row))
	return row

def street(stage, street, table):
	db = sqlite3.connect(main_dir+'/data/'+street+'.db')
	db.row_factory = sqlite3.Row
	cursor = db.cursor()
	result = cursor.execute("SELECT * FROM "+table+" ORDER BY id ASC").fetchall()
	cursor.close()
	return result

def message(stage, name, one = False):
	cursor = stage.universe.db_cursor
	if not one:
		result = cursor.execute("SELECT * FROM messages WHERE name = '"+name+"'").fetchall()
	else:
		result = cursor.execute("SELECT * FROM messages WHERE name = '"+name+"'").fetchone()
	cursor.close()
	return result

def is_locked(stage,clothe_type,garment):
	row				 = stage.universe.db_cursor.execute("""
	SELECT * 
		FROM unlock 
		WHERE   type = '"""+clothe_type+"""'
		AND	 garment = '"""+garment+"""'
	""").fetchone()
	if row['status'] == 'locked':
		return True
	else:
		return False
		
def is_beaten(stage,enemy):
	cursor = stage.universe.db_cursor
	result = cursor.execute("SELECT "+enemy+" FROM stage_enemies WHERE stage = 'Beaten'").fetchone()
	if int(result[0])>0:
		return True
	else:
		return False

def last_balls(level):
	cursor  = level.universe.db_cursor
	sql	 = "SELECT * FROM princess_garment ORDER BY id DESC LIMIT 3 OFFSET 1"
	result = cursor.execute(sql).fetchall()
	cursor.close()
	return result
	
def my_outfit(level, princess):
	cursor  = level.universe.db_cursor
	sql	 = "SELECT * FROM "+princess+" WHERE id = (SELECT MAX(id) FROM "+princess+")"
	result  = cursor.execute(sql).fetchone()
	cursor.close()
	return result

def different_hairs_used(level):
	cursor	= level.universe.db_cursor
	sql		= "SELECT DISTINCT hair FROM princess_garment"
	result	= cursor.execute(sql).fetchall()
	cursor.close()
	return len(result)

def beaten_enemies(level):
	cursor 	= level.universe.db_cursor
	sql 	= "SELECT * FROM stage_enemies WHERE stage = 'Beaten'"
	result	= cursor.execute(sql).fetchone()
	count = 0
	for i in ('schnauzer','old_lady', 'lion', 'viking_ship','footboy'):
		if result[i]:
			count += 1
	cursor.close()
	return count
