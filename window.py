import os
import time
import sys
import tty
import termios
import copy
from colorama import Fore, Back, Style
import datetime
import random

import config
from ball import Ball
from paddle import Paddle
from input import KBHit
from brick import Weak
from brick import Middle
from brick import Rainbow
from brick import Strong
from brick import Unbreakable
from powerup import Powerup
from powerup import Expand
from powerup import Shrink
from bullet import Bullet
from boss import Boss

class Window:
    def __init__(self):
        screen_size = os.get_terminal_size()
        self.keyboard = KBHit()
        self.height = int(3*(screen_size.lines/4)) - 1
        self.width = int(screen_size.columns/2)
        self.sprites = []
        self.paddle = Paddle(0)
        self.paddle.material="grab"
        self.kill = False
        self.bricks = []
        self.dummy = 0
        self.matrix = []
        self.bullets=[]
        self.lives=3
        self.score=0
        self.level=1
        self.levelTime=0
        self.bossActive=0        
        self.k=0
        self.brickTimer=500
        self.spTime=0
        self.debugger="hmm nothing"
    def handle_input(self):
        if self.keyboard.kbhit():
            inp = self.keyboard.getch().lower()
            if inp in config.play_keys:
                if inp == 'a':
                    if self.paddle.c-5 > 3:
                        self.paddle.move(-5)
                if inp == 'd':
                    if self.paddle.c+5 < self.width-self.paddle.size-3:
                        self.paddle.move(5)
        self.keyboard.flush()

    def setScreen(self):        
        self.matrix = [[*[" "] * self.width] for i in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                if j == 0 or j == self.width-1:
                    self.matrix[i][j] = "│"
                if i == 0:
                    if j == 0:
                        self.matrix[i][j] = "▛"
                    elif j == self.width-1:
                        self.matrix[i][j] = "▜"
                    else:
                        self.matrix[i][j] = "▀"
                elif i == self.height-1:
                    if j == 0:
                        self.matrix[i][j] = "▙"
                    elif j == self.width-1:
                        self.matrix[i][j] = "▟"
                    else:
                        self.matrix[i][j] = "▄"

    def addSprite(self, sprite):
        self.sprites.append(sprite)

    def addBrick(self, brick):
        self.bricks.append(brick)
    def addBullet(self,bullet):
        self.bullets.append(bullet)
    def removeBullet(self,bullet):
        self.bullets.remove(bullet)    
    def removeBrick(self, brick):        
        self.bricks.remove(brick)
    # check collision before moving the ball
    def moveBullets(self):
        i=0
        while i<len(self.bullets):
            self.bullets[i].move(self)
            if self.bullets[i].spritex=="" and self.bullets[i].vr==0:
                self.removeBullet(self.bullets[i])
            i+=1
    def assignSprites(self):
        j = 0        
        while j in range(len(self.sprites)):
            sprite = self.sprites[j]
            currentTime = self.frame
            if sprite.spritex == "x" or sprite.status == -1:
                self.sprites.remove(sprite)
                continue
            elif sprite.status == 1:     
                if sprite.spritex == "sp":
                    self.spTime=self.frame          
                if sprite.spritex == "e":
                    expand=Expand(sprite.r,sprite.c,sprite.spritex,self.paddle)
                    expand.powerItUp()
                if sprite.spritex == "s":
                    shrink=Shrink(sprite.r,sprite.c,sprite.spritex,self.paddle)
                    shrink.powerItUp()
                if sprite.spritex == "b":
                    i=0
                    newballs=[]
                    while i<len(self.sprites):
                        ball=self.sprites[i]
                        if type(ball).__name__ == "Ball":
                            r = ball.r
                            c = ball.c
                            ball2 = Ball(r=r, c=c,vr=ball.vr,vc=-ball.vc)                                
                            newballs.append(ball2)                             
                        i+=1
                    self.sprites+=newballs
                if sprite.spritex == "f":
                    for ball in self.sprites:
                        if type(ball).__name__ == "Ball":
                            ball.vr = -2
                            ball.vc = 2
                if sprite.spritex == "p":
                    self.paddle.material = "grab"
                sprite.time = self.frame
                sprite.status = 2
                self.dummy = sprite.time
                j += 1
                continue
            # print(sprite.status)
            if sprite.status == 2:
                if (self.frame-sprite.time) > 100:
                    if sprite.spritex == "sp":
                        self.spTime=0
                    if sprite.spritex == "e":
                        expand=Expand(sprite.r,sprite.c,sprite.spritex,self.paddle)
                        expand.powerItDown()
                    if sprite.spritex == "s":
                        shrink=Shrink(sprite.r,sprite.c,sprite.spritex,self.paddle)
                        shrink.powerItDown()                      
                    if sprite.spritex == "f":
                        for ball in self.sprites:
                            if type(ball).__name__ == "Ball":
                                ball.vc=1
                                ball.vr=-1
                    if sprite.spritex == "p":
                        self.paddle.material="normal"
                    sprite.status = -1
                if sprite.spritex=="sp":
                    if self.frame - sprite.time < 100:
                        diff=self.frame - sprite.time
                        if diff%10==0:
                            bullet=Bullet(self.paddle.r-1,self.paddle.c+int(self.paddle.size/2))
                            self.addBullet(bullet)
                j += 1
                continue                
            self.matrix[sprite.r][sprite.c] = sprite.color +sprite.spritex+Fore.RESET
            j += 1
    def makeLayout(self):
        if(self.level>4):
            return True        
        if(self.level==1):
            brick1 = Weak(5, 5)
            brick3 = Weak(5, self.width-15)
            # brick2 = Rainbow( 20, 30)
            brick2 = Strong( 20, 30)
            window.addBrick(brick1)
            window.addBrick(brick2)
            window.addBrick(brick3)

        if(self.level==2):
            brick1 = Strong(15, 30)
            brick2 = Middle( 20, 30)
            brick3 = Weak( 20, 40)
            brick4 = Unbreakable( 20, 60)        

            window.addBrick(brick1)
            window.addBrick(brick2)
            window.addBrick(brick3)
            window.addBrick(brick4)
        if(self.level==3):
            brick1 = Strong(15, 30)
            brick2 = Middle( 20, 30)
            brick3 = Weak( 20, 40)
            brick4 = Unbreakable( 20, 60)        
            brick5= Strong(25,40)
            brick6= Unbreakable(15,45)
            window.addBrick(brick1)
            window.addBrick(brick2)
            window.addBrick(brick3)
            window.addBrick(brick4)
            window.addBrick(brick5)
            window.addBrick(brick6)
        if(self.level==4):
            brick1 = Unbreakable(15,5)
            brick2 = Unbreakable(15,50)
            window.addBrick(brick1)
            window.addBrick(brick2)
            self.bossActive=1
            self.boss=Boss(5,self.paddle.c)
    def checkLevel(self):
        i=0
        while i< len(self.bricks):
            if type(self.bricks[i]).__name__ != "Unbreakable" or self.bossActive==1:
                return
            i+=1        
        self.level+=1            
        j=0
        self.paddle.material="grab"
        self.levelTime=self.frame
        self.paddle.time=self.frame
        while j<len(self.sprites):
            if type(self.sprites[j]).__name__ != "Ball":
                if self.sprites[j].spritex=="sp":
                    self.bullets.clear()
                    self.sprites[j].time=0
                self.sprites.remove(self.sprites[j])
            j+=1         
        self.bricks.clear()   
        self.makeLayout()        
    def moveBrickDown(self):
        if self.frame - self.levelTime > self.brickTimer:            
            i=0            
            while i<len(self.bricks):
                if self.bricks[i].r+1>=self.height-1:                
                    if len(self.bricks)==1:
                        self.kill=True                        
                        return
                    self.removeBrick(self.bricks[i])
                else:                                                                              
                    self.bricks[i].r=self.bricks[i].r+1 
                i+=1   
    def rainbowBrick(self):
        i=0
        while i<len(self.bricks):
            if self.bricks[i].material=="r" and self.bricks[i].state==0:
                self.bricks[i].strength=random.randint(1,3)
                self.bricks[i].color=self.bricks[i].colors[self.bricks[i].strength]
            i+=1
    def render(self):
        self.frame = 0
        os.system("xset r rate 1") 
        self.kill=self.makeLayout() 
        self.level=3       
        while True:
            begin = time.monotonic()
            self.frame += 1
            os.system("clear")
            if self.spTime!=0:            
                print("time passed: "+str(self.frame) +" "+ "Score: "+str(self.score) +" "+ "lives: "+str(self.lives) + " " + "level: " + str(self.level)+" "+"time left shooting: "+str(100-(self.frame-self.spTime)))                
            else:
                print("time passed: "+str(self.frame) +" "+ "Score: "+str(self.score) +" "+ "lives: "+str(self.lives) + " " + "level: " + str(self.level))            
            self.setScreen()
            self.handle_input()
            if(self.bossActive==1):
                # render the bombs and bossbricks here
                for i in range(self.boss.size):
                    self.matrix[self.boss.r][self.boss.c+i]=self.boss.color+self.boss.spritex+Fore.RESET                            
            for brick in self.bricks:
                for i in range(brick.size):
                    self.matrix[brick.r][brick.c+i] = brick.colors[brick.strength]+brick.spritex+Fore.RESET
            self.assignSprites() 
            self.moveBullets() 
            for bullet in self.bullets:
                self.matrix[bullet.r][bullet.c]=bullet.spritex                      
            for i in range(self.paddle.size):
                self.matrix[self.paddle.r][self.paddle.c +i] = self.paddle.color+self.paddle.symbol+Fore.RESET
            if self.spTime!=0:
                self.matrix[self.paddle.r][self.paddle.c]=Fore.RED+self.paddle.symbol+Fore.RESET
                self.matrix[self.paddle.r][self.paddle.c+self.paddle.size-1]=Fore.RED+self.paddle.symbol+Fore.RESET
            for i in range(self.height):
                for j in range(self.width):
                    pixel = self.matrix[i][j]
                    # if i==self.height-2 and j==4:
                    #     pixel=time.monotonic()
                    print(pixel, end="", sep="")
                print()
            # for brick in self.bricks:
            #     self.brickCollision(brick,brick.r,brick.c)
            i = 0
            while i < len(self.bricks):
                if self.bricks[i].brickCollision(self, self.bricks[i].r, self.bricks[i].c):
                    pass
                else:
                    i += 1
            for sprite in self.sprites:
                sprite.move(self, self.paddle)            
            self.checkLevel()
            self.rainbowBrick()
            while time.monotonic() - begin < config.frame_rate:
                pass
            if self.keyboard.kbhit():
                if self.keyboard.getch().lower() == 'x':
                    os.system("xset r rate 660 25")
                    break
            if self.kill==True:
                os.system("clear") 
                print(self.debugger)               
                os.system("xset r rate 660 25")
                break
            if self.keyboard.kbhit():
                if self.keyboard.getch().lower() == 'w':
                    self.paddle.material = "normal"
            if self.lives==0:
                os.system("clear")
                print("lmfao i succ at making games sorry!!")
                os.system("xset r rate 660 25")
                break


if __name__ == "__main__":
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    window = Window()    
    ball1 = Ball(10, 10, 1, 1, color=Fore.BLUE)
    # ball2=Ball(8,12,1,1,color=Fore.RED)
    # ball3=Ball(10,0,1,1,color=Fore.YELLOW)
    window.addSprite(ball1)    
    # window.addSprite(ball2)
    # window.addSprite(ball3)
    window.render()
