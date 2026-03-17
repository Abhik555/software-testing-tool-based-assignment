from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from pages.base_page import BasePage

class BillPayPage(BasePage):
    URL = "https://parabank.parasoft.com/parabank/billpay.htm"
    
    # Locators
    PAYEE_NAME = (By.NAME, "payee.name")
    PAYEE_STREET = (By.NAME, "payee.address.street")
    PAYEE_CITY = (By.NAME, "payee.address.city")
    PAYEE_STATE = (By.NAME, "payee.address.state")
    PAYEE_ZIP = (By.NAME, "payee.address.zipCode")
    PAYEE_PHONE = (By.NAME, "payee.phoneNumber")
    PAYEE_ACCOUNT = (By.NAME, "payee.accountNumber")
    VERIFY_ACCOUNT = (By.NAME, "verifyAccount")
    AMOUNT = (By.NAME, "amount")
    FROM_ACCOUNT = (By.NAME, "fromAccountId")
    SEND_BUTTON = (By.XPATH, "//input[@value='Send Payment']")
    SUCCESS_TEXT = (By.ID, "rightPanel")

    def open(self):
        self.driver.get(self.URL)

    def pay_bill(self, amount, account_number="12345"):
        self.enter_text(self.PAYEE_NAME, "Test Payee")
        self.enter_text(self.PAYEE_STREET, "123 Main St")
        self.enter_text(self.PAYEE_CITY, "Beverly Hills")
        self.enter_text(self.PAYEE_STATE, "CA")
        self.enter_text(self.PAYEE_ZIP, "90210")
        self.enter_text(self.PAYEE_PHONE, "555-1234")
        self.enter_text(self.PAYEE_ACCOUNT, account_number)
        self.enter_text(self.VERIFY_ACCOUNT, account_number)
        self.enter_text(self.AMOUNT, str(amount))
        
        time.sleep(1) # Dropdown population check
        try:
            from_select = Select(self.find_element(self.FROM_ACCOUNT))
            if len(from_select.options) > 0:
                from_select.select_by_index(0)
        except:
            pass
            
        time.sleep(2) # Stabilize DOM before clicking
        self.click_element(self.SEND_BUTTON)
        time.sleep(2) # Wait for page reload

    def get_success_message(self):
        return self.get_text(self.SUCCESS_TEXT)
