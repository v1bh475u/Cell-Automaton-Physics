import pygame
import random
import numpy as np
from HashTable import HashTable
import threading
# Setting up colors
white = (255, 255, 255)
black = (0, 0, 0)
sand_color = (209, 175, 25)
water_color = (39, 165, 196)
fire_color = (255, 117, 0)
wood_color = (112, 40, 9)
steam_color = (242, 233, 233)
lava_color = (237, 76, 31)
rock_color = (125, 109, 97)
oil_color=(173, 168, 142)
# Initializing pygame
pygame.init()
W, H = 400, 400
WIN = pygame.display.set_mode((W, H))
pygame.display.set_caption('Simulation')

            
def vary_color(color):
    if color == black:
        return black
    r, g, b = color
    # Varying each RGB component
    new_r = r
    new_g = min(max(g + random.randint(-50, 0), 0), 255)
    new_b = min(max(b + random.randint(-20, 20), 0), 255)
    return (new_r, new_g, new_b)  # Returning the modified color tuple


density=dict() 
density['sand']=5
density['water']=4
density['fire']=1
density['wood']=10
density['steam']=0
density['lava']=6
density['void']=1
density['rock']=10
density['oil'] = 3


class Cell:
    def __init__(self,x,y,type):
        self.dirty_flag =True
        self.type = type
        self.color = vary_color(color_mapper(type))
        self.lifetime=0
        self.lastvel= 1 if random.random()%2==1 else -1
        self.density=density[type]
        self.x=x
        self.y=y

def color_mapper(type):
    if type=='void':
        return black
    if type == 'sand':
        return sand_color
    elif type == 'water':
        return water_color
    elif type=='fire':
        return fire_color
    elif type == 'steam':
        return steam_color
    elif type == 'lava':
        return lava_color
    elif type == 'wood':
        return wood_color
    elif type == 'rock':
        return rock_color
    elif type == 'oil':
        return oil_color


class Grid:
    radius = 3
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cells_size = cell_size
        self.cells = HashTable()
        
    def insertCell(self, x, y, type):
        self.cells.set((x, y), Cell(x,y,type))
        
    def delCell(self, x, y):
        self.cells.delete((x, y))
    
    
    def clear(self):
        self.cells = [[Cell('void',black)] * self.width for _ in range(self.height)]
    
    def set(self, x, y, type,lifetime=0):
        # self.cells[y][x] = Cell(type,vary_color(color_mapper(type)),lifetime)
        for y1 in range(y-self.radius,y+self.radius):
            for x1 in range(x-self.radius,x+self.radius):
                self.cells[y1][x1] = Cell(type,vary_color(color_mapper(type)))
        
    def get_cell(self, x, y):
        if self.cells.has((x, y))==False:
            return None
        return self.cells.get((x,y))
    
    def movecell(self,x,y,cell):
        vel=cell.lastvel
        if x>cell.x: vel=1
        elif x<cell.x: vel=-1
        dest=self.get_cell(x,y)
        if dest==None:
            self.insertCell(x,y,cell.type)
            self.delCell(cell.x,cell.y)
        cell.lastvel=vel
        if dest: dest.lastvel=-vel
        
            
    def draw_grid(self):
        for i in self.cells.hashes:
            cell = self.cells.hashes[i]
            pygame.draw.rect(WIN, cell.color, pygame.Rect(cell.x * self.cells_size, cell.y * self.cells_size, self.cells_size, self.cells_size))

    def handle_mouse_click(self, x, y, type):
        grid_x = x // self.cells_size
        grid_y = y // self.cells_size
        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
            self.insertCell(grid_x, grid_y, type)
    
    def update_oil(self,x,y):
        if (y<self.height) and (x>0) and (x<self.width) and (y>0):
            cell=self.get_cell(x,y)
            below = self.get_cell(x,y+1)
            right = self.get_cell(x+1,y)
            left = self.get_cell(x-1,y)
            if below==None:
                self.movecell(x,y+1,cell)
            elif (left==None) and cell.lastvel==-1:
                self.movecell(x-1,y,cell)
            elif (right==None) and cell.lastvel==1:
                self.movecell(x+1,y,cell)
            
    def update_sand(self,x,y):
        if (y<self.height) and (x>0) and (x<self.width) and (y>0):
            cell=self.get_cell(x,y)
            below = self.get_cell(x,y+1)
            below_right = self.get_cell(x+1,y+1)
            below_left = self.get_cell(x-1,y+1)
            if below==None:
                self.movecell(x,y+1,cell)
            elif below_left==None:
                self.movecell(x-1,y+1,cell)
            elif below_right==None:
                self.movecell(x+1,y+1,cell)
                
    def update_water(self,x,y):
        if (y<self.height) and (x>0) and (x<self.width) and (y>0):
            cell=self.get_cell(x,y)
            below = self.get_cell(x,y+1)
            right = self.get_cell(x+1,y)
            left = self.get_cell(x-1,y)
            if below==None or below.type=='oil':
                self.movecell(x,y+1,cell)
            elif (left==None or left.type=='oil') and cell.lastvel==-1:
                self.movecell(x-1,y,cell)
            elif (right==None or right.type=='oil') and cell.lastvel==1:
                self.movecell(x+1,y,cell)
                
    def update_steam(self,x,y):
        if (y<self.height) and (x>0) and (x<self.width) and (y>0):
            if self.get_cell(x,y).lifetime>=50:
                self.delCell(x,y)
            else:
                cell=self.get_cell(x,y)
                fireside=cell.lastvel
                secside=-fireside
                moves=[(x+fireside,y-1),(x+secside,y-1),(x,y-1)]
                for move in moves:
                    dest=self.get_cell(move[0],move[1])
                    if move[0]<0 or move[0]>=self.width or move[1]<0 or move[1]>=self.height:
                        continue
                    if dest==None:
                        self.movecell(move[0],move[1],cell)
                        break
                
    def update_fire(self,x,y):
        if (y<self.height) and (x>0) and (x<self.width) and (y>0):
            cell=self.get_cell(x,y)
            if cell.lifetime>=20:
                cell.type='steam'
                cell.lifetime=0
                return
            fireside=cell.lastvel
            secside=-fireside
            moves=[(x+fireside,y-1),(x+secside,y-1),(x,y-1),(x+1,y),(x-1,y),(x,y+1),(x+fireside,y+1),(x+secside,y+1)]
            random.shuffle(moves)
            for move in moves:
                dest=self.get_cell(move[0],move[1])
                if move[0]<0 or move[0]>=self.width or move[1]<0 or move[1]>=self.height:
                    continue
                if dest:
                    if dest.type=='wood' or dest.type=='oil':
                        self.set(move[0],move[1],'fire')
                    elif dest.type=='water':
                        self.set(move[0],move[1],'steam')
                        self.delCell(x,y)
                else:
                    self.movecell(move[0],move[1],cell)
                    break      

    def update_lava(self,x,y):
        if (y<self.height) and (x>0) and (x<self.width) and (y>0):
            cell=self.get_cell(x,y)
            if cell.lifetime >= 500:
                cell.type = 'rock'
                cell.lifetime = 0
            else:
                below = self.get_cell(x,y+1)
                right = self.get_cell(x+1,y)
                left = self.get_cell(x-1,y)    
                hb_coords = [(x, y-1), (x+1, y-1), (x+1, y-1), (x-1, y), (x+1, y), (x,y+1), (x-1, y+1), (x+1, y+1)]
                for i in range(len(hb_coords)):
                    dest=self.get_cell(hb_coords[i][0],hb_coords[i][1])
                    if dest:
                        if dest[i].type == 'water':
                            self.set(hb_coords[i][0],hb_coords[i][1], 'rock')
                            self.set(x,y, 'steam')
                        elif dest[i].type == 'wood':
                            self.set(hb_coords[i][0],hb_coords[i][1], 'fire')
                        elif dest[i].type == 'oil':
                            self.set(hb_coords[i][0],hb_coords[i][1], 'fire')
                    else:
                        if below==None:
                            self.movecell(x,y+1,cell)
                        elif left==None and cell.lastvel==-1:
                            self.movecell(x-1,y,cell)
                        elif right==None and cell.lastvel==1:
                            self.movecell(x+1,y,cell)
            
    def update_pixel(self,x,y):
        self.cells.get((x,y)).lifetime+=1
        if self.get_cell(x,y).dirty_flag == True:
            if self.get_cell(x,y).type=='sand':
                self.update_sand(x,y)
            elif self.get_cell(x,y).type=='lava':
                self.update_water(x,y)
            elif self.get_cell(x,y).type=='fire':
                self.update_fire(x,y)
            elif self.get_cell(x,y).type== 'steam':
                self.update_steam(x,y)
            elif self.get_cell(x,y).type== 'water':
                self.update_water(x,y)
            elif self.get_cell(x,y).type == 'oil':
                self.update_oil(x,y)
            
                               
    def update_grid(self):
        temp=HashTable()
        for i in self.cells.hashes:
            cell = self.cells.hashes[i]
            temp.set((cell.x,cell.y),Cell(cell.x,cell.y,cell.type))
        for i in temp.hashes:
            cell = self.cells.hashes[i]
            self.update_pixel(cell.x,cell.y)
            cell.dirty_flag = False
    
    def clear_flags(self):
        for i in self.cells.hashes:
            cell = self.cells.hashes[i]
            cell.dirty_flag = True
    def setup(self):
        for y in range(self.height//2,self.height):
            for x in range(0,self.width):
                pygame.draw.rect(WIN, vary_color(rock_color), pygame.Rect(x * self.cells_size, y * self.cells_size, self.cells_size, self.cells_size))
        

def main():
    grid_obj = Grid(H//4,W,W//100)
    run = True
    clock = pygame.time.Clock()
    brush = None
    draw_type = 'fire'
    while run:
        clock.tick(60)
        grid_obj.setup()
        WIN.fill(black)
        grid_obj.draw_grid()
        grid_obj.setup()
        pygame.display.update()
        grid_obj.update_grid()
        grid_obj.clear_flags()
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]: draw_type = 'water'
        if pressed[pygame.K_s]: draw_type = 'sand'
        if pressed[pygame.K_q]: draw_type = 'wood'
        if pressed[pygame.K_f]: draw_type = 'fire'
        if pressed[pygame.K_r]: draw_type = 'steam'
        if pressed[pygame.K_t]: draw_type = 'lava'
        if pressed[pygame.K_o]: draw_type = 'oil'
        if pressed[pygame.K_p]: draw_type = 'rock'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    brush = event.pos
                    grid_obj.handle_mouse_click(brush[0],brush[1],draw_type)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # left button released
                    brush = None
            elif event.type == pygame.MOUSEMOTION:
                if brush: # left button still pressed
                    brush = event.pos
                    grid_obj.handle_mouse_click(brush[0],brush[1],draw_type)
    pygame.quit()

if __name__ == "__main__":
    main()
