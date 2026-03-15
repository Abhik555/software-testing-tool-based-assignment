import pytest
from pages.loan_page import LoanPage
from pages.login_page import LoginPage

class TestLoan:
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("john", "demo")

    @pytest.mark.bva
    @pytest.mark.parametrize("loan_amt, down_pmt, expected_status", [
        ("1000", "99", "Denied"),   # TC_01 
        ("1000", "100", "Approved") # TC_02
    ])
    def test_loan_approval_bva(self, driver, loan_amt, down_pmt, expected_status):
        """
        Maps to TC_01 and TC_02. Parameterized BVA for loan decision table.
        """
        loan_page = LoanPage(driver)
        loan_page.open()
        loan_page.apply_for_loan(loan_amt, down_pmt)
        
        status = loan_page.get_loan_status()
        assert status == expected_status
