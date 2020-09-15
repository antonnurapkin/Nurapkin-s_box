import pygame
import random
import math
import sqlite3

W = 500
H = 500

class Spaceship():
    def __init__(self,x,y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.img = pygame.image.load(r'C:\Users\TEMP.LAPTOP-GSC041CB.001\Documents\hotpng.png')  
        self.img = pygame.transform.scale(self.img, (150, 150))

    def draw_spaceship(self,sc):
        sc.blit(self.img, (self.x, self.y))

    def spaceship_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_ESCAPE]:
            exit() 

class Stones():
    def __init__(self,x,y,rad,color=(0,0,0)):
        self.x = x
        self.y = y
        self.rad = rad
        self.color = color
        self.speed = random.randint(2,6)

    def draw(self, sc):
        pygame.draw.circle(sc, self.color, (self.x, self.y), self.rad)
        if self.y == 0:
            self.rad = random.randint(10,50) 

    def move_ver(self):
        self.y += self.speed
        if self.y > H:
            self.y = 0
        if self.y == 0:
            self.x = random.randint(0,500)
   
class Stars():

    def __init__(self,x,y,rad,color = (0,0,0)):
        self.x = x
        self.y = y
        self.rad = rad
        self.color = color

    def move_ver_for_stars(self):
        self.x += 1
        if self.x > H:
            self.x = 0
        if self.x == 0:
            self.y = random.randint(0,500)

    def draw_stars(self,sc):
        pygame.draw.circle(sc,self.color,(self.y,self.x),self.rad)

def intersect(Stones,Spaceship):
    sh = 15
    if Spaceship.y + Spaceship.y//20 < Stones.y + Stones.rad and\
        (Spaceship.x + 150//2 - sh < Stones.x - Stones.rad < Spaceship.x + 150//2 + sh or\
        Spaceship.x + 150//2 - sh < Stones.x + Stones.rad < Spaceship.x + 150//2 + sh or\
        Spaceship.x + 150//2 - sh < Stones.x  < Spaceship.x + 150//2 + sh):
        return False
        #if Spaceship.y == Stones.y + Stones.rad and Spaceship.x + 150//2 - i == Stones.x :
            
def show_score(surface,points):
   font = pygame.font.Font(None, 24)
   score = font.render('Score: '+ str(int(points)),1,(255,255,255))
   surface.blit(score,(0, 0))

#List_stones = []
#for i in range(3):
#   List_stones.append(Stones(random.randint(0,W), 0, random.randint(10,50), (165, 42, 42)))


pygame.init()
fps = pygame.time.Clock()

sc = pygame.display.set_mode((W, H))

St1 = Stones(random.randint(0,W), 0, random.randint(10,50), (165, 42, 42))
St2 = Stones(random.randint(0,W), 0, random.randint(10,50), (165, 42, 42))
St3 = Stones(random.randint(0,W), 0, random.randint(10,50), (165, 42, 42))

Sp_sh = Spaceship((W-150)//2,H - 150,10)

List_stars = []
for i in range(30):
    List_stars.append(Stars(random.randint(0,W), random.randint(0,H), 1, (255, 255, 255)))

points = 0

connect = sqlite3.connect('SCORE_TABLE.db')
cursor = connect.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS players(player TEXT,score INT)')

sensor = True

while True:
    # проверка на нажатие крестика
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sensor = False
            break

    sc.fill((0, 0, 0))

    intersect(St1,Sp_sh)
    intersect(St2,Sp_sh)
    intersect(St3,Sp_sh)

    for i in List_stars:
        i.move_ver_for_stars()
        i.draw_stars(sc)        
    
    St1.move_ver()
    St2.move_ver()
    St3.move_ver()
    
    St1.draw(sc)
    St2.draw(sc)
    St3.draw(sc)

    Sp_sh.draw_spaceship(sc)
    Sp_sh.spaceship_control()

    show_score(sc,points)
    points = points + 0.01

    pygame.display.update()

    if sensor == False:
        break

    if intersect(St1,Sp_sh)==False or\
        intersect(St2,Sp_sh)==False or\
        intersect(St3,Sp_sh)==False:
        break

    fps.tick(120)

pygame.quit()

print("Ваш счёт:",round(points,0))
nickname = input("Введите свое имя: ")
cursor.execute(f"INSERT INTO players VALUES('{nickname}','{int(points)}')")

cursor.execute('SELECT * FROM players')
List_players = cursor.fetchall()

count = 0
for i in List_players:
    count += 1
print(count)
for j in range(count):
    for i in range(count-1):
        if List_players[i][1] < List_players[i+1][1]:
            List_players[i],List_players[i+1] = List_players[i+1],List_players[i]

print('Топ-5 лучших игроков\n')
for i in range(0,5):
    print(List_players[i][0],List_players[i][1])

connect.commit()
connect.close()



