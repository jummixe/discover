#PERSIK GAME YOU KNOW
import sys, pygame, copy, threading
from collections import deque
from pygame.locals import *
pygame.init()
#DEFINE THE CONSTANTS
size = wight, height = 640,480
LEFT = 1
global ThingPlace
#DEFINE THE COLORS
black =  0,0,0
alpha = 255,255,255

screen = pygame.display.set_mode(size)
NODE_X=1
NODE_Y=1
objects = []
clock = pygame.time.Clock()
total_level_width=60*64
total_level_height=55*64
x_offset=0
y_offset=0
class tile():
    def __init__(self,sprite,solid):
        self.sprite = sprite
        self.solid = solid

class object(object):

    def __init__(self,x,y,sprite,solid = False ,way = False,on_collision = None,live_component = None,jump=0,size_x=64,size_y=64,player = False ):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.solid = solid
        self.way = way
        self.on_collision = on_collision
        self.live_component = live_component
        self.jump=jump
        self.jump_speed=25
        self.size_x=size_x
        self.size_y=size_y
        self.true_x=self.x
        self.true_y=self.y
        self.right_x= self.x +size_x
        self.bottom_y= self.y +size_y
        self.bottom_y-16
        self.rect = Rect(self.x,self.y,64,64)
    def collision_check(self,x,y):
        if level_map[x/64][y/64].solid == True:
            return True
        else:
            return False

    def check_all(self,x_f,y_f):
        if y_f<=0:
           if level_map[self.true_x/64][(self.bottom_y+y_f)/64].solid==False:
             if level_map[self.right_x/64][(self.bottom_y+y_f)/64].solid==False:
              return True
        if y_f>=0:
           if level_map[self.true_x/64][(self.true_y-y_f)/64].solid==False:
              if level_map[self.right_x/64][(self.true_y-y_f)/64].solid==False:
                  return True
        if  x_f<=0:
           if level_map[(self.true_x+x_f)/64][self.true_y/64].solid==False:
              if level_map[(self.true_x+x_f)/64][((self.bottom_y)-16)/64].solid==False:
                 return True
        if x_f>=0:
           if level_map[(self.right_x+x_f)/64][self.true_y/64].solid==False:
              if level_map[(self.right_x+x_f)/64][((self.bottom_y)-16)/64].solid==False:
                    return True
    def make_it_true(self):
        self.true_x=self.x
        self.true_y=self.y + 15
        self.right_x= self.x +self.size_x
        self.bottom_y= self. y +self.size_y
        self.bottom_y-16

    def move(self,x_change ):
        if self.x>0:
            if self.check_all(x_change,0):
              self.x+=x_change
              self.make_it_true()

    def move_y(self,y_change ):
        if  self.check_all(0,y_change):
            self.y-=y_change
            self.make_it_true()

#CAMERA OFFSET SUPER DUPER
class camera():

    def __init__(self,x,y):
        self.x=x
        self.y=y
    def update(self,x,y):
        self.x=x
        self.y=y
    def apply(self):
        return x,y
#JUST SPRITE
class sprite():

    def __init__(self,name,image=None,size=None,rect=None):
        self.name = name
        self.size = size
        self.image = pygame.image.load(name)
        self.image = self.image.convert()
        self.image.set_colorkey((255,255,255))
        self.rect = Rect(0,0,64,64)
#Queue class, you know?
class queue():

    def __init__(self,queue=[],first=0,last=0):
        self.queue=deque([])
        self.first = first
        self.last =last
    def Send(self,key):
        if self.last<4:
            self.queue.append(key)

        else:
            self.last=4
            #103
            print('Dont forget to call police!')
    def Get(self,pos=0):
        if len(self.queue) is not 0:
            zet=self.queue.popleft()
            return zet


Main_queue=queue()

Jump_queue=queue()

persik_sprite = sprite('persik.png')
tile_sprite = sprite('tile.png')

level_map=[[ tile(sprite=tile_sprite.image,solid=True)
         for y in range(60) ]
         for x in range(55) ]
level_global_map=[[tile(sprite=tile_sprite.image,solid=True)
         for y in range(60) ]
         for x in range(55) ]

for x in range(0,20):
    for y in range(0,5):
        level_map[x][y].sprite = None
        level_map[x][y].solid = False

for x in range(1,0):
    for y in range(0,10):
        level_map[x][y].sprite =tile_sprite.image
        level_map[x][y].solid = true
persik = object(64,64,persik_sprite.image,player = True,size_x=64,size_y=64)
objects.append(persik)
pygame.display.flip()

def check_node(self):
        return (int(round(self.x/64)-4),int(round(self.y/64)-4))
def render_all():
    x_z=0
    y_z=0
    clock.tick(60)
    screen.fill(black)
    (NODE_X,NODE_Y)=check_node(persik)
    screen.blit(persik.sprite,(persik.x,persik.y))
   # for x in range (NODE_X-1, NODE_X+8):
   #     for y in range(NODE_Y-1, NODE_Y+8):
        #lint:disable\
    for x in range(0,11):
          for y in range(0,11):
            map_xoff=x%63
            map_yoff=y%63
            map_node =level_map[x][y].sprite
            if map_node is not None:
                screen.blit(map_node,(x*64- map_xoff,y*64- map_yoff ))
        #lint:enable
          y_z+=64
          y_z=0
          x_z+=64
    pygame.display.flip()
def all_moves():
    if level_map[persik.true_x/64][(persik.bottom_y-2)/64].solid==False:
       if persik.check_all(0,0):
          Jump_queue.Send(persik.move_y(-2))
    peka = Jump_queue.Get()
    if peka== persik.move_y:
        peka(7)
    t_1= threading.Thread(target=Main_queue.Get)
    t_1.start()
pygame.key.set_repeat(1,3)

while True:
    all_moves()
    render_all()
    zet = 50
    for event in pygame.event.get():

        if event.type == pygame.QUIT:sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
            #Get MOUSE POSITION IN x,y

            (x_mouse,y_mouse) = pygame.mouse.get_pos()
            #IF there is any buttons in position, swap it to clicked state
            print(level_map[x_mouse/64][y_mouse/64].solid)
            level_map[x_mouse/64][y_mouse/64].solid=True
            level_map[x_mouse/64][y_mouse/64].sprite=tile_sprite.image
            print(x_mouse/64,y_mouse/64)
            print(persik.true_x/64,persik.true_y/64)


        keys_press=pygame.key.get_pressed()
        if keys_press:
            if persik.jump==1:
                persik.jump=0

        if keys_press[K_SPACE]:
           if level_map[persik.true_x/64][(persik.bottom_y-2)/64].solid==True:
               for i in range(0,10):
                  to_send = persik.move_y
                  Jump_queue.Send(to_send)
        if  keys_press[K_LEFT]:
            EventPlayer = persik.move(-7 )
            Main_queue.Send(EventPlayer)
        if  keys_press[K_RIGHT]:
            EventPlayer=persik.move(7)
            Main_queue.Send( EventPlayer)
        if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
            #Get MOUSE POSITION IN x,y

            (x_mouse,y_mouse) = pygame.mouse.get_pos()

