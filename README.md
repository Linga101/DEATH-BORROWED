# DEATH BORROWED ⏳💀

**DEATH BORROWED** is an intense 2D top-down survival horror game built natively in Python using the `pygame-ce` engine. 

You spawn in a pitch-black, interconnected village with nothing but a ticking 5-minute lifespan. The darkness hides aggressive zombies, terrifying beasts, and locked doors. Every time an enemy touches you, they steal a chunk of your borrowed time. Your only objective is to scramble through the darkness, find the items required to unlock the final gate, and escape before your health/timer drains to zero.

## Features ✨

* **Fog of War Lighting Engine**: Start the game shrouded in claustrophobic darkness. You must find the Flashlight tool to dynamically double your light radius and reveal your surroundings.
* **Aggressive Chaser AI**: Enemies don't just stand still. Zombies will lock onto your coordinates and relentlessly chase you down across the screen.
* **Zone Transitioning**: Explore a seamlessly connected map containing 10 uniquely named zones, including custom procedurally drawn environments like the Muddy Graveyard.
* **Object-Oriented Physics Box**: Complete continuous collision detection allowing interactive real-time combat and exploration.

## How to Play 🎮

### Controls
* **Up / Down / Left / Right Arrow Keys**: Move the Player
* **T Key**: Touch / Pickup a nearby Item
* **K Key**: Kill / Melee Attack an adjacent Zombie

### Strategy
Navigate the village by walking into the wooden doors. Some doors are locked and require specific items (like a Map or a Key) to be in your Bag to proceed. If a zombie catches you, they will instantly drain 60 seconds off your life clock. Strike first, secure the keys, and find the FREEDOM zone!

## Installation & Setup 🛠️

1. Ensure **Python 3.10+** is installed on your machine.
2. Clone this repository locally.
3. Activate the virtual environment (or create one):
   ```bash
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   ```
4. Install requirements:
   ```bash
   pip install pygame-ce
   ```
5. Launch the game!
   ```bash
   python main.py
   ```
