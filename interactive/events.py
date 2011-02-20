from settings import *
import pygame
import fairy
import random
import database
import database.update
import interactive
import interactive.popup

def pn(some_number):
    return round(some_number*scale)

def choose_event(level,starting_game=False):
#    if level.event_counter:
#        level.event_counter += 1
#        if level.event_counter > 600:
#            level.event_counter = 0
#    else:
    princess_pos = level.princesses[0].center_distance
    if starting_game:
        level.princesses[0].center_distance = pn(5220)
        level.event_counter += 1
        intro_first_day = database.query.message(level, 'first day a')
        if intro_first_day[0]['count'] == 0:
            level.Fairy = 'loading'
            message_text = random.choice(intro_first_day)['message']
            level.fae[0] = fairy.Message(level, message = message_text)
            database.update.use_message(level,'intro')
    elif level.name == "bathhouse":
        if pn(4700) < princess_pos < pn(5000):
            create_message(level,'maddelines house')
        elif pn(8700) < princess_pos < pn(9000):
            create_message(level,'magic beauty parlor')
        elif pn(850) <princess_pos < pn(1050):
            create_message(level,"bathhouse")
    elif level.name == "accessory":
        if princess_pos < pn(360):
            create_message(level,"accessory hall")
        elif pn(8300) < princess_pos:
            create_message(level,"sleeping beautys palace")
    elif level.name == "dress":
        if princess_pos < pn(300):
            create_message(level,"dress tower")
        elif pn(8900) < princess_pos:
            create_message(level,"snow-whites castle")
    elif level.name == "makeup":
        if princess_pos <pn(300):
            create_message(level,"make-up tower")
        elif pn(8900) < princess_pos:
            create_message(level,"cinderellas castle")
    elif level.name == "shoes":
        if princess_pos < pn(300):
            create_message(level,"shoes shop")
        if princess_pos > pn(8900):
            create_message(level,"rapunzels villa")

    if level.unlocking:
        unlock(level,level.unlocking)


def create_message(level, name, unique=True):
    level.event_counter +=1
    row = database.query.message(level, name, one = True)
    if row['count'] == 0 or unique==False:
        print "Here comes the Fairy "+name
        level.fairy = 'loading'
        pygame.mixer.Channel(0).play(level.fae[1].whistle)
        level.fae[0] = fairy.Message(level, message = row['message'])
        database.update.use_message(level, name)

def unlock(level, unlocking):
    if database.query.is_locked(level,unlocking['type'],unlocking['name']):
        popup = interactive.popup.Unlocking_Message(level, unlocking)
        level.unlocking['list'] = [popup, interactive.popup.Unlocking_Icon(level,popup,unlocking)]
        database.update.unlock(level, unlocking['type'],unlocking['name'])
        database.update.use_message(level,unlocking['name'])
