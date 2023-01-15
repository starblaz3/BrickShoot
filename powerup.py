import random
from colorama import Fore
class Powerup:
    def __init__(self,r,c,vr,vc):
        self.powers=["e","s","b","f","p","sp"]
        self.spritex="sp"
        # self.powers[random.randint(0,5)]
        self.color=Fore.RED
        self.r=r
        self.c=c
        self.vr=vr
        self.vc=vc
        self.counter=0
        self.va=8
        self.status=0
        self.time=-1        
        # remove the sprite instance in list before assigning to pixel
    def paddleCollision(self,paddle):
        if (self.c >= paddle.c) and (self.c <= (paddle.c+paddle.size)) :
            if self.r >= paddle.r or self.r+self.vr >= paddle.r:
                self.status=1
    def move(self,window,paddle):
        if self.status==0:
            self.paddleCollision(paddle)
            #top 
            if (self.r < 2) or ((self.r + self.vr) < 2):
                self.vr=-self.vr
            #bottom
            if (self.r > (window.height-2)) or ((self.r+self.vr)>window.height-2):
                self.vr=0
                self.spritex="x"            
            #right
            if (self.c > window.width-1) or ((self.c + self.vc) > window.width):
                self.vc=-self.vc                
            #left               
            if (self.c < 1) or ((self.c + self.vc) < 1):
                self.vc=-self.vc
            else:
                self.r=self.r+self.vr
                self.c=self.c+self.vc
                self.counter+=1
                if (self.counter % self.va)==0:
                    self.vr+=1
    def powerItUp(self,symbol):
        self.spritex=symbol
class Expand(Powerup):
    def __init__(self, r, c,symbol,paddle):
        super().__init__(r, c,vr,vc)
        self.paddle=paddle
        self.spritex=symbol
    def powerItUp(self):        
        self.paddle.c = self.paddle.c-5
        self.paddle.size += 10
    def powerItDown(self):
        self.paddle.c = self.paddle.c+5
        self.paddle.size = self.paddle.size-10
class Shrink(Powerup):
    def __init__(self, r, c,symbol,paddle):
        super().__init__(r, c,vr,vc)
        self.paddle=paddle
        self.spritex=symbol
    def powerItUp(self):     
        self.paddle.c = self.paddle.c+2
        self.paddle.size = self.paddle.size-4
    def powerItDown(self):
        self.paddle.c = self.paddle.c-2
        self.paddle.size = self.paddle.size+4 

    