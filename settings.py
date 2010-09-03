import os
scale =1
main_dir = os.getcwd()
Snow_White      = {'skin': 'pink', 'hair': 'hair_snowwhite', 'icon': 'princess-icon-apple.png',   'name' : 'Snow_White'}
Cinderella      = {'skin': 'tan' , 'hair': 'hair_cinderella','icon': 'princess-icon-shoe.png'   , 'name' : 'Cinderella'}
Rapunzel        = {'skin': 'pink', 'hair': 'hair_rapunzel'  ,'icon': 'princess-icon-brush.png'  , 'name' : 'Rapunzel'}
Sleeping_Beauty = {'skin': 'pink', 'hair': 'hair_sleeping'  ,'icon': 'princess-icon-spindle.png', 'name' : 'Sleeping_Beauty'}
def p(positions):
    return [int(i*scale) for i in positions ]

