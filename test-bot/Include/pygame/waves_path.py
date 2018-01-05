# IT WAS HARD BUT I CAN, IT WAS MISERABLE BUT I TRYED.
# AND I....


#PERSIK GAME YOU KNOW
import sys, pygame, copy, threading,random,math
from collections import deque
from pygame.locals import *
import time

start = time.time()


pygame.init()
#DEFINE THE CONSTANTS
size = wight, height = 640,480
LEFT = 1
global ThingPlace
#DEFINE THE COLORS
black =  0,0,0
alpha = 255,255,255

screen = pygame.display.set_mode(size)
global win
win=0
objects = []
clock = pygame.time.Clock()
class tile():
    def __init__(self,solid,value):
        self.solid=solid
        self.value=value
class object():
    def __init__(self,x,y):
        self.x = x
        self.y = y
#JUST SPRITE.
class sprite():

    def __init__(self,name,image=None,size=None):
        self.name = name
        self.size = size
        self.image = pygame.image.load(name)
        self.image = self.image.convert()
        self.image.set_colorkey((255,255,255))

level_map=[[ tile(solid=False,value=0)
         for y in range(128) ]
         for x in range(128) ]
for y in range(128):
    for x in range(128):
        if random.randint(0,3)==1:
            level_map[x][y].solid=True
        else:
            level_map[x][y].solid=False

persik = object(2,2)
objects.append(persik)
pygame.display.flip()


class pathfinding():
    def __init__(self,x_start,y_start,x_end,y_end,x,y,value,path_map):
        self.path_map=copy.deepcopy(level_map)
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end
        self.value=value
        self.x=x_start
        self.y=y_start
        self.open_list=deque([])
        self.closed_list=deque([])
    def distance_to(self, x_to,y_to,xs,ys):
        #return the distance to another object
        dx = x_to - xs
        dy = y_to - ys
        return math.sqrt(dx ** 2 + dy ** 2)
    def calculate(self,x,y):
        self.path_map[x][y].value = self.value
        if (x+1)<128 :
            if   self.path_map[x+1][y].value==0 and  self.path_map[x+1][y].solid==False:
                 self.path_map[x+1][y].value=self.value
                 self.open_list.append(x+1)
                 self.open_list.append(y)
        if  (x-1)>0 :
            if  self.path_map[x-1][y].value==0  and self.path_map[x-1][y].solid==False:
                 self.path_map[x-1][y].value=self.value
                 self.open_list.append(x-1)
                 self.open_list.append(y)
        if  (y+1)<128:
            if  self.path_map[x][y+1].value==0 and self.path_map[x][y+1].solid==False:
                 self.path_map[x][y+1].value=self.value
                 self.open_list.append(x)
                 self.open_list.append(y+1)
        if  (y-1)>0:
            if  self.path_map[x ][y-1].value==0  and self.path_map[x ][y-1].solid==False:
                 self.path_map[x ][y-1].value=self.value
                 self.open_list.append(x)
                 self.open_list.append(y-1)
        self.x=x
        self.y=y
    def cho_choose(self):
        self.value+=1
        if len(self.open_list)<>0:
          x_s=self.open_list.popleft()
          y_s=self.open_list.popleft()
          self.calculate(x_s,y_s)
        elif self.x==5 and self.y==5:
            self.calculate(55,55)
        else:
            win=1
        if self.path_map[5][5].value>0:
            win=1



path = pathfinding(5,5,64,64,5,5,2,level_map)
z=0

def render_all():
    path.cho_choose
    if path.path_map[5][5].value>0:
        screen.fill((100,255,100))
        finish = time.time()
        print (finish - start)
    else:
        screen.fill(black)
    for i in objects:
            screen.set_at((i.x ,i.y), (255, 0, 0))


while True:
    render_all()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:sys.exit()

        keys_press=pygame.key.get_pressed()
        if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
            #Get MOUSE POSITION IN x,y
            (x_mouse,y_mouse) = pygame.mouse.get_pos()


