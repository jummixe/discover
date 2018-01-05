import sys, pygame, copy
from pygame.locals import *
pygame.init()
#DEFINE THE CONSTANTS
map_widght = 60
map_height = 40
size = wight, height = 640,480
LEFT = 1
global ThingPlace
#DEFINE THE COLORS
black =  0,0,0
alpha = 255,255,255

#BUTTONS
buttons = []

#ROSES ARE GREEN, VIOLETS ARE TOO, IF YOU READ THIS STROKES, THEN THEY ARE FOR YOU.
#THING is just group of sprites, and methods to work with them.
#SPRITE is an image, it's direction
#MAP consists of TILES
#TERRAIN IS TYPE OF TILE!

#INIT THE SCREEN
screen = pygame.display.set_mode(size)



#ADMIN CLASS FOR ME
class admin():

    def __init__(self,thingtoplace = None):
        self.thingtoplace = thingtoplace

#THING - GROUP OF SPRITES IN DIFFRENET DIRECTION REPRESENTING THINGS
class thing():

    def __init__(self,name,directions=[]):
        self.name = name
        self.directions = directions

    def find_direction(self,direction):
        for i in self.directions:
            if i.direction == direction:
                return i.image
        return 'wtf'
#JUST SPRITE.

class sprite():

    def __init__(self,name,direction,image=None,size=None):
        self.name = name
        self.direction = direction
        self.size = size
        self.image = pygame.image.load(name)
        self.image = self.image.convert()
        self.image.set_colorkey((255,255,255))

#TILE ON MAP
class tile():

    def __init__(self,type):
        self.type = type

#Button
class button():

    def __init__(self, sprite, sprite_clicked, sprite_off, use_function, WhatToPlace = None, state= False):

        self.use_function = use_function
        #CURRENT SPRITE IS SOO COOL
        self.sprite = sprite_off
        #WHEN BUTTON IS CLICKED THIS SPRITE YOU TAKES
        self.sprite_clicked = sprite_clicked
        #WHEN BUTTON IS NOT CLIKED - THIS ONES
        self.sprite_off = sprite_off
        self.state = False
        self.WhatToPlace = WhatToPlace
        #NEED THIS TO CALCULATE CLICK-ZONz
        buttons.append(self)
    def change_state(self):
        if self.state == False:
            for i in buttons:
                i.state = False
                i.sprite= i.sprite_off
            self.state = True
            self.sprite = self.sprite_clicked
            #If it's about placing things:
            if self.WhatToPlace:
               self.use_function(self.WhatToPlace)
            else:
                self.use_function()
        else:
            self.state = False
            self.sprite = self.sprite_off
Max = admin()
#DECORATION ON MAP
class terrain():

    def __init__(self,thing,name,direction, sprite=None,blocked = False,rails = None):
        self.thing = thing
        self.name = name
        self.direction = direction
        self.blocked = blocked
        self.rails = rails
        #Nice func return a sprite of this direction from thing.
        self.sprite =  self.thing.find_direction(self.direction)


#Rails Sprite
rails_hor = sprite('rails_h.png',direction = 'h')
rails_ver = sprite('rails_v.png',direction = 'v')

#Buttons Rails
button_ver = sprite('button_ver.png',direction ='0')
button_ver_clicked = sprite('button_ver_clicked.png',direction = '0')

button_hor = sprite('button_hor.png',direction = '0')
button_hor_clicked = sprite('button_hor_clicked.png',direction = '0')
grass_sprite = sprite('empty.png',direction='v')
#All rails as a group

rails = thing('rails',[rails_hor ,rails_ver])

grass = thing('grass',[grass_sprite])

grass_ter = terrain(grass,name='grass_sprite',direction='v')
rails_hor_ter = terrain(rails,name='rails',direction='h')
rails_ver_ter = terrain(rails,name='rails',direction='v')


def choose_thing(WhatToPlace):
    Max.thingtoplace = WhatToPlace


button_ver_rails = button(sprite = button_ver.image ,
                   sprite_clicked = button_ver_clicked.image,
                   sprite_off = button_ver.image,
                   WhatToPlace = rails_ver_ter,
                   use_function = choose_thing)

button_hor_rails = button(sprite = button_hor.image ,
                   sprite_clicked = button_hor_clicked.image,
                   sprite_off = button_hor.image,
                   WhatToPlace = rails_hor_ter,
                   use_function = choose_thing)


map = [[ tile(rails_hor_ter)
         for y in range(map_height) ]
         for x in range(map_widght) ]
buttons_map = [['0'
                for y in range(7) ]
                for x in range(10) ]
buttons_map[0][0] = button_hor_rails
buttons_map[1][0] = button_ver_rails
map[5][5].type = rails_ver_ter
pygame.display.flip()

zet = 0

def map_borders(x,y):
    if x>1 and x<map_widght-1:
                if y>1 and x<map_height-1:
                    return True

while True:
    zet = 50
    for event in pygame.event.get():

        if event.type == pygame.QUIT:sys.exit()

        if event.type == KEYDOWN and event.key == K_q:
             print('Pressed q, what a fool')

        elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
            #Get MOUSE POSITION IN x,y

            (x_mouse,y_mouse) = pygame.mouse.get_pos()
            #IF there is any buttons in position, swap it to clicked state
            if buttons_map[x_mouse/64][y_mouse/64] is not '0':
                buttons_map[x_mouse/64][y_mouse/64].change_state()
            elif Max.thingtoplace is not None:
                map[x_mouse/60][y_mouse/40].type=Max.thingtoplace

                print(map[x_mouse/60][y_mouse/40].type)
    screen.fill(black)

    for x in range(map_widght):
         for y in range(map_height):
            map_node = map[x][y].type.sprite
            screen.blit(map_node,(x*60 ,y*40 ))
    for x in range(10):
        for y in range(7):
            if buttons_map[x][y] is not '0':
               screen.blit(buttons_map[x][y].sprite,(x*64,y*64))

    pygame.display.flip()
