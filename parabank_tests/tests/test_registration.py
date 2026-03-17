import pytest
from pages.register_page import RegisterPage
import time

class TestRegistration:
    
    @pytest.mark.ep
    def test_invalid_registration(self, driver):
        """
        Maps to TC_06. Tests invalid Registration EP (Missing field).
        """
        register_page = RegisterPage(driver)
        register_page.open()
        
        data = {
            'last_name': 'Doe',
            'street': '123 Main',
            'city': 'LA',
            'state': 'CA',
            'zip_code': '90001',
            'phone': '1234567890',
            'ssn': '000-00-0000',
            'username': f'user_{int(time.time())}',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        register_page.register_user(data)
        error_msg = register_page.get_first_name_error()
        assert "First name is required" in error_msg

    @pytest.mark.ep
    def test_valid_registration(self, driver):
        """
        Maps to TC_07. Tests valid registration flow.
        """
        register_page = RegisterPage(driver)
        register_page.open()
        
        unique_username = f"user_{int(time.time())}"
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'street': '123 Main',
            'city': 'LA',
            'state': 'CA',
            'zip_code': '90001',
            'phone': '1234567890',
            'ssn': '000-00-0000',
            'username': unique_username,
            'password': 'password123',
            'confirm_password': 'password123'
        }
        register_page.register_user(data)
        success = register_page.get_success_message()
        assert "Your account was created successfully" in success
