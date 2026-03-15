import pytest
from pages.billpay_page import BillPayPage
from pages.login_page import LoginPage

class TestBillPay:
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("john", "demo")

    @pytest.mark.bva
    @pytest.mark.xfail(reason="BUG-001: System accepts $0.00 bill pay amount")
    def test_bill_pay_zero_amount(self, driver):
        """
        Maps to TC_03. Tests BVA $0 bug. 
        """
        billpay_page = BillPayPage(driver)
        billpay_page.open()
        billpay_page.pay_bill(0.00)
        
        success = billpay_page.get_success_message()
        if "Complete" in success:
            pytest.fail("BUG: System successfully processed a $0.00 bill payment")
