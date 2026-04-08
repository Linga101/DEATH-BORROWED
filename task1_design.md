# Task 1 - Decomposition and Design

## 1. Specification and Required Outcomes
The program to be developed is a graphical 2D interactive game titled **"DEATH BORROWED"**. It is a single-player survival game set in a village, where the player must kill NPCs/animals to extend their limited lifespan (maximum 5 minutes). The game is divided into 4 phases. At each phase, the player must collect a specific item to pass through a door and advance. The player has a bag capable of storing a maximum of 4 items at any given time.

**Required Outcomes:**
* A working Python program (using Pygame-CE) with a minimum of 10 different positions/zones for the player to navigate.
* A minimum of 5 different items to collect.
* An interactive interface (graphical or text-based options) taking player input (Name, Move, Turn, Kill, Touch).
* Character name input at the start of the game.
* An object-oriented approach (e.g., utilizing Classes for Player, Items, and Game State).
* The bag must be limited to exactly 4 items.

## 2. Success Criteria
1. The game allows the player to input their character's name at the beginning.
2. The game tracks the player's 5-minute maximum lifespan and decreases it over time.
3. The player can move between at least 10 different interconnected positions.
4. There are at least 5 distinct items available to pick up (Map, Flashlight, Energy Bar, Gun, First Aid Kit, etc.).
5. The player's bag (inventory system) properly enforces a maximum capacity of 4 items.
6. The game executes 4 phases smoothly with correctly enforced door-checks for specific items.
7. The code uses Object-Oriented Programming (OOP) principles effectively.
8. The game correctly handles errors (such as attempting to pick up an item when the bag is full).

## 3. Story, Layout, and Items
**Story:** You wake up in a cursed village where your life is rapidly ticking away. The only way to survive is to borrow time from the living by "killing" entities and collecting specific artifacts to escape through four locked doors.

**Available Items (5+):** 1. *Map*, 2. *Flashlight*, 3. *Energy Bar*, 4. *Gun*, 5. *First Aid Kit*, 6. *Knife*.

**Layout (10 Positions):**
The village is a 2D grid area broken into various zones:
1. `Spawn Point`
2. `Village Square` (Door 1)
3. `Alleyway`
4. `Abandoned House` (Map located here)
5. `Dark Path` (Needs Flashlight)
6. `Forest Edge` (Flashlight located here)
7. `Graveyard` (Door 2)
8. `Old Well` (NPCs to kill)
9. `Giant Animal Lair` (Energy Bar and Gun usage)
10. `Final Gate` (Door 3 & 4)

## 4. Data Structures
* **Lists**: The `bag` structured as a Python `list` to store collected items, continuously checking `if len(bag) < 4`.
* **Dictionaries**: The `map_layout` using dictionaries to represent positions and their connecting valid adjacent positions, or `Item` properties.
* **Classes (Objects)**:
  * `Player(name)`: attributes = `lifespan`, `bag`, `current_position`.
  * `Item(name, required_phase)`: attributes = `name`, `is_collected`.
  * `Zone(name, description, items_present, npcs_present)`: attributes = `connections`.

## 5. Subproblems (Decomposition)
1. **Game Initialization**: How do we set up the screen, timer, and get the player's name?
2. **Movement & Navigation**: How do we continuously update player X,Y coordinates and check boundaries against the 10 zones?
3. **Inventory Management**: How do we collect items, check if it's the correct item, and enforce the 4-item limit?
4. **Action System**: How do we handle "kill", "touch", and "door check"?
5. **Phase/State Machine**: How does the game transition from Phase 1 to Phase 4 seamlessly?

## 6. Structure Diagram
```text
[Main Menu & Setup] -> [Init Player & Map] -> [Game Loop]
                                                  |
     +-------------------+------------------+-----+-------------+
     |                   |                  |                   |
[Input Handler]   [Update State]    [Render Screen]       [Timer Check]
- Move            - Check Phase     - Draw map/text       - End game if 0
- Touch           - Check Door      - Draw inventory
- Kill            - Entity Death    
```

## 7. Algorithms & Pseudocode
### Inventory Collection Algorithm
```pseudocode
FUNCTION touch_item(item):
    IF length(player.bag) < 4 THEN
        ADD item TO player.bag
        PRINT "Item added to bag"
        REMOVE item FROM current_zone
    ELSE
        PRINT "Bag is full! Drop something first."
    END IF
END FUNCTION
```

### Door Check Algorithm
```pseudocode
FUNCTION check_door(door_required_item):
    IF door_required_item IN player.bag THEN
        PRINT "Door opened! Next Phase."
        player.current_phase = player.current_phase + 1
        RETURN TRUE
    ELSE
        PRINT "You do not have the required item to pass."
        RETURN FALSE
    END IF
END FUNCTION
```
