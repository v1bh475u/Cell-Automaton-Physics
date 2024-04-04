import pygame
import random
import math
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
W, H = 1200,600
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
    def __init__(self,type,color,lifetime=0):
        self.dirty_flag =True
        self.type = type
        self.color = color
        self.lifetime=lifetime
        self.lastvel= 1 if random.random()%2==1 else -1
        self.density=density[type]
    def update_color(self):
        if type=='sand':
            color = vary_color(sand_color)

class Player:
    def __init__(self, grid, x, y, color):
        self.grid = grid
        self.x = x
        self.y = y
        self.color = color

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy


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
    radius = 1
    def __init__(self, width, height, cell_size, chunk_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.chunk_size = chunk_size
        self.num_chunks_x = math.ceil(width / chunk_size)
        self.num_chunks_y = math.ceil(height / chunk_size)
        self.cell = [[Cell('void',black)] * width for _ in range(height)]
        self.dirty_chunks = set()  # Track dirty chunks

    def update_chunk(self, chunk_x, chunk_y,life):
        start_x = chunk_x * self.chunk_size
        start_y = chunk_y * self.chunk_size
        end_x = min(start_x + self.chunk_size, self.width)
        end_y = min(start_y + self.chunk_size, self.height)
        self.dirty_chunks.add((chunk_x,chunk_y,life+1))
        self.dirty_chunks.remove((chunk_x,chunk_y,life))
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                self.update_pixel(x, y)

    def update_dirty_chunks(self):
        dirty_chunks_copy = self.dirty_chunks.copy()  # Create a copy of the dirty chunks set
        for chunk_x, chunk_y,life in dirty_chunks_copy:
            if life>=5:
                self.dirty_chunks.remove((chunk_x,chunk_y,life))
            
            try:
                self.update_chunk(chunk_x, chunk_y,life)
            except:
                continue

    def clear(self):
        self.cell = [[Cell('void',black)] * self.width for _ in range(self.height)]

    def swap(self,a,b):

        self.cell[a[1]][a[0]].dirty_flag = False
        self.cell[b[1]][b[0]].dirty_flag = False
        temp = self.get_cell(*a)
        self.cell[a[1]][a[0]] = self.cell[b[1]][b[0]]
        self.cell[b[1]][b[0]] = temp

        chunk_x1 = a[0] // self.chunk_size
        chunk_y1 = a[1] // self.chunk_size
        chunk_x2 = b[0] // self.chunk_size
        chunk_y2 = b[1] // self.chunk_size
        self.dirty_chunks.add((chunk_x1, chunk_y1,0))
        self.dirty_chunks.add((chunk_x2, chunk_y2,0))
    
    def set(self, x, y, type,lifetime=0):
        # self.cell[y][x] = Cell(type,vary_color(color_mapper(type)),lifetime)
        for y1 in range(y-self.radius,y+self.radius):
            for x1 in range(x-self.radius,x+self.radius):
                self.cell[y1][x1] = Cell(type,vary_color(color_mapper(type)))
        
    def get_cell(self, x, y):
        return self.cell[y][x]

    def draw_grid(self):
        for y in range(self.height):
            for x in range(self.width):
                color = self.cell[y][x].color
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(WIN, color, rect)
                # for time in range(5):
                #     if (x // self.chunk_size, y // self.chunk_size,time) in self.dirty_chunks:
                #         pygame.draw.rect(WIN, white, rect, 1)



    def handle_mouse_click(self, x, y, type):
        grid_x = x // self.cell_size
        grid_y = y // self.cell_size
        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
            self.set(grid_x, grid_y, type)
            chunk_x = grid_x // self.chunk_size
            chunk_y = grid_y // self.chunk_size
            self.dirty_chunks.add((chunk_x, chunk_y,0))
            self.dirty_chunks.add((chunk_x+1, chunk_y,0))
            self.dirty_chunks.add((chunk_x-1, chunk_y,0))
            self.dirty_chunks.add((chunk_x, chunk_y+1,0))
            self.dirty_chunks.add((chunk_x, chunk_y-1,0))
    
    
    def update_oil(self,x,y):
        mylist = [0,1]
        a = random. choice(mylist)
        if (y!=self.height-1) and (x!=0) and (x!=self.width-1):
            below = self.get_cell(x,y+1)
            right = self.get_cell(x+1,y)
            left = self.get_cell(x-1,y)
            if below.type != 'sand' and below.type!='rock' and below.type!='oil':
                self.swap((x,y),(x,y+1))
            elif left.type != 'sand' and left.type!='rock' and left.type!='oil' and a==0:
                self.swap((x,y),(x-1,y))
            elif right.type != 'sand' and right.type!='rock' and right.type!='oil' and a==1:
                self.swap((x,y),(x+1,y))
            
    def update_sand(self,x,y):
        if (y!=self.height-1) and (x!=0) and (x!=self.width-1):
            below = self.get_cell(x,y+1)
            below_right = self.get_cell(x+1,y+1)
            below_left = self.get_cell(x-1,y+1)
            if below.color==black:
                self.swap((x,y),(x,y+1))
            elif below_left.color==black:
                self.swap((x,y),(x-1,y+1))
            elif below_right.color==black:
                self.swap((x,y),(x+1,y+1))
    def update_water(self,x,y):
        mylist = [0,1]
        a = random. choice(mylist)
        if (y!=self.height-1) and (x!=0) and (x!=self.width-1):
            below = self.get_cell(x,y+1)
            right = self.get_cell(x+1,y)
            left = self.get_cell(x-1,y)
            if below.type =='void':
                self.swap((x,y),(x,y+1))
            elif (left.type == 'void' or left.type=='oil') and a==0:
                self.swap((x,y),(x-1,y))
            elif (right.type == 'void' or right.type=='oil') and a==1:
                self.swap((x,y),(x+1,y))
                
    def update_steam(self,x,y):
        mylist = [0,1]
        a = random. choice(mylist)
        if (y!=self.height-1) and (x!=0) and (x!=self.width-1) and(y!=0):
            if self.get_cell(x,y).lifetime>=50:
                self.set(x,y,'void',0)
            else:
                cell=self.get_cell(x,y)
                fireside=cell.lastvel
                secside=-fireside
                moves=[(x+fireside,y-1),(x+secside,y-1),(x,y-1)]
                below = self.get_cell(x,y-1)
                right = self.get_cell(x+1,y)
                left = self.get_cell(x-1,y)
                if below.type == 'void':
                    self.swap((x,y),moves[0])
                elif left.type == 'void' and a==0:
                    self.swap((x,y),(x-1,y))
                elif right.type == 'void' and a==1:
                    self.swap((x,y),(x+1,y))
                
    def update_fire(self,x,y):
        if(y!=self.height-1) and (x!=0) and (x!=self.width-1) and (y!=0):
            cell=self.get_cell(x,y)
            fireside=cell.lastvel
            secside=-fireside
            moves=[(x+fireside,y-1),(x+secside,y-1),(x,y-1)]
            random.shuffle(moves)
            if cell.lifetime>=20:
                self.set(x,y,'steam',0)
            else:
                if self.get_cell(*(moves[0])).type=='void':
                    self.swap((x,y),moves[0])
                moves=[(x+fireside,y-1),(x+secside,y-1),(x,y-1),(x+1,y),(x-1,y),(x,y+1),(x+fireside,y+1),(x+secside,y+1)]
                for move in moves:
                    if self.get_cell(*move).type=='wood' or self.get_cell(*move).type=='oil':
                        self.set(*move,'fire',0)
                    if self.get_cell(*move).type=='water':
                        self.set(*move,'steam',0)
                        self.set(x,y,'void',0)
                    

    def update_lava(self,x,y):
        mylist = [0,1]
        a = random. choice(mylist)
        if (y!=self.height-1) and (x!=0) and (x!=self.width-1):
            if self.get_cell(x,y).lifetime >= 500:
                self.set(x,y,'rock')
            else:
                below = self.get_cell(x,y+1)
                right = self.get_cell(x+1,y)
                left = self.get_cell(x-1,y)
                top = self.get_cell(x,y-1)
                if below.type == 'void':
                    self.swap((x,y),(x,y+1))
                elif left.type == 'void' and a==0:
                    self.swap((x,y),(x-1,y))
                elif right.type == 'void' and a==1:
                    self.swap((x,y),(x+1,y))
                    
                top = self.get_cell(x,y-1)
                top_left = self.get_cell(x-1, y-1)
                top_right = self.get_cell(x+1, y-1)
                left = self.get_cell(x-1, y)
                right = self.get_cell(x+1, y)
                bottom_left = self.get_cell(x-1, y+1)
                bottom_right = self.get_cell(x+1, y+1)
                hitbox = [top, top_left, top_right, left, right, below, bottom_left, bottom_right]
                hb_coords = [(x, y-1), (x+1, y-1), (x+1, y-1), (x-1, y), (x+1, y), (x,y+1), (x-1, y+1), (x+1, y+1)]
                for i in range(len(hitbox)):
                    if hitbox[i].type == 'water':
                        self.set(*hb_coords[i], 'rock')
                        self.set(x,y, 'steam')
                    elif hitbox[i].type == 'wood':
                        self.set(*hb_coords[i], 'fire')
                    elif hitbox[i].type == 'oil':
                        self.set(*hb_coords[i], 'fire')

                
                
                
                
                

            
    def update_pixel(self,x,y):
        self.cell[y][x].lifetime+=1
        if self.get_cell(x,y).dirty_flag == True:
            if self.get_cell(x,y).type=='sand':
                self.update_sand(x,y)
            elif self.get_cell(x,y).type=='water':
                self.update_water(x,y)
            elif self.get_cell(x,y).type=='fire':
                self.update_fire(x,y)
            elif self.get_cell(x,y).type== 'steam':
                self.update_steam(x,y)
            elif self.get_cell(x,y).type== 'lava':
                self.update_lava(x,y)
            elif self.get_cell(x,y).type == 'oil':
                self.update_oil(x,y)
            if y+1<self.height and self.cell[y][x].lifetime>10:
                if self.get_cell(x,y).density>self.get_cell(x,y+1).density and self.get_cell(x,y).type!='rock' and self.get_cell(x,y).type!='wood':
                    self.swap((x,y),(x,y+1))
                               
    def update_grid(self):
        self.update_dirty_chunks()
    
    def clear_flags(self):
        for y in range(self.height):
            for x in range(self.width):
                self.get_cell(x,y).dirty_flag = True


def main():
    grid_obj = Grid(200,100,6,10)
    run = True
    clock = pygame.time.Clock()
    brush = None
    draw_type = 'fire'

    while run:
        clock.tick(60)
        WIN.fill(black)
        grid_obj.draw_grid()
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    brush = event.pos
                    grid_obj.handle_mouse_click(*brush,draw_type)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # left button released
                    brush = None
            elif event.type == pygame.MOUSEMOTION:
                if brush: # left button still pressed
                    brush = event.pos
                    grid_obj.handle_mouse_click(*brush,draw_type)
    pygame.quit()

if __name__ == "__main__":
    main()