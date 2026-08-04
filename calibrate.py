import ctypes
import json
import time
import winsound
from pathlib import Path
import pyautogui

CALIBRATION_FILE = Path(__file__).parent / "calibration.json"
VK_SPACE = 0x20  # Virtual key code for Spacebar

# returns True if the spacebar is currently pressed down anywhere on system
def is_space_pressed():
    return (ctypes.windll.user32.GetAsyncKeyState(VK_SPACE) & 0x8000) != 0

# waits for user to press Spacebar returns mouse position (x, y)
def wait_for_space():
    # Wait until spacebar is released if it's currently held
    while is_space_pressed():
        time.sleep(0.05)

    # Wait for spacebar press
    while not is_space_pressed():
        time.sleep(0.02)

    x, y = pyautogui.position()
    
    # Audio feedback confirmation beep (Hz, ms)
    winsound.Beep(1000, 150)
    
    # Wait until spacebar is released
    while is_space_pressed():
        time.sleep(0.05)

    return x, y

def calibrate():
    print("=" * 60)
    print("MINESWEEPER CALIBRATION TOOL")
    print("=" * 60)
    print("Instructions:")
    print("Hover your mouse over the corner in your browser & press SPACEBAR!")
    print("You will hear a confirmation BEEP for each press.\n")

    print("[STEP 1/2] Hover mouse over TOP-LEFT corner of board grid & press SPACEBAR...")
    x1, y1 = wait_for_space()
    print(f"   ---> Top-Left recorded at: ({x1}, {y1})\n")

    time.sleep(0.3)

    print("[STEP 2/2] Hover mouse over BOTTOM-RIGHT corner of board grid & press SPACEBAR...")
    x2, y2 = wait_for_space()
    print(f"   ---> Bottom-Right recorded at: ({x2}, {y2})\n")

    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    cal_data = {
        "left": left,
        "top": top,
        "width": width,
        "height": height
    }

    with open(CALIBRATION_FILE, "w") as f:
        json.dump(cal_data, f, indent=4)

    # Double victory beep
    winsound.Beep(1200, 150)
    winsound.Beep(1500, 200)

    print("=" * 60)
    print(f"Saved to calibration.json:")
    print(f" {json.dumps(cal_data)}")
    print("=" * 60)

if __name__ == "__main__":
    calibrate()
