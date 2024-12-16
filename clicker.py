import pyautogui
import time

# Number of repetitions
num_repeats = 200

# Delay between actions (in seconds)
initial_delay = 10
delay = 10

time.sleep(initial_delay)

for i in range(num_repeats):
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save(f'screenshot_{i}.png')  # Save screenshot if needed
    
    # Wait for the specified delay
    time.sleep(delay)

    # Click at the current mouse position
    #pyautogui.click()
    pyautogui.press('left')

    print(f"Iteration {i + 1}/{num_repeats} completed")

print("Process completed!")
