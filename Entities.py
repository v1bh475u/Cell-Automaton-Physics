import pygame
import math
import numpy as np
from abc import abstractmethod
# from button import Button
# from physics import particle
from vector import Vector
from random import randint


#setting up colors
red = (235, 64, 52)
white = (255, 255, 255)
green = (18,204,25)
blue = (66,135,245)

#initializing pygame
pygame.init()
W,H = 400,400
WIN = pygame.display.set_mode((W,H))
pygame.display.set_caption('Simulation')

class grid:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.values = [0]*(self.width*self.height)
    
    def clear(self):
        self.values = [0]*(self.width*self.height)
    
    def set(self,x,y,color):
        self.values[y* self.width+x] = color
    
    def swap(self,a,b):
        temp = self.values[a]
        self.values[a]=self.values[b]
        self.values[b]=temp

    def isEmpty(self,index):
        return self.values[index] ==0
    
    def drawgrid(self):
        for y in range(self.height):
            for x in range(self.width):
                color = (255, 255, 255) if self.values[y* self.width+x]==1 else (0, 0, 0)
                pygame.draw.rect(WIN, color, (x * 40, y * 40, 40, 40))
class Entity:
    health = 100
    def __init__(self,x,y,type,dir):
        self.x = x
        self.y = y
        self.color = (255,255,255)
        self.width = 40
        self.height = 40
        self.type=type
        self.dir=dir
    @abstractmethod
    def move(self):
        pass
    def attack(self,attack_type, attack_range, damage_per_sec):

        self.dps = damage_per_sec
        self.attack_range = attack_range
        #propagate(self.x+self.width/2,self.dir,attack_range,attack_type, damage_per_sec)

class Player(Entity):
    def __init__(self,x,y,type,dir):
        super().__init__(x,y,type,dir)
        self.color = (0,255,0)
        self.type = 4
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= 1
        if keys[pygame.K_RIGHT]:
            self.x += 1
        if keys[pygame.K_UP]:
            self.y -= 1
        if keys[pygame.K_DOWN]:
            self.y += 1
    def PlayerAttack(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_Z]:
            self.attack(0)#fire
        elif keys[pygame.K_X]:
            self.attack(1)#water
        elif keys[pygame.K_C]:
            self.attack(2)#sand

class Enemy(Entity):
    def __init__(self,x,y,type,dir, move_range, vision_range, damage_per_sec):
        super().__init__(x,y,type,dir)
        self.damage_per_sec = damage_per_sec
        
        self.color = (255,0,0)
        self.move_range = move_range
        self.attack_range = vision_range
        

    def move(self, other):
        mov =0        
        while True:
            if abs(self.x - other.x) <= self.attack_range/2:
                if self.x-other.x > 0:
                    self.dir = -1
                    self.Attack()
                else:
                    self.dir = 1

                    self.Attack()
            else:
                if mov<self.move_range/2 and self.dir == 1:
                    self.x += 1
                    mov += 1
                elif abs(mov) == self.move_range/2 :
                    self.dir = -(self.dir)
                elif abs(mov)<self.move_range/2 and self.dir == -1:
                    self.x -= 1
                    mov -= 1
            
            

        

    def Attack(self):
        self.attack(self.type,self.attack_range, self.damage_per_sec)
    
    
def main():
    gridd = grid(10,10)
    run = True
    clock = pygame.time.Clock()

    while run:
        
        
        clock.tick(60)
        WIN.fill((0, 0, 0))
        # drawGrid()
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    pygame.quit()

main()