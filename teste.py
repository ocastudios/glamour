import Image
import pygame

try:
    import psyco
    psyco.log()
    psyco.profile(1.0)
except:
    pass
#Create lists

for i in xrange(50):
#    im = Image.open("/home/nelson/Bazaar/Glamour/glamour/data/images/scenario/bathhouse_st/bathhouse/Bathhouse.png")
    im2 = pygame.image.load("/home/nelson/Bazaar/Glamour/glamour/data/images/scenario/bathhouse_st/bathhouse/Bathhouse.png")
    
    
#    imagem =Image.open("/home/nelson/Bazaar/Glamour/glamour/data/images/scenario/bathhouse_st/left_house/base/0.png")
    imagem2 = pygame.image.load("/home/nelson/Bazaar/Glamour/glamour/data/images/scenario/bathhouse_st/left_house/base/0.png")
    
#    im.paste(imagem,(0,0))
    im2.blit(imagem2,(0,0))
