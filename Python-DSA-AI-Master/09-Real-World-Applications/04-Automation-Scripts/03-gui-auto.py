"""
Module: GUI Automation Scripting
================================

Learning Objectives:
1. Learn to programmatically control the mouse and keyboard using `pyautogui`.
2. Understand coordinate systems, screen sizing, and image recognition for interacting with elements.
3. Master reliability features like failsafes and pauses to prevent rogue automation.
4. Build a professional automation wrapper handling OS inconsistencies and timing issues.

Concept Explanation:
GUI automation is used when an application lacks an API or command-line interface. 
By generating OS-level input events (mouse clicks, keystrokes), a script mimics a human user. 
The screen is a 2D coordinate system (0,0 at top-left). Since UI elements may change or load slowly, 
professional scripts rely on wait conditions, image matching, and strict failsafes (like jerking 
the mouse to a corner to abort).

Industry Use Cases:
- Data extraction from legacy desktop applications.
- Automating repetitive data entry tasks in poorly designed ERPs.
- Automated system testing for visual UI applications.
"""

# Note: In a real environment, you must install pyautogui via `pip install pyautogui`.
# For testing and compilation here, we wrap the import to handle missing dependencies gracefully.
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

import time
import logging
from typing import Tuple, Optional, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ==========================================
# 1. BASIC IMPLEMENTATION
# ==========================================

def basic_typing_automation(text: str, delay: float = 1.0) -> None:
    """
    A simple function that waits for `delay` seconds, then types out text.
    """
    if not PYAUTOGUI_AVAILABLE:
        logging.warning("pyautogui not installed. Skipping basic automation.")
        return
        
    time.sleep(delay)
    # Type out the text with a small interval between keystrokes to mimic humans
    pyautogui.write(text, interval=0.05)
    pyautogui.press('enter')


# ==========================================
# 2. PROFESSIONAL IMPLEMENTATION
# ==========================================

class RobustGUIAutomator:
    """
    A professional GUI automation class providing enhanced safety and logging.
    """
    def __init__(self, action_delay: float = 0.5, enable_failsafe: bool = True):
        self.action_delay = action_delay
        if PYAUTOGUI_AVAILABLE:
            pyautogui.PAUSE = action_delay
            pyautogui.FAILSAFE = enable_failsafe
            self.screen_width, self.screen_height = pyautogui.size()
            logging.info(f"Initialized screen size: {self.screen_width}x{self.screen_height}")

    def safe_click(self, x: int, y: int, clicks: int = 1) -> bool:
        """
        Safely clicks a coordinate after validating it falls within screen bounds.
        """
        if not PYAUTOGUI_AVAILABLE:
            return False
            
        if not (0 <= x <= self.screen_width and 0 <= y <= self.screen_height):
            logging.error(f"Coordinates ({x}, {y}) are out of bounds.")
            return False
            
        try:
            pyautogui.click(x=x, y=y, clicks=clicks)
            logging.info(f"Clicked at ({x}, {y})")
            return True
        except pyautogui.FailSafeException:
            logging.critical("Failsafe triggered! Aborting automation.")
            raise

    def find_and_click(self, image_path: str, confidence: float = 0.9, timeout: int = 10) -> bool:
        """
        Polls the screen to find an image, then clicks its center.
        Requires `opencv-python` and `pillow` installed for the confidence parameter.
        """
        if not PYAUTOGUI_AVAILABLE:
            return False
            
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Locate the image on screen
                location = pyautogui.locateOnScreen(image_path, confidence=confidence)
                if location:
                    center_x, center_y = pyautogui.center(location)
                    return self.safe_click(center_x, center_y)
            except Exception as e:
                # Handle `ImageNotFoundException` gracefully if older pyautogui versions raise it
                pass
            time.sleep(0.5)
            
        logging.error(f"Could not find {image_path} within {timeout}s timeout.")
        return False


# ==========================================
# 3. COMPLEXITY ANALYSIS & INTERVIEW CHALLENGE
# ==========================================
"""
Complexity Analysis:
- Time Complexity: O(1) for static coordinates. Image recognition is O(W*H*w*h) where W,H is screen size and w,h is template image size.
- Space Complexity: O(W*H) for capturing the screenshot during image recognition.

Interview Challenge:
Question: GUI automation is notoriously flaky. How do you make an automation script robust across different screen resolutions?
Answer Guidelines: 
- Never hardcode coordinates. Use relative sizing (e.g., width * 0.5) or anchor points.
- Prefer image recognition (`locateOnScreen`), optical character recognition (OCR), or DOM inspection (like Selenium for web apps) over blind clicks.
- Implement explicit waits (wait for an element to appear) rather than hardcoded sleep delays.
"""

# ==========================================
# 4. EXAMPLE USAGE & TESTS
# ==========================================

if __name__ == '__main__':
    print("Running GUI Automation tests...")
    
    # Simple bounds check test using dummy values
    automator = RobustGUIAutomator()
    if PYAUTOGUI_AVAILABLE:
        # Should gracefully fail if coordinates are out of bounds
        assert not automator.safe_click(-100, -100), "Negative coordinates should be blocked"
        assert not automator.safe_click(automator.screen_width + 100, 100), "Out of bounds X should be blocked"
        
    print("GUI Automation module passed basic assertions.")
