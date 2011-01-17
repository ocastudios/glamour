#import pygame


#class Panel():
#    def __init__(self,pos,size,background):
#        self.pos = pos
#        self.size = size
#        self.background = background
#        self.data = []

#    def print_data(self):
#        for i in self.data:
#            infor_surface = i.font.render((i.title+': '+str(i.variable)),1,(0,0,0))
#            screen_surface.blit (infor_surface,(self.pos[0]+i.pos[0],self.pos[1]+i.pos[1]))


#class Data():
#    def __init__(self,title,variable,pos,level,index,fonte='FreeSans',size=40):
#        self.level  = level
#        self.title  = title
#        self.index  = index
#        self.pos    = pos
#        self.font   = pygame.font.Font(main_dir+'/data/fonts/Domestic_Manners.ttf',size)
#        self.label  = self.font.render((self.title+str(variable)),1,(0,0,0))
#        self.level.panel.insert(index,self)

#    def update(self,variable):
#        self.label = self.font.render((self.title+str(variable)),1,(0,0,0))
#        self.level.panel[self.index]=(self)
