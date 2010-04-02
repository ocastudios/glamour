import scenarios
import obj_images
import enemy
import skies
import fairy
import floors
import clouds
import random
import moving_scenario
import glamour_stars
import princess
import os
import panel
import pygame
#import itertools
import camera
import mousepointer
import inside
import ball
import sqlite3
import events
from settings import *
#TODO Insert every rect that is moving in stage class self.all and use main display.update to update only the different rects.
#TODO substitute all these lists by a single list, blitting on the screen using the class to estipulate the order.

def p(positions):
    return [int(i*scale) for i in positions ]
###Gate Positions###
bathhousegate = p([480, 8138])
dressgate =     p([800, 4142,8471])
accessorygate = p([1497,4174,7836])
makeupgate =    p([1200,4661,8231])
shoegate =      p([1198,4690,8140])


class Stage():
    enemy_dir = 'data/images/enemies/'
    maindir        = 'data/images/scenario/'
    princesses = None
    def __init__(self,universe):
        self.name = None
        self.size = int(9600*scale)
        self.universe       = universe
        self.cameras=[camera.GameCamera(self,-4220*scale)]
        self.gates          = []
        self.clock          = []
        self.floor_heights  = {}
        self.floor          = universe.floor-186*scale
        self.menus          = []
        self.panel          = []
        self.pointer        = []
        self.scenarios_front= []
        self.animated_scenarios =[]
        self.blitlist       = ('sky', 'background', 'moving_scenario', 'scenarios', 'animated_scenarios' ,'gates',  'lights', 'princesses','enemies', 'menus')
        self.foreground     = []
        self.white          = Foreground(self.universe)
        self.down_bar       = Bar(self,'down')
        self.up_bar         = Bar(self,'up')
        self.bar_height     = self.up_bar.tile_size[1]
        self.down_bar_y     = self.universe.height
        self.up_bar_y       = - self.bar_height
        self.bar_goal       = self.universe.height/3
        self.bar_speed      = 1
        self.game_mouse     = mousepointer.MousePointer(pygame.mouse.get_pos(),self, type = 2)
        self.pointer        = [glamour_stars.Glamour_Stars(self),self.game_mouse]
        self.inside         = self.dress_castle()
        self.princess_castle= None
        self.fairy          = True
        self.omni_directory = 'data/images/scenario/omni/'
        self.ball           = None
        self.endmusic       = pygame.event.Event(pygame.USEREVENT,{'music':'finished'})
        self.enemies_list   = {                            'BathhouseSt': ['Bird', 'Butterfly'] ,                            'DressSt':['Bird'],                            'AccessorySt':['Schnauzer'],                            'MakeupSt':['OldLady'],                             'ShoesSt': ['FootBoy']
                            }
        self.ballroom = { 'day': scenarios.Background(110,self,self.maindir+'ballroom/ballroom_day/'),
                          'night': scenarios.Background(110,self,self.maindir+'ballroom/ballroom_night/')}
        self.event_counter = 0
        self.starting_game = True

    def dress_castle(self):
        return inside.Inside(self,'dress',('pink','plain','red','yellow'))

    def accessory_castle(self):
        return inside.Inside(self,'accessory',('crown','purse','ribbon','shades'))

    def makeup_castle(self):
        return inside.Inside(self,'face',('eyelids','eyeshades','lipstick','simple'))

    def hair_castle(self):
        return inside.Inside(self,'hair',('black','brown','cinderella','rapunzel','rastafari', 'red', 'short', 'sleeping', 'snowwhite', 'yellow'))

    def shoes_castle(self):
        return inside.Inside(self,'shoes',('crystal','red','slipper','white'))

    def bathhouse_castle(self):
        return inside.Inside(self,'shower', [])

    def what_is_my_height(self,object):
        try:        y_height = self.floor_heights[int(object.center_distance+(object.size[0]/2))]
        except:     y_height = self.floor
        return      y_height

    def update_all(self):
        self.game_mouse.update()
        events.choose_event(self)
        act = self.act = self.universe.action
        dir = self.direction = self.universe.dir
        if self.universe.clock_pointer.count > 160:
            if self.background[0] == self.ballroom['day']:
                self.background = [self.ballroom['night']]
        else:
            if self.background[0] == self.ballroom['night']:
                self.background = [self.ballroom['day']]
        if self.universe.clock_pointer.time == 'ball':
            self.ball = self.ball or ball.Ball(self, self.universe, self.princesses[0])
            self.ball.update_all    ()
            for i in self.pointer:
                self.universe.screen_surface.blit(i.image,i.pos)
                i.update_all()
        else:
            if self.ball:
                self.ball = None
            self.cameras[0].update_all()
            self.universe.movement(self.direction)
            for att in self.blitlist:
                if att == 'lights':
                    if self.universe.clock_pointer.time == 'night':
                        for i in self.lights:
                            if i['status'] == 'on':
                                self.universe.screen_surface.blit(i['images'].list[i['images'].itnumber.next()],i['position'].pos)
                                i['position'].update_pos()
                            if i['status'] == 'off' and random.randint(0,10) == 0:
                                i['status'] = 'on'
                                i['position'].update_pos()
                else:
                    exec('[self.universe.screen_surface.blit(i.image,i.pos) for i in self.'+att+' if i and i.image ]')
                    exec('[i.update_all() for i in self.'+att+' if i]')
            for effect in self.princesses[0].effects:
                self.universe.screen_surface.blit(effect[0],effect[1])
            for i in self.scenarios_front:
                self.universe.screen_surface.blit(i.image,i.pos)
                i.update_all()
            [self.universe.screen_surface.blit(i.arrow_image,i.arrow_pos)
                            for i in self.gates if self.princesses[0].rect.colliderect(i.rect) and i.arrow_image]
            for i in self.floor_image:
                self.universe.screen_surface.blit(i.image,i.pos)
                i.update_all()
            for i in self.foreground:
                self.universe.screen_surface.blit(i.image,i.pos)
                i.update_all()
            if self.princesses[0].inside:
                self.update_insidebar()
            elif self.sky[0].night_image:
                self.universe.screen_surface.blit(self.sky[0].night_image,(0,0))
            for i in self.clock:
                self.universe.screen_surface.blit(i.image,i.pos)
            for i in self.panel:
                self.universe.screen_surface.blit(i.label,i.pos)
                i.update((self.princesses[0].center_distance,self.princesses[0].pos[1]))
            for i in self.pointer:
                self.universe.screen_surface.blit(i.image,i.pos)
                i.update_all()
            if self.fairy:
                for i in self.fae:
                    self.universe.screen_surface.blit(i.image,i.pos)
                    i.update_all()

    def update_insidebar(self):
        self.universe.screen_surface.blit(self.white.image,(0,0))
        if self.inside.status[:4] == 'bath': #Bath Castle
            if self.inside.status == 'bath':
                self.white.alpha_value = 0
                self.inside.status = 'bath_loading'
            elif self.inside.status == 'bath_loading':
                self.white.image.set_alpha(self.white.alpha_value)
                if self.white.alpha_value < 200:
                    self.white.alpha_value += 10
                if self.white.alpha_value >= 200:
                    self.inside.status = 'bath_choosing'
            elif self.inside.status == 'bath_choosing':
                self.princesses[0].dirt = 0
                self.universe.db_cursor.execute("UPDATE save SET dirt = "+str(self.princesses[0].dirt)+" WHERE name = '"+self.princesses[0].name+"'")
                print "You look lovely all cleaned up!"
                self.princesses[1] = None
                self.inside.status = 'bath_done'
            elif self.inside.status == 'bath_done':
                if self.white.alpha_value > 0:
                    self.white.alpha_value -= 10
                    self.white.image.set_alpha(self.white.alpha_value)
                else:
                    self.white.alpha_value = 0
                    self.inside.status = 'bath_openning'
                self.white.image.set_alpha(self.white.alpha_value)
            elif self.inside.status == 'bath_openning':
                for i in self.gates:
                    if i.rect.colliderect(self.princesses[0].rect):
                        i.open = True
                        if i.images.number >= i.images.lenght -1:
                            self.inside.status = 'bath_closing'
            elif self.inside.status == 'bath_closing':
                for i in self.gates:
                    if i.rect.colliderect(self.princesses[0].rect):
                        i.outside()
                self.princesses[0].inside = False
        else: #Choosing Clothes Castles
            self.universe.screen_surface.blit(self.down_bar.image,(0,self.down_bar_y))
            self.universe.screen_surface.blit(self.up_bar.image,(0,self.up_bar_y))
            if self.inside.status == 'inside':
                self.up_bar_y = -self.bar_height
                self.down_bar_y = self.universe.height
                self.white.alpha_value = 0
                self.inside.status = 'loading'
            elif self.inside.status == 'loading':
                self.white.image.set_alpha(self.white.alpha_value)
                if self.white.alpha_value < 200:
                    self.white.alpha_value += 10
                if self.down_bar_y > 2*self.bar_goal:
                    self.down_bar_y -= self.bar_speed
                if self.up_bar_y + self.bar_height< self.bar_goal:
                    self.up_bar_y += self.bar_speed
                if self.bar_speed < 20:
                    self.bar_speed += self.bar_speed
                if self.white.alpha_value > 150:
                    self.inside.status = 'choosing'
            elif self.inside.status == 'choosing':
                self.universe.screen_surface.blit(self.princesses[0].image,
                                        ((self.universe.width/2)-(self.princesses[0].image_size[0]/2),
                                        (self.universe.height/2)-(self.princesses[0].image_size[1]/2)))
                [self.universe.screen_surface.blit(i.image,i.pos) for i in self.inside.buttons]
                [i.update_all() for i in self.inside.buttons]
                [self.universe.screen_surface.blit(i.image,i.pos) for i in self.inside.items if i.queue]
                [i.update_all() for i in self.inside.items]
            elif self.inside.status == 'done':
                self.down_bar_y += self.bar_speed
                self.up_bar_y -= self.bar_speed
                if self.bar_speed < 20:
                    self.bar_speed += self.bar_speed
                if self.white.alpha_value > 0:
                    self.white.alpha_value -= 10
                    self.white.image.set_alpha(self.white.alpha_value)
                else:
                    self.white.image.alpha_value = 0
                self.white.image.set_alpha(self.white.alpha_value)
                if self.down_bar_y > self.universe.height and self.up_bar_y < -self.bar_height and self.white.alpha_value == 0:
                    self.inside.status = 'openning'
            elif self.inside.status == 'openning':
    #            self.level.blitlist = ('sky','background','moving_scenario','scenarios','gates','enemies','menus','princesses')
                for i in self.gates:
                    if i.rect.colliderect(self.princesses[0].rect):
                        i.open = True
                        if i.images.number >= i.images.lenght -1:
                            self.inside.status = 'closing'
            elif self.inside.status == 'closing':
                for i in self.gates:
                    if i.rect.colliderect(self.princesses[0].rect):
                        i.outside()
                self.princesses[0].inside = False
        try:
            x = self.universe.width/2 + self.princesses[0].image_size[0]
            y = (self.universe.height/2)-(self.princesses[0].image_size[1]/2)
            self.universe.screen_surface.blit(self.inside.princess_image, (x,y))
        except:
            pass

    def select_enemies(self, allowed_enemies, street):
        self.enemies = []
        universe_cursor = self.universe.db_cursor
        row     = universe_cursor.execute("SELECT * FROM stage_enemies WHERE stage = '"+street+"'").fetchone()
        for e in allowed_enemies:
            if int(row[e]):
                name = e.replace('_',' ').title()
                name = name.replace(' ','')
                exec('self.enemies.append(enemy.'+name+'(scale*(random.randint(0,9000)),self))')

    def create_scenario(self,street):
        db = sqlite3.connect('data/'+street+'.db')
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        self.scenario_row = cursor.execute("SELECT * FROM scenario ORDER BY id ASC").fetchall()
        self.scenarios_prep  = []
        for i in self.scenario_row:
            if i['invert'] == 1:
                if i['height'] != 0:
                    img = scenarios.Scenario(scale*i['xpos'],i['directory'],self, invert=True, height= int(i['height']*scale))
                else:
                    img = scenarios.Scenario(scale*i['xpos'],i['directory'],self, invert=True)
            else:
                if i['height'] != 0:
                    img = scenarios.Scenario(scale*i['xpos'],i['directory'],self, height= int(i['height']*scale))
                else:
                    img = scenarios.Scenario(scale*i['xpos'],i['directory'],self)
            self.scenarios_prep.append(img)
        self.scenarios = BigScenario(self),
        for i in self.scenarios_prep:
            self.scenarios[0].image.blit(i.image,i.pos)
        cursor.close()
        self.sky             = [skies.Sky(self.maindir+'skies/daytime/daytime.png',self,self.universe.clock_pointer)]
        self.clouds          =   [scenarios.Cloud(self) for cl in range(3)]
        [self.sky[0].image.blit(i.image,i.pos) for i in self.clouds]

    def create_front_scenario(self,street):
        db = sqlite3.connect('data/'+street+'.db')
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        front_row = cursor.execute("SELECT * FROM front_scenario ORDER BY id ASC").fetchall()
        self.scenarios_front = []
        for i in front_row:
            if i['type'] == 'scenario':
                if i['height'] == 0:
                    self.scenarios_front.append(scenarios.Scenario(scale*i['xpos'],i['directory'],self))
                else:
                    self.scenarios_front.append(scenarios.Scenario(scale*i['xpos'],i['directory'],self,height = i['height']*scale))
            elif i['type'] == 'flower':
                self.scenarios_front.append(scenarios.Flower(scale*i['xpos'],i['directory'],self,i['frames']))
            elif i['type'] == 'frontscenario':
                self.scenarios_front.append(scenarios.FrontScenario(scale*i['xpos'],i['directory'],self,i['ind']))
        cursor.close()

    def set_floor_heights(self,height,width,street):
        ### set_floor ###
        db = sqlite3.connect('data/'+street+'.db')
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        self.floor_heights = [height*scale]*int((width*scale))
        count   = 0
        for row in cursor.execute("SELECT * FROM floor ORDER BY id ASC").fetchall():
            for r in range(row['start']*scale,row['end']*scale):
                self.floor_heights[r]=row['value']*scale
        cursor.close()

    def BathhouseSt(self,goalpos = None):
        self.name = 'bathhouse'
        db = sqlite3.connect('data/bathhouse.db')
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        self.animated_scenarios = []
        if goalpos:
            self.princesses[0].center_distance = goalpos
            self.universe.center_x = -goalpos+(self.universe.width/2)
        self.gates = []
        self.directory = self.maindir+'bathhouse_st/'
        self.background = [self.ballroom['day']]
        self.create_scenario('bathhouse')
        self.gates =   [scenarios.BuildingDoor(p((1063,453)),self.directory+'bathhouse/door/',self,self.bathhouse_castle(),bath = True),
                        scenarios.BuildingDoor(p((5206,500)),self.directory+'home/door/',self, inside.Home(self)    ),
                        scenarios.BuildingDoor(p((9305,503)),self.directory+'magic_beauty_salon/door/',self,self.hair_castle()),
                        scenarios.Gate(bathhousegate[0], self.maindir+'omni/gate/',self,self.ShoesSt, goalpos = shoegate[2],),
                        scenarios.Gate(bathhousegate[1], self.maindir+'omni/gate/',self,self.AccessorySt,goalpos = accessorygate[0])]
        self.select_enemies(('schnauzer', 'butterfly', 'old_lady', 'footboy', 'bird','hawk'),'BathhouseSt')
        self.floor_image= [floors.Floor(c,self.directory+'floor/tile/',self) for c in range(24)]
        floors.Bridge(self.directory+'floor/japanese_bridge/',5,self)
        self.moving_scenario = [moving_scenario.Billboard(self)]
        self.create_front_scenario('bathhouse')
        self.music = "data/sounds/music/bathhouse_day.ogg"
        pygame.mixer.music.load("data/sounds/music/bathhouse_day_intro.ogg")
        pygame.mixer.music.queue(self.music)
        pygame.mixer.music.queue(self.music)
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

        ### set_floor ###
        self.set_floor_heights(186,9400,'bathhouse')
        self.animated_scenarios =[]
        self.lights = []
        for i in self.scenarios_prep:
            try:
                if i.lights:
                    self.lights.append(i.lights)
            except:
                pass
        self.princesses = self.princesses or [princess.Princess(self),None]
        panel.Data('', self.princesses[0].center_distance, p((300, 0)), self,0,size=120)
        if self.starting_game:
            events.choose_event(self,starting_game=True)
            self.starting_game = False

    def DressSt(self,goalpos = None):
        self.name = 'dress'
        self.animated_scenarios = []
        self.universe.center_x = -goalpos+(self.universe.width/2)
        self.princesses[0].center_distance = goalpos
        self.gates = []
        self.directory = self.maindir+'dress_st/'
        self.create_scenario('dress')

        self.animated_scenarios = [scenarios.Scenario(0,self.directory+'Dress_Tower/flag/',self,index=0)]

        self.select_enemies(('schnauzer', 'butterfly', 'old_lady', 'footboy', 'bird'),'DressSt')
        self.gates = [scenarios.BuildingDoor(p((155,318)),self.directory+'Dress_Tower/door/',self,self.dress_castle()),
                      scenarios.BuildingDoor(p((9092,430)),self.directory+'snow_white_castle/door/',self, inside.Princess_Home(self,Snow_White)),
                      scenarios.Gate(dressgate[0], 'data/images/scenario/omni/gate/',self,self.AccessorySt,goalpos = accessorygate[2]),
                      scenarios.Gate(dressgate[1], 'data/images/scenario/omni/gate/',self,self.ShoesSt,goalpos = shoegate[1]),
                      scenarios.Gate(dressgate[2], 'data/images/scenario/omni/gate/',self,self.MakeupSt,goalpos = makeupgate[0])]

        self.floor_image= [floors.Floor(c,self.directory+'floor/',self) for c in range(30)]
        self.create_front_scenario('dress')
        self.music = "data/sounds/music/dress_day_intro.ogg"
        pygame.mixer.music.load("data/sounds/music/dress_day_intro.ogg")
        pygame.mixer.music.queue(self.music)
        pygame.mixer.music.queue(self.music)
        pygame.mixer.music.play()
        self.princesses = self.princesses or [princess.Princess(self),None]
        self.lights = []
        for i in self.scenarios_prep:
            try:
                if i.lights:
                    self.lights.append(i.lights)
            except:
                pass
        self.set_floor_heights(185,9400,'dress')

    def AccessorySt(self,goalpos = None):
        self.name = "accessory"
        self.animated_scenarios             = []
        self.universe.center_x              = -goalpos+(self.universe.width/2)
        self.princesses[0].center_distance  = goalpos
        self.gates                          = []
        self.directory = self.maindir+'accessory_st/'
        self.create_scenario('accessory')

        self.select_enemies(('schnauzer', 'butterfly', 'old_lady', 'footboy', 'bird','hawk','viking_ship'),'AccessorySt')
        self.gates.extend([
            scenarios.BuildingDoor(p((330,428)),self.directory+'accessory_tower/door/',self,self.accessory_castle()),
            scenarios.BuildingDoor(p((8809,425)),self.directory+'castle/door/',self,inside.Princess_Home(self, Sleeping_Beauty)),
            scenarios.Gate(accessorygate[0], 'data/images/scenario/omni/gate/',self,self.BathhouseSt,goalpos = bathhousegate[1]),
            scenarios.Gate(accessorygate[1], 'data/images/scenario/omni/gate/',self,self.MakeupSt,goalpos = makeupgate[1]),
            scenarios.Gate(accessorygate[2], 'data/images/scenario/omni/gate/',self,self.DressSt , goalpos = dressgate[0])
                        ])

        self.floor_image= [floors.Floor(fl,self.directory+'floor/tile/',self) for fl in range(30)]
        self.floor_image.extend([floors.Water(wat,self.directory+'water/tile/',self) for wat in range(11)])
        self.floor_image.extend([enemy.VikingShip(9000*scale,self)])
        self.floor_image.extend([floors.Water2(wat,self.directory+'water/tile/',self) for wat in range(11)])

        floors.Drain(self.directory+'floor/left_bank_front/',2,self)
        floors.Drain(self.directory+'floor/right_bank_front/',3,self)
        floors.Drain(self.directory+'floor/left_bank_front/',20,self)
        floors.Drain(self.directory+'floor/right_bank_front/',21,self)

        self.create_front_scenario('accessory')
        self.music = "data/sounds/music/accessory_day.ogg"
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.queue(self.music)
        pygame.mixer.music.queue(self.music)
        pygame.mixer.music.play()

        self.princesses = self.princesses or [princess.Princess(self),None]
        self.set_floor_heights(194,9400,'accessory')
        self.lights = []

        self.enemies = []
        cursor = self.universe.db_cursor
        row     = cursor.execute("SELECT * FROM stage_enemies WHERE stage = 'BathhouseSt'").fetchone()
        allowed_enemies = ('schnauzer', 'butterfly', 'old_lady', 'footboy', 'bird','hawk')
        for e in allowed_enemies:
            if int(row[e]):
                name = e.replace('_',' ').title()
                name = name.replace(' ','')
                exec('self.enemies.append(enemy.'+name+'(scale*(random.randint(0,9000)),self))')

        for i in self.scenarios_prep:
            try:
                if i.lights:
                    self.lights.append(i.lights)
            except:
                pass

    def MakeupSt(self,goalpos = None):
        self.name = "makeup"
        self.animated_scenarios = []
        self.universe.center_x = -goalpos+(self.universe.width/2)
        self.princesses[0].center_distance = goalpos
        self.gates = []
        self.directory = self.maindir+'makeup_st/'
        self.create_scenario('makeup')
        self.enemies = []
        cursor = self.universe.db_cursor
        row     = cursor.execute("SELECT * FROM stage_enemies WHERE stage = 'BathhouseSt'").fetchone()
        allowed_enemies = ('schnauzer', 'butterfly', 'old_lady', 'footboy', 'bird','hawk')
        for e in allowed_enemies:
            if int(row[e]):
                name = e.replace('_',' ').title()
                name = name.replace(' ','')
                exec('self.enemies.append(enemy.'+name+'(scale*(random.randint(0,9000)),self))')

        self.gates.extend([ scenarios.Gate(makeupgate[x],'data/images/scenario/omni/gate/',self,y,goalpos = z)
                            for x,y,z in
                            ((0, self.DressSt, dressgate[2]),
                             (1, self.AccessorySt, accessorygate[1]),
                             (2, self.ShoesSt ,shoegate[0]))
                            ])
        self.gates.extend([scenarios.BuildingDoor(p((130,225)),self.directory+'make-up_castle/door/',self,self.makeup_castle()),
                     scenarios.BuildingDoor(p((8900,225)),self.directory+'sleeping_castle/door/',self,inside.Princess_Home(self,Sleeping_Beauty))])
        self.floor_image= [floors.Floor(fl,self.directory+'floor/',self) for fl in range(30)]
        self.scenarios_front = [scenarios.Scenario(0,self.directory+'make-up_castle/front/',self)]
        self.princesses = self.princesses or [princess.Princess(self),None]
        self.animated_scenarios = [ enemy.Lion(3200*scale,self),
                                    enemy.Monkey(3500*scale,self),
                                    scenarios.Scenario(2923*scale,self.directory+'zoo/base/',self)]
        self.animated_scenarios.insert(1,self.animated_scenarios[0].tail)

        self.lights = []
        for i in self.scenarios_prep:
            try:
                if i.lights:
                    self.lights.append(i.lights)
            except:
                pass
        self.set_floor_heights(192,9400,'makeup')
        self.music = "data/sounds/music/makeup_day.ogg"
        pygame.mixer.music.load("data/sounds/music/makeup_day_intro.ogg")
        pygame.mixer.music.queue(self.music)
        pygame.mixer.music.queue(self.music)
        pygame.mixer.music.play()

    def ShoesSt(self,goalpos=None):
        self.name = "shoes"
        self.animated_scenarios = []
        self.universe.center_x = -goalpos+(self.universe.width/2)
        self.princesses[0].center_distance = goalpos
        self.gates = []
        self.directory = self.maindir+'shoes_st/'
        self.create_scenario('shoes')
        self.animated_scenarios = [scenarios.Scenario(scale*7137,self.directory+'fountain/base/',self)]
        self.enemies = []
        cursor = self.universe.db_cursor
        row     = cursor.execute("SELECT * FROM stage_enemies WHERE stage = 'BathhouseSt'").fetchone()
        allowed_enemies = ('schnauzer', 'butterfly', 'old_lady', 'footboy', 'bird','hawk')
        for e in allowed_enemies:
            if int(row[e]):
                name = e.replace('_',' ').title()
                name = name.replace(' ','')
                exec('self.enemies.append(enemy.'+name+'(scale*(random.randint(0,9000)),self))')
        self.gates = [scenarios.BuildingDoor(p((50,503)),self.directory+'shoes_tower/door/',self,self.shoes_castle()),
        scenarios.BuildingDoor(p((8500,503)),self.directory+'rapunzel_castle/door/',self,inside.Princess_Home(self, Rapunzel)),
        scenarios.Gate(shoegate[0],'data/images/scenario/omni/gate/',self,self.MakeupSt, goalpos = makeupgate[0]),
        scenarios.Gate(shoegate[1],'data/images/scenario/omni/gate/',self,self.DressSt,  goalpos = dressgate[1]),
        scenarios.Gate(shoegate[2],'data/images/scenario/omni/gate/',self,self.BathhouseSt, goalpos = bathhousegate[0]),]
        self.floor_image= [floors.Floor(c,self.directory+'floor/',self) for c in range(30)]
        self.create_front_scenario('shoes')
        self.music = "data/sounds/music/shoes_day.ogg"
        pygame.mixer.music.load("data/sounds/music/shoes_day_intro.ogg")
        pygame.mixer.music.queue(self.music)
        pygame.mixer.music.queue(self.music)
        pygame.mixer.music.play()
        self.princesses = self.princesses or [princess.Princess(self),None]
        self.set_floor_heights(192,9400,'shoes')
        self.lights = []
        for i in self.scenarios_prep:
            try:
                if i.lights:
                    self.lights.append(i.lights)
            except:
                pass


class Foreground():
    def __init__(self,universe):
        self.pos = 0,0
        self.image = pygame.Surface((universe.width,universe.height)).convert()
        self.image.fill((255,255,255))
        self.alpha_value = 0
        self.image.set_alpha(self.alpha_value)

    def update_all(self):
        if self.inside:
            if self.alpha_value < 200:
                self.alpha_value += 10
        else:
            if self.alpha_value > 0:
                self.alpha_value -= 15
            if self.alpha_value < 0:
                self.image.set_alpha(self.alpha_value)
                alpha_value = 0
        if 180 > self.alpha_value > 40:
            self.image.set_alpha(self.alpha_value)


class Bar():
    def __init__(self,level, up_or_down):
        tile = pygame.image.load('data/images/interface/omni/small_bar/0.png').convert_alpha()
        if up_or_down == 'up':
            tile = pygame.transform.flip(tile,0,1)
        screen_size = 1440,900 #level.universe.width, level.universe.height
        tile_size   = tile.get_size()
        image_prep  = pygame.Surface((screen_size[0],tile_size[1]),pygame.SRCALPHA).convert_alpha()
        bar_positions = range(0,(screen_size[0]/tile_size[0]+1))
        [image_prep.blit(tile,(i*tile_size[0],0)) for i in bar_positions]
        self.tile   = obj_images.scale_image(tile)
        self.tile_size = self.tile.get_size()
        self.image  = obj_images.scale_image(image_prep)


class BigScenario():
    def __init__(self,level):
        self.level      = level
        self.image      = pygame.Surface((9600*scale,level.universe.height), pygame.SRCALPHA).convert_alpha()
        self.pos        = [self.level.universe.center_x,0]

    def update_all(self):
        self.pos[0]         = self.level.universe.center_x
