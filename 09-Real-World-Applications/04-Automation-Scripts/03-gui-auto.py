"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (GUI AUTOMATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A company uses a legacy 1990s accounting software that does not have an API, 
# does not have a database connection, and cannot export to CSV. To transfer 
# 500 invoices into the new web system, a junior clerk must manually click 
# "File -> Copy", switch windows, and click "Paste" 500 times. It takes 2 weeks.
#
# A senior engineer installs `PyAutoGUI`. They mathematically program the Python 
# script to seize control of the physical mouse and keyboard via OS-level hardware 
# interrupts. The script locates the exact (X, Y) pixel coordinates of the 
# "Copy" button on the screen using image recognition, clicks it, switches windows, 
# and pastes the data. It transfers all 500 invoices flawlessly in 4 minutes 
# while the engineer gets coffee.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master OS-level hardware interception via PyAutoGUI.
# - Understand the X,Y coordinate geometry of modern monitors.
# - Execute algorithmic keystrokes and fail-safe mechanisms.
#
# ==============================================================================
"""

import time
import sys

# Gracefully handle missing pyautogui dependency
try:
    import pyautogui
    HAS_GUI = True
except ImportError:
    HAS_GUI = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MATHEMATICAL GEOMETRY OF THE MONITOR
# ==============================================================================
# The screen is a mathematical grid.
# (0,0) is the absolute TOP-LEFT corner of the primary monitor.
# X increases to the Right.
# Y increases Downwards.

def demonstrate_screen_geometry():
    section_header("Hardware Interception: Screen Geometry")
    
    if not HAS_GUI:
        print("  [ERROR] PyAutoGUI is not installed.")
        print("  Run `pip install pyautogui` to execute this lab locally.")
        return
        
    # We dynamically query the Operating System for the exact resolution!
    width, height = pyautogui.size()
    print(f"  [METRICS] Active Monitor Resolution: {width}x{height}")
    
    # We query the exact current location of the physical mouse!
    current_x, current_y = pyautogui.position()
    print(f"  [METRICS] Current Mouse Position: X:{current_x} Y:{current_y}")


# ==============================================================================
# 4. THE AUTOMATION SCRIPT (ROBOTIC EXECUTION)
# ==============================================================================
def execute_robotic_automation():
    section_header("Robotic Execution: Mouse and Keyboard Takeover")
    
    if not HAS_GUI:
        print("  [SIMULATION] We will mathematically simulate what the script would do.")
        print("    -> Move mouse to (500, 500) over 1.0 seconds.")
        print("    -> Type 'Hello, World!' at 0.1s per keystroke.")
        print("    -> Press 'Enter' key.")
        return
        
    print("  [WARNING] Python is about to seize control of your physical mouse!")
    print("  *** FAILSAFE: Slam the mouse to any of the 4 CORNERS of the screen to abort! ***")
    
    # We give the user 3 seconds to read the warning!
    for i in range(3, 0, -1):
        print(f"  Starting in {i}...")
        time.sleep(1)
        
    try:
        # --- 1. MOUSE MOVEMENT ---
        print("\n  [ACTION 1] Moving the mouse mathematically...")
        # (X, Y, Duration) - The duration ensures the movement is smooth (human-like),
        # not instantly teleporting, which often crashes legacy UI systems!
        pyautogui.moveTo(500, 500, duration=1.0)
        
        # --- 2. CLICKING ---
        print("  [ACTION 2] Executing Left Click...")
        pyautogui.click() # Clicks exactly where the mouse currently is
        
        # --- 3. KEYBOARD INJECTION ---
        print("  [ACTION 3] Injecting Keystrokes...")
        # `interval=0.1` adds a 100ms delay between every letter, perfectly
        # simulating a human typing 120 Words Per Minute.
        pyautogui.write("Hello from the Python Automation Script!", interval=0.05)
        
        # --- 4. HARDWARE KEYS ---
        print("  [ACTION 4] Pressing hardware keys...")
        pyautogui.press('enter')
        
        # Hotkeys (e.g., CTRL + C, CTRL + V)
        # pyautogui.hotkey('ctrl', 'c') 
        
        print("\n  [SUCCESS] Control returned to human operator.")
        
    except pyautogui.FailSafeException:
        # This catches the catastrophic abort if the user slammed the mouse to the corner!
        print("\n  [ABORT] FailSafe Triggered! Automation instantly terminated.")


def run_all_labs():
    demonstrate_screen_geometry()
    execute_robotic_automation()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why is 'Teleporting' the mouse instantly using `pyautogui.moveTo(500, 500)` dangerous when automating legacy applications?"
   Senior Answer: "Many legacy operating systems and $1990$s GUI frameworks rely on internal 'Hover' states or OS-level event queues (like `MouseMoveEvent`) to calculate focus. If Python mathematically teleports the cursor from $(0,0)$ to $(500,500)$ in $0.00$ milliseconds, the legacy application never receives the intermediate coordinate packets. It physically doesn't realize the mouse is hovering over the button, so when Python executes `pyautogui.click()`, the application ignores it. By adding `duration=0.5` (a half-second), Python mathematically interpolates the path, bombarding the OS with intermediate coordinates (e.g., $(250,250)$), forcing the legacy application to correctly register the hover state before the click executes."

2. Interviewer: "What is the PyAutoGUI Fail-Safe, and why is it architecturally mandatory?"
   Senior Answer: "When Python takes control of the physical mouse and keyboard, it does so at the OS interrupt level. If a developer accidentally writes an infinite `while True` loop that rapidly clicks the center of the screen, the human operator physically cannot regain control. They cannot click the 'Stop' button in their IDE because Python instantly steals the mouse back every millisecond. The only way to stop the script would be to pull the physical power plug out of the wall. PyAutoGUI's Fail-Safe solves this. Before executing *any* command, the C-level library checks the current mouse $(X,Y)$. If $X=0$ or $Y=0$ (the user violently slammed the mouse into the physical corner of the monitor), the library intentionally crashes the Python interpreter via a `FailSafeException`, immediately severing the hardware lock."

3. Interviewer: "If a button is located at $(500, 500)$ on your $1080$p monitor, but the script is deployed to a $4K$ server monitor, what happens to the automation?"
   Senior Answer: "It catastrophically fails. Hardcoding exact $(X, Y)$ pixel coordinates creates 'Resolution Dependency'. On a $4K$ monitor, coordinate $(500, 500)$ might be an empty white space, meaning the script will blindly click nothing. Senior automation engineers never hardcode coordinates. They use PyAutoGUI's Image Recognition (`pyautogui.locateCenterOnScreen('submit_button.png')`). The library uses the OpenCV C++ engine to mathematically scan the current monitor's RGB matrix, locate the exact pixels matching the PNG file regardless of resolution or monitor size, calculate the dynamic $(X,Y)$ center of that specific bounding box, and click it flawlessly."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Automation (GUI Interception) Completed.")
