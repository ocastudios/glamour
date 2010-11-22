from settings import *
import fairy
import random

def choose_event(level,starting_game=False):
    if level.event_counter:
        level.event_counter += 1
        if level.event_counter > 600:
            level.event_counter = 0
    else:
        princess_pos = level.princesses[0].center_distance
        if starting_game:
            level.princesses[0].center_distance = 5220*scale
            level.event_counter += 1
            intro_first_day = level.universe.db_cursor.execute("SELECT * FROM messages WHERE name = 'first day a'").fetchall()
            if intro_first_day[0]['count'] == 0:
                level.Fairy = 'loading'
                message_text = random.choice(intro_first_day)['message']
                level.fae[0] = fairy.Message(level, message = message_text)
                level.universe.db_cursor.execute('UPDATE messages SET count = 1 WHERE type = "intro";')
                level.universe.db.commit()
        elif level.name == "bathhouse":
            if 4700*scale < princess_pos < 5000*scale:
                create_message(level,'maddelines house')
            elif 8700*scale < princess_pos < 9000*scale:
                create_message(level,'magic beauty parlor')
            elif 850*scale <princess_pos < 1050*scale:
                create_message(level,"bathhouse")
        elif level.name == "accessory":
            if princess_pos < 360:
                create_message(level,"accessory hall")
            elif 8300 < princess_pos:
                create_message(level,"sleeping beautys palace")
        elif level.name == "dress":
            if princess_pos < 300:
                create_message(level,"dress tower")
            elif 8900 < princess_pos:
                create_message(level,"snow-whites castle")
        elif level.name == "makeup":
            if princess_pos <300:
                create_message(level,"make-up tower")
            elif 8900 < princess_pos:
                create_message(level,"cinderellas castle")
        elif level.name == "shoes":
            if princess_pos < 300:
                create_message(level,"shoes shop")
            if princess_pos > 8900:
                create_message(level,"rapunzels villa")


def create_message(level, name, unique=True):
    level.event_counter +=1
    row = level.universe.db_cursor.execute("SELECT * FROM messages WHERE name = '"+name+"'").fetchone()
    if row['count'] == 0 or unique==False:
        print "Here comes the Fairy "+name
        level.fairy = 'loading'
        level.fae[0] = fairy.Message(level, message = row['message'])
        level.universe.db_cursor.execute("UPDATE messages SET count = 1 WHERE name = '"+name+"'")
        level.universe.db.commit()
