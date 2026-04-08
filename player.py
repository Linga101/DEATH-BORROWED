import pygame
from settings import *

class Player:
    def __init__(self, name="Hero"):
        self.name = name
        self.bag = []
        self.max_bag_size = 4
        self.current_zone = None
        self.lifespan = GAME_TIME_LIMIT
        
        # Graphical properties
        self.rect = pygame.Rect(WIDTH//2, HEIGHT//2, PLAYER_SIZE, PLAYER_SIZE)
        self.frame_counter = 0
        self.bob_offset = 0
    
    def update_position(self, keys):
        dx, dy = 0, 0
        is_moving = False
        
        if keys[pygame.K_UP]:
            dy = -PLAYER_SPEED
            is_moving = True
        if keys[pygame.K_DOWN]:
            dy = PLAYER_SPEED
            is_moving = True
        if keys[pygame.K_LEFT]:
            dx = -PLAYER_SPEED
            is_moving = True
        if keys[pygame.K_RIGHT]:
            dx = PLAYER_SPEED
            is_moving = True
            
        # Move rect horizontally
        self.rect.x += dx
        if self.rect.left < 20: self.rect.left = 20
        if self.rect.right > WIDTH - 20: self.rect.right = WIDTH - 20
            
        # Move rect vertically
        self.rect.y += dy
        # Boundary constraints (leaving room for UI at top and bottom)
        if self.rect.top < 150: self.rect.top = 150
        if self.rect.bottom > HEIGHT - 100: self.rect.bottom = HEIGHT - 100
        
        # Bobbing Animation
        if is_moving:
            self.frame_counter += 1
            if (self.frame_counter // 10) % 2 == 0:
                self.bob_offset = -3 # move up 3 pixels visually
            else:
                self.bob_offset = 3 # move down 3 pixels visually
        else:
            self.frame_counter = 0
            self.bob_offset = 0

    def add_item(self, item):
        if len(self.bag) < self.max_bag_size:
            self.bag.append(item)
            return True, f"You picked up {item.name}."
        return False, "Bag is full! You can only carry 4 items."

    def has_item(self, item_name):
        return any(item.name == item_name for item in self.bag)
