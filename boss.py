# u have to render the boss, bricks and bombs like sprites in window
from colorama import Fore
class Boss:
    def __init__(self,r,c):
        self.r=r
        self.c=c
        self.bombs=[]
        self.bricks=[]
        self.lives=15
        self.size=10
        self.bricksLeft=2
        self.spritex="▇"
        self.color=Fore.CYAN
        