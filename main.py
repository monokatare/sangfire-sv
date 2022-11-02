import pygame
import random
import sys
pygame.init()
backcolor=(255,255,255)
hpcolor = (255, 0, 0)
SCREEN_WIDTH = 1280//2
SCREEN_HEIGHT = 960//2
clock=pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
flag=True
mobs=[]
weapon=[]
small_font = pygame.font.SysFont(None, 36)
hp_pont=''

class boom:
    def __init__(self):
        self.img = pygame.image.load('boom.png')
        self.loc= pygame.Rect(self.img.get_rect())
        self.img = pygame.transform.scale(self.img, (30, 30))
        self.dx=0
        self.dy=0
        self.attack=50
    def start(self,x,y):
        self.loc.x=x
        self.loc.y=y
    def draw(self):
        screen.blit(self.img, self.loc)
    def move(self):
        self.loc.x+=self.dx*20
        self.loc.y+=self.dy*20
    def move_check(self):
        while True:
            list=[1,-1,0]
            dx=random.choice(list)
            dy=random.choice(list)
            if dx!=0 or dy!=0:
                break
        self.dx=dx
        self.dy=dy

class player:
    def __init__(self):
        self.hp=100
        self.speed=10
        self.img = pygame.image.load('hero.png')
        self.move_flag=''
        self.img = pygame.transform.scale(self.img, (40, 40))
        self.loc = pygame.Rect(self.img.get_rect())
        self.loc.x=200
        self.loc.y=300
    def draw(self):
        hp_pont = str(self.hp)
        self.hp_image = small_font.render(hp_pont, True, hpcolor)
        screen.blit(self.img, self.loc)
        screen.blit(self.hp_image,(self.loc.x,self.loc.y-30))
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
    def death_check(self,x,y,attack):
        if (abs(self.loc.x-x)<=30 and abs(self.loc.y-y)<=30):
            self.hp-=attack

class zombie():
    def __init__(self,speed):
        self.hp=100
        self.img = pygame.image.load('zom.png')
        self.img = pygame.transform.scale(self.img, (30, 30))
        self.loc= pygame.Rect(self.img.get_rect())
        self.dx=1+speed
        self.dy=1+speed
        self.attack=10
    def start(self):
        spawnlistx=list(range(-2*SCREEN_WIDTH,-SCREEN_WIDTH))+list(range(SCREEN_WIDTH,2*SCREEN_WIDTH))
        spawnlisty=list(range(-2*SCREEN_HEIGHT,-SCREEN_HEIGHT))+list(range(SCREEN_HEIGHT,2*SCREEN_HEIGHT))

        self.loc.x = random.choice(spawnlistx)
        self.loc.y = random.choice(spawnlisty)
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
    def death_check(self,x,y,i,attack):
        if (abs(self.loc.x - x) <= 30 and abs(self.loc.y - y) <= 30):
            self.hp-=attack
        if self.hp<=0:
            mobs.remove(i)
    def draw(self):
        screen.blit(self.img, self.loc)
class enderman():
    def __init__(self,speed):
        self.hp = 500
        self.img = pygame.image.load('enderman.png')
        self.img = pygame.transform.scale(self.img, (30, 30))
        self.loc = pygame.Rect(self.img.get_rect())
        self.dx = 1 + speed
        self.dy = 1 + speed
        self.attack=10
    def start(self):
        spawnlistx=list(range(-2*SCREEN_WIDTH,-SCREEN_WIDTH))+list(range(SCREEN_WIDTH,2*SCREEN_WIDTH))
        spawnlisty=list(range(-2*SCREEN_HEIGHT,-SCREEN_HEIGHT))+list(range(SCREEN_HEIGHT,2*SCREEN_HEIGHT))

        self.loc.x = random.choice(spawnlistx)
        self.loc.y = random.choice(spawnlisty)
    def move(self,x,y):
        elist=[0,1,2]
        epoint=random.choice(elist)
        if epoint==0:
            if abs(x-self.loc.x)>50 and abs(y-self.loc.y)>50:
                self.loc.x+=10*(self.dx)
                self.loc.y+=10*(self.dy)

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
    def death_check(self,x,y,i,attack):
        if (abs(self.loc.x - x) <= 30 and abs(self.loc.y - y) <= 30):
            self.hp-=attack
        if self.hp<=0:
            mobs.remove(i)
    def draw(self):
        screen.blit(self.img, self.loc)


def Rungame():
    global flag
    p1=player()
    boom1=boom()
    for i in range(10):
        speed=random.randint(1,3)
        ender=enderman(speed)
        mobs.append([ender,ender.loc.x,ender.loc.y,ender.attack]) # (인덱스 0번: 객체 1번: x위치 2번: y위치 3번: 공격력)

    for i in range(10):
        speed=random.randint(1,6)
        zom=zombie(speed)
        mobs.append([zom,zom.loc.x,zom.loc.y,zom.attack])
    for i in mobs:
        i[0].start()
    i=0
    while flag:
        clock.tick(15)
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
        for monster in mobs:
            # (인덱스 0번: 객체 1번: 객체의 x위치 2번: 객체의 y위치 3번: 객체의 공격력)
            # 리스트의 객체 위치 업데이트
            monster[1]=monster[0].loc.x
            monster[2]=monster[0].loc.y
            p1.death_check(monster[1],monster[2],monster[3])
            monster[0].death_check(boom1.loc.x,boom1.loc.y,monster,boom1.attack)
            monster[0].move(p1.loc.x,p1.loc.y)
            monster[0].draw()
        if len(mobs)==0 or p1.hp<=0:
            flag=False
        pygame.display.update()
Rungame()
pygame.quit()