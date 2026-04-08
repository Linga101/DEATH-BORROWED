# Implementation Plan: DEATH BORROWED

We will build the 2D game "DEATH BORROWED" using Python. I have reviewed your game specifications, and it sounds like an exciting survival adventure! To make sure it performs well and is easy to distribute, I have prepared a technical plan and some recommendations.

## Recommendations & Proposed Tech Stack

1. **Game Engine**: We will use **Pygame-CE** (Community Edition). It is the modern, highly optimized fork of the classic Pygame framework, providing better performance and modern features for 2D games in Python.
2. **Perspective**: A **Top-Down 2D view** (similar to classic RPGs like Zelda) would work best. This fits perfectly with actions like "move forward, turn around, explore a village, and find a door."
3. **Distribution**: We will use a virtual environment (`venv`) for development, and when the game is ready, we will package it using **PyInstaller**. This will create a standalone executable (`.exe` for Windows) so that anyone can play the game without needing Python installed on their system.
4. **Game Architecture**: We'll use a **State Machine** pattern. The game will transition between states: `MainMenu`, `Phase1`, `Phase2`, `Phase3`, `Phase4`, `GameOver`, and `Victory`.

## User Review Required

> [!WARNING]
> Please review the open questions below to clarify a few details before we proceed with coding.

## Open Questions

1. **Phase 3 Item Clarification**: You mentioned that the 4 required items are a flashlight, a map, energy bars, and a gun. 
   - Phase 1 requires the **Map**.
   - Phase 2 requires the **Flashlight**.
   - Phase 4 requires the **Energy Bar** and **Gun**.
   - What exactly is the required item for **Phase 3**? You mentioned the player acts relying on the map to kill an animal/person to get an item. Should the item dropped in Phase 3 be the *Energy Bar*, and then Phase 4 is specifically finding the *Gun*? Or perhaps Phase 3 requires the *Knife/Hammer*? Please let me know how you'd like to map out the items!
2. **"Touch" Mechanic**: You mentioned a 'touch' action. Do you want this to be a specific key press (e.g., pressing `E` to interact/touch) that tells the player what is in front of them, or should it be automatic when the player walks over the item?
3. **Art & Assets**: Since this is a 2D game, we will need graphics (sprites) for the player, villagers, animals, items, and the village background. For now, I can use simple colored shapes (rectangles/circles) as placeholders so we can test the gameplay loop, and we can replace them with actual images later. Does that sound good?

## Proposed Changes

We will set up the project structure incrementally. 

### Game Structure Setup
We will establish the folder structure and virtual environment.

#### [NEW] [requirements.txt](file:///c:/Users/linga/Music/DEATH%20BORROWED/requirements.txt)
Will contain the `pygame-ce` library.

#### [NEW] [main.py](file:///c:/Users/linga/Music/DEATH%20BORROWED/main.py)
The entry point of our game.

#### [NEW] [settings.py](file:///c:/Users/linga/Music/DEATH%20BORROWED/settings.py)
Will hold game constants (screen width, height, colors, FPS, 10-minute timer).

#### [NEW] [player.py](file:///c:/Users/linga/Music/DEATH%20BORROWED/player.py)
Will handle the player's movement, lifespan tracking, inventory, and actions (kill, run, touch).

#### [NEW] [game.py](file:///c:/Users/linga/Music/DEATH%20BORROWED/game.py)
Will manage the game states (phases), timers, and collisions.

## Verification Plan

### Automated Tests
- We will test the movement, collision detection, and timer systems individually using debugging outputs.

### Manual Verification
- We will playtest each phase manually to ensure the map, flashlight mechanic for the dark path, and door checks work perfectly.
- We will ensure the single 10-minute global timer runs flawlessly across all phases.
