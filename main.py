import pygame
import random
import time
SCREEN_WIDTH = 1280//2
SCREEN_HEIGHT = 960//2 # 스크린의 가로, 세로
backcolor=(255,255,255)
hpcolor = (255, 0, 0) # 색깔 RGB
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #화면 설정
clock=pygame.time.Clock() # 게임 내 시간 변수
flag=True
mobs=[] # 몬스터 객체 리스트
weapons=[] # 무기 객체 리스트
class weapon:
    def __init__(self):
        self.size="무기 사이즈"
        self.Time="무기 지속시간"
        self.str="무기 데미지"
        self.throw="무기 관통력"
        self.speed="투사체 속도"
        self.dx=1 # x 벡터 방향
        self.dy=1 # y 벡터 방향
        self.img = "해당 무기 이미지"
        self.loc= "해당 무기 위치"
    def start(self,start_time):
        self.start_time=start_time #무기의 생성 시간
    def move_check(self):
        # 무기의 방향 벡터를 랜덤으로 정해줌
        while True:
            list=[1,-1,0]
            dx=random.choice(list)
            dy=random.choice(list)
            if dx!=0 or dy!=0:
                break
        self.dx=dx
        self.dy=dy
    def move(self):
        #무기 이동
        self.loc.x+=self.dx*self.speed
        self.loc.y+=self.dy*self.speed
    def time_check(self,game_time,x,y):
        # 만약 무기의 지속 시간이 다했다면 플레이어의 위치로 이동
        if game_time-self.start_time>=self.Time:
            self.loc.x=x
            self.loc.y=y
            self.start_time=game_time # 무기 생성 시간 갱신
            self.move_check()
    def draw(self):
        screen.blit(self.img,self.loc)

class boom(weapon):
    def __init__(self):
        self.size=40
        self.Time=2
        self.str=10
        self.throw=3
        self.speed=10
        self.dx=1 # x 벡터 방향
        self.dy=1 # y 벡터 방향
        self.img = pygame.image.load("C:/Users/ASUS/PycharmProjects/pygame/게임 이미지/boom.png")
        self.loc = pygame.Rect(self.img.get_rect())
        self.img = pygame.transform.scale(self.img, (self.size, self.size))

class player:
    def __init__(self):
        #초기 설정값
        self.size=30
        self.hp_size=50
        self.hp=100
        self.str = 10
        self.speed = 5
        self.level=0
        self.exp=0
        self.img = pygame.image.load('C:/Users/ASUS/PycharmProjects/pygame/게임 이미지/hero.png')
        self.hp_img = pygame.image.load('C:/Users/ASUS/PycharmProjects/pygame/게임 이미지/hp.png')
        self.loc = pygame.Rect(self.img.get_rect())
        self.img = pygame.transform.scale(self.img, (self.size, self.size))
        self.hp_img = pygame.transform.scale(self.hp_img, (self.hp_size,10))
        self.loc.x=200
        self.loc.y=300
    def move(self):
        #움직이는 함수
        key_event = pygame.key.get_pressed()
        if key_event[pygame.K_LEFT]:
            self.loc.x -= self.speed
        if key_event[pygame.K_RIGHT]:
            self.loc.x += self.speed
        if key_event[pygame.K_UP]:
            self.loc.y -= self.speed
        if key_event[pygame.K_DOWN]:
            self.loc.y += self.speed
    def draw(self):
        #그리는 함수
        self.hp_size=self.hp//2
        if self.hp_size<=0:
            self.hp_size=0
        self.hp_img = pygame.transform.scale(self.hp_img, (self.hp_size, 10))
        screen.blit(self.img, (self.loc.x, self.loc.y))
        screen.blit(self.hp_img, (self.loc.x-10, self.loc.y - 20))
    def death_check(self,x,y,str,size):
        #몬스터와 충돌하였는지 판별, x,y,srt,size= 몬스터의 값
        if (abs(self.loc.x - x) <= size and abs(self.loc.y - y) <= size):
            self.hp-=str//10



class monster:
    def __init__(self):
        self.size= "몬스터 크기"
        self.hp="몬스터 체력"
        self.str="몬스터 공격력"
        self.speed="몬스터 속도"
        self.dx=1 # x 벡터 방향
        self.dy=1 # y 벡터 방향
        self.img = "해당 몬스터 이미지"
        self.loc= "해당 몬스터 위치"
    def start(self):
        # 몬스터 스폰 위치 지정
        spawnlistx=list(range(-2*SCREEN_WIDTH,-SCREEN_WIDTH))+list(range(SCREEN_WIDTH,2*SCREEN_WIDTH))
        spawnlisty=list(range(-2*SCREEN_HEIGHT,-SCREEN_HEIGHT))+list(range(SCREEN_HEIGHT,2*SCREEN_HEIGHT))
        self.loc.x = random.choice(spawnlistx)
        self.loc.y = random.choice(spawnlisty)
    def draw(self):
        screen.blit(self.img, self.loc)
    def move(self,x,y):
        #몬스터가 플레이어에게 이동하게 하는 함수
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
    def death_check(self,x,y,str,size):
        #몬스터의 무기와 충돌 여부 확인
        if (abs(self.loc.x - x) <= size and abs(self.loc.y - y) <= size):
            self.hp-=str
        if self.hp<=0:
            mobs.remove(self)
            return -1 # 몬스터 삭제됨
        return 0 #몬스터 삭제 되지 않음


class zombie(monster):
    def __init__(self):
        self.size=30
        self.hp=100
        self.str=20
        self.speed=5
        self.dx=1
        self.dy=1
        self.img = pygame.image.load('C:/Users/ASUS/PycharmProjects/pygame/게임 이미지/zom.png')
        self.img = pygame.transform.scale(self.img, (self.size, self.size))
        self.loc= pygame.Rect(self.img.get_rect())
class slenderman(monster):
    def __init__(self):
        self.size=50
        self.hp=150
        self.str=10
        self.speed=1
        self.dx=1
        self.dy=1
        self.img = pygame.image.load('C:/Users/ASUS/PycharmProjects/pygame/게임 이미지/enderman.png')
        self.img = pygame.transform.scale(self.img, (self.size, self.size))
        self.loc= pygame.Rect(self.img.get_rect())
    def move(self,x,y):
        super().move(x,y)
        # 기존 move 함수에 슬랜더맨 텔레포트 기능 추가
        elist = [0, 1, 2, 3,4,5,6,7,8,9,10]
        epoint = random.choice(elist)
        if epoint == 0:
            self.loc.x += 10 * (self.dx)
            self.loc.y += 10 * (self.dy)

def Rungame():
    global flag
    # 게임 시작 시간
    game_time = int(time.time())
    # 좀비 1 객체 생성
    zom1=zombie()
    # 몬스터 리스트에 넣어주기
    mobs.append(zom1)
    slen1=slenderman()
    mobs.append(slen1)
    p1 = player()
    for i in range(10):
        # 폭탄 10개 생성
        boom1=boom()
        boom1.loc.x=p1.loc.x
        boom1.loc.y=p1.loc.y
        weapons.append(boom1)
    for monsters in mobs:
        #몬스터들 스폰 위치 지정
        monsters.start()
    for weapon in weapons:
        #무기 위치 지정 및 무기 생성 시간 기록
        weapon.start(int(time.time())-game_time)
    while flag:
        # 현재 시간
        remain_time= int(time.time())-game_time
        clock.tick(60)
        screen.fill(backcolor)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
        p1.move()
        # 플레이어 좌표값
        player_x=p1.loc.x
        player_y=p1.loc.y
        for weapon in weapons:
            #무기 지속 시간 체크
            weapon.time_check(remain_time,player_x,player_y)
            weapon.move()
            weapon.draw()
        for monsters in mobs:
            #몬스터의 좌표,힘,크기 값
            mob_x=monsters.loc.x
            mob_y=monsters.loc.y
            mob_str=monsters.str
            mob_size=monsters.size
            #플레이어의 좌표를 받아 몬스터를 움직인다
            monsters.move(player_x,player_y)
            for weapon in weapons:
                #무기의 좌표,힘,크기 값
                weapon_x=weapon.loc.x
                weapon_y=weapon.loc.y
                weapon_str=weapon.str
                weapon_size=weapon.size
                #몬스터가 무기에 충돌했는지를 판정
                if monsters.death_check(weapon_x,weapon_y,weapon_str,weapon_size)<0:
                    break
            # 플레이어가 몬스터와 충돌했는지를 판정
            p1.death_check(mob_x,mob_y,mob_str,mob_size)
            monsters.draw()
        p1.draw()
        pygame.display.update()
Rungame()
pygame.quit()