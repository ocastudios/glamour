import scenario.scenarios   as scenarios
import utils.obj_images     as obj_images
import interactive.enemy    as enemy
import scenario.skies       as skies
import interactive.fairy    as fairy
import scenario.floors      as floors
import interface.widget     as widget
import random
import scenario.moving_scenario as moving_scenario
import interface.glamour_stars as glamour_stars
import interactive.princess as princess
import os
import interface.game_clock as game_clock
import pygame
import interactive.camera   as camera
import interface.mousepointer as mousepointer
import interface.inside     as inside
import interface.ball       as ball
import sqlite3
import interactive.events   as events
#import gametext
from settings import *

###Gate Positions###
bathhousegate = p([480, 8138])
dressgate =     p([800, 4142,8471])
accessorygate = p([1497,4174,7836])
makeupgate =    p([1200,4661,8231])
shoegate =      p([1198,4690,8140])


class Stage():
    enemy_dir =     'data/images/enemies/'
    maindir   =     'data/images/scenario/'
    princesses = None
    def __init__(self,universe):
        self.name = None
        self.size = int(9600*scale)
        self.universe       = universe
        self.cameras        =[camera.GameCamera(self,-4220*scale)]
        self.gates          = []
        self.clock          = [game_clock.GameClock(self),game_clock.ClockPointer(self)]
        self.floor_heights  = {}
        self.floor          = universe.floor-186*scale
        self.menus          = []
        self.panel          = [None,None,glamour_stars.Glamour_Stars(self)]
        self.pointer        = []
        self.scenarios_front= []
        self.animated_scenarios =[]
        self.blitlist       = ('sky', 'background', 'moving_scenario', 'scenarios', 'animated_scenarios' ,'gates',  'lights', 'princesses','enemies', 'menus')
        self.foreground     = []
        self.white          = Foreground(self.universe)
        self.black          = Foreground(self.universe, color=(0,0,0), path= 'data/images/interface/loading/back.png')
        self.bar            = {'down': Bar(self,'down'), 'up': Bar(self,'up'), 'left': Bar(self,'left'), 'right': Bar(self,'right')}
        self.bar_goal       = self.universe.height/3
        self.bar_speed      = 1
        self.game_mouse     = mousepointer.MousePointer(self)
        self.pointer        = [self.game_mouse]
        self.inside         = None
        self.princess_castle= None
        self.fairy          = False
        self.omni_directory = 'data/images/scenario/omni/'
        self.ball           = None
        self.endmusic       = pygame.event.Event(pygame.USEREVENT,{'music':'finished'})
        self.ballroom = { 'day': scenarios.Background(110,self,self.maindir+'ballroom/ballroom_day/'),
                          'night': scenarios.Background(110,self,self.maindir+'ballroom/ballroom_night/')}
        self.event_counter  = 0
        self.starting_game  = True
        self.fae = [None,fairy.Fairy(20,self)]
        self.pause          = Pause(self)
        self.paused         = False
        self.water_level    = 1440*scale
        self.mouse_pos      = pygame.mouse.get_pos()
        self.exit_sign      = None
        self.loading_icons  = (obj_images.OneSided(main_dir+'/data/images/interface/loading/sun_n_moon_shadow/'),
                               obj_images.OneSided(main_dir+'/data/images/interface/loading/sun_n_moon/'),
                               obj_images.OneSided(main_dir+'/data/images/interface/loading/carriage/')
                               )
        self.margin = obj_images.image(main_dir+'/data/images/shadow-B.png')
        self.enemy_channel = pygame.mixer.Channel(6)

    def dress_castle(self):
        return inside.Inside(self,'dress',('pink','plain','red','yellow'))

    def accessory_castle(self):
        return inside.Inside(self,'accessory',('crown','purse','ribbon','shades'))

    def makeup_castle(self):
        return inside.Inside(self,'face',('eyelids','eyeshades','lipstick','simple'))

    def hair_castle(self):
        hair_list = random.sample(('black','brown','cinderella','rapunzel','rastafari', 'red', 'short', 'sleeping', 'snowwhite', 'yellow'), 5)
        return inside.Inside(self,'hair',hair_list)

    def shoes_castle(self):
        return inside.Inside(self,'shoes',('crystal','red','slipper','white'))

    def bathhouse_castle(self):
        return inside.Inside(self,'shower', [])

    def pause_game(self):
        return inside.Pause(self)

    def what_is_my_height(self,object,pos_x = None):
        try:
            y_height = self.floor_heights[(pos_x or int(object.center_distance+round(object.size[0]/2)) )]
        except:
            y_height = self.floor
        return      y_height

    def update_all(self):
        self.game_mouse.update()
        self.mouse_pos  = self.game_mouse.mouse_pos
        events.choose_event(self)
        self.act = self.universe.action
        self.direction = self.universe.dir
        if not self.ball:
            self.blit_all()
        if self.black.alpha_value > 0:
            self.changing_stages_darkenning(-1)
        if self.paused:
            if self.enemy_channel.get_sound():
                self.enemy_channel.fadeout(1500)
            self.update_pause()
        elif self.fairy and not self.princesses[0].inside and not self.ball:
            self.update_fairytip()
        else:
            if self.clock[1].count > 160:
                if self.background[0] == self.ballroom['day']:
                    self.background = [self.ballroom['night']]
            else:
                if self.background[0] == self.ballroom['night']:
                    self.background = [self.ballroom['day']]
            if self.clock[1].time == 'ball' and not self.princesses[0].inside:
                if self.enemy_channel.get_sound():
                    self.enemy_channel.fadeout(1500)
                self.enemy_channel
                self.ball = self.ball or ball.Ball(self, self.universe, self.princesses[0])
                self.ball.update_all()
            else:
                if self.ball:
                    self.ball = None
                self.cameras[0].update_all()
                self.universe.movement(self.direction)
                if not self.inside or (not self.inside.status == "choosing") or not self.princesses[0].inside:
                    for att in self.blitlist:
                        if att == 'lights':
                            if self.clock[1].time == 'night':
                                for i in self.lights:
                                    if i['status'] == 'on':
                                        i['position'].update_pos()
                                    if i['status'] == 'off' and random.randint(0,10) == 0:
                                        i['status'] = 'on'
                                        i['position'].update_pos()
                        else:
                            for i in self.__dict__[att]:
                                if i:
                                    i.update_all()

                    now_playing = self.enemy_channel.get_sound()
                    weight = 0
                    actual_class = None
                    for i in self.enemies:
                        if i.music and i.music['sound'] == now_playing:
                            weight = i.music['weight']
                            actual_class = i.__class__
                    set_classes = []
                    for i in self.enemies:
                        if i.music:
                            distance = 0
                            if (i.pos[0]/scale)-1440 > 0:
                                distance = (i.pos[0]/scale)-1440
                            elif i.pos[0]-(i.size[0]/scale) < 0:
                                distance = ((i.pos[0]/scale)+(i.size[0]/scale))*-1
                            if distance<1000:
                                my_turn = True
                                if self.enemy_channel.get_busy() and i.music['weight'] <= weight and i.music['sound']!=now_playing:
                                    my_turn = False
                                if my_turn:
                                    if i.__class__ != actual_class and i.music['sound']!= now_playing:
                                        self.enemy_channel.play(i.music['sound'])

                                    if distance > 0:
                                        volume = 1-(distance/1000)
                                    else:
                                        volume = 1
                                    if volume==0 and i.__class__ not in set_classes:
                                        self.enemy_channel.stop()
                                    if i.__class__ not in set_classes or volume ==1:
                                        if volume<=1:
                                            present_volume = self.enemy_channel.get_volume()
                                            if (1-volume)-present_volume > .2:
                                                self.enemy_channel.set_volume(present_volume+.2)
                                            else:
                                                self.enemy_channel.set_volume(volume)
                                        if 1-volume <.8:
                                            present_volume = pygame.mixer.music.get_volume()
                                            if (1-volume)-present_volume > .2:
                                                pygame.mixer.music.set_volume(present_volume+.2)
                                            else: 
                                                pygame.mixer.music.set_volume(1-volume)
                                        set_classes.append(i.__class__)
                            else:
                                if now_playing == i.music['sound'] and i.__class__ not in set_classes:
                                    i.music['sound'].stop()

                for i in self.scenarios_front+self.floor_image+self.foreground:
                    i.update_all()
                if self.princesses[0].inside:
                    self.update_insidebar()
                if not self.inside or (not self.inside.status == "choosing") or not self.princesses[0].inside:
                    for i in self.clock:
                        i.update_all()
                for i in self.panel:
                    if i:
                        i.update_all()
                self.exit_sign.update_all()
        for i in self.pointer:
            i.update_all()
            self.universe.screen_surface.blit(i.image,i.pos)

    def blit_all(self):
        screen = self.universe.screen_surface
        for att in self.blitlist:
            if att == 'lights':
                if self.clock[1].time == 'night':
                    for i in self.lights:
                        if i['status'] == 'on':
                            screen.blit(i['images'].list[i['images'].itnumber.next()],i['position'].pos)
            else:
                for i in self.__dict__[att]:
                    if i and i.image:
                        screen.blit(i.image,i.pos)
        for i in self.princesses[0].effects :
            screen.blit(i.image,i.pos)
        for i in self.scenarios_front:
            screen.blit(i.image,i.pos)
        if self.exit_sign.image:
            screen.blit(self.exit_sign.image, self.exit_sign.pos)
        for i in self.floor_image:
            screen.blit(i.image,i.pos)
        for i in self.foreground:
            screen.blit(i.image,i.pos)
        if self.sky[0].night_image:
            screen.blit(self.sky[0].night_image,(0,0))
        for i in self.clock:
            screen.blit(i.image,i.pos)
        for i in self.panel:
            if i:
                screen.blit(i.image,i.pos)
        if self.fairy:
            for i in self.fae:
                screen.blit(i.image,i.pos)
        screen.blit(self.margin,(0,0))

    def update_insidebar(self):
        if self.inside.status[:4] == 'bath': #Bath Castle
            self.universe.screen_surface.blit(self.white.image,(0,0))
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
            self.universe.screen_surface.blit(self.white.image,(0,0))
            self.universe.screen_surface.blit(self.bar['down'].image,(0,self.bar['down'].pos))
            self.universe.screen_surface.blit(self.bar['up'].image,(0,self.bar['up'].pos))
            if self.inside.status == 'inside':
                self.bar['up'].pos = -self.bar['up'].size[1]
                self.bar['down'].pos = self.universe.height
                self.white.alpha_value = 0
                self.inside.status = 'loading'
            elif self.inside.status == 'loading':
                pygame.mixer.music.fadeout(1500)
                self.white.image.set_alpha(self.white.alpha_value)
                if self.white.alpha_value < 200:
                    self.white.alpha_value += 10
                if self.bar['down'].pos > 2*self.bar_goal:
                    self.bar['down'].pos -= self.bar_speed
                if self.bar['up'].pos + self.bar['up'].size[1]< self.bar_goal:
                    self.bar['up'].pos += self.bar_speed
                if self.bar_speed < 20*scale:
                    self.bar_speed += self.bar_speed
                if self.white.alpha_value > 150:
                    self.inside.status = 'choosing'
                    pygame.mixer.music.load(self.inside.music)
                    pygame.mixer.music.play(-1)
            elif self.inside.status == 'choosing':
                self.princesses[0].update_all()
                [self.universe.screen_surface.blit(i.image,i.pos) for i in self.inside.items]
                [i.update_all() for i in self.inside.items]
                if self.inside.big_princess:
                    for i in self.inside.big_princess.images:
                        if i:
                            self.universe.screen_surface.blit(i,self.inside.big_princess.pos)
                [self.universe.screen_surface.blit(i.image,i.pos) for i in self.inside.buttons]
                [i.update_all() for i in self.inside.buttons]
                if self.inside.__class__== inside.Inside:
                    if self.inside.chosen_item:
                        self.universe.screen_surface.blit(self.inside.chosen_item.image,self.inside.chosen_item.pos)
                elif self.inside.__class__==inside.Home:
                    pos  = 500
                    for img in self.inside.past_balls:
                        self.universe.screen_surface.blit(img, p([pos,400]))
                        pos +=200
                try:
                    x = 880*scale
                    y = 270*scale
                    self.universe.screen_surface.blit(self.inside.princess_image, (x,y))
                except:
                    pass
            elif self.inside.status == 'done':
                pygame.mixer.music.fadeout(1500)
                self.princesses[0].update_all()
                self.bar['down'].pos += self.bar_speed
                self.bar['up'].pos -= self.bar_speed
                if self.bar_speed < 20*scale:
                    self.bar_speed += self.bar_speed
                if self.white.alpha_value > 0:
                    self.white.alpha_value -= 10
                    self.white.image.set_alpha(self.white.alpha_value)
                else:
                    self.white.alpha_value = 0
                self.white.image.set_alpha(self.white.alpha_value)
                if self.bar['down'].pos > self.universe.height and self.bar['up'].pos < -self.bar['up'].size[1] and self.white.alpha_value == 0:
                    pygame.mixer.music.load(self.music)
#                    pygame.mixer.music.queue(self.music)
#                    pygame.mixer.music.queue(self.music)
                    pygame.mixer.music.play(-1)
                    self.inside.status = 'openning'
            elif self.inside.status == 'openning':
                self.princesses[0].update_all()
                for i in self.gates:
                    if i.rect.colliderect(self.princesses[0].rect):
                        i.open = True
                        if i.images.number >= i.images.lenght -1:
                            self.inside.status = 'closing'
            elif self.inside.status == 'closing':
                print 'Getting out of the door'
                for i in self.gates:
                    if i.rect.colliderect(self.princesses[0].rect):
                        i.outside()
                self.princesses[0].inside = False


    def choice_screen(self, screen,condition):
        self.universe.screen_surface.blit(self.white.image,(0,0))
        self.universe.screen_surface.blit(self.bar['down'].image,(0,self.bar['down'].pos))
        self.universe.screen_surface.blit(self.bar['up'].image,(0,self.bar['up'].pos))
        if screen.status == 'inside':
            pygame.mixer.music.fadeout(1500)
            self.bar['up'].pos = -self.bar['up'].size[1]
            self.bar['down'].pos = self.universe.height
            self.white.alpha_value = 0
            screen.status = 'loading'
        elif screen.status == 'loading':
            self.white.image.set_alpha(self.white.alpha_value)
            if self.white.alpha_value < 200:
                self.white.alpha_value += 10
            if self.bar['down'].pos > 2*self.bar_goal:
                self.bar['down'].pos -= self.bar_speed
            if self.bar['up'].pos + self.bar['up'].size[1]< self.bar_goal:
                self.bar['up'].pos += self.bar_speed
            if self.bar_speed < 20*scale:
                self.bar_speed += self.bar_speed
            if self.white.alpha_value > 150:
                screen.status = 'choosing'
                pygame.mixer.music.load(screen.music)
                pygame.mixer.music.play(-1)
        elif screen.status == 'choosing':
            pass
        elif screen.status == 'done':
            pygame.mixer.music.fadeout(1500)
            self.bar['down'].pos += self.bar_speed
            self.bar['up'].pos -= self.bar_speed
            if self.bar_speed < 20*scale:
                self.bar_speed += self.bar_speed
            if self.white.alpha_value > 0:
                self.white.alpha_value -= 10
                self.white.image.set_alpha(self.white.alpha_value)
            else:
                self.white.alpha_value = 0
            self.white.image.set_alpha(self.white.alpha_value)
            if self.bar['down'].pos > self.universe.height and self.bar['up'].pos < -self.bar['up'].size[1] and self.white.alpha_value == 0:
                pygame.mixer.music.load(self.music)
#                pygame.mixer.music.queue(self.music)
#                pygame.mixer.music.queue(self.music)
                pygame.mixer.music.play(-1)
                screen.status = 'finished'

    def update_pause(self):
        princess = self.princesses[0]
        self.choice_screen(self.pause,self.paused)
        if self.pause.status == 'choosing':
            for i in self.pause.buttons:
                self.universe.screen_surface.blit(i.image, i.pos)
                i.update_all()
                if princess.image:
                    self.universe.screen_surface.blit(princess.image,
                                        ((self.universe.width/2)-(princess.image_size[0]/2),
                                        (self.universe.height/2)-(princess.image_size[1]/2)))
            if self.fairy:
                for i in self.fae:
                    i.update_all()
        elif self.pause.status == 'done':
            pass
        elif self.pause.status == 'finished':
            self.paused = False

    def update_fairytip(self):
        pymusic = pygame.mixer.music
        self.universe.screen_surface.blit(self.white.image,(0,0))
        if self.fairy == 'loading':
            self.white.image.set_alpha(self.white.alpha_value)
            if self.white.alpha_value < 200:
                self.white.alpha_value += 50
                volume = pymusic.get_volume()
                if 0.6 >= volume > 0.1:
                    volume -= .01
                    pymusic.set_volume(volume)
            if self.white.alpha_value > 150:
                self.fairy = 'speaking'
        elif self.fairy == "speaking":
            if self.universe.action[0]in ('jump','kiss'):
                self.fae[0].end_message()
            for i in self.fae:
                self.universe.screen_surface.blit(i.image,i.pos)
                i.update_all()
        elif self.fairy == 'done':
            self.princesses[0].update_all()
            if self.bar_speed < round(20*scale):
                self.bar_speed += self.bar_speed
            if self.white.alpha_value > 0:
                volume = pymusic.get_volume()
                if .6 >= volume >= 0: 
                    volume += .01
                    if volume >.6:
                        volume=.6
                    pymusic.set_volume(volume)
                self.white.alpha_value -= 50
                self.white.image.set_alpha(self.white.alpha_value)
            else:
                self.white.alpha_value = 0
                self.fairy = None
            self.white.image.set_alpha(self.white.alpha_value)

    def select_enemies(self, allowed_enemies, street):
        self.enemies = []
        universe_cursor = self.universe.db_cursor
        row     = universe_cursor.execute("SELECT * FROM stage_enemies WHERE stage = '"+street+"'").fetchone()
        enemy.Butterfly._registry = []
        for e in allowed_enemies:
            if int(row[e]):
                name = e.replace('_',' ').title()
                name = name.replace(' ','')
                if name == 'Footboy':
                    name = 'FootBoy'
                maximum = 1
                if name in ("Butterfly" , "Bird") :
                    maximum = 2+int(self.princesses[0].points/30)
                for i in range(0,random.randint(1,maximum)):
                    pos_x = scale*(random.randint(1400,7000))
                    self.enemies.append(enemy.__dict__[name](pos_x,self))
            self.loading()
#        self.enemies.append(enemy.Schnauzer(pos_x,self))

    def loading(self):
        if self.black.alpha_value > 100:
            self.universe.screen_surface.blit(self.black.image,(0,0))
            shadow = self.loading_icons[0]
            world = self.loading_icons[1]
            carriage = self.loading_icons[2]
            world_pos =   ((self.universe.width/2)-(world.size[0]/2), (self.universe.height/2)-(world.size[1]/2))
            carriage_pos = (world_pos[0]+(182*scale),world_pos[1]+(75*scale))
            for i in self.loading_icons:
                i.update_number()
            self.universe.screen_surface.blit(shadow.list[world.number],(world_pos[0],(world_pos[1]+60*scale)) )
            self.universe.screen_surface.blit(world.list[world.number],world_pos)
            self.universe.screen_surface.blit(carriage.list[carriage.number],carriage_pos)
            self.universe.screen_surface.blit(self.bar['left'].image,(self.bar['left'].pos,0))
            self.universe.screen_surface.blit(self.bar['right'].image,(self.bar['right'].pos,0))
            pygame.display.flip()

    def bring_side_bars(self,darkenning):
        self.universe.screen_surface.blit(self.black.image,(0,0))
        self.universe.screen_surface.blit(self.bar['left'].image,(self.bar['left'].pos,0))
        self.universe.screen_surface.blit(self.bar['right'].image,(self.bar['right'].pos,0))
        if self.bar['left'].pos < 0-(self.bar['left'].size[0]/5):
            self.bar['left'].pos += self.bar_speed
        else:
            self.bar['left'].pos = 0-(self.bar['left'].size[0]/5)
        if self.bar['right'].pos > self.universe.width-(self.bar['right'].size[0]-(self.bar['right'].size[0]/5) ):
            self.bar['right'].pos -= self.bar_speed
        else:
            self.bar['right'].pos = self.universe.width-(self.bar['right'].size[0]-(self.bar['right'].size[0]/5) )
        if self.bar_speed < 20*scale:
            self.bar_speed += self.bar_speed
        self.black.alpha_value += (5*darkenning)
        self.black.image.set_alpha(self.black.alpha_value)
        self.universe.clock.tick(self.universe.frames_per_second)
        pygame.display.flip()

    def changing_stages_darkenning(self,darkenning=1):
        self.bar['left'].pos = -self.bar['left'].size[0]
        self.bar['right'].pos = self.universe.width
        self.universe.screen_surface.blit(self.black.image,(0,0))
        if darkenning > 0:
            pygame.display.flip()
            while self.black.alpha_value<255:
                self.bring_side_bars(darkenning)
        if self.black.alpha_value > 255:
            self.black.alpha_value = 255
        elif self.black.alpha_value < 0:
            self.black.alpha_value = 0
        self.black.image.set_alpha(self.black.alpha_value)
        self.black.alpha_value += (10*darkenning)

    def create_scenario(self,street):
        self.loading()
        self.viking_ship = None
        db = sqlite3.connect(main_dir+'/data/'+street+'.db')
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        self.loading()
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
            self.loading()
            self.scenarios_prep.append(img)
        self.scenarios = BigScenario(self),
        self.lights = []
        for i in self.scenarios_prep:
            self.scenarios[0].image.blit(i.image,i.pos)
            try:
                if i.lights:
                    self.lights.append(i.lights)
            except:
                pass
            self.loading()
        cursor.close()
        self.sky             = [skies.Sky(self)]
        self.clouds          =   [scenarios.Cloud(self) for cl in range(3)]
        self.loading()
        [self.sky[0].image.blit(i.image,i.pos) for i in self.clouds]
        self.loading()

    def create_front_scenario(self,street):
        db = sqlite3.connect(main_dir+'/data/'+street+'.db')
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
                self.scenarios_front.append(scenarios.Scenario(scale*i['xpos'],i['directory'],self,i['ind']))
            self.loading()
        cursor.close()

    def set_floor_heights(self,height,width,street):
        db = sqlite3.connect(main_dir+'/data/'+street+'.db')
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        self.floor_heights = [round(height*scale)]*int(round(width*scale))
        for row in cursor.execute("SELECT * FROM floor ORDER BY id ASC").fetchall():
            for r in range(int(round(int(row['start'])*scale)),int(round(int(row['end'])*scale))):
                self.floor_heights[r]=row['value']*scale
        cursor.close()
        self.loading()

    def stage_music(self,intro, music):
        pygame.mixer.music.fadeout(4000)
        self.loading()
        self.music = main_dir+"/data/sounds/music/"+music
        pygame.mixer.music.load(main_dir+"/data/sounds/music/"+intro)
        self.loading()
        pygame.mixer.music.queue(self.music)
        pygame.mixer.music.queue(self.music)
        self.loading()
        pygame.mixer.music.play()
        self.loading()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.mixer.music.set_volume(.6)


    def create_stage(self,translatable_name,goalpos,hardname):
        if self.enemy_channel.get_sound():
            self.enemy_channel.fadeout(1500)
        self.changing_stages_darkenning()
        self.loading()
        self.name = hardname
        db = sqlite3.connect(main_dir+'/data/'+hardname+'.db')
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        self.loading()
        self.princesses = self.princesses or [princess.Princess(self),None]
        self.animated_scenarios = []
        self.loading()
        if goalpos:
            self.princesses[0].center_distance = goalpos
            self.universe.center_x = -goalpos+(self.universe.width/2)
        self.gates = []
        self.directory = self.maindir+hardname+'_st/'
        self.background = [self.ballroom['day']]
        self.loading()
        self.moving_scenario = [moving_scenario.Billboard(self)]
        self.loading()
        self.animated_scenarios =[]
        self.exit_sign  = self.exit_sign or scenarios.ExitSign(self)
        self.loading()
        cursor.close()
        self.create_scenario(hardname)
        self.create_front_scenario(hardname)
        self.panel          = [widget.GameText(t(translatable_name), (300,20), self,font_size = 30),
                               None,
                               glamour_stars.Glamour_Stars(self),
                               widget.GameText(self.princesses[0].name, (660,47), self, font_size = 70,fonte='Chopin_Script.ttf'),
                               glamour_stars.Lil_Star_Back(self,(1020,0)),
                               glamour_stars.Lil_Stars(self, (1030,10)),
                               widget.GameText(str(self.princesses[0].points), (1000,20),self,font_size = 30)
        ]


    def BathhouseSt(self,goalpos = None, clean_princess = False):
        self.set_floor_heights(186,9400,'bathhouse')
        self.create_stage(t('Bathhouse St'),goalpos,'bathhouse')
        gates = (   [(1063,453),'bathhouse/door/',self.bathhouse_castle(),True],
                    [(5206,500),'home/door/', inside.Home(self), False], 
                    [(9305,503),'magic_beauty_salon/door/',self.hair_castle(),False])
        self.loading()
        doors = (   [bathhousegate[0], self.ShoesSt,shoegate[2]],
                    [bathhousegate[1], self.AccessorySt, accessorygate[0]])
        self.loading()
        self.gates = [  scenarios.BuildingDoor(p(i[0]),self.directory+i[1],self,i[2],bath=i[3]) for i in gates]
        self.loading()
        self.gates.extend([scenarios.Gate(i[0], self.maindir+'omni/gate/',self,i[1], goalpos = i[2]) for i in doors])
        self.loading()
        self.select_enemies(('schnauzer', 'butterfly', 'old_lady', 'footboy', 'bird'),'BathhouseSt')
        self.floor_image= [floors.Floor(c,self.directory+'floor/tile/',self) for c in range(24)]
        self.loading()
        floors.Bridge(self.directory+'floor/japanese_bridge/',5,self)
        self.loading()
        self.stage_music("bathhouse_day_intro.ogg","bathhouse_day.ogg")
        self.loading()
        if self.starting_game:
            events.choose_event(self,starting_game=True)
            self.starting_game = False
        if clean_princess:
            self.princesses[0].dirt = 0
            self.universe.db_cursor.execute("UPDATE save SET dirt = "+str(self.princesses[0].dirt)+" WHERE name = '"+self.princesses[0].name+"'")
            print "You look lovely all cleaned up!"
            self.princesses[1] = None
            
    def DressSt(self,goalpos = None):
        self.create_stage(t('Dress St'), goalpos,'dress')
        self.animated_scenarios = [scenarios.Scenario(0,self.directory+'Dress_Tower/flag/',self)]
        self.loading()
        self.select_enemies(('schnauzer', 'butterfly', 'old_lady', 'footboy', 'bird','carriage'),'DressSt')
        self.gates = [scenarios.BuildingDoor(p((155,318)),self.directory+'Dress_Tower/door/',self,self.dress_castle()),
                      scenarios.BuildingDoor(p((9194,430)),self.directory+'snow_white_castle/door/',self, inside.Princess_Home(self,Snow_White)),
                      scenarios.Gate(dressgate[0], 'data/images/scenario/omni/gate/',self,self.AccessorySt,goalpos = accessorygate[2]),
                      scenarios.Gate(dressgate[1], 'data/images/scenario/omni/gate/',self,self.ShoesSt,goalpos = shoegate[1]),
                      scenarios.Gate(dressgate[2], 'data/images/scenario/omni/gate/',self,self.MakeupSt,goalpos = makeupgate[0])]
        self.loading()
        self.floor_image= [floors.Floor(c,self.directory+'floor/',self) for c in range(30)]
        self.loading()
        self.stage_music("dress_day_intro.ogg","dress_day.ogg")
        self.set_floor_heights(185,9400,'dress')

    def AccessorySt(self,goalpos = None):
        self.create_stage(t('Accessory St'), goalpos,'accessory')

        self.select_enemies(('schnauzer', 'butterfly', 'old_lady', 'bird'),'AccessorySt')
        self.viking_ship = enemy.VikingShip(5000*scale,self)
        self.loading()
        self.gates.extend([
            scenarios.BuildingDoor(p((330,428)),self.directory+'accessory_tower/door/',self,self.accessory_castle()),
            scenarios.BuildingDoor(p((8809,425)),self.directory+'castle/door/',self,inside.Princess_Home(self, Sleeping_Beauty)),
            scenarios.Gate(accessorygate[0], 'data/images/scenario/omni/gate/',self,self.BathhouseSt,goalpos = bathhousegate[1]),
            scenarios.Gate(accessorygate[1], 'data/images/scenario/omni/gate/',self,self.MakeupSt,goalpos = makeupgate[1]),
            scenarios.Gate(accessorygate[2], 'data/images/scenario/omni/gate/',self,self.DressSt , goalpos = dressgate[0])
                        ])
        self.loading()
        self.floor_image= [floors.Floor(fl,self.directory+'floor/tile/',self) for fl in range(30)]
        self.loading()
        self.floor_image.extend([floors.Water(wat,self.directory+'water/tile/',self) for wat in range(11)])
        self.loading()
        self.floor_image.extend([self.viking_ship])
        self.loading()
        self.floor_image.extend([floors.Water2(wat,self.directory+'water/tile/',self) for wat in range(11)])
        self.loading()
        [floors.Drain(self.directory+'floor/'+i[0]+'_bank_front/',i[1],self) for i in [('left',2),('right',3),('left',20),('right',21)]]
        self.loading()
        self.stage_music("accessory_day.ogg","accessory_day.ogg")
        self.set_floor_heights(194,9400,'accessory')

    def MakeupSt(self,goalpos = None):
        self.create_stage(t('Makeup St'),goalpos,'makeup')
        self.select_enemies(('carriage','schnauzer', 'butterfly', 'old_lady', 'footboy', 'bird'),'MakeupSt')
        self.gates.extend([ scenarios.Gate(makeupgate[x],'data/images/scenario/omni/gate/',self,y,goalpos = z)
                            for x,y,z in
                            ((0, self.DressSt, dressgate[2]),
                             (1, self.AccessorySt, accessorygate[1]),
                             (2, self.ShoesSt ,shoegate[0]))
                            ])
        self.loading()
        self.gates.extend([scenarios.BuildingDoor(p((130,225)),self.directory+'make-up_castle/door/',self,self.makeup_castle()),
                     scenarios.BuildingDoor(p((9082,301)),self.directory+'sleeping_castle/door/',self,inside.Princess_Home(self,Sleeping_Beauty))])
        self.loading()
        self.floor_image= [floors.Floor(fl,self.directory+'floor/',self) for fl in range(30)]
        self.loading()
        available_animals = random.sample( (enemy.Lion, enemy.Monkey, enemy.Elephant, enemy.Penguin, enemy.Giraffe), 3 )
        self.animated_scenarios = [ i(self) for i in available_animals]
        self.loading()
        self.animated_scenarios.append(scenarios.Scenario(2923*scale,self.directory+'zoo/base/',self))
        self.loading()
        tail = None
        if enemy.Lion in available_animals:
            for i in self.animated_scenarios:
                if i.__class__ == enemy.Lion:
                    tail = True
                break
        if tail:
            self.animated_scenarios.insert(1,i.tail)
        self.loading()
        self.set_floor_heights(192,9400,'makeup')
        self.loading()
        self.stage_music("makeup_day_intro.ogg","makeup_day.ogg")

    def ShoesSt(self,goalpos=None):
        self.create_stage(t('Shoes St'),goalpos,'shoes')
        self.animated_scenarios = [scenarios.Scenario(scale*7137,self.directory+'fountain/base/',self)]
        self.loading()
        self.select_enemies(('carriage','schnauzer', 'butterfly', 'old_lady', 'footboy', 'bird'),'ShoesSt')
        self.gates = [scenarios.BuildingDoor(p((372,273)),self.directory+'shoes_tower/door/',self,self.shoes_castle()),
        scenarios.BuildingDoor(p((9440,374)),self.directory+'rapunzel_castle/door/',self,inside.Princess_Home(self, Rapunzel)),
        scenarios.Gate(shoegate[0],'data/images/scenario/omni/gate/',self,self.MakeupSt, goalpos = makeupgate[2]),
        scenarios.Gate(shoegate[1],'data/images/scenario/omni/gate/',self,self.DressSt,  goalpos = dressgate[1]),
        scenarios.Gate(shoegate[2],'data/images/scenario/omni/gate/',self,self.BathhouseSt, goalpos = bathhousegate[0]),]
        self.floor_image= [floors.Floor(c,self.directory+'floor/',self) for c in range(30)]
        self.loading()
        self.stage_music("shoes_day_intro.ogg","shoes_day.ogg")
        self.set_floor_heights(192,9601,'shoes')
        self.loading()

class Foreground():
    def __init__(self,universe, color=(255,255,255), path=None):
        self.pos = 0,0
        if path:
            self.image = obj_images.image(path, alpha = False)
        else:
            self.image = pygame.Surface((universe.width,universe.height)).convert()
            self.image.fill(color)
        self.alpha_value = 0
        self.image.set_alpha(self.alpha_value)
        self.status = None

    def update_all(self):
        pass

class Bar():
    def __init__(self,level, up_or_down):
        if up_or_down in ('left','right'):
            if up_or_down == 'left':
                self.image = obj_images.image('data/images/interface/omni/left_bar/0.png')
                self.size = self.image.get_size()
                self.pos = -self.size[0]
            else:
                self.image = obj_images.image('data/images/interface/omni/left_bar/0.png',invert=True)
                self.size = self.image.get_size()
                self.pos = level.universe.width
        else:
            tile = obj_images.image('data/images/interface/omni/small_bar/0.png')
            if up_or_down == 'up':
                tile = pygame.transform.flip(tile,0,1)
                self.pos = -tile.get_height()
            else:
                self.pos = level.universe.height
            screen_size = 1440,900 #level.universe.width, level.universe.height
            tile_size   = tile.get_size()
            image_prep  = pygame.Surface((screen_size[0],tile_size[1]),pygame.SRCALPHA).convert_alpha()
            bar_positions = range(0,(screen_size[0]/tile_size[0]+1))
            [image_prep.blit(tile,(i*tile_size[0],0)) for i in bar_positions]
            self.tile   = obj_images.scale_image(tile)
            self.tile_size = self.tile.get_size()
            self.image  = obj_images.scale_image(image_prep)
            self.size = self.image.get_size()


class BigScenario():
    def __init__(self,level):
        self.level      = level
        self.image      = pygame.Surface((9600*scale,level.universe.height), pygame.SRCALPHA).convert_alpha()
        self.pos        = [self.level.universe.center_x,0]

    def update_all(self):
        self.pos[0]         = self.level.universe.center_x


class Pause():
    def __init__(self, level):
        self.status = 'outside'
        self.level  = level
        resume      = widget.GameText(t('Resume'),(360,400),self.level,font_size=80, fonte='Chopin_Script.ttf')
        ok_pos      = (resume.pos[0]+(resume.size[0]/2))/scale,(resume.pos[1]+(resume.size[1]))/scale+50
        ok_button   = widget.Button(main_dir+'/data/images/interface/title_screen/button_ok/',ok_pos,self.level,self.resume)
        quit        = widget.GameText(t('Quit'),(1080,400),self.level,font_size= 80, fonte='Chopin_Script.ttf')
        cancel_pos  = (quit.pos[0]+(quit.size[0]/2))/scale,(quit.pos[1]+(quit.size[1]))/scale+50
        cancel_button = widget.Button(main_dir+'/data/images/interface/title_screen/button_cancel/',cancel_pos,self.level,exit)
        title       = widget.GameText(t('Game Paused'),(720,100),self.level, fonte='Chopin_Script.ttf', font_size=120)
        self.buttons    = (resume, ok_button, quit, cancel_button, title)
        self.music  = main_dir+'/data/sounds/music/1stSnowfall.ogg'

    def resume(self):
        self.status = 'done'

    def do_nothing(self):
        pass

    def update_all(self):
        pass
