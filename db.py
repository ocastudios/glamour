# -*- coding: utf-8 -*-
import obj_images
import princess
import pygame
import drapes
import os
import db
import sqlite3
import messages
from pygame.locals import *


def create_save_db(url,name):
        print "creating or connecting to the database"
        db         = sqlite3.connect(url)
        db_cursor  = db.cursor()
        print "creating save table"
        db_cursor.execute("""
          CREATE TABLE save (
              name                VARCHAR(30)    PRIMARY KEY,
              dirt                VARCHAR(30),
              points              INTEGER,
              level               VARCHAR(30),
              position            REAL,
              center_distance     REAL
              );
            """)
        garment = """
              id INTEGER PRIMARY KEY,
              hair_back           VARCHAR(30),
              skin                VARCHAR(30),
              face                VARCHAR(30),
              hair                VARCHAR(30),
              shoes               VARCHAR(30),
              dress               VARCHAR(30),
              arm                 VARCHAR(30),
              armdress            VARCHAR(30),
              accessory           VARCHAR(30)
                """
        print "creating garment tables"
        db_cursor.execute("""CREATE TABLE princess_garment("""+ garment +""");""")
        db_cursor.execute("""CREATE TABLE rapunzel("""+ garment + """);""")
        db_cursor.execute("""CREATE TABLE snow_white("""+ garment + """);""")
        db_cursor.execute("""CREATE TABLE cinderella("""+ garment + """);""")
        db_cursor.execute("""CREATE TABLE sleeping_beauty("""+ garment + """);""")
        print "creating stage enemies table"
        db_cursor.execute("""
          CREATE TABLE  stage_enemies (
            id              INTEGER         PRIMARY KEY,
            stage           VARCHAR(30),
            schnauzer       INTEGER,
            carriage        INTEGER,
            butterfly       INTEGER,
            old_lady        INTEGER,
            lion            INTEGER,
            elephant        INTEGER,
            monkey          INTEGER,
            viking_ship     INTEGER,
            footboy         INTEGER,
            bird            INTEGER,
            hawk            INTEGER);
            """)
        print "create messages table"
        db_cursor.execute("""CREATE TABLE messages(
            id              INTEGER     PRIMARY KEY,
            type            VARCHAR(30),
            name            VARCHAR(30),
            message         VARCHAR(600),
            count           INTEGER);
            """)
        [db_cursor.execute("INSERT INTO messages VALUES ("+str(i[0])+",'"+ i[1]+"','"+ i[2]+"','"+ messages.enemy[i[2]].replace("'","''")+"',0);") for i in (
            [1, "enemy", "birdy"],          [2, "enemy", "butterflies"],        [3, "enemy", "carriage"],            [4, "enemy", "elephant"],       [5, "enemy", "footboy" ],           [6, "enemy", "giraffe" ],            [7, "enemy", "hawk"    ],       [8, "enemy", "lion"    ],           [9, "enemy", "monkey"  ],            [10,"enemy", "old lady" ],      [11,"enemy", "penguin"  ],          [12,"enemy", "schnauzer"],            [13,"enemy", "viking ship"])]
        
        [db_cursor.execute("INSERT INTO messages VALUES ("+ str(i[0])+",'"+ i[1]+"','"+ i[2]+"','"+ messages.place[i[2]].replace("'","''")+"',0);") for i in (
            [14,"place", "bathhouse"  ],    [15,"place", "accessory hall"],     [16,"place", "cinderellas castle"],            [17,"place", "drains"],         [18,"place", "dress tower"],        [19,"place", "gateway"],            [20,"place", "maddelines house"],[21,"place", "magic beauty parlor"],[22,"place", "make-up tower"],            [23,"place", "rapunzels villa"],[24,"place", "shoes shop"],         [25,"place", "sleeping beautys palace"],            [26,"place", "snow-whites castle"],[27,"place", "zoo"])]
        [db_cursor.execute("INSERT INTO messages VALUES ("+ str(i[0])+",'"+ i[1]+"','"+ i[2]+"','"+ messages.event[i[2]].replace("'","''")+"',0);") for i in (
            [28,"event", "dirty"],[29,"event", "dirty 2"],[30,"event", "dirty 3"],[31,"event", "save game"],            [32,"event", "day start 1" ],[33,"event", "day start 2" ],[34,"event", "day start 3" ],            [35,"event", "day start 4" ],[36,"event", "day start 5" ],[37,"event", "day start 6" ],            [38,"event", "day start 7" ],[39,"event", "day start 8" ],[40,"event", "day start 9" ],            [41,"event", "day start 10"],[42,"event", "day start 11"],[43,"event", "day start 12"],            [44,"event", "day start 13"],[45,"event", "day start 14"])]
        [db_cursor.execute("INSERT INTO messages VALUES ("+ str(i[0])+",'"+ i[1]+"','"+ i[2]+"','"+ messages.intro[i[2]].replace("'","''")+"',0);") for i in (
            [46,"intro", "first day a"],[47,"intro", "first day b"],[48,"intro", "first day c"],[49,"intro", "first day d"],            [50,"intro", "first day e"],[51,"intro", "first day f"],[52,"intro", "first day g"],[53,"intro", "first day h"],
            [54,"intro", "first day i"])]
        db.commit()
