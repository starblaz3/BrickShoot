from powerup import Powerup
class Bullet:
    def __init__(self,r,c):
        self.r=r
        self.c=c
        self.vr=-1
        self.spritex="|"
    def brickCollision(self,window):
        i=0
        while i<len(window.bricks):
            brick=window.bricks[i]
            if (brick.r>=self.r or brick.r>=self.r+self.vr) and (brick.c<=self.c and (brick.c+brick.size)>=self.c):
                if brick.material == "r":
                    if brick.state==0:
                        brick.state=1                            
                if brick.material != "u":
                    brick.strength = brick.strength-1
                self.spritex=""
                self.vr=0
                if brick.strength <= 0:
                    powerup1 = Powerup(brick.r+1, brick.c,1,0)
                    window.score+=1
                    window.addSprite(powerup1)
                    window.removeBrick(brick)                
            i+=1
    def topCollision(self,window):
        if self.r<2 or (self.r+self.vr)<2:
            self.spritex=""
            self.vr=0
    def move(self,window):
        self.brickCollision(window)
        self.topCollision(window)
        self.r=self.r+self.vr
