import pygame
import random
from settings import *

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        # Random spawn within playable bounds
        self.rect = pygame.Rect(
            random.randint(50, WIDTH - 50 - ITEM_SIZE),
            random.randint(150, HEIGHT - 150 - ITEM_SIZE),
            ITEM_SIZE, ITEM_SIZE
        )

class NPC:
    def __init__(self, name):
        self.name = name
        self.is_dead = False
        self.rect = pygame.Rect(
            random.randint(50, WIDTH - 50 - NPC_SIZE),
            random.randint(150, HEIGHT - 150 - NPC_SIZE),
            NPC_SIZE, NPC_SIZE
        )
        self.move_timer = 0
        self.direction = [0, 0]
        self.attack_cooldown = 0

    def update(self, player_rect=None):
        if self.is_dead: return
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # If given a player, chase them! (Aggressive Zombie AI)
        if player_rect:
            if self.rect.centerx < player_rect.centerx: self.rect.x += 1
            elif self.rect.centerx > player_rect.centerx: self.rect.x -= 1
            
            if self.rect.centery < player_rect.centery: self.rect.y += 1
            elif self.rect.centery > player_rect.centery: self.rect.y -= 1
        else:
            # Fallback wandering
            self.move_timer -= 1
            if self.move_timer <= 0:
                self.move_timer = random.randint(30, 120)
                self.direction = [random.choice([-1, 0, 1]) * 2, random.choice([-1, 0, 1]) * 2]
            self.rect.x += self.direction[0]
            self.rect.y += self.direction[1]
        
        # Enforce boundaries so they don't wander off screen
        if self.rect.left < 20: self.rect.left = 20
        if self.rect.right > WIDTH - 20: self.rect.right = WIDTH - 20
        if self.rect.top < 150: self.rect.top = 150
        if self.rect.bottom > HEIGHT - 100: self.rect.bottom = HEIGHT - 100

class Door:
    def __init__(self, target_zone, required_item, direction):
        self.target_zone = target_zone
        self.required_item = required_item
        self.direction = direction
        
        # Determine position based on direction
        if direction == 'North':
            self.rect = pygame.Rect(WIDTH//2 - DOOR_SIZE//2, 150, DOOR_SIZE, DOOR_SIZE)
        elif direction == 'South':
            self.rect = pygame.Rect(WIDTH//2 - DOOR_SIZE//2, HEIGHT - 100 - DOOR_SIZE, DOOR_SIZE, DOOR_SIZE)
        elif direction == 'West':
            self.rect = pygame.Rect(20, HEIGHT//2 - DOOR_SIZE//2, DOOR_SIZE, DOOR_SIZE)
        elif direction == 'East':
            self.rect = pygame.Rect(WIDTH - 20 - DOOR_SIZE, HEIGHT//2 - DOOR_SIZE//2, DOOR_SIZE, DOOR_SIZE)

class Zone:
    def __init__(self, name, description, items=None, npcs=None):
        self.name = name
        self.description = description
        self.items = items if items else []
        self.npcs = npcs if npcs else []
        self.doors = [] # List of Door objects

    def connect(self, direction, zone, required_item=None):
        self.doors.append(Door(zone, required_item, direction))
