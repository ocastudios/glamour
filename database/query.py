# -*- coding: utf-8 -*-
import random
import pygame
import os
import db
import sqlite3

from settings import *

def unlocked(stage, clothe_type, field = None, limit_n_random = False):
    row                 = stage.universe.db_cursor.execute("""
        SELECT * 
            FROM unlock 
            WHERE   type = '"""+clothe_type+"""'
            AND     status  = 'unlocked'
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
    if not one:
        return stage.universe.db_cursor.execute("SELECT * FROM messages WHERE name = '"+name+"'").fetchall()
    else:
        return stage.universe.db_cursor.execute("SELECT * FROM messages WHERE name = '"+name+"'").fetchone()

def is_locked(stage,clothe_type,garment):
    row                 = stage.universe.db_cursor.execute("""
    SELECT * 
        FROM unlock 
        WHERE   type = '"""+clothe_type+"""'
        AND     garment = '"""+garment+"""'
    """).fetchone()
    if row['status'] == 'locked':
        return True
    else:
        return False
