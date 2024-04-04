import pygame
from ground import *
from Player import Player
# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rectangle Player")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

running = True
grid_obj = Grid(WIDTH//4,HEIGHT//10,WIDTH//100)
player = Player(0, 0, 50, 50)
clock = pygame.time.Clock()
brush = None
draw_type = 'fire'
WIN.fill(black)
level=1
grid_obj.draw_object('wood','tree.txt')
platforms=grid_obj.get_platform(level)
while running:
    for platform in platforms:
        if player.y+player.height==platform.top:
            player.on_ground=True
    clock.tick(60)
    grid_obj.draw_grid()
    grid_obj.draw_platform(WIN,level)
    grid_obj.update_grid()
    player.draw(WIN,WHITE)
    pygame.display.update()
    grid_obj.clear_flags()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: draw_type = 'water'
    if keys[pygame.K_s]: draw_type = 'sand'
    if keys[pygame.K_q]: draw_type = 'wood'
    if keys[pygame.K_f]: draw_type = 'fire'
    if keys[pygame.K_r]: draw_type = 'steam'
    if keys[pygame.K_t]: draw_type = 'lava'
    if keys[pygame.K_o]: draw_type = 'oil'
    if keys[pygame.K_p]: draw_type = 'rock'
    player.move(keys, WIDTH, HEIGHT,grid_obj)

    # Check if player is floating on water
    if level==3:
        if player.rect.colliderect(water_surface):
            player.float_on_water()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
        for platform in platforms:
            if player.rect.height+player.rect.top>=platform.top:
                player.land_on_platform(platform)
                break
    # Update the display
    pygame.display.flip()

    # Add a small delay to control the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
