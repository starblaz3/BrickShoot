from colorama import Fore,Back,Style

class Ball:
    def __init__(self,r=0,c=0,vr=1,vc=1,color=Fore.BLUE):
        self.r=r
        self.c=c
        self.vr=vr
        self.vc=vc
        self.color=color
        self.spritex="⬤"
        self.status=0
    def available(self,height,width):
        return {
            "left":self.c>1 or self.c+self.vc>1,
            "right":self.c < width-2 or self.c+self.vc<width-2,
            "up":self.r>1 or self.r+self.vr>1,
            "down":self.r < height -2 or self.r+self.vr<height-2,
        }
    def deflect(self,available,window):
        # if not available["left"]:
        #     self.vc=1
        # if not available["right"]:
        #     self.vc=-1
        # if not available["up"]:
        #     self.vr=1
        # if not available["down"]:
        #     self.vr=-1
        #     # window.kill=True
        # #top 
        if self.r < 2 or self.r+self.vr <2:
            self.vr=1
        #bottom
        if self.r > window.height-2 or self.r+self.vr>window.height-2:
            window.lives=window.lives-1
            for sprite in window.sprites:
                if type(sprite).__name__=="Ball":
                    sprite.r=window.paddle.r-1
                    sprite.c=window.paddle.c+int(window.paddle.size/2)
        #right
        if self.c > window.width -2 or self.c +self.vc > window.width -2:
            self.vc=-1
        #left 
        if self.c < 2 or self.c+self.vc < 2:
            self.vc=1
    def paddleCollision(self,paddle,window): 
        if window.frame - paddle.time < 50:
            if paddle.material=="grab":
                self.c=paddle.c+int(paddle.size/2)
                self.r=paddle.r-1    
        if self.r >= paddle.r-3 and self.c > paddle.c and self.c < (paddle.c+paddle.size):            
            if self.c < (paddle.c + int(paddle.size/4)):
                if paddle.material=="grab":
                    self.c=paddle.c+int(paddle.size/2)
                    self.r=paddle.r-1
                self.vc=-4
                self.vr=-1                
                window.moveBrickDown()
            elif self.c < (paddle.c + int(paddle.size/2)):
                if paddle.material=="grab":
                    self.c=paddle.c+int(paddle.size/2)
                    self.r=paddle.r-1
                self.vc=-1
                self.vr=-1                
                window.moveBrickDown()
            elif self.c < (paddle.c + 3*int(paddle.size/4)):
                if paddle.material=="grab":
                    self.c=paddle.c+int(paddle.size/2)
                    self.r=paddle.r-1
                self.vc=1
                self.vr=-1                
                window.moveBrickDown()                
            else :
                if paddle.material=="grab":
                    self.c=paddle.c+int(paddle.size/2)
                    self.r=paddle.r-1
                self.vc=4
                self.vr=-1
                window.moveBrickDown()
    def move(self,window,paddle):
        self.deflect(self.available(window.height,window.width),window)
        self.paddleCollision(paddle,window)
        self.r+=self.vr
        self.c+=self.vc
    def draw(self):
        print(self.color + self.spritex + self.reset)