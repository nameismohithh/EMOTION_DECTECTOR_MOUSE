import time
import math
import threading
from collections import deque

import numpy as np
import joblib

from pynput import mouse
import tkinter as tk

model = joblib.load("mouse_mood_model.sav")
label_encoder = joblib.load("mouse_mood_label_encoder.sav")

WINDOW_SIZE = 30
buffer = deque(maxlen=WINDOW_SIZE)

prev_time = None
prev_x = None
prev_y = None

running = True
current_mood = "Detecting..."

MOOD_COLORS = {
    "calm": "#4CAF50",
    "focused": "#2196F3",
    "stressed": "#FF9800",
    "angry": "#F44336",
    "Detecting...": "#9E9E9E"
}

def predict_mood():
    if len(buffer) < 5:
        return None
    X = np.array(buffer)
    preds = model.predict(X)
    values, counts = np.unique(preds, return_counts=True)
    majority = values[counts.argmax()]
    return label_encoder.inverse_transform([majority])[0]

def on_move(x, y):
    global prev_time, prev_x, prev_y, current_mood, running
    if not running:
        return False

    t = time.time()
    if prev_time is None:
        prev_time, prev_x, prev_y = t, x, y
        return

    dt = t - prev_time
    if dt <= 0:
        return
    dx = x - prev_x
    dy = y - prev_y
    dist = math.sqrt(dx*dx + dy*dy)
    speed = dist / dt

    buffer.append([dt, dist, speed, 0])

    prev_time, prev_x, prev_y = t, x, y

    mood = predict_mood()
    if mood:
        current_mood = mood

def on_click(x, y, button, pressed):
    global running
    from pynput.mouse import Button
    if pressed and button == Button.right:
        running = False
        return False

def listener_thread():
    with mouse.Listener(on_move=on_move, on_click=on_click) as listener:
        listener.join()

def start_gui():
    global current_mood

    root = tk.Tk()
    root.title("Mouse Emotion Detector")
    root.geometry("400x250")

    mood_var = tk.StringVar()
    mood_var.set(current_mood)

    label = tk.Label(root, textvariable=mood_var, font=("Helvetica", 32, "bold"), width=20)
    label.pack(pady=40)

    def update():
        mood_var.set(current_mood)
        label.config(bg=MOOD_COLORS.get(current_mood, "#9E9E9E"), fg="white")
        if running:
            root.after(200, update)

    update()
    root.mainloop()

if __name__ == "__main__":
    t = threading.Thread(target=listener_thread, daemon=True)
    t.start()
    start_gui()
