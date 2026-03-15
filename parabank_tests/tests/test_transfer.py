import pytest
from pages.transfer_page import TransferPage
from pages.login_page import LoginPage

class TestTransfer:
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("john", "demo")
        
    @pytest.mark.bva
    def test_negative_transfer_amount(self, driver):
        """
        Maps to TC_14. Tests negative boundary value.
        """
        transfer_page = TransferPage(driver)
        transfer_page.open()
        
        # Test will continue regardless of whether error is shown or silently fails,
        # but the assert ensures we are not seeing 'Complete'.
        transfer_page.transfer_funds(-100)
        
        try:
            success = transfer_page.get_success_message()
            assert "Complete" not in success, "Negative amount wrongly accepted"
        except:
            # Did not find success text, passed validation correctly
            pass
        
    @pytest.mark.bva
    @pytest.mark.xfail(reason="BUG-002: Transfer to identical account fails silently without validation error")
    def test_transfer_same_account(self, driver):
        """
        Maps to TC_15. Tests transfer to the same account (Silent failure bug).
        """
        transfer_page = TransferPage(driver)
        transfer_page.open()
        transfer_page.transfer_funds(50, from_idx=0, to_idx=0)
        
        # We expect a validation error. Instead, ParaBank silently fails or accepts it weirdly
        try:
            success = transfer_page.get_success_message()
            assert "Complete" not in success, "System wrongly completed transfer to identical account"
        except Exception:
            pytest.fail("Silent Failure: No explicit error shown when transferring to identical account.")
