from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 30)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click_element(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        # Scroll the element into the center of the viewport to avoid overlay interceptions
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        import time
        time.sleep(0.5) 
        element = self.wait.until(EC.element_to_be_clickable(locator))
        time.sleep(1)
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    def enter_text(self, locator, text):
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        import time
        time.sleep(0.5)
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        import time
        for _ in range(5):
            try:
                element = self.wait.until(EC.presence_of_element_located(locator))
                return element.text
            except Exception:
                time.sleep(1)
        return ""
