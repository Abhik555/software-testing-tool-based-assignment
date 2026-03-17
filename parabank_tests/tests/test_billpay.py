import pytest
from pages.billpay_page import BillPayPage
from pages.login_page import LoginPage
import time

class TestBillPay:
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("john", "demo")

    @pytest.mark.bva
    def test_bill_pay_zero_amount(self, driver):
        """
        Maps to TC_03. Tests BVA $0 bug. 
        """
        billpay_page = BillPayPage(driver)
        billpay_page.open()
        time.sleep(2)
        
        billpay_page.pay_bill(0.00)
        
        success = billpay_page.get_success_message()
        
        assert "Complete" not in success, "Bill Pay processed with 0 amount!"
    
    @pytest.mark.bva
    def test_bill_pay_normal(self , driver):
        billpay_page = BillPayPage(driver)
        billpay_page.open()
        time.sleep(2)
        
        billpay_page.pay_bill(100)
        
        success = billpay_page.get_success_message()
        
        assert "Complete" in success , "Bill pay not processed"