# Comprehensive Test Execution Guide for ParaBank

This document breaks down exactly how the Selenium framework works under the hood, from the moment [pytest](file:///c:/Users/Abthedev/OneDrive%20-%20BENNETT%20UNIVERSITY/BU%206th%20Semester/Software%20Testing%20Tool%20based%20assignment/V2/parabank_tests/conftest.py#14-23) is executed to the final test completion, using the test scripts as examples.

## Phase 1: Test Initialization & Setup ([conftest.py](file:///c:/Users/Abthedev/OneDrive%20-%20BENNETT%20UNIVERSITY/BU%206th%20Semester/Software%20Testing%20Tool%20based%20assignment/V2/parabank_tests/conftest.py) & [driver_factory.py](file:///c:/Users/Abthedev/OneDrive%20-%20BENNETT%20UNIVERSITY/BU%206th%20Semester/Software%20Testing%20Tool%20based%20assignment/V2/parabank_tests/utils/driver_factory.py))

When you run `uv run pytest`, Pytest first looks for a [conftest.py](file:///c:/Users/Abthedev/OneDrive%20-%20BENNETT%20UNIVERSITY/BU%206th%20Semester/Software%20Testing%20Tool%20based%20assignment/V2/parabank_tests/conftest.py) file to load global fixtures. 

1. **`@pytest.fixture(scope="function") def driver(request):`** 
   - Before *every single test*, Pytest triggers this fixture. 
   - It calls `DriverFactory.get_driver()`.
2. **`DriverFactory.get_driver()`** 
   - This method utilizes `webdriver-manager` to silently download the correct version of ChromeDriver that matches your computer's installed Google Chrome browser.
   - It initializes `webdriver.Chrome()`, applying the `--window-size=1920,1080` option to ensure a consistent viewport so elements don't get hidden behind dynamic mobile CSS. 
   - Pytest `yield`s this fresh, maximized browser instance to the test method.

## Phase 2: Page Object Interactivity ([base_page.py](file:///c:/Users/Abthedev/OneDrive%20-%20BENNETT%20UNIVERSITY/BU%206th%20Semester/Software%20Testing%20Tool%20based%20assignment/V2/parabank_tests/pages/base_page.py))

Every page in our framework (e.g., [LoginPage](file:///c:/Users/Abthedev/OneDrive%20-%20BENNETT%20UNIVERSITY/BU%206th%20Semester/Software%20Testing%20Tool%20based%20assignment/V2/parabank_tests/pages/login_page.py#4-30), [TransferPage](file:///c:/Users/Abthedev/OneDrive%20-%20BENNETT%20UNIVERSITY/BU%206th%20Semester/Software%20Testing%20Tool%20based%20assignment/V2/parabank_tests/pages/transfer_page.py#6-41)) inherits from [BasePage](file:///c:/Users/Abthedev/OneDrive%20-%20BENNETT%20UNIVERSITY/BU%206th%20Semester/Software%20Testing%20Tool%20based%20assignment/V2/parabank_tests/pages/base_page.py#4-24), giving them access to core Selenium interactions wrapped with **Explicit Waits**.

*Why this matters:* Web pages don't load instantly. If Selenium tries to click a button before the browser finishes rendering it, it throws exceptions (like the `TimeoutException` or `NoSuchElement`).

Let's look at a core method in [base_page.py](file:///c:/Users/Abthedev/OneDrive%20-%20BENNETT%20UNIVERSITY/BU%206th%20Semester/Software%20Testing%20Tool%20based%20assignment/V2/parabank_tests/pages/base_page.py):

```python
def click_element(self, locator):
    element = self.wait.until(EC.element_to_be_clickable(locator))
    element.click()
```
- **`locator`:** A tuple containing the strategy and value, like [(By.ID, "login-btn")](file:///c:/Users/Abthedev/OneDrive%20-%20BENNETT%20UNIVERSITY/BU%206th%20Semester/Software%20Testing%20Tool%20based%20assignment/V2/parabank_tests/pages/register_page.py#23-25).
- **`self.wait.until`:** The framework uses `WebDriverWait(driver, 15)`. It will actively poll the browser's DOM for up to 15 seconds.
- **`EC.element_to_be_clickable`:** It specifically waits until the element is physically present, visible, *and* not covered by other elements before doing `.click()`.

## Phase 3: Test Execution Example ([test_loan.py](file:///c:/Users/Abthedev/OneDrive%20-%20BENNETT%20UNIVERSITY/BU%206th%20Semester/Software%20Testing%20Tool%20based%20assignment/V2/parabank_tests/tests/test_loan.py))

Let's break down [test_loan_approval_bva](file:///c:/Users/Abthedev/OneDrive%20-%20BENNETT%20UNIVERSITY/BU%206th%20Semester/Software%20Testing%20Tool%20based%20assignment/V2/parabank_tests/tests/test_loan.py#13-28) line by line:

```python
@pytest.fixture(autouse=True)
def setup(self, driver):
```
**Setup Block:** Before the loan test starts, it inherently requires a logged-in user. The `autouse=True` fixture automatically runs, instantiating [LoginPage](file:///c:/Users/Abthedev/OneDrive%20-%20BENNETT%20UNIVERSITY/BU%206th%20Semester/Software%20Testing%20Tool%20based%20assignment/V2/parabank_tests/pages/login_page.py#4-30), navigating to the URL, and securely logging in as "john/demo".

```python
@pytest.mark.parametrize("loan_amt, down_pmt, expected_status", [ ... ])
def test_loan_approval_bva(self, driver, loan_amt, down_pmt, expected_status):
```
**Parameterization:** This decorator tells Pytest to run this exact test method multiple times. The first time, `loan_amt` gets "1000", `down_pmt` gets "99", and `expected_status` gets "Denied". The second time, variables are populated with the approved values.

```python
    loan_page = LoanPage(driver)
    loan_page.open()
```
**Page Navigation:** We instantiate the [LoanPage](file:///c:/Users/Abthedev/OneDrive%20-%20BENNETT%20UNIVERSITY/BU%206th%20Semester/Software%20Testing%20Tool%20based%20assignment/V2/parabank_tests/pages/loan_page.py#6-37) model using the active driver, and `.open()` commands the browser to navigate to the `requestloan.htm` endpoint.

```python
    loan_page.apply_for_loan(loan_amt, down_pmt)
```
**Action:** The test hands control to the POM. Inside [apply_for_loan](file:///c:/Users/Abthedev/OneDrive%20-%20BENNETT%20UNIVERSITY/BU%206th%20Semester/Software%20Testing%20Tool%20based%20assignment/V2/parabank_tests/pages/loan_page.py#19-33):
- `self.enter_text(self.LOAN_AMOUNT_INPUT, str(amount))` locates the text box and types the amount.
- `time.sleep(1)` acts as a microscopic network buffer. ParaBank makes an internal AJAX request to load the users' Accounts into a dropdown list.
- `from_select.select_by_index(0)` utilizes Selenium's `Select` class to choose the very first account from the dropdown. 
- `self.click_element` submits the form.

```python
    status = loan_page.get_loan_status()
    assert status == expected_status
```
**Validation:** We extract the resulting textual status from the DOM (e.g., "Denied"). The `assert` statement is the heart of the test; if [status](file:///c:/Users/Abthedev/OneDrive%20-%20BENNETT%20UNIVERSITY/BU%206th%20Semester/Software%20Testing%20Tool%20based%20assignment/V2/parabank_tests/pages/loan_page.py#34-37) does not equal `expected_status` (e.g., the system approved a loan it shouldn't have), Pytest immediately registers a failure.

## Phase 4: Test Teardown and Reporting

Once the `assert` statement finishes (evaluating to pass or fail):

1. **Failure Hook ([check_test_result](file:///c:/Users/Abthedev/OneDrive%20-%20BENNETT%20UNIVERSITY/BU%206th%20Semester/Software%20Testing%20Tool%20based%20assignment/V2/parabank_tests/conftest.py#24-37)):**
   - If the assertion failed, Pytest triggers our custom hook in [conftest.py](file:///c:/Users/Abthedev/OneDrive%20-%20BENNETT%20UNIVERSITY/BU%206th%20Semester/Software%20Testing%20Tool%20based%20assignment/V2/parabank_tests/conftest.py).
   - It captures the literal pixel state of the browser display via `driver.save_screenshot()` and stamps the file with the current `datetime`.

2. **Clean Up (`yield` return):**
   - Control returns to the [driver](file:///c:/Users/Abthedev/OneDrive%20-%20BENNETT%20UNIVERSITY/BU%206th%20Semester/Software%20Testing%20Tool%20based%20assignment/V2/parabank_tests/conftest.py#7-13) fixture in [conftest.py](file:///c:/Users/Abthedev/OneDrive%20-%20BENNETT%20UNIVERSITY/BU%206th%20Semester/Software%20Testing%20Tool%20based%20assignment/V2/parabank_tests/conftest.py).
   - `driver_instance.quit()` is executed. This natively severs the connection to the Chrome executable and destroys the temporary browser profile, ensuring memory is freed.

3. **Report Generation (`pytest-html`):**
   - After all parameterized instances finish, Pytest aggregates the success/failure statuses.
   - Because we launched with `--html=report.html`, the `pytest-html` plugin parses the run results and structures the stylized HTML page you see in your workspace.
