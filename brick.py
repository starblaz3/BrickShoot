from colorama import Fore

from powerup import Powerup
class Brick:
    def __init__(self,r,c):
        self.r=r
        self.c=c
        self.size=8                
        self.spritex="▇"    
        self.colors={
            1:Fore.BLUE,
            2:Fore.GREEN,
            3:Fore.YELLOW,
            10:Fore.RED
        }
    def brickCollision(self,window,a,b):
        for i, ball in enumerate(window.sprites):
            if type(ball).__name__ == "Ball":
                # top or bottom
                tempr=ball.vr
                tempc=ball.vc
                if ball.c >= self.c and ball.c <= self.c+self.size:
                    if (ball.r > self.r-2 or ball.r+ball.vr > self.r-2) and (ball.r < self.r):
                        tempr=ball.vr
                        ball.vr = -ball.vr                    
                        if self.material == "r":
                            if self.state==0:
                                self.state=1                            
                        if self.material != "u":
                            self.strength = self.strength-1
                    elif (ball.r < self.r+2 or ball.r+ball.vr < self.r+2) and (ball.r > self.r):
                        tempr=ball.vr
                        ball.vr = -ball.vr
                        if self.material == "r":
                            if self.state==0:
                                self.state=1      
                        if self.material != "u":
                            self.strength = self.strength-1
                # right or left
                if ball.r == self.r:
                    if (ball.c < self.c+self.size+1 or ball.c+ball.vc < self.c+self.size+1) and (ball.c > self.c+self.size):
                        tempc=ball.vc
                        ball.vc = -ball.vc
                        if self.material == "r":
                            if self.state==0:
                                self.state=1      
                        if self.material != "u":
                            self.strength = self.strength-1
                    elif (ball.c > self.c-2 or ball.c+ball.vc > self.c-2) and (ball.c < self.c):
                        tempc=ball.vc
                        ball.vc = -ball.vc
                        if self.material == "r":
                            if self.state==0:
                                self.state=1      
                        if self.material != "u":
                            self.strength = self.strength-1
                if self.strength <= 0:
                    powerup1 = Powerup(self.r+0, self.c+1,tempr,tempc)
                    window.score+=1
                    window.addSprite(powerup1)
                    window.removeBrick(self)
                    return True            
class Weak(Brick):
    def __init__(self, r, c):
        super().__init__(r, c)        
        self.material="b"
        self.strength=1
        self.color=self.colors[self.strength]
class Middle(Brick):
    def __init__(self, r, c):
        super().__init__(r, c)        
        self.material="b"
        self.strength=2
        self.color=self.colors[self.strength]
class Strong(Brick):
    def __init__(self, r, c):
        super().__init__(r, c)        
        self.material="b"
        self.strength=3
        self.color=self.colors[self.strength]
class Rainbow(Brick):
    def __init__(self, r, c):
        super().__init__(r, c)        
        self.material="r"
        self.strength=3
        self.state=0
        self.color=self.colors[self.strength]        
class Unbreakable(Brick):
    def __init__(self, r, c):
        super().__init__(r, c)                
        self.material="u"
        self.strength=10
        self.color=self.colors[self.strength]