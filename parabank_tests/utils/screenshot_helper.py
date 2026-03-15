import os

def take_screenshot(driver, name):
    os.makedirs('screenshots', exist_ok=True)
    screenshot_path = os.path.join('screenshots', f"{name}.png")
    driver.save_screenshot(screenshot_path)
    return screenshot_path
