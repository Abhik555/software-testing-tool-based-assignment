from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from pages.base_page import BasePage

class LoanPage(BasePage):
    URL = "https://parabank.parasoft.com/parabank/requestloan.htm"
    
    # Locators
    LOAN_AMOUNT_INPUT = (By.ID, "amount")
    DOWN_PAYMENT_INPUT = (By.ID, "downPayment")
    FROM_ACCOUNT_DROPDOWN = (By.ID, "fromAccountId")
    APPLY_BUTTON = (By.XPATH, "//input[@value='Apply Now']")
    STATUS_TEXT = (By.ID, "loanStatus")

    def open(self):
        self.driver.get(self.URL)

    def apply_for_loan(self, amount, down_payment):
        self.enter_text(self.LOAN_AMOUNT_INPUT, str(amount))
        self.enter_text(self.DOWN_PAYMENT_INPUT, str(down_payment))
        
        time.sleep(1) # Dropdown population wait
        
        try:
            from_select = Select(self.find_element(self.FROM_ACCOUNT_DROPDOWN))
            if len(from_select.options) > 0:
                from_select.select_by_index(0)
        except:
            pass
            
        self.click_element(self.APPLY_BUTTON)

    def get_loan_status(self):
        # Returns: Approved or Denied
        return self.get_text(self.STATUS_TEXT)
