import princess
import os
import datetime
import pygame
from settings import *

def save_file(level, hairback = None, skin = None, face = None, hair = None, shoes = None, dress = None, arm = None, armdress = None, accessory = None, past_ball = None, great_past_ball = None, position = None, Ball = None):
    universe = level.universe
    princess = level.princesses[0]
    #avoid errors in case there are no saved files
    try:
        os.mkdir(universe.main_dir+'/data/saves/'+str(princess.name))
    except:
        pass
    dir = universe.main_dir+'/data/saves/'+str(princess.name)

#    old_file = open('data/saves/'+princess.name+'/'+princess.name+'.glamour','r').readlines()
    day = datetime.datetime.today()
#    for i in ['hairback', 'skin', "face", "hair", "shoes", "dress", "arm", "armdress", "accessory"]:
#        exec('if not '+i+':\n'+
#            '    for line in old_file:\n'+
#            '       if i == line.split()[0]: '+i+' = line.split()[1]')
    if dress == "dress_yellow":
        armdress = "sleeve_yellow"
    elif dress == "dress_red":
        armdress = "sleeve_red"
    else:
        armdress = "None"
    hair_backs = ['hair_black','hair_brown','hair_rastafari','hair_rapunzel','hair_red']
    if hair in hair_backs:
        hairback = hair+'_back'
    else:
        hairback = "None"

    for street in ['BathhouseSt','DressSt','AccessorySt','MakeupSt','ShoesSt']:
        exec(street +" = ''")
        for i in level.enemies_list[street]:
            exec(street + "=" + street + "+ ' ' + i + ' ' ")


#    files = []
#    new_file = open('data/saves/'+princess.name+'/'+princess.name+'.glamour','w')
#    files.append(new_file)
#    if Ball:
#        backupfile = open('data/saves/'+princess.name+'/'+princess.name+'_backup.glamour','w')
#        files.append(backupfile)

    cursor = level.universe.db_cursor
    cursor.execute("UPDATE save SET center_distance = '"+str(int(princess.center_distance/scale))+"' WHERE name = '"+str(princess.name)+"'")
    cursor.execute("UPDATE princess_garment SET hair_back = '"+str(hairback)+"' WHERE id = (SELECT max(id) FROM princess_garment)")
    cursor.execute("UPDATE princess_garment SET skin     = '"+str(skin)+"' WHERE id =  (SELECT max(id) FROM princess_garment)")
    cursor.execute("UPDATE princess_garment SET face     = '"+str(face)+"' WHERE id =  (SELECT max(id) FROM princess_garment)")
    cursor.execute("UPDATE princess_garment SET hair     = '"+str(hair)+"' WHERE id =  (SELECT max(id) FROM princess_garment)")
    cursor.execute("UPDATE princess_garment SET shoes    = '"+str(shoes)+"' WHERE id =  (SELECT max(id) FROM princess_garment)")
    cursor.execute("UPDATE princess_garment SET dress    = '"+str(dress)+"' WHERE id =  (SELECT max(id) FROM princess_garment)")
    cursor.execute("UPDATE princess_garment SET arm      = '"+str(arm)+"'   WHERE id =  (SELECT max(id) FROM princess_garment)")
    cursor.execute("UPDATE princess_garment SET armdress = '"+str(armdress)+"' WHERE id =  (SELECT max(id) FROM princess_garment)")
    cursor.execute("UPDATE princess_garment SET accessory= '"+str(accessory)+"' WHERE id =  (SELECT max(id) FROM princess_garment)")
    cursor.execute("UPDATE save SET dirt     = '"+str(princess.dirt)+"' WHERE name = '"+str(princess.name)+"'")
    cursor.execute("UPDATE save SET points   = '"+str(princess.points)+"' WHERE name = '"+str(princess.name)+"'")
    


#    for i in files:
#        new_file.write(
#            '#This is a saved file of the glamour game.\n'
#            '#It was recorded on '+str(day.month)+'/'+str(day.day)+'/'+str(day.year)+' at '+str(day.hour)+':'+str(day.minute)+'\n'
#            'name           '+ str(princess.name) + '\n'
#            'center_distance '+ str(int(princess.center_distance/scale))+'\n'
#            'hairback       '+ str(hairback) + ' 0'+'\n'
#            'skin           '+ str(skin) + ' 1'+'\n'
#            'face           '+ str(face) + ' 2'+'\n'
#            'hair           '+ str(hair) + ' 3'+'\n'
#            'shoes          '+ str(shoes)+' 4'+'\n'
#            'dress          '+ str(dress)+' 5'+'\n'
#            'arm            '+ str(arm)  +  ' 6'+'\n'
#            'armdress       '+ str(armdress) +' 7'+'\n'
#            'accessory      '+ str(accessory) +' 8'+'\n'
#            'dirt           '+ str(princess.dirt)+ '\n'
#            '#Points'+'\n'
#            'points 0'+'\n'
#            '#Level'+'\n'
#            'level level'+'\n'
#            'position       '+ str(position) +'\n'
#            'past_ball          None \n'
#            'great_past_ball    None\n'
#            'BathhouseSt    '+ BathhouseSt +'\n'
#            'DressSt        '+ DressSt     +'\n'
#            'AccessorySt    '+ AccessorySt +'\n'
#            'MakeupSt       '+ MakeupSt    +'\n'
#            'ShoesSt        '+ ShoesSt     + '\n'
#            'level.princesses_garment'
#                    )
#    new_file.close()
    print "O arquivo save.py foi utilizado "
    if Ball:
        backupfile.close()



    return 'data/saves/'+princess.name+'/'+princess.name+'.glamour'
