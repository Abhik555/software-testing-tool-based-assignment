from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class RegisterPage(BasePage):
    URL = "https://parabank.parasoft.com/parabank/register.htm"
    
    # Locators
    FIRST_NAME = (By.ID, "customer.firstName")
    LAST_NAME = (By.ID, "customer.lastName")
    STREET = (By.ID, "customer.address.street")
    CITY = (By.ID, "customer.address.city")
    STATE = (By.ID, "customer.address.state")
    ZIP_CODE = (By.ID, "customer.address.zipCode")
    PHONE = (By.ID, "customer.phoneNumber")
    SSN = (By.ID, "customer.ssn")
    USERNAME = (By.ID, "customer.username")
    PASSWORD = (By.ID, "customer.password")
    CONFIRM_PASSWORD = (By.ID, "repeatedPassword")
    REGISTER_BUTTON = (By.XPATH, "//input[@value='Register']")
    SUCCESS_MESSAGE = (By.XPATH, "//div[@id='rightPanel']/p")
    FIRST_NAME_ERROR = (By.ID, "customer.firstName.errors")

    def open(self):
        self.driver.get(self.URL)

    def register_user(self, data):
        if 'first_name' in data:
            self.enter_text(self.FIRST_NAME, data['first_name'])
        if 'last_name' in data:
            self.enter_text(self.LAST_NAME, data['last_name'])
        if 'street' in data:
            self.enter_text(self.STREET, data['street'])
        if 'city' in data:
            self.enter_text(self.CITY, data['city'])
        if 'state' in data:
            self.enter_text(self.STATE, data['state'])
        if 'zip_code' in data:
            self.enter_text(self.ZIP_CODE, data['zip_code'])
        if 'phone' in data:
            self.enter_text(self.PHONE, data['phone'])
        if 'ssn' in data:
            self.enter_text(self.SSN, data['ssn'])
        if 'username' in data:
            self.enter_text(self.USERNAME, data['username'])
        if 'password' in data:
            self.enter_text(self.PASSWORD, data['password'])
        if 'confirm_password' in data:
            self.enter_text(self.CONFIRM_PASSWORD, data['confirm_password'])
        
        self.click_element(self.REGISTER_BUTTON)

    def get_success_message(self):
        return self.get_text(self.SUCCESS_MESSAGE)

    def get_first_name_error(self):
        return self.get_text(self.FIRST_NAME_ERROR)
