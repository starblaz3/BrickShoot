from colorama import Fore,Back,Style
import os

class Paddle:
    def __init__(self,time,color=Fore.GREEN,size=15):
        currentSize=os.get_terminal_size()
        self.r=int(3*(currentSize.lines/4))-6
        self.c=int((int(currentSize.columns/2)-size)/2)
        self.symbol="▇"
        self.color=color
        self.size=size  
        self.material="normal"  
        self.time=time          
    def move(self,dir):
        self.c=self.c+dir





