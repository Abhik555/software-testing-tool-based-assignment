from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    URL = "https://parabank.parasoft.com/parabank/index.htm"
    # Locators
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//input[@value='Log In']")
    ERROR_TEXT = (By.CLASS_NAME, "error")
    LOGOUT_LINK = (By.LINK_TEXT, "Log Out")

    def open(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
    
    def get_error_message(self):
        return self.get_text(self.ERROR_TEXT)

    def is_logged_in(self):
        try:
            self.find_element(self.LOGOUT_LINK)
            return True
        except:
            return False
