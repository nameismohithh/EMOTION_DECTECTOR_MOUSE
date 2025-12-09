import time
import pandas as pd
from pynput import mouse
import os

mood = input("Enter emotion label (calm/focused/stressed/angry etc.): ").strip()

events = []  # event_type, timestamp, x, y, is_click, mood

print("\nMove the mouse according to the emotion you entered.")
print("RIGHT CLICK once to stop.\n")

def on_move(x, y):
    events.append(['move', time.time(), x, y, 0, mood])

def on_click(x, y, button, pressed):
    if pressed:
        events.append(['click', time.time(), x, y, 1, mood])
        if button == mouse.Button.right:
            return False

with mouse.Listener(on_move=on_move, on_click=on_click) as listener:
    listener.join()

if events:
    df = pd.DataFrame(events, columns=['event_type', 'timestamp', 'x', 'y', 'is_click', 'mood'])
    file_exists = os.path.exists("mouse_raw_data.csv")
    df.to_csv("mouse_raw_data.csv", mode='a' if file_exists else 'w',
              header=not file_exists, index=False)
    print(f"Saved {len(events)} events to mouse_raw_data.csv")
else:
    print("No events were recorded.")
