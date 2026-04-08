# Task 3 - Testing

## 1. Testing Strategy
* **Unit Testing:** Individual classes (`Player`, `Zone`, `Item`) will be tested. For example, ensuring that `player.add_item()` correctly appends to the bag, but rejects any 5th item.
* **Integration Testing:** Ensuring the connection between `Player` movement and `Zone` door checks work flawlessly. For instance, testing `player.move('North')` when the door requires the "Map".
* **System Testing (Run-Throughs):** Manual play-testing of the game from the "Start Screen" to the "Victory" screen to ensure the 10-minute timer ticks down, entity killing extends it, and doors correctly trigger sequence logic.
* **Whitebox Testing:** Using print statements in `main.py` explicitly to trace the `game_timer` variable, the `state` changes, and the length of the `player.bag`.

## 2. Test Data
* **Normal Data**: Moving "North" to an open door. "Hero" as player name.
* **Extreme Data**: Adding exactly 4 items to the bag to check if the 4th item is accepted.
* **Invalid Data**: Trying to move "Up" in a room with no northern connection. Trying to pick up a 5th item.

## 3. Test Log

| Test # | Test Purpose | Input Data | Expected Result | Actual Result | Evidence / Screenshot ref |
|--------|--------------|------------|-----------------|---------------|--------------------------|
| 1 | Test Character Name Input | Keystrokes "John", then ENTER | Player object created with name "John". State changes to PLAYING. | Player successfully named "John". Screen shifts to Playing UI. | See Screenshot 1 |
| 2 | Test Movement into open area | Press LEFT ARROW (West) | Player moves to Alleyway, zone text updates. | Zone changes to "Alleyway". | See Screenshot 2 |
| 3 | Test Movement into locked area | Press NORTH ARROW without a Map | Return locked error. Player stays in Square. | Error "Door locked! You need: Map" outputted in log. | See Screenshot 3 |
| 4 | Test item pickup | Press 'T' on Map | Map item moves from Zone to Bag. | Bag counter updates to 1/4. | See Screenshot 4 |
| 5 | Test 4-item bag limit (Invalid data) | Generate 5 items, press 'T' 5 times | 5th attempt yields error. | "Bag is full!" output in log. | See Screenshot 5 |
| 6 | Test Timer | Wait 1 minute | Timer goes from 10:00 to 09:00. | Timer displays "Lifespan left: 9:00" | See Screenshot 6 |
| 7 | Test Entity Kill | Press 'K' near an NPC | NPC marked dead. Timer gains +1:00. | NPC reads "(Dead)", Timer adds 60 secs. | See Screenshot 7 |
| 8 | Test Game Over (Extreme data) | Timer reaches 0 | State transitions to "GAME_OVER". | Game Over screen successfully drawn. | See Screenshot 8 |
| 9 | Test Victory | Enter 'FREEDOM' zone | State transitions to "VICTORY". | Victory screen drawn, loop terminates appropriately.| See Screenshot 9 |

## 4. Assessment of Success Criteria
* **Criteria 1 & 2:** Met successfully. UI displays name input and a ticking clock.
* **Criteria 3:** Met. There are 10 unique zones with valid graph connections.
* **Criteria 4 & 5:** Met. There are 6 items implemented. Players cannot hold more than 4 items.
* **Criteria 6 & 7:** Met. Game states update flawlessly. OOP has been thoroughly used to represent game entities (`player.py`, `game_objects.py`, `main.py`).
