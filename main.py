import pygame
import sys
from settings import *
from player import Player
from game_objects import Item, NPC, Zone, Door

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("DEATH BORROWED")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 24)
        self.big_font = pygame.font.SysFont('arial', 48)
        self.running = True

        self.state = "START_SCREEN"
        self.player_name_input = ""
        self.player = None
        self.message_log = ["Welcome to DEATH BORROWED."]
        self.game_timer = GAME_TIME_LIMIT
        self.transition_timer = 0
        self.transition_zone = None
        self.transition_direction = None
        self.load_assets()
        self.initialize_world()

    def load_assets(self):
        try:
            # Load and scale images
            self.assets = {}
            
            # Grass Tile (tile it or stretch it, let's blur/stretch for simple BG)
            bg = pygame.image.load("assets/grass_tile.png").convert()
            self.assets['bg'] = pygame.transform.scale(bg, (WIDTH, HEIGHT))
            
            # Player
            player_img = pygame.image.load("assets/player_sprite.png").convert()
            player_img.set_colorkey(WHITE)
            self.assets['player'] = pygame.transform.scale(player_img, (PLAYER_SIZE+10, PLAYER_SIZE+10))
            
            # Map Item
            map_img = pygame.image.load("assets/item_map.png").convert()
            map_img.set_colorkey(WHITE)
            self.assets['map'] = pygame.transform.scale(map_img, (ITEM_SIZE+10, ITEM_SIZE+10))
            
            # Other Item
            item_img = pygame.image.load("assets/item_flashlight.png").convert()
            item_img.set_colorkey(WHITE)
            self.assets['item'] = pygame.transform.scale(item_img, (ITEM_SIZE+10, ITEM_SIZE+10))

            # NPC
            npc_img = pygame.image.load("assets/npc_villager.png").convert()
            npc_img.set_colorkey(WHITE)
            self.assets['npc'] = pygame.transform.scale(npc_img, (NPC_SIZE+20, NPC_SIZE+20))
            
            # Door
            door_img = pygame.image.load("assets/door_sprite.png").convert()
            door_img.set_colorkey(WHITE)
            self.assets['door'] = pygame.transform.scale(door_img, (DOOR_SIZE, DOOR_SIZE))
            
        except Exception as e:
            print("Error loading assets:", e)
            self.assets = None

    def log(self, msg):
        self.message_log.append(msg)
        if len(self.message_log) > 3:
            self.message_log.pop(0)

    def initialize_world(self):
        map_item = Item("Map", "A dusty map of the village.")
        flashlight = Item("Flashlight", "A heavy metal flashlight.")
        energy_bar = Item("Energy Bar", "Restores some lifespan.")
        gun = Item("Gun", "A rusted revolver.")

        z1 = Zone("Spawn Point", "You wake up in a cold, stone room.")
        z2 = Zone("Village Square", "The center of the village.")
        z3 = Zone("Alleyway", "A dark, narrow street.", items=[map_item])
        z4 = Zone("Abandoned House", "Smells like mold and decay.")
        z5 = Zone("Dark Path", "It is pitch black here.")
        z6 = Zone("Forest Edge", "The trees are dying.", items=[flashlight])
        z7 = Zone("Graveyard", "Tombstones everywhere.", npcs=[NPC("Grave Robber")])
        z8 = Zone("Old Well", "A deep, echoing well.", npcs=[NPC("Villager")], items=[energy_bar])
        z9 = Zone("Giant Animal Lair", "A terrifying beast lives here.", items=[gun])
        z10 = Zone("Final Gate", "The exit. You need a Gun to survive.")
        win_zone = Zone("FREEDOM", "You escaped!")
        
        # Add a test zombie and item to the Village Square so the player sees them early!
        test_zombie = NPC("Wandering Zombie")
        z2.npcs.append(test_zombie)
        z2.items.append(map_item) # Move map to square for easier early game

        # Doors map bidirectional connections
        z1.connect('North', z2)
        z2.connect('South', z1)
        z2.connect('West', z3)
        z2.connect('East', z4)
        z3.connect('East', z2)
        z4.connect('West', z2)
        
        # Door 1 overrides (North from Square needs Map)
        z2.connect('North', z5, required_item='Map')
        z5.connect('South', z2)
        z5.connect('West', z6)
        z6.connect('East', z5)
        
        # Door 2 (East from Dark Path needs Flashlight)
        z5.connect('East', z7, required_item='Flashlight')
        z7.connect('West', z5)
        z7.connect('North', z8)
        z8.connect('South', z7)
        z7.connect('East', z9)
        z9.connect('West', z7)
        z9.connect('North', z10)
        z10.connect('South', z9)
        z10.connect('North', win_zone, required_item='Gun')

        self.start_zone = z1

    def draw_text(self, text, font, color, x, y):
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))

    def move_player_to(self, zone, entry_direction):
        self.player.current_zone = zone
        # Position player far enough away from the door they came through to prevent a teleport glitch!
        if entry_direction == 'North':
            self.player.rect.y = HEIGHT - 220
        elif entry_direction == 'South':
            self.player.rect.y = 220
        elif entry_direction == 'East':
            self.player.rect.x = 100
        elif entry_direction == 'West':
            self.player.rect.x = WIDTH - 120
            
        if zone.name == "FREEDOM":
            self.state = "VICTORY"

    def update(self):
        if self.state == "TRANSITION":
            self.transition_timer -= 1
            if self.transition_timer <= 0:
                self.move_player_to(self.transition_zone, self.transition_direction)
                if self.state != "VICTORY":
                    self.state = "PLAYING"
                    
        elif self.state == "PLAYING":
            self.game_timer -= 1 / FPS
            if self.game_timer <= 0:
                self.state = "GAME_OVER"

            keys = pygame.key.get_pressed()
            self.player.update_position(keys)
            
            # Update NPCs and check for attacks
            for npc in self.player.current_zone.npcs:
                # Tell NPC where the player is so they can chase!
                npc.update(self.player.rect)
                
                # Check if the zombie catches up to the player
                if not npc.is_dead and self.player.rect.colliderect(npc.rect):
                    if getattr(npc, 'attack_cooldown', 0) <= 0:
                        self.game_timer -= 60
                        npc.attack_cooldown = 120 # 2 seconds of invulnerability from this zombie
                        self.log("Zombie bit you! Lost 1 MINUTE!")

            # Check door collision
            for door in self.player.current_zone.doors:
                if self.player.rect.colliderect(door.rect):
                    # Trying to walk through door
                    if door.required_item and not self.player.has_item(door.required_item):
                        self.log(f"Door locked! You need: {door.required_item}")
                        # Push back slightly to prevent sticking
                        if door.direction == 'North': self.player.rect.y += 10
                        elif door.direction == 'South': self.player.rect.y -= 10
                        elif door.direction == 'East': self.player.rect.x -= 10
                        elif door.direction == 'West': self.player.rect.x += 10
                    else:
                        self.log(f"Moved {door.direction}.")
                        # Trigger Transition Screen
                        self.transition_zone = door.target_zone
                        self.transition_direction = door.direction
                        self.transition_timer = 2 * FPS # Hold black screen for 2 seconds
                        self.state = "TRANSITION"

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if self.state == "START_SCREEN":
                    if event.key == pygame.K_RETURN:
                        if self.player_name_input.strip() == "":
                            self.player_name_input = "Hero"
                        self.player = Player(self.player_name_input)
                        self.player.current_zone = self.start_zone
                        self.state = "PLAYING"
                        self.log("Press arrow keys to walk. T to touch, K to kill.")
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name_input = self.player_name_input[:-1]
                    else:
                        self.player_name_input += event.unicode
                
                elif self.state == "PLAYING":
                    # Touch / Pickup Items
                    if event.key == pygame.K_t:
                        hit_something = False
                        for item in self.player.current_zone.items[:]:
                            # Inflate the rect by 60 pixels to make it much easier to hit!
                            if self.player.rect.inflate(60, 60).colliderect(item.rect):
                                hit_something = True
                                success, msg = self.player.add_item(item)
                                self.log(msg)
                                if success:
                                    self.player.current_zone.items.remove(item)
                                break
                        if not hit_something:
                            self.log("You touch the ground. Nothing here.")

                    # Kill NPCs
                    elif event.key == pygame.K_k:
                        hit_something = False
                        for npc in self.player.current_zone.npcs:
                            # Inflate the rect to make killing easier
                            if self.player.rect.inflate(60, 60).colliderect(npc.rect):
                                hit_something = True
                                if not npc.is_dead:
                                    npc.is_dead = True
                                    self.game_timer += 60  
                                    self.log(f"Killed {npc.name}. +60 seconds.")
                                else:
                                    self.log("They are already dead.")
                                break
                        if not hit_something:
                            self.log("You swing at the air. No one to kill.")

    def draw_tombstone(self, x, y):
        # Base shadow
        pygame.draw.ellipse(self.screen, (20, 20, 20), (x-10, y+30, 50, 15))
        # Main stone
        pygame.draw.rect(self.screen, (100, 100, 100), (x, y, 30, 40), border_radius=15)
        # Inner carving
        pygame.draw.rect(self.screen, (70, 70, 70), (x+5, y+10, 20, 20), border_radius=5)

    def draw_tree(self, x, y):
        # Shadow
        pygame.draw.ellipse(self.screen, (15, 15, 15), (x-20, y+60, 60, 20))
        # Trunk
        pygame.draw.rect(self.screen, (40, 30, 20), (x, y+20, 20, 50))
        # Leaves (Dead/Dark)
        pygame.draw.circle(self.screen, (20, 30, 20), (x+10, y+20), 25)
        pygame.draw.circle(self.screen, (15, 25, 15), (x-5, y+10), 20)
        pygame.draw.circle(self.screen, (15, 25, 15), (x+25, y+10), 20)
        pygame.draw.circle(self.screen, (10, 20, 10), (x+10, y-5), 20)

    def draw(self):
        self.screen.fill(BLACK)
        
        if self.state == "START_SCREEN":
            self.draw_text("DEATH BORROWED", self.big_font, RED, WIDTH//2 - 120, HEIGHT//2 - 50)
            self.draw_text("Enter Character Name: " + self.player_name_input, self.font, WHITE, WIDTH//2 - 150, HEIGHT//2)
            self.draw_text("Press ENTER to start", self.font, GRAY, WIDTH//2 - 100, HEIGHT//2 + 50)
            
        elif self.state == "TRANSITION":
            if self.transition_zone:
                self.draw_text(f"Entering: {self.transition_zone.name}", self.big_font, GREEN, WIDTH//2 - 200, HEIGHT//2 - 50)
                self.draw_text("Prepare yourself...", self.font, WHITE, WIDTH//2 - 80, HEIGHT//2 + 20)

        elif self.state == "PLAYING":
            # Draw Background Graphics First
            if self.player.current_zone.name == "Graveyard":
                # Muddy dark dirt layer
                pygame.draw.rect(self.screen, (35, 30, 30), (0, 0, WIDTH, HEIGHT))
                
                # Render decorative Graveyard Scenery
                graveyard_positions = [
                    (100, 200, 'tree'), (250, 180, 'tomb'), (320, 190, 'tomb'),
                    (600, 220, 'tree'), (500, 350, 'tomb'), (150, 400, 'tree'),
                    (700, 450, 'tree'), (650, 300, 'tomb'), (80, 500, 'tomb')
                ]
                for px, py, p_type in graveyard_positions:
                    if p_type == 'tree': self.draw_tree(px, py)
                    elif p_type == 'tomb': self.draw_tombstone(px, py)
            else:
                if hasattr(self, 'assets') and self.assets:
                    self.screen.blit(self.assets['bg'], (0,0))
                else:
                    self.screen.fill(BLACK)
                    # Floor boundary fallback
                    pygame.draw.rect(self.screen, DARK_GRAY, (20, 150, WIDTH-40, HEIGHT-250))
                
            # Header
            self.draw_text(f"Zone: {self.player.current_zone.name}", self.big_font, WHITE, 20, 20)
            mins = int(self.game_timer // 60)
            secs = int(self.game_timer % 60)
            color = GREEN if self.game_timer > 60 else RED
            self.draw_text(f"Lifespan left: {mins}:{secs:02d}", self.big_font, color, WIDTH - 350, 20)
            self.draw_text(self.player.current_zone.description, self.font, WHITE, 20, 80)
            
            # Render Doors (Exits)
            for door in self.player.current_zone.doors:
                if hasattr(self, 'assets') and self.assets:
                    self.screen.blit(self.assets['door'], door.rect.topleft)
                    # Add lock indicator if locked
                    if door.required_item and not self.player.has_item(door.required_item):
                        pygame.draw.rect(self.screen, RED, door.rect, 2)
                else:
                    color = RED if door.required_item and not self.player.has_item(door.required_item) else PURPLE
                    pygame.draw.rect(self.screen, color, door.rect)
                
            # Render Items
            for item in self.player.current_zone.items:
                if hasattr(self, 'assets') and self.assets:
                    img = self.assets['map'] if item.name == "Map" else self.assets['item']
                    self.screen.blit(img, item.rect.topleft)
                else:
                    pygame.draw.rect(self.screen, YELLOW, item.rect)
                
            # Render NPCs
            for npc in self.player.current_zone.npcs:
                bob = -3 if not npc.is_dead and hasattr(npc, 'move_timer') and (npc.move_timer // 10) % 2 == 0 else 0
                rect_pos = (npc.rect.x, npc.rect.y + bob)
                
                if hasattr(self, 'assets') and self.assets:
                    if not npc.is_dead:
                        self.screen.blit(self.assets['npc'], rect_pos)
                    else:
                        img = self.assets['npc'].copy()
                        img.set_alpha(100) # Ghostly if dead
                        self.screen.blit(img, npc.rect.topleft)
                else:
                    color = GRAY if npc.is_dead else RED
                    pygame.draw.rect(self.screen, color, (rect_pos[0], rect_pos[1], npc.rect.width, npc.rect.height))
                
            # Render Player
            p_pos = (self.player.rect.x, self.player.rect.y + self.player.bob_offset)
            if hasattr(self, 'assets') and self.assets:
                 self.screen.blit(self.assets['player'], p_pos)
            else:
                 pygame.draw.rect(self.screen, BLUE, (p_pos[0], p_pos[1], self.player.rect.width, self.player.rect.height))

            # FOG OF WAR (Lighting System)
            fog = pygame.Surface((WIDTH, HEIGHT))
            fog.fill((0, 0, 0)) # Pitch black
            # Determine light radius - increased heavily so player can see doors
            light_radius = 500 if self.player.has_item("Flashlight") else 200
            # Carve out the light circle
            pygame.draw.circle(fog, (255, 255, 255), (self.player.rect.centerx, self.player.rect.centery), light_radius)
            fog.set_colorkey((255, 255, 255))
            fog.set_alpha(240) # Mostly opaque darkness
            self.screen.blit(fog, (0,0))

            # UI Bottom Panel (Backdrop)
            pygame.draw.rect(self.screen, BLACK, (0, HEIGHT - 100, WIDTH, 100))
            pygame.draw.line(self.screen, GRAY, (20, HEIGHT - 90), (WIDTH - 20, HEIGHT - 90))
            
            # Header Panel (Backdrop)
            pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, 100))
            
            # Text UI overlay
            self.draw_text(f"Zone: {self.player.current_zone.name}", self.big_font, WHITE, 20, 20)
            mins = int(self.game_timer // 60)
            secs = int(self.game_timer % 60)
            self.draw_text(f"Lifespan: {mins}:{secs:02d}", self.big_font, WHITE, WIDTH - 350, 20)
            self.draw_text(self.player.current_zone.description, self.font, WHITE, 20, 80)
            
            # HEALTH/TIME BAR!
            time_ratio = self.game_timer / GAME_TIME_LIMIT
            if time_ratio < 0: time_ratio = 0
            if time_ratio > 1: time_ratio = 1
            bar_color = GREEN if time_ratio > 0.4 else (YELLOW if time_ratio > 0.2 else RED)
            pygame.draw.rect(self.screen, DARK_GRAY, (WIDTH - 350, 70, 300, 15))
            pygame.draw.rect(self.screen, bar_color, (WIDTH - 350, 70, 300 * time_ratio, 15))

            # Inventory
            inv_txt = ", ".join([i.name for i in self.player.bag]) if self.player.bag else "Empty"
            self.draw_text(f"BAG: {inv_txt}", self.font, GREEN, 20, HEIGHT - 80)

            # Message Log
            for i, msg in enumerate(self.message_log[-2:]):
                self.draw_text(msg, self.font, WHITE, 400, HEIGHT - 80 + (i * 30))

        elif self.state == "GAME_OVER":
            self.draw_text("GAME OVER", self.big_font, RED, WIDTH//2 - 100, HEIGHT//2 - 50)
            
        elif self.state == "VICTORY":
            self.draw_text("YOU SURVIVED", self.big_font, GREEN, WIDTH//2 - 150, HEIGHT//2 - 50)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
