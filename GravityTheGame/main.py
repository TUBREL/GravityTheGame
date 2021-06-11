import pygame
import math
import os
import random
import importlib
from GameData import Gravitygamephysics as Phys  #- gravity code needs made into class structure

xres = 1280
yres = 720
planetcolours = tuple(["blue","green","orange","pink","purple"])


cwd = os.getcwd()
print(cwd)
done = False
levelscore = 0
class map():
    def __init__(self):
        self.background = pygame.image.load(cwd+"\Graphics\Background\Background_fullscreen.png")
        self.bg = pygame.transform.scale(self.background, [xres, yres])
        self.font = pygame.font.Font('freesansbold.ttf', 32)
    def graphics(self):
        screen.blit(self.bg,(0,0))

    def textscreen(self):
        text = self.font.render("Score :" + str(levelscore) + "               Level :" + str(Level) + "                 Lives :" + str(Lives), False,(255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (xres / 2, 20)
        screen.blit(text, textRect)
    def menu(self):
        self.titled = self.font.render("Gravity, The Game", False,(255, 255, 255))
        self.titledRect = self.titled.get_rect()
        self.titledRect.center = (xres / 2, (yres / 2)-80)
        screen.blit(self.titled, self.titledRect)
    def endscreen(self):
        screen.blit(self.bg, (0, 0))
        end = self.font.render("Your Final Score :"+str(levelscore), False,(255, 255, 255))
        textRect = end.get_rect()
        textRect.center = (xres /2, (yres/2)-50)
        screen.blit(end, textRect)
    def levelselect(self):
        self.levels = open(cwd+"\GameData\Levels.dat","r+")
        self.leveldata = []
        self.gamedata = []
        self.i = 0
        for line in self.levels :
            self.lone = line.rstrip()
            self.sploot = self.lone.split(" -- ")
            self.leveldata = []
            for self.n in self.sploot :
                print(self.n)
                self.raw = self.n.split(",")
                self.leveldata.append(self.raw)
            self.gamedata.append(self.leveldata)
            self.i += 1
        return self.gamedata,self.i
    def update(self):
        clock.tick(60)  # 60 fps
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
class buttons(pygame.sprite.Sprite):
    def __init__(self,text,Rectcenter):
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.rectsize = [200,100]
        self.image = pygame.Surface(self.rectsize).convert()
        pygame.draw.rect(self.image, [255, 255, 255], [0, 0,200,100],6,1)
        self.buttontext = self.font.render(text, False, (255, 255, 255)).convert()
        self.buttontextRect = self.buttontext.get_rect()
        self.buttontextRect.center = Rectcenter
        self.rect = self.image.get_rect()
        self.rect.center = Rectcenter
        self.buttontext.set_alpha(200)
    def update(self,mousepoint):
        screen.blit(self.image, self.rect)
        screen.blit(self.buttontext, self.buttontextRect)
        if self.rect.collidepoint(mousepoint):
            return pygame.mouse.get_pressed()[0]
        return False




class projectile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(cwd+"\Graphics\Rocket.png")
        self.image = pygame.transform.scale(self.image, [40, 25]).convert()
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect() #hitbox
        self.collision = False
        self.x = 50
        self.y = yres/2
        self.angle = 0

    def draw(self):
        self.rect.center = (self.x, self.y)
        self.rotated = pygame.transform.rotate(self.image, -self.angle)
        screen.blit(self.rotated, (self.rect.center))
    def move(self):
        if launched ==True :
            coord = Phys.gravity.position(Gamedata[Level-1])
            self.angle = math.degrees(math.atan(coord[3] / coord[2]))
        else :
            coord = [50,yres/2,0,0]
            self.angle = 0
            self.collision = False
        self.x = coord[0]
        self.y = coord[1]
        if pygame.sprite.spritecollide(rocket, planet_list, False, pygame.sprite.collide_circle_ratio(0.5)):
            print("Hit something")
            self.collision = True
        if launched == False :
            self.collision = False
        return self.x,self.y,coord[2],coord[3],self.collision
    def mousecheck(self):
        self.mousepoint = pygame.mouse.get_pos()
        self.mousecollision = self.rect.collidepoint(self.mousepoint)
        if self.mousecollision == True and pygame.mouse.get_pressed()[0]:
            return True
        else :
            return False

class launcharrow(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface([100,60]).convert()
        self.image.set_colorkey([0,0,0])
        pygame.draw.polygon(self.image,[255,0,0],[[100,30],[60,0],[60,60]],0)
        pygame.draw.rect(self.image,[255,0,0],[0,15,80,30]) #(screen,colour,[topleftcoord,w,h])
        self.rect = self.image.get_rect()
        self.x = 70
        self.y = yres/2
    def draw(self):
        mousepoint = pygame.mouse.get_pos()
        self.numerator = (mousepoint[1]-coord[1])
        self.denominator = (mousepoint[0]-coord[0])
        self.magnitude = math.sqrt(self.numerator**2+self.denominator**2)
        if self.magnitude > 150 :
            self.magnitude = 150
        self.newimage = pygame.transform.scale(self.image, [int(self.magnitude), 15])
        if self.denominator > 0:
            self.angle = -math.degrees(math.atan(self.numerator/self.denominator))
        elif self.denominator < 0 :
            self.angle = math.degrees(math.atan(self.numerator/self.denominator))
        else :
            self.angle = 0
        #print(self.angle)
        self.rotated = pygame.transform.rotate(self.newimage,self.angle)
        self.x = 70+(self.magnitude*math.cos(math.radians(self.angle)))
        self.y = ((yres/2))-(self.magnitude*math.sin(math.radians(self.angle)))
        self.rect.center = (self.x, self.y)
        self.rectsize = self.rotated.get_rect().center
        screen.blit(self.rotated, (self.rect.center[0]-self.rectsize[0],self.rect.center[1]-self.rectsize[1]+10))
        return self.magnitude,self.angle
class planet(pygame.sprite.Sprite):
    def __init__(self,planets,n):
        self.planets = planets
        pygame.sprite.Sprite.__init__(self)
        self.r = int(planets[n][2])
        self.planetnumber = str(random.randint(1,5))
        self.planetcolour = planetcolours[random.randint(0,4)]
        print("Loaded planet",self.planetnumber,self.planetcolour)
        self.image = pygame.image.load(cwd+"\Graphics\planet"+self.planetnumber+"\planet"+self.planetnumber+"_"+self.planetcolour+".png")
        self.image = pygame.transform.scale(self.image, [2*self.r,2*self.r]).convert()
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
    def draw(self,n):
        self.x = int(self.planets[n][0])
        self.y = int(self.planets[n][1])
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, (self.rect))

class wormhole(pygame.sprite.Sprite):
    def __init__(self,radius):
        pygame.sprite.Sprite.__init__(self)
        self.r = radius
        self.image = pygame.image.load(cwd+"\Graphics\Blackhole.png")
        self.image = pygame.transform.scale(self.image, [2*self.r,2*self.r]).convert()
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
    def draw(self):
        self.x = xres
        self.y = yres/2
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, (self.rect))
pygame.init()
screen = pygame.display.set_mode((xres, yres), pygame.SCALED,vsync=1)
print(xres,"x",yres)
pygame.display.set_caption("GravityTheGame")
clock = pygame.time.Clock()
M = map()
rocket = projectile()
arrow = launcharrow()
blackholeradius = 200
blackhole = wormhole(blackholeradius)

Gamedata,Numberoflevels = M.levelselect()
k = 0
while k <= Numberoflevels-1:
    del Gamedata[k][0]
    k += 1
planet_list = pygame.sprite.Group()
GameStart = True
M.graphics()
GameOver = False
loaded = False
Level = 1
Lives = 5
Menu = True
Brexit = False
Gameover = False

APlanet = planet(Gamedata[Level-1], 0)
planet_list.add(APlanet)
while Brexit == False:
    while Menu == True:
        if loaded == False :
            StartButton = buttons("Start",[xres/2,yres/2])
            BrexitButton = buttons("Exit",[xres/2,(yres/2)+110])
        mousepoint = pygame.mouse.get_pos()
        M.graphics()
        M.menu()
        Game = StartButton.update(mousepoint)
        Brexit = BrexitButton.update(mousepoint)
        M.update()
        if Game == True or Brexit == True:
            Menu = False
            loaded = False
    while Game == True:
        if GameStart == True :
            print("Executed")
            coord = [20, yres / 2,0,0,False]
            print(loaded,Level)
            if loaded == False:
                planet_list.empty()
                print("Emptied groups")
            launched = False
            n = 0
            while n <= len(Gamedata[Level-1])-1:
                APlanet = planet(Gamedata[Level-1], n)
                planet_list.add(APlanet)
                n += 1
                loaded = True
            velocity = 0
            startlaunch = False
            GameStart = False


        if done == True :
            launched = False
            done = False
            coord = rocket.move()
            print(coord)
            startlaunch = False

        #drawing
        M.graphics()
        blackhole.draw()
        rocket.draw()
        if startlaunch == False:
            startlaunch = rocket.mousecheck()
            launched = False
        if startlaunch == True and launched == False :
            if pygame.mouse.get_pressed()[0]:
                launch = arrow.draw()
            else:
                launched = True
                Phys.gravity.initial(xres,yres,launch[0],launch[1])
        n = 0

        for x in planet_list:
            x.draw(n)
            n += 1
        M.textscreen()
        M.update()

        if coord[0] >= xres and abs((yres/2)-coord[1]) < blackholeradius:
            levelscore += int(abs((yres/2)-coord[1]))
            print("score!")
            GameStart = True
            done = True
            loaded = False
            Level += 1
        elif coord[0] < 0 or coord[1] < 0 or coord[0] > xres or coord[1] > yres :
            done = True
            print("Sprite has left the chat")
            Lives -= 1
            print("Lives :",Lives)
        elif launched == True :
            coord = rocket.move()
            if coord[4] == True :
                done = True
                Lives -= 1
        if Lives <= 0 or Level > Numberoflevels:
            print("Out of lives")
            Lives = 5
            done = True
            Gameover = True
            loaded = False
            Game = False
    while Gameover == True :
        if loaded == False :
            RetryButton = buttons("Retry",[(xres/2)-110,(yres/2)+50])
            EndExitButton = buttons("Exit",[(xres/2)+110,(yres/2)+50])
            loaded = True
        M.graphics()
        M.endscreen()
        mousepoint = pygame.mouse.get_pos()
        M.endscreen()
        Game = RetryButton.update(mousepoint)
        Brexit = EndExitButton.update(mousepoint)

        if Game == True :
            Level = 1
            GameStart = True


        if Brexit == True or Game == True :
            Gameover = False
            loaded = False
        M.update()
pygame.quit()
