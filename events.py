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
            level.event_counter += 1
            intro_first_day = level.universe.db_cursor.execute("SELECT * FROM messages WHERE name = 'first day a'").fetchone()
            if intro_first_day['count'] == 0:
                level.Fairy = True
                level.fae = [fairy.Message(level, message = intro_first_day['message']),fairy.Fairy(20,level)]
                level.universe.db_cursor.execute("UPDATE messages SET count = 99999999 WHERE name = 'first day a'")
                level.universe.db.commit()
            else:
                intro = level.universe.db_cursor.execute("SELECT * FROM messages WHERE type = 'intro' AND count = (SELECT MIN(count) FROM messages WHERE type = 'intro')").fetchall()
                level.fairy = True
                least_used = level.universe.db_cursor.execute("select min(count) as count from messages where type = 'intro'").fetchone()['count']
                print intro
                message_number = random.randint(0,len(intro)-1)
                message_text = intro[message_number]
                text = message_text['message']
                level.fae = [fairy.Message(level, message = text),fairy.Fairy(20,level)]
                level.universe.db_cursor.execute('UPDATE messages SET count = '+str(least_used+1)+' where message = "'+text+'";')
                level.universe.db.commit()
        elif level.name == "bathhouse":
            if 4480*scale < princess_pos < 5560*scale:
                create_message(level,'maddelines house')
            elif princess_pos > 8840*scale:
                create_message(level,'magic beauty parlor')
            elif princess_pos < 1590*scale:
                create_message(level,"bathhouse")
        elif level.name == "accessory":
            if princess_pos < 360:
                create_message(level,"accessory hall")
            elif 4230 < princess_pos:
                create_message(level,"sleeping beautys palace")
        elif level.name == "dress":
            if princess_pos < 300:
                create_message(level,"dress tower")
            elif 4440 < princess_pos:
                create_message(level,"snow-whites castle")
        elif level.name == "makeup":
            if princess_pos <300:
                create_message(level,"make-up tower")
            elif 4430 < princess_pos:
                create_message(level,"cinderellas castle")
        elif level.name == "shoes":
            if princess_pos < 300:
                create_message(level,"shoes shop")
            if princess_pos > 4500:
                create_message(level,"rapunzels villa")


def create_message(level, name, unique=True):
    level.event_counter +=1
    row = level.universe.db_cursor.execute("SELECT * FROM messages WHERE name = '"+name+"'").fetchone()
    if row['count'] == 0 or unique==False:
        print "Here comes the Fairy "+name
        level.fairy = True
        level.fae[0] = fairy.Message(level, message = row['message'])
        level.universe.db_cursor.execute("UPDATE messages SET count = 1 WHERE name = '"+name+"'")
        level.universe.db.commit()
