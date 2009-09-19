import pygame
import obj_images
import random

class Ball():
    directory = 'data/images/interface/ball/'
    def __init__(self, level, universe, princess):

        self.background      = pygame.Surface((9600,level.universe.height),pygame.SRCALPHA).convert_alpha()
        for file in (self.directory+'ball-back.png',self.directory+'back-bubbles.png'):
            self.background.blit(pygame.image.load(file), (0,0))
        self.left_bar   = VerticalBar(self)
        self.princess   = princess
        self.Bar        = VerticalBar(self)
        self.Frame      = BallFrame(self)
        self.level      = level
        self.universe   = universe
        self.dancers    = [
                            Dancer([1200,100]),
                            Dancer([200,200]),
                            Dancer([800,300]),
                            Dancer([600,400]),
                            Dancer([300,600])
                            ]

        pygame.mixer.music.load("data/sounds/music/strauss_waltz_wedley.ogg")
        pygame.mixer.music.play()


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
            self.universe.screen_surface.blit(i.symbol,(i.symbolpos,i.pos[1]-100))
            i.update_all()


class VerticalBar():
    def __init__(self, ball, right_or_left = 'left'):
        self.image = pygame.image.load('data/images/interface/ball/golden-bar.png').convert_alpha()
        if right_or_left == 'right':
            self.image = pygame.transform.flip(self.image, 1,0)
        self.size = self.image.get_size()
        self.position = [-self.size[0],0]
        self.speed = 5
        self.ready = False

    def update_all(self):
        if self.position[0] < 90:
            self.position[0] += self.speed
            self.speed += 5
        else:
            self.position[0] = 90
            self.ready = True


class BallFrame():
    def __init__(self, ball):
        self.image = pygame.image.load('data/images/interface/ball/back-frame.png').convert_alpha()
        self.size = self.image.get_size()
        self.position = [30, -self.size[1]]
        self.speed = 5
        self.ball = ball
        self.princesses = [
                FairyTalePrincess(self, 100,'hair_snowwhite','skin_pink', 'princess-icon-apple.png'),
                FairyTalePrincess(self, 200,'hair_cinderella','skin_tan','princess-icon-shoe.png'),
                FairyTalePrincess(self, 300,'hair_rapunzel','skin_pink', 'princess-icon-brush.png'),
                FairyTalePrincess(self, 400,'hair_sleeping','skin_pink','princess-icon-spindle.png')
                        ]
        self.texts = [
                VerticalGameText("Yesterday's ball", (100,200), self),
                VerticalGameText("Tonight's ball", (100,500), self),
                    ]

    def update_all(self):
        if self.ball:
            if self.position[1] + (self.size[1]/2) < (self.ball.universe.height/2):
                self.speed +=2
            else:
                self.speed = 0
            self.position[1] += self.speed


class FairyTalePrincess():
    def __init__(self, frame, position_x, hair, skin, icon):
        princess_directory  = 'data/images/princess/'
        ball_directory      = 'data/images/interface/ball/'
        self.frame      = frame
        self.image      = pygame.Surface((200,200),pygame.SRCALPHA).convert_alpha()
        images          = [ pygame.image.load(princess_directory+skin+'/stay/0.png').convert_alpha(),
                            pygame.image.load(princess_directory+hair+'/stay/0.png').convert_alpha()]
        self.position   = [position_x, 200]
        for img in images:
            self.image.blit(img, (0,0))
        self.symbol     =   pygame.image.load(ball_directory+icon).convert_alpha()
        self.symbolpos  = position_x + (self.image.get_width()/2) - (self.symbol.get_width()/2)
        self.pos        = [ self.frame.position[0]+self.position[0],
                            self.frame.position[1]+self.position[1]]

    def update_all(self):
        self.pos        = [self.frame.position[0]+self.position[0],
                           self.frame.position[1]+self.position[1]]


class StarBall():
    def __init__(self):
        self.images = obj_images.OneSided('data/images/interface/ball/star-score/')
        self.image = self.images.list[self.images.itnumber()]
        self.position = (10,1000)

    def update_all(self):
        self.image = self.images.list[self.images.itnumber()]


class GameText():
    def __init__(self,text,pos,frame,fonte='Domestic_Manners.ttf', font_size=20, color=(0,0,0),second_font = 'Chopin_Script.ttf'):
        self.frame      = frame
        self.font      = pygame.font.Font('data/fonts/'+fonte,font_size)
        self.image      = self.font.render(text,1,color)
        self.position   = pos
        self.size       = self.image.get_size()
        self.pos        = [self.frame.position[0]+self.position[0]-(self.size[0]/2),
                           self.frame.position[1]+self.position[1]-(self.size[1]/2)]
    def update_all(self):
        self.pos        = [self.frame.position[0]+self.position[0]-(self.size[0]/2),
                           self.frame.position[1]+self.position[1]-(self.size[1]/2)]


class VerticalGameText(GameText):
    def __init__(self,text,pos,menu, fonte='Domestic_Manners.ttf',font_size = 30, color = (0,0,0)):
        GameText.__init__(self,text,pos,menu,fonte,font_size,color)
        self.image = pygame.transform.rotate(self.image,90)


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
