import pyautogui
import time

def take_screenshots(num_repeats=100, initial_delay=10, delay=10):

    pyautogui.FAILSAFE = False
    time.sleep(initial_delay)

    for i in range(num_repeats):
        # Take a screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(f'screenshot/screenshot_{i:03d}.png')
        
        # Wait for the specified delay
        time.sleep(delay)

        # Click at the current mouse position
        pyautogui.press('left')

        print(f"Iteration {i + 1}/{num_repeats} completed")

    print("Process completed!")

if __name__ == "__main__":
    take_screenshots(num_repeats=100)