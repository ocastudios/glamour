import pygame
import obj_images
import random
import gametext
from settings import *


def p(positions):
    return [int(i*scale) for i in positions ]

class Ball():
    directory = 'data/images/interface/ball/'
    def __init__(self, level, universe, princess):
        self.position = 0,0
        self.universe   = universe
        self.boyfriend  = None
        universe.db.commit()
        self.texts      = []
        self.texts+= [StarBall()]
        self.compute_glamour_points(level)
        self.background      = pygame.Surface((level.universe.width,level.universe.height),pygame.SRCALPHA).convert_alpha()
        for file in (self.directory+'ball-back.png',self.directory+'back-bubbles.png'):
            self.background.blit(obj_images.scale_image(pygame.image.load(file).convert_alpha()), (0,0))
        self.left_bar   = VerticalBar(self)
        self.princess   = princess
        self.Bar        = VerticalBar(self)
        self.Frame      = BallFrame(self)
        self.level      = level
        self.dancers    = [Dancer(p(i)) for i in [1200,100],[200,200],[800,300],[600,400],[300,600]]
        self.buttons = [BallButton('data/images/interface/title_screen/button_ok/',(300*scale,200*scale), self.level)]
        pygame.mixer.music.load("data/sounds/music/strauss_waltz_wedley.ogg")
        pygame.mixer.music.play()
        general_enemies_list = ['Schnauzer', 'Bird', 'OldLady', 'FootBoy','Butterfly']
        stage_list           = ['BathhouseSt', 'DressSt', 'AccessorySt', 'MakeupSt','ShoesSt']
        for stage in stage_list:
            chosen_enemy = random.choice(general_enemies_list)
            self.level.enemies_list[stage] = [chosen_enemy]
            general_enemies_list.remove(chosen_enemy)
        self.level.enemies_list[random.choice(['DressSt', 'MakeupSt','ShoesSt'])].append('Carriage')
        princesses_list      = ['Cinderella', 'Snow_White', 'Sleeping_Beauty','Rapunzel']
        garment_list         = ['Accessory', 'Dress', 'Shoes','Makeup']
        Accessory_list       = ['crown', 'purse','ribbon','shades']
        Dress_list           = ['pink','plain','red','yellow']
        Shoes_list           = ['crystal','red','slipper','white']
        Makeup_list          = ['eyelids','eyeshades','lipstick','simple']
        self.counter         = 0

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
        for i in self.Frame.texts:
            self.universe.screen_surface.blit(i.image,i.pos)
            i.update_all()
        for i in self.Frame.princesses:
            self.universe.screen_surface.blit(i.image,i.pos)
            self.universe.screen_surface.blit(i.symbol,(i.symbolpos,i.pos[1]-100*scale))
            i.update_all()
        for i in self.buttons:
            self.universe.screen_surface.blit(i.image,i.pos)
            i.update_all()
        if self.counter > 90:
            for i in self.texts:
                self.universe.screen_surface.blit(i.image,i.pos)
                i.update_all()
        if self.counter == 100:
            self.texts+= [gametext.Horizontal("and won the heart of", p((1090,237)), self,font_size = 40)]        if self.counter == 110:
            self.texts+= [gametext.Horizontal(".", p((1300,237)), self,font_size = 40)]        if self.counter == 120:
            self.texts+= [gametext.Horizontal(" .", p((1300,237)), self,font_size = 40)]        if self.counter == 130:
            self.texts+= [gametext.Horizontal("  .", p((1300,237)), self,font_size = 40)]
        if self.counter > 150:
            if self.boyfriend:
                self.universe.screen_surface.blit(self.boyfriend.image,self.boyfriend.pos)
                self.boyfriend.update_all()
        if self.counter == 160:
            if self.boyfriend:
                self.texts += [gametext.Horizontal(self.boyfriend.name,p([1156,280]),self, font_size = 60,color=(58,56,0))]
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
        last_ball_garments = others_garments["last_ball"]+princess_garments["last_ball"]
        past_repetitions = sum([last_ball_garments.count(i) for i in princess_garments["this_ball"]])
        garments_history = princess_rows[:-1]+fairy_tale_rows
        number_of_balls    = len(princess_rows)
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
        new_glamour_points = past_glamour_points+glamour_points
        cursor.execute("UPDATE save SET points = "+str(new_glamour_points))
        level.universe.db.commit()
        self.texts += [
                gametext.Horizontal("You've", p((1064,81)), self,font_size = 40),
                gametext.Horizontal("got", p((1100,128)), self,font_size = 40),
                gametext.Horizontal("glamour", p((1309,151)), self,font_size = 40),
                gametext.Horizontal("points", p((1309,185)), self,font_size = 40),
                gametext.Horizontal(str(int(glamour_points)), p((1200,120)),self,font_size=80)
        ]
        total_points = int(glamour_points+accumulated_points)
        if glamour_points >= 30:
            self.boyfriend = BoyFriend(total_points)
        print level.panel
        level.panel[1]  = gametext.Horizontal(str(total_points), p((1000,30)), self,font_size = 80, color=(58,56,0))
        print "segunda vez" + str(level.panel)


class VerticalBar():
    def __init__(self, ball, right_or_left = 'left'):
        self.image = obj_images.scale_image(pygame.image.load('data/images/interface/ball/golden-bar.png').convert_alpha())
        if right_or_left == 'right':
            self.image = pygame.transform.flip(self.image, 1,0)
        self.size = self.image.get_size()
        self.position = [-self.size[0],0]
        self.speed = 5
        self.ready = False

    def update_all(self):
        if self.position[0] < 90*scale:
            self.position[0] += self.speed
            self.speed += 5
        else:
            self.position[0] = 90*scale
            self.ready = True


class BallFrame():
    def __init__(self, ball):
        self.image = obj_images.scale_image(pygame.image.load('data/images/interface/ball/back-frame.png').convert_alpha())
        self.size = self.image.get_size()
        self.position = [30*scale, -self.size[1]]
        self.speed = 5
        self.ball = ball
        self.princesses = [
                FairyTalePrincess(self, 100*scale, 'hair_snowwhite', 'pink', 'princess-icon-apple.png',  name = 'Snow_White'),
                FairyTalePrincess(self, 200*scale, 'hair_cinderella','tan','princess-icon-shoe.png',     name = 'Cinderella'),
                FairyTalePrincess(self, 300*scale, 'hair_rapunzel',  'pink', 'princess-icon-brush.png',  name = 'Rapunzel'),
                FairyTalePrincess(self, 400*scale, 'hair_sleeping',  'pink','princess-icon-spindle.png', name = 'Sleeping_Beauty')
                        ]
        self.texts = [
                gametext.Vertical("Yesterday's ball", p((100,200)), self),
                gametext.Vertical("Tonight's ball", p((100,500)), self),
                    ]
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
        self.ball.universe.db.commit()


class FairyTalePrincess():
    def __init__(self, frame, position_x, hair, skin, icon, name = None):
        skin_body       = 'skin_'+skin
        skin_arm        = 'arm_'+skin
        princess_directory  = 'data/images/princess/'
        ball_directory      = 'data/images/interface/ball/'
        self.frame      = frame
        self.file       = frame.ball.universe.file
        self.image      = obj_images.scale_image(pygame.Surface((200,200),pygame.SRCALPHA).convert_alpha())
        self.position   = [position_x, 200*scale]
        self.symbol     =  obj_images.image(ball_directory+icon)
        self.symbolpos  = position_x + (self.image.get_width()/2) - (self.symbol.get_width()/2)
        self.pos        = [ self.frame.position[0]+self.position[0],
                            self.frame.position[1]+self.position[1]]
        name_lower = name.lower()
        cursor = self.frame.ball.universe.db_cursor
        row     = cursor.execute("SELECT * FROM "+name_lower+" WHERE id = (SELECT MAX(id) FROM "+name_lower+")").fetchone()
        if row['hair_back'] > 0:
            self.image.blit(obj_images.image(princess_directory+row['hair']+"_back/stay/0.png"),(0,0))
        self.image.blit(obj_images.image(princess_directory+row['skin']+'/stay/0.png'),     (0,0))
        self.image.blit(obj_images.image(princess_directory+row['hair']+'/stay/0.png'),     (0,0))
        self.image.blit(obj_images.image(princess_directory+row['face']+'/stay/0.png'),     (0,0))
        self.image.blit(obj_images.image(princess_directory+row['dress']+'/stay/0.png'),    (0,0))
        self.image.blit(obj_images.image(princess_directory+row['accessory']+'/stay/0.png'),(0,0))
        self.image.blit(obj_images.image(princess_directory+row['arm']+'/stay/0.png'),      (0,0))
        self.image.blit(obj_images.image(princess_directory+row['shoes']+'/stay/0.png'),    (0,0))
        self.image = pygame.transform.flip(self.image,1,0)

    def update_all(self):
        self.pos        = [self.frame.position[0]+self.position[0],
                           self.frame.position[1]+self.position[1]]


class StarBall():
    def __init__(self):
        self.images = obj_images.OneSided('data/images/interface/ball/star-score/')
        self.image = self.images.list[0]
        self.pos = p([1100,34])

    def update_all(self):
        self.image = self.images.list[self.images.itnumber.next()]


class BoyFriend():
    def __init__(self, points):
        boyfriend = None
        if points >= 30:
            boyfriend = "gentleman_decent"
        if points >= 65:
            boyfriend = "knight_reliable"
        if points >= 105:
            boyfriend = "baron_serious"
        if points >= 175:
            boyfriend = "count_loving"
        if points >= 255:
            boyfriend = "marquess_attractive"
        if points >= 345:
            boyfriend = "duke_intelligent"
        if points >= 465:
            boyfriend = "prince_charming"
        if points >= 685:
            boyfriend = "king_kindhearted"
        if points >= 1000:
            boyfriend = "emperor_awesome"
        self.image= obj_images.image('data/images/interface/ball/boyfriends/'+boyfriend+'/0.png')
        self.name = boyfriend.replace("_"," ").title()
        self.pos = p([1156,298])

    def update_all(self):
        pass


class Dancer():
    def __init__(self, position):
        self.images = obj_images.There_and_back_again('data/images/interface/ball/dancers/', exclude_border = True)
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


class BallButton():
    def __init__(self,directory,position,level):
        self.level      = level
        self.images     = obj_images.Buttons(directory,5)
        self.image      = self.images.list[self.images.number]
        self.size       = self.image.get_size()
        self.position   = position
        self.pos        = [(self.position[0]-(self.image.get_size()[0]/2)),
                           (self.position[1]-(self.image.get_size()[1])/2)]
        self.rect       = pygame.Rect(self.pos,self.size)

    def update_all(self):
        self.update_pos()
        self.click_detection()

    def update_pos(self):
        self.pos        = [(self.position[0]-(self.image.get_size()[0]/2)),
                           (self.position[1]-(self.image.get_size()[1])/2)]
        self.rect = pygame.Rect(self.pos,self.size)

    def invert_images(self,list):
        inv_list=[]
        for img in list:
            inv = pygame.transform.flip(img,1,0)
            inv_list.append(inv)
        return inv_list

    def click_detection(self):
        self.rect = pygame.Rect(self.pos,self.size)
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image = self.images.list[self.images.itnumber.next()]
            if self.level.universe.click:
                self.level.BathhouseSt(goalpos = 5520*scale)
                self.level.clock[1].count = 0
                self.level.clock[1].time = "morning"
        else:
            if self.image != self.images.list[0]:
                self.image = self.images.list[self.images.itnumber.next()]
