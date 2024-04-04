import pygame

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.jump_force = 10
        self.gravity = 1
        self.is_jumping = False
        self.rect = pygame.Rect(x, y, width, height)

    def move(self, keys, screen_width, screen_height):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        if keys[pygame.K_UP] and not self.is_jumping:
            self.is_jumping = True
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        if self.is_jumping:
            self.y -= self.jump_force
            self.jump_force -= self.gravity
            if self.jump_force < -10:
                self.is_jumping = False
                self.jump_force = 10

        if self.y < screen_height - self.height:
            self.y += self.gravity

        self.x = max(0, min(screen_width - self.width, self.x))
        self.y = max(0, min(screen_height - self.height, self.y))

        self.rect.topleft = (self.x, self.y)

    def float_on_water(self):
        self.y -= 2  # Adjust the player's vertical position while floating

    def land_on_platform(self, platform):
        self.y = platform.top - self.height  # Align the player's bottom with the platform's top
        self.jump_force = 10  # Reset jump force when landing on the platform

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
