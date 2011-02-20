# -*- coding: utf-8 -*-

from settings import *


def clean_up(level):
    level.universe.db_cursor.execute("UPDATE save SET dirt = "+str(level.princesses[0].dirt)+" WHERE name = '"+level.princesses[0].name+"'")
    level.universe.db.commit()

def unlock(level, type, garment):
    level.universe.db_cursor.execute("UPDATE unlock SET status = 'unlocked' WHERE type = '"+type+"' and garment = '"+garment+"'")
    level.universe.db.commit()

def use_message(level, name):#, name):
    level.universe.db_cursor.execute("UPDATE messages SET count = 1 WHERE name = '"+name+"';")
    level.universe.db.commit()
    

