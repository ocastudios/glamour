import pygame


class Panel():
    def __init__(self,pos,size,background):
        self.pos = pos
        self.size = size
        self.background = background
        self.data = []
    def print_data(self):
        for infor in self.data:
            infor_surface = infor.font.render((infor.title+': '+str(infor.variable)),1,(0,0,0))
            screen_surface.blit (infor_surface,(self.pos[0]+infor.pos[0],self.pos[1]+infor.pos[1]))
class Data():
    def __init__(self,title,variable,pos,level,index,fonte='FreeSans',size=40):
        self.level = level        
        self.title = title
        self.index = index
        self.pos = pos
        self.font=pygame.font.Font('data/fonts/Domestic_Manners.ttf',size)
        self.label = self.font.render((self.title+str(variable)),1,(0,0,0))

        for i in level:
            i.panel.insert(index,(self.label,self.pos))

    def update(self,variable):
        self.label = self.font.render((self.title+str(variable)),1,(0,0,0))
        for i in self.level:
            i.panel[self.index]=(self.label,self.pos)
