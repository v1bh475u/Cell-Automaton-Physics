import pygame

class Player:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 10
        self.jump_height=20
        self.gravity = 2
        self.y_vel = self.jump_height
        self.is_jumping = False
        self.rect = pygame.Rect(x, y, width, height)
        self.left = False
        self.right = False
        self.on_ground = False
        self.walkCount = 0
        self.walkRight = [pygame.image.load('Game/R1.png'), pygame.image.load('Game/R2.png'), pygame.image.load('Game/R3.png'), pygame.image.load('Game/R4.png'), pygame.image.load('Game/R5.png'), pygame.image.load('Game/R6.png'), pygame.image.load('Game/R7.png'), pygame.image.load('Game/R8.png'), pygame.image.load('Game/R9.png')]
        self.walkLeft = [pygame.image.load('Game/L1.png'), pygame.image.load('Game/L2.png'), pygame.image.load('Game/L3.png'), pygame.image.load('Game/L4.png'), pygame.image.load('Game/L5.png'), pygame.image.load('Game/L6.png'), pygame.image.load('Game/L7.png'), pygame.image.load('Game/L8.png'), pygame.image.load('Game/L9.png')]

        self.char = pygame.image.load('Game/standing.png')
    def is_void(self,grid,x,y):
        if grid.get_cell(x//grid.cell_size,y//grid.cell_size).type=='void':
            return True
        return False
    
    def is_front_clear(self,grid):
        for y in range(self.y,self.y+self.height+1):
            if not self.is_void(grid,self.x+self.width+1,y):
                return False
        return True
    def is_back_clear(self,grid):
        for y in range(self.y,self.y+self.height+1):
            if not self.is_void(grid,self.x-1,y):
                return False
        return True
    def is_top_clear(self,grid):
        for x in range(self.x,self.x+self.width+1):
            if not self.is_void(grid,x,self.y-1):
                return False
        return True
    def is_bottom_clear(self,grid):
        for x in range(self.x,self.x+self.width+1):
            if not self.is_void(grid,x,self.y+self.height):
                return False
        return True
    def move(self, keys, screen_width, screen_height,grid_obj):
        if keys[pygame.K_LEFT] and self.is_back_clear(grid_obj):
            self.x -= self.speed
            self.left = True
            self.right = False
        elif keys[pygame.K_RIGHT] and self.is_front_clear(grid_obj):
            self.x += self.speed
            self.right = True
            self.left = False
        else:
            self.walkCount = 0
            self.left = False
            self.right = False
            

        if keys[pygame.K_UP] and not self.is_jumping:
            self.is_jumping = True
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        if self.is_jumping:
            self.y -= self.y_vel
            self.y_vel -= self.gravity
            if self.y_vel < -self.jump_height:
                self.is_jumping = False
                self.y_vel = self.jump_height

        if self.y < screen_height - self.height and not self.on_ground and self.is_bottom_clear(grid_obj):
            self.y += self.gravity
        self.x = max(0, min(screen_width - self.width, self.x))
        self.y = max(0, min(screen_height - self.height, self.y))

        self.rect.topleft = (self.x, self.y)

    def float_on_water(self):
        self.y -= 2  # Adjust the player's vertical position while floating

    def land_on_platform(self, platform):
        self.y = platform.top - self.height# Align the player's bottom with the platform's top
        self.is_jumping=False
        self.y_vel = self.jump_height  # Reset jump force when landing on the platform

    def draw(self, screen, color):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if self.left:
            screen.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            screen.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        else:
            screen.blit(self.char, (self.x, self.y))


