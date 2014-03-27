# -*- coding: utf-8 -*-
import interactive.princess as princess
import pygame
import os
import db
import sqlite3
import interactive.messages as messages
from pygame.locals import *

def connect_db(url, universe):
		universe.db = sqlite3.connect(url)
		universe.db.row_factory = sqlite3.Row
		universe.db_cursor = db_cursor = universe.db.cursor()

def create_save_db(url,name = None, hairback = None, hair = None, skin= None, arm = None, universe = None):
		print "creating or connecting to the database"
		universe.db = sqlite3.connect(url)
		universe.db.row_factory = sqlite3.Row
		universe.db_cursor = universe.db.cursor()
		print "creating save table"
		universe.db_cursor.execute("""
		  CREATE TABLE save (
				name				VARCHAR(30)	PRIMARY KEY,
				dirt				INTEGER,
				points				INTEGER,
				level				VARCHAR(30),
				position			REAL,
				center_distance		REAL,
				won					INTEGER
				);
			""")
		garment = """
			  id INTEGER PRIMARY KEY,
			  hair_back			REAL,
			  skin				VARCHAR(30),
			  face				VARCHAR(30),
			  hair				VARCHAR(30),
			  shoes				VARCHAR(30),
			  dress				VARCHAR(30),
			  arm				VARCHAR(30),
			  armdress			VARCHAR(30),
			  accessory			VARCHAR(30)
				"""
		print "creating garment tables"
		universe.db_cursor.execute("""CREATE TABLE princess_garment("""+ garment +""");""")
		universe.db_cursor.execute("""CREATE TABLE rapunzel("""+ garment + """);""")
		universe.db_cursor.execute("""CREATE TABLE snow_white("""+ garment + """);""")
		universe.db_cursor.execute("""CREATE TABLE cinderella("""+ garment + """);""")
		universe.db_cursor.execute("""CREATE TABLE sleeping_beauty("""+ garment + """);""")
		print "creating stage enemies table"
		universe.db_cursor.execute("""
		  CREATE TABLE  stage_enemies (
			id			  INTEGER		 PRIMARY KEY,
			stage		   VARCHAR(30),
			schnauzer	   INTEGER,
			carriage		INTEGER,
			butterfly	   INTEGER,
			old_lady		INTEGER,
			lion			INTEGER,
			elephant		INTEGER,
			monkey		  INTEGER,
			viking_ship	 INTEGER,
			footboy		 INTEGER,
			bird			INTEGER,
			hawk			INTEGER);
			""")
		print "create messages table"
		universe.db_cursor.execute("""CREATE TABLE messages(
			id			  INTEGER	 PRIMARY KEY,
			type			VARCHAR(30),
			name			VARCHAR(30),
			message		 VARCHAR(600),
			count		   INTEGER);
			""")
		print "create unlock table"
		universe.db_cursor.execute("""CREATE TABLE unlock(
			id			  INTEGER	 PRIMARY KEY,
			garment		 VARCHAR(30),
			status		  VARCHAR(30),
			type			VARCHAR(30));
			""")
		[universe.db_cursor.execute("INSERT INTO messages VALUES ("+str(i[0])+",'"+ i[1]+"','"+ i[2]+"','"+ messages.enemy[i[2]].replace("'","''")+"',0);") for i in (
			[1, "enemy", "birdy"],		  [2, "enemy", "butterflies"],		[3, "enemy", "carriage"],
			[4, "enemy", "elephant"],	   [5, "enemy", "footboy" ],		   [6, "enemy", "giraffe" ],
			[7, "enemy", "hawk"	],	   [8, "enemy", "lion"	],		   [9, "enemy", "monkey"  ],
			[10,"enemy", "old lady" ],	  [11,"enemy", "penguin"  ],		  [12,"enemy", "schnauzer"],
			[13,"enemy", "viking ship"])]
		
		[universe.db_cursor.execute("INSERT INTO messages VALUES ("+ str(i[0])+",'"+ i[1]+"','"+ i[2]+"','"+ messages.place[i[2]].replace("'","''")+"',0);") for i in (
			[14,"place", "bathhouse"  ],	[15,"place", "accessory hall"],	 [16,"place", "cinderellas castle"],
			[17,"place", "drains"],		 [18,"place", "dress tower"],		[19,"place", "gateway"],
			[20,"place", "maddelines house"],[21,"place", "magic beauty parlor"],[22,"place", "make-up tower"],
			[23,"place", "rapunzels villa"],[24,"place", "shoes shop"],		 [25,"place", "sleeping beautys palace"],
			[26,"place", "snow-whites castle"],[27,"place", "zoo"])]
		[universe.db_cursor.execute("INSERT INTO messages VALUES ("+ str(i[0])+",'"+ i[1]+"','"+ i[2]+"','"+ messages.event[i[2]].replace("'","''")+"',0);") for i in (
			[28,"event", "dirty"],[29,"event", "dirty 2"],[30,"event", "dirty 3"],[31,"event", "save game"],
			[32,"event", "day start 1" ],[33,"event", "day start 2" ],[34,"event", "day start 3" ],
			[35,"event", "day start 4" ],[36,"event", "day start 5" ],[37,"event", "day start 6" ],
			[38,"event", "day start 7" ],[39,"event", "day start 8" ],[40,"event", "day start 9" ],
			[41,"event", "day start 10"],[42,"event", "day start 11"],[43,"event", "day start 12"],
			[44,"event", "day start 13"],[45,"event", "day start 14"])]
		[universe.db_cursor.execute("INSERT INTO messages VALUES ("+ str(i[0])+",'"+ i[1]+"','"+ i[2]+"','"+ messages.intro[i[2]].replace("'","''")+"',0);") for i in (
			[46,"intro", "first day a"],[47,"intro", "first day b"],[48,"intro", "first day c"],[49,"intro", "first day d"],
			[50,"intro", "first day e"],[51,"intro", "first day f"],[52,"intro", "first day g"],[53,"intro", "first day h"],
			[54,"intro", "first day i"])]
		universe.db_cursor.execute("INSERT INTO save VALUES('"+name+"', 0 , 0 ,'level','(0,0)',5220, 0);")
		universe.db_cursor.execute("INSERT INTO princess_garment VALUES(1,'"+
						str(hairback)+"','"+skin+"','face_simple','"+hair+"','shoes_slipper','dress_plain','"+arm+"', 'None','accessory_ribbon');")
		universe.db_cursor.execute("INSERT INTO cinderella VALUES(1,0,'skin_tan','face_eyeshades','hair_cinderella','shoes_crystal', 'dress_red','arm_tan','sleeve_red','accessory_shades');")
		universe.db_cursor.execute("INSERT INTO snow_white VALUES(1,'None','skin_pink','face_eyelids','hair_snowwhite','shoes_red','dress_yellow','arm_pink','sleeve_yellow','accessory_purse');")
		universe.db_cursor.execute("INSERT INTO sleeping_beauty VALUES(1,'None','skin_pink','face_simple','hair_sleeping','shoes_slipper','dress_plain','arm_pink',0,'accessory_crown');")
		universe.db_cursor.execute("INSERT INTO rapunzel VALUES(1,'hair_rapunzel_back','skin_pink','face_simple','hair_rapunzel','shoes_white','dress_yellow','arm_pink','sleeve_yellow','accessory_ribbon');")
		universe.db_cursor.execute("INSERT INTO stage_enemies VALUES(1,'BathhouseSt',0,0,0,0,0,0,0,0,0,0,0);")
		universe.db_cursor.execute("INSERT INTO stage_enemies VALUES(2,'AccessorySt',0,0,0,0,0,0,0,0,0,0,0);")
		universe.db_cursor.execute("INSERT INTO stage_enemies VALUES(3,'DressSt',	0,0,0,0,0,0,0,0,0,1,1);")
		universe.db_cursor.execute("INSERT INTO stage_enemies VALUES(4,'MakeupSt',	0,0,0,1,0,0,0,0,0,0,0);")
		universe.db_cursor.execute("INSERT INTO stage_enemies VALUES(5,'ShoesSt',	0,0,0,0,0,0,0,0,1,0,0);")
		universe.db_cursor.execute("INSERT INTO stage_enemies VALUES(6,'Beaten',		0,0,0,0,0,0,0,0,0,0,0);")
		
		[universe.db_cursor.execute("INSERT INTO unlock VALUES("+str(i[0])+",'"+i[1]+"','"+i[2]+"','"+i[3]+"');") for i in (
			[1,	'beret',	'locked',	'accessory'],
			[2,	'crown',	'unlocked',	'accessory'],
			[3,	'mask',		'locked',	'accessory'],
			[4,	'purse',	'unlocked',	'accessory'],
			[5,	'ribbon',	'unlocked',	'accessory'],
			[6,	'shades',	'locked',	'accessory'],
			[7,	'indian',	'locked',	'dress'],
			[8,	'kimono',	'locked',	'dress'],
			[9,	'pijamas',	'locked',	'dress'],
			[10,	'pink',		'unlocked',	'dress'],
			[11,	'plain',	'unlocked',	'dress'],
			[12,	'red',		'unlocked',	'dress'],
			[13,	'yellow',	'locked',	'dress'],
			[14,	'eyelids',	'unlocked',	'face'],
			[15,	'eyeshades',	'unlocked',	'face'],
			[16,	'geisha',	'locked',	'face'],
			[17,	'indian',	'locked',	'face'],
			[18,	'lipstick',	'locked',	'face'],
			[19,	'clean',	'locked',	'face'],
			[20,	'simple',	'unlocked',	'face'],
			[21,	'black',	'unlocked',	'hair'],
			[22,	'brown',	'unlocked',	'hair'],
			[23,	'cinderella',	'locked',	'hair'],
			[24,	'rapunzel',	'locked',	'hair'],
			[25,	'rastafari',	'unlocked',	'hair'],
			[26,	'red',		'unlocked',	'hair'],
			[27,	'short',	'unlocked',	'hair'],
			[28,	'sleeping',	'locked',	'hair'],
			[29,	'snowwhite',	'locked',	'hair'],
			[30,	'yellow',	'unlocked',	'hair'],
			[31,	'boots',	'locked',	'shoes'],
			[32,	'crystal',	'locked',	'shoes'],
			[33,	'flower',	'locked',	'shoes'],
			[34,	'red',		'unlocked',	'shoes'],
			[35,	'slipper',	'unlocked',	'shoes'],
			[36,	'white',	'unlocked',	'shoes'],
			[37,	'braid_and_tail','unlocked','hair'],
			[38,	'geisha',		'unlocked','hair']
				)]
		universe.db.commit()



