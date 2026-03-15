from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from pages.base_page import BasePage

class TransferPage(BasePage):
    URL = "https://parabank.parasoft.com/parabank/transfer.htm"
    
    # Locators
    AMOUNT_INPUT = (By.ID, "amount")
    FROM_ACCOUNT_DROPDOWN = (By.ID, "fromAccountId")
    TO_ACCOUNT_DROPDOWN = (By.ID, "toAccountId")
    TRANSFER_BUTTON = (By.XPATH, "//input[@value='Transfer']")
    SUCCESS_TEXT = (By.XPATH, "//div[@id='rightPanel']/div/div/h1")
    # ParaBank silent failure: Transfer throws no error if source = destination

    def open(self):
        self.driver.get(self.URL)

    def transfer_funds(self, amount, from_idx=0, to_idx=1):
        self.enter_text(self.AMOUNT_INPUT, str(amount))
        
        # Wait for dropdown to be populated
        time.sleep(5) # ParaBank accounts load asynchronously
        
        try:
            from_select = Select(self.find_element(self.FROM_ACCOUNT_DROPDOWN))
            if from_idx < len(from_select.options):
                from_select.select_by_index(from_idx)
                
            to_select = Select(self.find_element(self.TO_ACCOUNT_DROPDOWN))
            if to_idx < len(to_select.options):
                to_select.select_by_index(to_idx)
        except:
            pass # Failsafe if not enough accounts are registered
            
        self.click_element(self.TRANSFER_BUTTON)

    def get_success_message(self):
        return self.get_text(self.SUCCESS_TEXT)
