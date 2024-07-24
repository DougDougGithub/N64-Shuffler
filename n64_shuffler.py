import random
import time
import keyboard
import threading
import sys
from rich import print
from audio_player import AudioManager
from obs_websockets import OBSWebsocketsManager

# P64 save states work a bit differently from other emulators:
# There is an "active save slot" at any given time
# You press 0-9 to swap to a different active slot
# F5 saves the state to the current active slot, F7 loads state from the active slot

MINIMUM_SLOT_TIME = 2 # The minimum time we'll play a specific save slot
MAXIMUM_SLOT_TIME = 20 # The minimum time we'll play a specific save slot

# If this is set to true, the program will display the # of remaining races in OBS
# If you don't want to bother with OBS, just set this to false
# Note that you will need to activate the OBS Websockets server for this to work
USING_OBS_WEBSOCKETS = True 
OBS_TEXT_SOURCE = "RACES LEFT" # Name this whatever text element you want to be updated in OBS

remaining_slots = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
current_slot = None  # The current game slot
previous_slot = None  # The previous game slot
multiple_slots_remain = True
audio_manager = AudioManager()
if USING_OBS_WEBSOCKETS:
    try:
        obswebsockets_manager = OBSWebsocketsManager()
    except:
        print("\n\n[red italic]OBS is not open or websockets aren't enabled. Try opening OBS.\n")
        time.sleep(5)
        exit()
stop_thread = threading.Event()
sleep_time = 0.1  # Amount of time to sleep, in seconds
last_swap = 0  # The time when the last game swap happened
last_spacebar = 0  # The time when the last spacebar interrupt occurred
SPACEBAR_COOLDOWN = 2  # Cooldown time for the spacebar interrupt, in seconds

def swap_game():
    global last_swap, current_slot, previous_slot, multiple_slots_remain
    
    # Update OBS text
    if USING_OBS_WEBSOCKETS:
        obswebsockets_manager.set_text(OBS_TEXT_SOURCE, f"SPEEDRUNS LEFT: {len(remaining_slots)}")

    # Swap to new slot
    if len(remaining_slots) > 1: # If there's at least 2 unfinished slots, load a new random slot
        while True: # Pick new random slot that isn't the same as previous
            current_slot = random.choice(remaining_slots)
            if current_slot != previous_slot:
                previous_slot = current_slot
                break
        keyboard.press(current_slot) # Swap to new active slot
        time.sleep(0.05)
        keyboard.release(current_slot)
        keyboard.press('F7') # Load the state in the active slot
        time.sleep(0.1)
        keyboard.release('F7')
        print(f"\nSWAPPING TO SLOT {current_slot}!")
    elif len(remaining_slots) == 1 and multiple_slots_remain: # If this is the first time we've gotten to the last slot, we swap to it, then set a flag so that we don't swap again
         multiple_slots_remain = False
         current_slot = random.choice(remaining_slots)
         audio_manager.play_audio("Final Speedrun.mp3",False,False)
         keyboard.press(current_slot) # Swap to new active slot
         time.sleep(0.05)
         keyboard.release(current_slot)
         keyboard.press('F7') # Load the state in the active slot
         time.sleep(0.1)
         keyboard.release('F7')
         print(f"\nSWAPPING TO SLOT {current_slot}!")
    elif len(remaining_slots) == 0: # Challenge completed!
        audio_manager.play_audio("You Have Completed The Challenge.mp3",False,False)
        time.sleep(60)
        sys.exit()

    last_swap = time.time()  # Store the current time
    print(f"Remaining Slots: {remaining_slots}\n")

    # Wait random amount of time
    random_time = random.randint(MINIMUM_SLOT_TIME, MAXIMUM_SLOT_TIME) * (1/sleep_time)  # Multiply by inverse of sleep_time. We do this so that we can run this function every 0.1 seconds instead of every second, to make it feel more responsive
    for i in range(int(random_time)):  # Make sure to cast to an int, as it could be a float
        if stop_thread.is_set():
            break
        time.sleep(sleep_time)

    # Save the slot
    keyboard.press('F5')

    time.sleep(0.1) # Wait 0.1 seconds inbetween save->load, so that P64 can process it

# Runs on separate thread and alerts swap_game() if spacebar is pressed
def keyboard_listener():
    global last_spacebar, current_slot
    while True:
        if keyboard.is_pressed('space'):
            if time.time() - last_swap >= 1 and time.time() - last_spacebar >= SPACEBAR_COOLDOWN:  # Check if enough time has passed since the last game swap, and if enough time has passed since the last spacebar interrupt
                last_spacebar = time.time()  # Store the current time
                if current_slot and current_slot in remaining_slots:
                    remaining_slots.remove(current_slot)  # Remove current_slot from unfinished_slots
                    print(f"Removed {current_slot} from unfinished_slots")
                stop_thread.set()  # Signal the other thread to stop
                if len(remaining_slots) > 1:
                    # This plays anytime you remove a run from the list
                    # Feel free to change this to whatever sound you want
                    audio_manager.play_audio("Speedrun Complete.mp3",False,False)
                break
        time.sleep(0.05)

######################################################################

print("\nPRESS SPACEBAR TO BEGIN!")
audio_manager.play_audio("Press Spacebar To Begin.mp3", False)
keyboard.wait('space')

audio_manager.play_audio("Starting in 3 2 1.mp3", False)
countdown = 3
while countdown > 0:
    print(f"\nSTARTING IN {countdown}")
    countdown -= 1
    time.sleep(1)

while True:
    stop_thread.clear()
    listener = threading.Thread(target=keyboard_listener)
    listener.start()

    swap_game()

    while listener.is_alive():  
        # the listener thread is still waiting for the space bar, so let's start a new game
        stop_thread.clear()
        swap_game()
