# Task 4 - Technical Documentation

## 1. Installation and User Guide

### How to Install and Run
1. Ensure Python 3.x is installed on your computer.
2. In the folder containing your game files, create a virtual environment:
   * **Windows/PowerShell**: `python -m venv venv`
   * Activate it: `.\venv\Scripts\Activate`
3. Install the required graphics library:
   * `pip install pygame-ce`
4. Run the game:
   * `python main.py`

### User Instructions
* Upon starting, the game will ask for your character's name. Type it and press **ENTER**.
* Use the **UP, DOWN, LEFT, RIGHT** arrow keys to navigate between the 10 zones in the village.
* Press **'T'** to Touch the ground and pick up any items in the zone. You can carry a maximum of 4 items.
* Press **'K'** to Kill an entity in the zone and absorb its lifespan. (1 minute added to timer).
* Some doors require specific items (Map, Flashlight, Gun) to progress. You must find them to move forward.
* The game ends over immediately if the timer hits 0.

---

## 2. Technical Documentation

### Libraries Used
* **`pygame` (pygame-ce version)**: Used for rendering the graphical user interface, text surfaces, capturing keyboard inputs asynchronously, handling the 60 FPS clock, and drawing colored shapes to represent UI.
* **`sys`**: Used specifically for `sys.exit()` to cleanly terminate the Python process once the Pygame window is safely closed.

### Identification of Classes and Sub-Programs

#### 1. `main.py`
Contains the core `Game` class which implements a state-machine loop.
* `Game.__init__()`: Initializes Pygame, creates the window, and sets up fonts.
* `Game.initialize_world()`: Bootstraps the objects. Creates all `Item`, `NPC`, and `Zone` instances and connects them up to form the 10-zone map.
* `Game.update()`: Runs 60 times a second. Deducts time from the global `game_timer` variable and checks for "GAME OVER" or "VICTORY" win states.
* `Game.events()`: Pygame event polling loop. Handles keyboard `KEYDOWN` events for capturing Name Input, Arrow Keys (calling `attempt_move`), 'T' key for `Player.add_item()`, and 'K' for kills.
* `Game.draw()`: Renders the entire screen based on current state (draws black background, blits white/colored text to surfaces, loops through items).

#### 2. `player.py`
Contains the `Player` class.
* `Player.__init__(name)`: Sets name, empty list for `bag`, and sets lifespan seconds.
* `Player.move(direction)`: Checks the `current_zone.connections` dictionary. Also checks the `current_zone.doors` dictionary to see if the required item exists in the bag by calling `has_item()`. Returns boolean tuple (`True`/`False`, message).
* `Player.add_item(item)`: Enforces the 4-item capacity limit. Returns `True` if successful, appending the item to `self.bag`.
* `Player.has_item(item_name)`: Generator function that returns `True` if the item matches inside the player's inventory list.

#### 3. `game_objects.py`
Contains modular, reusable class blueprints for world entities.
* `Item.__init__()`: Defines item name and description.
* `NPC.__init__()`: Defines entity name and boolean `is_dead` flag.
* `Zone.__init__()`: Defines a room/location in the game. Stores lists for `items` and `npcs`, and dictionaries for `doors` and `connections`.
* `Zone.connect(direction, zone)`: Helper method to link two Zone objects together bidirectionally or monotonically.
