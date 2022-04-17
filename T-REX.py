
from random import randint
from turtle import speed, update
import pygame
import sys

pygame.init()

class Dino():
    def __init__(self):
        self.sprites = [image_load("trex1.png",(50,50)),
                        image_load("trex2.png",(50,50)),
                        image_load("trex3.png",(50,50)),
                        image_load("trex4.png",(50,50))]
        
        self.rect = self.sprites[0].get_rect()
        self.rect.x = 40
        self.rect.width = 40
        self.currSprite = 0
        self.jump = 0
        self.onTheGround = False
        
    
    def update(self):
        self.onTheGround = False

        #jump
        self.rect.move_ip(0,self.jump)
        self.jump+=0.4

        #ground
        if(self.rect.bottom > 270):
            self.rect.bottom = 270
            self.onTheGround = True

        
    def jumpRex(self):
        if(self.onTheGround):
            self.jump = -13
    
    def draw(self):
        global screen
        
        if(self.currSprite == 3):
            self.currSprite = 3
        elif(self.onTheGround ):
            if(self.currSprite <= 1 ):
                self.currSprite = 2
            else:
                self.currSprite = 1
        else:
            self.currSprite = 0
        
        screen.blit(self.sprites[self.currSprite],self.rect)
    
    def dead(self):
        self.currSprite = 3
    def isDead(self):
        return self.currSprite == 3

class Clouds():
    def __init__(self,path,x,y):
        self.sprite = image_load(path,(50,30))
        self.rect = self.sprite.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        global width
        self.rect.move_ip(-1.7,0)
        if(self.rect.right < 0):
            self.rect.left = width+30
            self.rect.y = randint(10,200)
    def draw(self):
        global screen
        screen.blit(self.sprite,self.rect)

class Cactus():
    def __init__(self,x):
        self.sprites = [image_load("cactus1.png",(32,65)),
                        image_load("cactus2.png",(65,65)),
                        image_load("cactus3.png",(75,65))]
        
        
        self.speed = -3.5
        self.currSprite = randint(0,2)
        self.rect = self.sprites[self.currSprite].get_rect()
        self.rect.x = x
        self.rect.bottom = 270
    def update(self):
        global width
        self.rect.move_ip(self.speed,0)

        if(Trex.rect.colliderect(self.rect)):
            Trex.dead()
        
        if(self.rect.right < 0):
            self.rect.left = width*4
            self.currSprite = randint(0,2)
            self.rect.size = self.sprites[self.currSprite].get_rect().size
            self.speed -= 0.1
    def draw(self):
        global screen
        screen.blit(self.sprites[self.currSprite],self.rect)


def image_load(path,size = None):
    new_surface = pygame.image.load(path)
    if size!=None :
        new_surface = pygame.transform.scale(new_surface,size)
    return new_surface

def setup():
    global clouds,cactus
    clouds = [Clouds("cloud.png",width,50),
        Clouds("cloud.png",width+100,150),
        Clouds("cloud.png",width+600,200),
        Clouds("cloud.png",width-400,70),
        Clouds("cloud.png",width-50,111)] 


    cactus = [Cactus(width),
          Cactus(width+600),
          Cactus(width+1100),
          Cactus(width+1600),
          Cactus(width+2300)]

def update():
    global Trex,clouds,cactus
    Trex.update()
    
    for c in clouds:
        c.update()
    for c in cactus:
        c.update()
    
def draw():
    global screen,Trex,cactus,clouds,gameOver,buttonGameOver
    screen.fill((100,100,100))
    screen.fill((180,180,180),pygame.Rect(0,260,width,100))

    for c in clouds:
        c.draw()

    for c in cactus:
        c.draw()
    
    Trex.draw()

    if(Trex.isDead()):
        goImg = gameOverImg.get_rect()
        goImg.center = (width/2,height/2)
        screen.blit(gameOverImg,goImg)
        goImg.center = (553,height/2+40)
        screen.blit(buttonGameOver,goImg)

    pygame.display.flip()

#global variabals 
winSize = width,height = 800,360
screen = pygame.display.set_mode(winSize,vsync=1)
Run = False
gameOverImg = image_load("gameover.png")
buttonGameOver = image_load("button.png")

Trex = Dino() 

clouds = None
cactus = None



setup()

while(not Run):

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_SPACE]:
            Trex.jumpRex()
        
    if(Trex.isDead()):
        pygame.event.clear()
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_r]:
            Trex = Dino()
            setup()
    else:
        update()

    draw()

    pygame.time.Clock().tick(120)
