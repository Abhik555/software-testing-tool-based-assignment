import pytest
from pages.login_page import LoginPage

class TestLogin:
    
    @pytest.mark.ep
    def test_valid_login(self, driver):
        """
        Maps to TC_04. Tests valid equivalence partition.
        """
        login_page = LoginPage(driver)
        login_page.open()
        
        # Using default demo credentials
        login_page.login("john", "demo")
        assert login_page.is_logged_in(), "User failed to login with valid credentials"

    @pytest.mark.ep
    def test_invalid_password(self, driver):
        """
        Maps to TC_05. Tests invalid equivalence partition.
        """
        login_page = LoginPage(driver)
        login_page.open()
        
        login_page.login("john", "wrong_password")
        error_msg = login_page.get_error_message()
        assert "The username and password could not be verified" in error_msg
