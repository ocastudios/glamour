import pygame
import utils.obj_images as obj_images
import random
import interface.widget as widget
import utils.save as save
from settings import *

import gettext
t = gettext.translation('glamour', 'locale')
_ = t.ugettext

def p(positions):
    return [int(round(i*scale)) for i in positions ]

class Ball():
    directory = data_dir+'/images/interface/ball/'
    def __init__(self, level, universe, princess):
        self.position = 0,0
        self.universe   = universe
        self.boyfriend  = None
        cursor = level.universe.db_cursor
        universe.db.commit()
        self.texts      = []
        self.texts+= [StarBall()]
        self.level      = level
        self.compute_glamour_points(level)
        self.background      = pygame.Surface((level.universe.width,level.universe.height),pygame.SRCALPHA).convert_alpha()
        for file in (self.directory+'ball-back.png',self.directory+'back-bubbles.png'):
            self.background.blit(obj_images.scale_image(pygame.image.load(file).convert_alpha()), (0,0))
        self.left_bar   = VerticalBar(self)
        self.princess   = princess
        self.Bar        = VerticalBar(self)
        self.Frame      = BallFrame(self)

        self.dancers    = [Dancer(p(i)) for i in [1200,100],[200,200],[800,300],[600,400],[300,600]]
        self.buttons = [widget.Button(data_dir+'/images/interface/title_screen/button_ok/',(1050,700), self.level,self.return_to_game)]
        pygame.mixer.music.load(data_dir+"/sounds/music/strauss_waltz_wedley.ogg")
        pygame.mixer.music.play()
        princesses_list      = ['Cinderella', 'Snow_White', 'Sleeping_Beauty','Rapunzel']
        garment_list         = ['Accessory', 'Dress', 'Shoes','Makeup']
        Accessory_list       = ['crown', 'purse','ribbon','shades']
        Dress_list           = ['pink','plain','red','yellow']
        Shoes_list           = ['crystal','red','slipper','white']
        Makeup_list          = ['eyelids','eyeshades','lipstick','simple']
        self.counter         = 0
        self.bigprincess = BigPrincess(self)

    def update_all(self):

        self.left_bar.update_all()
        self.level.game_mouse.update()
        self.universe.screen_surface.blit(self.background,(0,0))
        for i in self.dancers:
            self.universe.screen_surface.blit(i.image,i.position)
            i.update_all()
        self.universe.screen_surface.blit(self.Frame.image,self.Frame.position)
        self.Frame.update_all()
        self.universe.screen_surface.blit(self.Bar.image,self.Bar.position)
        self.Bar.update_all()
        if self.counter > 60:
            self.universe.screen_surface.blit(self.bigprincess.image,self.bigprincess.pos)
            self.bigprincess.update_all()
        if self.counter > 90:
            for i in self.texts:
                self.universe.screen_surface.blit(i.image,i.pos)
                i.update_all()
        if self.boyfriend:
            if self.counter == 100:
                self.texts+= [widget.GameText(_("and won the heart of"), (1090,237), self,font_size = 40)]
            if self.counter == 110:
                self.texts+= [widget.GameText(".", (1300,237), self,font_size = 40)]
            if self.counter == 120:
                self.texts+= [widget.GameText(" .", (1300,237), self,font_size = 40)]
            if self.counter == 130:
                self.texts+= [widget.GameText("  .", (1300,237), self,font_size = 40)]
            if self.counter > 150:
                self.universe.screen_surface.blit(self.boyfriend.image,self.boyfriend.pos)
                self.boyfriend.update_all()
        if self.counter > 160:
            for i in self.buttons:
                self.universe.screen_surface.blit(i.image,i.pos)
                i.update_all()

        if self.counter == 160:
            if self.boyfriend:
                self.texts += [widget.GameText(self.boyfriend.name,(1156,280),self, font_size = 60,color=(58,56,0))]

        if self.counter <= 160:
            self.counter += 1

    def compute_glamour_points(self,level):
        garments= ('face','shoes','dress','accessory')
        cursor = level.universe.db_cursor
        princess_rows = cursor.execute("SELECT * FROM princess_garment").fetchall()
        fairy_tale_rows = [
                cursor.execute("SELECT * FROM "+princess_name).fetchall() for princess_name in ("cinderella","rapunzel","sleeping_beauty","snow_white")
                        ]
        save_row     = cursor.execute("SELECT * FROM save").fetchone()
        accumulated_points = int(save_row["points"])
        princess_garments   = {
                    "this_ball":[princess_rows[len(princess_rows)-1][item] for item in garments],
                    "last_ball":[princess_rows[len(princess_rows)-2][item] for item in garments]
                            }
        others_garments     = {
                    "this_ball":[],
                    "last_ball":[]
                            }
        for row in fairy_tale_rows:
            for item in garments:
                others_garments["this_ball"].append(row[len(row)-1][item])
                others_garments["last_ball"].append(row[len(row)-2][item])


        print "Others Garments "+str(others_garments["this_ball"])
        print "Princess Garments"+str(princess_garments["this_ball"])

        present_repetitions = sum([others_garments["this_ball"].count(i) for i in princess_garments["this_ball"]])
        last_ball_garments  = others_garments["last_ball"]+princess_garments["last_ball"]
        past_repetitions    = sum([last_ball_garments.count(i) for i in princess_garments["this_ball"]])
        garments_history    = princess_rows[:-1]+fairy_tale_rows
        number_of_balls     = len(princess_rows)
        history_repetitions = sum([garments_history.count(i) for i in princess_garments["this_ball"]])

        print "The total repetition points for the garments in this ball is "+ str(present_repetitions)
        print "The total repetition points for the garments last ball is "+ str(past_repetitions)
        print "Fashion points is equal to 34 - 3*repetition_points - past_repetition_points"
        fashion = 34-(3*present_repetitions)-(past_repetitions)
        print "Your total Fashion points is " + str(fashion)
        dirty   = (fashion * save_row['dirt'])/3
        print "Your total Dirt points is "+ str(dirty)
        creativity = fashion*(.5-(history_repetitions/number_of_balls))
        print "Youtr total creativity points is " + str(creativity)
        glamour_points = fashion-dirty+creativity
        print "YOUR TOTAL GLAMOUR POINTS THIS BALL IS "+ str(glamour_points)+" !!!!"
        print "Now I am going to save your points"
        print "YOU HAVE ACCUMULATED A TOTAL OF " +str(accumulated_points+glamour_points)+" glamour points."
        save_table = cursor.execute("SELECT * FROM save").fetchone()
        past_glamour_points = save_table['points']
        new_glamour_points = int(past_glamour_points)+int(glamour_points)

        self.level.princesses[0].points = new_glamour_points
        cursor.execute("UPDATE save SET points = "+str(new_glamour_points))

        stage_list           = ['BathhouseSt', 'DressSt', 'AccessorySt', 'MakeupSt','ShoesSt']
        print "Preparing the new set of enemies for each stage"
        for stage in stage_list:
            general_enemies_list = ['schnauzer', 'carriage','butterfly','old_lady','viking_ship','footboy','bird']
            print "Removing enemies from "+stage
            for i in general_enemies_list:
                sql = 'update stage_enemies set '+i+'=0 where stage = "'+stage+'"'
                cursor.execute(sql)
            print "New Enemies List for "+stage
            enemy_number = random.randint(1,3)
            for i in range(enemy_number):
                chosen_enemy = random.choice(general_enemies_list)
                general_enemies_list.remove(chosen_enemy)
                print chosen_enemy
                sql = 'update stage_enemies set '+chosen_enemy+'=1 where stage = "'+stage+'"'
                cursor.execute(sql)

        level.universe.db.commit()
#        save.save_file(self.level)
        thumbnail = pygame.transform.flip(pygame.transform.smoothscale(self.level.princesses[0].stay_img.left[0],(100,100)),1,0)
        pygame.image.save(thumbnail,data_dir+'/saves/'+self.level.princesses[0].name+'/thumbnail.PNG')
        self.texts += [
                #Translators: consider the whole sentence: You've got X glamour points
                widget.GameText(_("You've"),  (1064,81),  self,font_size = 40),
                widget.GameText(_("got"),     (1100,128), self,font_size = 40),
                widget.GameText(_("glamour"), (1309,151), self,font_size = 40),
                widget.GameText(_("points"),  (1309,185), self,font_size = 40),
                widget.GameText(str(int(glamour_points)), (1200,120),self,font_size=80)
        ]
        total_points = int(glamour_points+accumulated_points)
        if total_points >= 30:
            self.boyfriend = BoyFriend(total_points)
        level.panel[1]  = widget.GameText(str(total_points), (1000,30), self,font_size = 80, color=(58,56,0))

    def return_to_game(self):
        self.level.BathhouseSt(goalpos = round(5220*scale), clean_princess = True)
        self.level.clock[1].count = 0
        self.level.clock[1].time = "morning"


class VerticalBar():
    def __init__(self, ball, right_or_left = 'left'):
        self.image = obj_images.scale_image(pygame.image.load(data_dir+'/images/interface/ball/golden-bar.png').convert_alpha())
        if right_or_left == 'right':
            self.image = pygame.transform.flip(self.image, 1,0)
        self.size = self.image.get_size()
        self.position = [-self.size[0],0]
        self.speed = 5
        self.ready = False

    def update_all(self):
        if self.position[0] < round(90*scale):
            self.position[0] += self.speed
            self.speed += 5
        else:
            self.position[0] = round(90*scale)
            self.ready = True


class BallFrame():
    def __init__(self, ball):
        self.image = pygame.Surface(p((677,673)),pygame.SRCALPHA).convert_alpha()
        background = obj_images.image(data_dir+'/images/interface/ball/back-frame.png')
        self.size = self.image.get_size()
        self.position = [round(30*scale), -self.size[1]]
        self.speed = 5
        self.ball = ball
        princesses = [FairyTalePrincess(self, i[0], i[1], i[2], i[3], iconpos= i[5], name = i[4]) for i in (
                [(130,150), 'hair_snowwhite', 'pink', 'princess-icon-apple.png', 'Snow_White',   220],
                [(240,150), 'hair_cinderella','tan',  'princess-icon-shoe.png',    'Cinderella', 335],
                [(350,150), 'hair_rapunzel',  'pink', 'princess-icon-brush.png', 'Rapunzel'  ,   440],
                [(460,150), 'hair_sleeping',  'pink', 'princess-icon-spindle.png','Sleeping_Beauty', 560])]
        past_princesses= [FairyTalePrincess(self,i[0],i[1],i[2], name=i[3],ball=1) for i in (
                [(130,400), 'hair_snowwhite', 'pink', 'Snow_White'],
                [(240,400), 'hair_cinderella','tan',  'Cinderella'],
                [(350,400), 'hair_rapunzel',  'pink', 'Rapunzel'],
                [(460,400), 'hair_sleeping',  'pink', 'Sleeping_Beauty']) ]
        frametexts = [
                widget.GameText(_("Tonight's ball"),      (0,0), self, rotate = 90),
                widget.GameText(_("Yesterday's ball"),    (0,0), self, rotate = 90)
                    ]
        for i in past_princesses:
            self.image.blit(i.image,i.pos)
        self.image.blit(background,(0,0))
        self.image.blit(frametexts[0].image, p((0, 130)))
        self.image.blit(frametexts[1].image, p((0, 360)))
        for i in princesses:
            self.image.blit(i.image,i.pos)
            if i.symbol:
                self.image.blit(i.symbol,(i.symbolpos,round(i.pos[1]-round(100*scale) )))
        self.set_next_ball_clothes()

    def update_all(self):
        if self.ball:
            if self.position[1] + (self.size[1]/2) < (self.ball.universe.height/2):
                self.speed +=2
            else:
                self.speed = 0
            self.position[1] += self.speed

    def set_next_ball_clothes(self):
        cursor = self.ball.universe.db_cursor
        faces   = ("face_eyelids", "face_eyeshades","face_lipstick","face_simple")
        dresses = ("dress_pink","dress_plain", "dress_red", "dress_yellow")
        arm_dresses = (0,0,1,1)
        accessories = ("accessory_crown","accessory_purse","accessory_ribbon","accessory_shades")
        shoes   = ("shoes_crystal","shoes_red","shoes_slipper","shoes_white")
        for p in ("rapunzel","cinderella","sleeping_beauty","snow_white"):
            dress_no = random.randint(0,len(dresses)-1)
            row = cursor.execute("SELECT * FROM "+p+" WHERE id = (SELECT MAX(id) FROM "+p+")").fetchone()
            cursor.execute("INSERT INTO "+p+" VALUES ("+str(row['id']+1)+" , "+str(row["hair_back"])+" , '"+row["skin"]+"', '"+random.choice(faces)+"' , '"+row['hair']+"' , '"+random.choice(shoes)+"' , '"+dresses[dress_no]+"', '"+row['arm']+"', "+str(arm_dresses[dress_no])+", '"+random.choice(accessories)+"')")
        row = cursor.execute("SELECT * FROM princess_garment WHERE id = (SELECT MAX(id) FROM princess_garment)").fetchone()
        cursor.execute("INSERT INTO princess_garment VALUES ("+str(row['id']+1)+" , '"+str(row["hair_back"])+"' , '"+row["skin"]+"', '"+row['face']+"' , '"+row['hair']+"' , '"+row['shoes']+"' , '"+row['dress']+"', '"+row['arm']+"', '"+str(row['armdress'])+"', '"+row['accessory']+"')")
        self.ball.universe.db.commit()


class FairyTalePrincess():
    def __init__(self, frame, position, hair, skin, icon=None, iconpos=None, name = "princess_garment", ball = 0):
        """Creates Thumbnail of Princesses to remember past balls

           The parameters are self, frame (or level), position, hair, skin, icon, name (name of the princess in the database, if no name, than player), ball (number of the ball to show - counted backwards).
           """
        skin_body       = 'skin_'+skin
        skin_arm        = 'arm_'+skin
        princess_directory  = data_dir+'/images/princess/'
        ball_directory      = data_dir+'/images/interface/ball/'
        self.frame      = frame
        self.file       = frame.ball.universe.file
        self.image      = obj_images.scale_image(pygame.Surface((200,200),pygame.SRCALPHA).convert_alpha())
        name_lower = name.lower()
        self.position   = p(position)
        self.symbol = None
        if name != "princess_garment":
            if icon:
                self.symbol     =  obj_images.image(ball_directory+icon)
                self.symbolpos  = int(round(iconpos*scale  - (float(self.symbol.get_width())/2)))
        sql                 = "SELECT * FROM "+name_lower+" WHERE id = (SELECT MAX(id)-"+str(ball)+" FROM "+name_lower+")"
        self.pos            = [self.position[0],self.position[1]]
        cursor = self.frame.ball.universe.db_cursor
        row    = cursor.execute(sql).fetchone()
        if row:
            if row['hair_back'] > 0:
                self.image.blit(obj_images.image(princess_directory+row['hair']+"_back/stay/0.png"),(0,0))
            [self.image.blit(obj_images.image(princess_directory+row[i]+'/stay/0.png'),(0,0)) for i in ('skin', 'hair', 'face', 'dress', 'accessory', 'arm', 'shoes')]
            self.image = pygame.transform.flip(self.image,1,0)

    def update_all(self):
        self.pos        = [self.frame.position[0]+self.position[0],
                           self.frame.position[1]+self.position[1]]


class StarBall():
    def __init__(self):
        self.images = obj_images.OneSided(data_dir+'/images/interface/ball/star-score/')
        self.image = self.images.list[0]
        self.pos = p([1100,34])

    def update_all(self):
        self.image = self.images.list[self.images.itnumber.next()]


class BoyFriend():
    def __init__(self, points):
        print "Oh my! You are so beautiful that most certainly someone will fall for you tonight!"
        boyfriend = None
        if points >= 30:
            boyfriend = "gentleman_decent"
            self.name = _('Gentleman Decent')
        if points >= 65:
            boyfriend = "knight_reliable"
            self.name = _('Knight Reliable')
        if points >= 105:
            boyfriend = "baron_serious"
            self.name = _('Baron Serious')
        if points >= 175:
            boyfriend = "count_loving"
            self.name = _('Count Loving')
        if points >= 255:
            boyfriend = "marquess_attractive"
            self.name = _('Marquess Attractive')
        if points >= 345:
            boyfriend = "duke_intelligent"
            self.name = _('Duke Intelligent')
        if points >= 465:
            boyfriend = "prince_charming"
            self.name = _('Prince Charming')
        if points >= 685:
            boyfriend = "king_kindhearted"
            self.name = _('King Kindhearted')
        if points >= 1000:
            boyfriend = "emperor_awesome"
            self.name = _('Emperor Awesome')
        print "The heart of "+boyfriend+" is yours!"
        self.image= obj_images.image(data_dir+'/images/interface/ball/boyfriends/'+boyfriend+'/0.png')
#        self.name = boyfriend.replace("_"," ").title()
        self.pos = p([1000,298])

    def update_all(self):
        pass


class BigPrincess():
    def __init__(self, ball):
        princess_directory  = data_dir+'/images/princess/'
        ball_directory      = data_dir+'/images/interface/ball/'
        big_image      = pygame.Surface((400,400),pygame.SRCALPHA).convert_alpha()
        self.pos        = p([ 670,398])
        cursor = ball.universe.db_cursor
        sql = "SELECT * FROM princess_garment WHERE id=(SELECT MAX(id) FROM princess_garment)"
        row = cursor.execute(sql).fetchone()
        for part in ["hair_back","skin","face","hair","shoes","dress","arm","armdress","accessory"]:
            if row[part] and row[part]!="None":
                img = pygame.image.load(princess_directory+row[part]+"/big.png").convert_alpha()
                big_image.blit(img, (0,0))
        dirt     = int(cursor.execute("SELECT * FROM save").fetchone()['dirt'])
        if dirt >0:
            big_image.blit(pygame.image.load(princess_directory+"dirt"+str(dirt)+"/big.png").convert_alpha(),(0,0))
        self.image = obj_images.scale_image(big_image,invert=True)

    def update_all(self):
        pass



class Dancer():
    def __init__(self, position):
        self.images = obj_images.There_and_back_again(data_dir+'/images/interface/ball/dancers/', exclude_border = True)
        self.image  = self.images.list[self.images.itnumber.next()]
        self.position = position
        self.images.number = random.randint(0,20)
        if random.randint(0,9) < 4:
            self.list = self.images.left
        else:
            self.list = self.images.right

    def update_all(self):
        self.image  = self.images.list[self.images.number]
        self.images.update_number()

