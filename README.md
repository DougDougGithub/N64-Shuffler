# N64 Shuffler
This is code that swaps between save states on an N64 emulator.
Written by DougDoug. Feel free to use this for whatever you want! Credit is appreciated but not required.

DISCLAIMER: This code has nothing to do with any Nintendo games or properties or programs. There are no Nintendo assets or property in this project whatesoever. It is simply code that presses keys to randomly save and load save states.
If you want to use this for N64 games, you will need to find your own legal version of an N64 game and an N64 emulator.

Also, this is not amazing code, the multi-threading is pretty messy but whatever fuck it it works. I won't be reviewing pull requests but feel free to fork the project and use it for whatever you want.

## SETUP:
1) This was written in Python 3.9.2. Install page here: https://www.python.org/downloads/release/python-392/

2) Run `pip install -r requirements.txt` to install all modules.

3) The code can update a text source in OBS to show the number of remaining save states. If you want to use this, first open up OBS. Make sure you're running version 28.X or later. Click Tools, then WebSocket Server Settings. Make sure "Enable WebSocket server" is checked. Then set Server Port to '4455' and set the Server Password to 'TwitchChat9'. If you use a different Server Port or Server Password in your OBS, just make sure you update the websockets_auth.py file accordingly. Then create a text source in OBS called "RACES LEFT" - the code will update this text source to display how many save states are left. If you don't want to use any of this OBS stuff, just set the USING_OBS_WEBSOCKETS variable to false.

4) Make sure that the hotkeys in your emulator match the hotkeys in the code. Specifically, numbers 0-9 should activate different save states, F5 should save the current active save state, F7 should load the current active save state.

## Using the App

1) Run `n64_shuffler.py'

2) Once it's running, press spacebar to begin the countdown.

3) At this point the code will "shuffle" to a new save state every 2 to 20 seconds. 

4) When you've "finished" with one of the save states, press spacebar. It will mark that state as finished and remove it from the list. You can repeat this until there are no more states left.
