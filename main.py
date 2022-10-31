import pygame
import random
pygame.init()
backcolor=(255,255,255)
SCREEN_WIDTH = 1280/2
SCREEN_HEIGHT = 960/2
clock=pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
flag=True
zs=[]

class boom:
    def __init__(self):
        self.img = pygame.image.load('boom.png')
        self.loc= pygame.Rect(self.img.get_rect())
        self.img = pygame.transform.scale(self.img, (30, 30))
        self.dx=0
        self.dy=0
    def start(self,x,y):
        self.loc.x=x
        self.loc.y=y
    def draw(self):
        screen.blit(self.img, self.loc)
    def move(self):
        self.loc.x+=self.dx*40
        self.loc.y+=self.dy*40
    def move_check(self):
        list=[1,-1]
        dx=random.choice(list)
        dy=random.choice(list)
        self.dx=dx
        self.dy=dy

class player:
    def __init__(self):
        self.hp=100
        self.speed=10
        # 사람 이미지, 폭탄 이미지
        self.img = pygame.image.load('hero.png')
        self.move_flag=''
        self.img = pygame.transform.scale(self.img, (40, 40))
        self.loc = pygame.Rect(self.img.get_rect())
        self.loc.x=200
        self.loc.y=300
    def draw(self):
        screen.blit(self.img, self.loc)
    def move(self):
        self.move_flag=''
        key_event = pygame.key.get_pressed()
        if key_event[pygame.K_LEFT]:
            self.loc.x-= self.speed
            self.move_flag='left'

        if key_event[pygame.K_RIGHT]:
            self.loc.x+= self.speed
            self.move_flag='right'

        if key_event[pygame.K_UP]:
            self.loc.y-= self.speed
            self.move_flag='up'

        if key_event[pygame.K_DOWN]:
            self.loc.y += self.speed
            self.move_flag='down'

class zombie():
    def __init__(self,speed):
        self.hp=100
        self.img = pygame.image.load('zom.png')
        self.img = pygame.transform.scale(self.img, (30, 30))
        self.loc= pygame.Rect(self.img.get_rect())
        self.dx=1+speed
        self.dy=1+speed
    def start(self):
        self.loc.x = random.randint(-SCREEN_WIDTH, 2*SCREEN_WIDTH)
        self.loc.y = random.randint(-SCREEN_HEIGHT, 2*SCREEN_HEIGHT)
    def move(self,x,y):
        if x>=self.loc.x:
            if self.dx<0:
                self.dx*=-1
        elif x<self.loc.x:
            if self.dx>0:
                self.dx*=-1
        if y>=self.loc.y:
            if self.dy<0:
                self.dy*=-1
        elif y<self.loc.y:
            if self.dy>0:
                self.dy*=-1
        self.loc.x+=self.dx
        self.loc.y+=self.dy
    def death_check(self,x,y):
        global zs
        if abs(self.loc.x-x)<=30 and abs(self.loc.y-y)<=30:
            zs.remove(self)
    def draw(self):
        screen.blit(self.img, self.loc)


def Rungame():
    global flag
    global zs
    p1=player()
    boom1=boom()
    for i in range(100):
        speed=random.randint(1,5)
        zs.append(zombie(speed))
    for i in zs:
        i.start()
    i=0
    while flag:
        clock.tick(30)
        screen.fill(backcolor)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
        p1.move()
        p1.draw()
        if (boom1.loc.x>SCREEN_WIDTH or boom1.loc.x<0) or (boom1.loc.y>SCREEN_HEIGHT or boom1.loc.y<0):
            i=0
        while i==0:
            boom1.start(p1.loc.x,p1.loc.y)
            boom1.move_check()
            i+=1
        boom1.move()
        boom1.draw()
        for i in zs:
            i.death_check(boom1.loc.x,boom1.loc.y)
            i.move(p1.loc.x,p1.loc.y)
            i.draw()
        if len(zs)==0:
            flag=False
        pygame.display.update()
Rungame()
pygame.quit()