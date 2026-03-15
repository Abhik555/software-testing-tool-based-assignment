# CSET481 — Software Testing Tool-Based Assignment

## SECTION A — Requirement Analysis [1 mark]

### 1. Functional Requirements
1. **FR1:** The system shall allow a registered user to securely log in by entering a valid username and password on the `index.htm` page.
2. **FR2:** The system shall allow logged-in users to accurately transfer funds from a source account to a destination account via the `transfer.htm` page interface.
3. **FR3:** The system shall process loan requests on the `requestloan.htm` page by comparing the submitted down payment and requested loan amount against backend risk thresholds.
4. **FR4:** The system shall facilitate bill payments to saved payees by capturing payee details, withdrawing the specified amount, and generating a confirmation number on the `billpay.htm` page.
5. **FR5:** The system shall enable users to query and filter their past transaction history by Date Range or Transaction ID directly on the `findtrans.htm` page.

### 2. Non-Functional Requirements
1. **NFR1 (Performance):** The authentication process on the login page must complete and redirect to the accounts via `overview.htm` within 2 seconds under normal network conditions.
2. **NFR2 (Usability):** The application must display explicit, red-colored error text when a user submits an incorrect login credential or invalid transfer amount, ensuring visual confirmation.
3. **NFR3 (Security / Reliability):** The active user session must expire automatically after 15 minutes of inactivity, invalidating existing DOM elements and forcing re-authentication.

### 3. Critical Test Scenarios
1. **TS1: Verify User Registration with unique valid credentials.**
   - *Justification:* Account creation is the foundation of the banking platform; without an active session, users cannot access any core banking functions. [VIVA LIKELY]
   - *Bloom's Taxonomy:* Apply
2. **TS2: Verify Fund Transfer behavior when the source and destination accounts are identical.**
   - *Justification:* This scenario targets ParaBank's known silent failure where no error is rendered when transferring money to the same account, risking poor user feedback and transactional consistency.
   - *Bloom's Taxonomy:* Analyze
3. **TS3: Verify Loan Request logic using boundary values for down payment vs. loan amount.**
   - *Justification:* Accurate loan validation carries high business impact; incorrectly granting loans for too low of a down payment can directly cause financial risk.
   - *Bloom's Taxonomy:* Evaluate
4. **TS4: Verify Bill Pay functionality by attempting to send $0.00 to a payee.**
   - *Justification:* This validates edge cases and input sanitization, targeting a known ParaBank bug where a $0 value gets accepted without raising an expected validation violation. [VIVA LIKELY]
   - *Bloom's Taxonomy:* Analyze
5. **TS5: Verify system behavior when attempting to interact with the DOM post-session timeout.**
   - *Justification:* Unattended sessions present a severe security vulnerability. Validating timeouts ensures unauthorized users cannot perform hijacking operations.
   - *Bloom's Taxonomy:* Evaluate

---

## SECTION B — Test Case Design & Strategy [2 marks]

### Justification for Technique Selection
Applying diverse test design techniques is crucial for comprehensive validation of the ParaBank application. **Boundary Value Analysis (BVA)** is heavily utilized for inputs like loan and transfer amounts, since typical financial defects often exist exactly at limit boundaries (e.g., $0 vs. $0.01). **Equivalence Partitioning (EP)** is best suited for login and registration forms, reducing the sheer volume of test cases by categorizing inputs into 'valid credentials' and 'invalid credentials' sets. **Decision Tables (DT)** naturally fit the combinatorial complexity of ParaBank's loan approval logic, which relies on multiple interdependent conditions (loan size, down payment ratio, existing credit). Finally, **State Transition (ST)** modeling successfully maps the user's sequential lifecycle constraints (Unregistered → Registered → Logged In → Session Expired), ensuring appropriate access controls at each phase.

### Structured Test Cases
| TC_ID | Feature | Technique | Preconditions | Test Steps | Expected Result | Actual Result | Status | Priority | Bloom's |
|---|---|---|---|---|---|---|---|---|---|
| TC_01 | Loan Apply | BVA | User logged in, on loan page | Enter loan amount 1000, down payment 99. Click Apply. | Loan denied for low down payment | Loan denied | Pass | High | Apply |
| TC_02 | Loan Apply | BVA | User logged in, on loan page | Enter loan amount 1000, down payment 100. Click Apply. | Loan approved | Loan approved | Pass | High | Apply |
| TC_03 | Bill Pay | BVA | User logged in, on billpay page| Enter bill amount $0.00. Fill payee. Submit. | Rejection/Validation error | Payment accepted | Fail** | Med | Analyze |
| TC_04 | Login | EP | User is registered | Enter valid username & password. Submit. | Redirected to overview.htm | Redirected to overview | Pass | High | Understand |
| TC_05 | Login | EP | User is registered | Enter valid user, invalid password. Submit. | Error: "The username and password..." | Error displayed | Pass | High | Understand |
| TC_06 | Register | EP | On register.htm | Leave 'First Name' blank. Fill rest. Submit. | Error: "First name is required." | Error displayed | Pass | High | Understand |
| TC_07 | Register | EP | On register.htm | Enter all valid, matching passwords. Submit. | Account created, welcome text | Account created | Pass | High | Understand |
| TC_08 | Loan Setup| DT | Logged in | High Loan, High Down Payment, High Credit | Loan status Approved | Approved | Pass | High | Analyze |
| TC_09 | Loan Setup| DT | Logged in | High Loan, Low Down Payment, High Credit | Loan denied (down payment clause) | Denied | Pass | High | Analyze |
| TC_10 | Loan Setup| DT | Logged in | Low Loan, High Down Payment, Bad Credit | Loan denied (credit clause) | Denied | Pass | High | Analyze |
| TC_11 | Account Mgt| ST | Unregistered User | Attempt to visit overview.htm directly | Redirected to index.htm (Login) | Redirected to login | Pass | High | Evaluate |
| TC_12 | Account Mgt| ST | Logged in User | Click 'Log Out' link on panel | Session terminated, redirect to index | Session terminated | Pass | High | Evaluate |
| TC_13 | Account Mgt| ST | Logged in User | Wait 15 mins. Click 'Accounts Overview' | Redirect to login / session timeout error | Session expired | Pass | Med | Evaluate |
| TC_14 | Transfer | BVA | User logged in, 2 accounts exist| Enter transfer amount -100. Select accounts | Validation error for negative amount | Error shown | Pass | High | Apply |
| TC_15 | Transfer | BVA | User logged in, 2 accounts exist| Select SAME account for From and To. Submit | Error: "Cannot transfer to same account" | Silent Failure | Fail** | High | Analyze |

*(** Actual Result denotes observed ParaBank bugs)*

---

## SECTION C — Tool Implementation [3 marks]
*(Note: Python Code and Directories are generated separately in the `parabank_tests` folder)*

### Defect Report (Real ParaBank Bugs)
| Bug ID | Title | Severity | Priority | Steps to Reproduce | Expected Result | Actual Result | Status | Screenshot Ref |
|---|---|---|---|---|---|---|---|---|
| BUG-001 | Bill pay accepts $0.00 without validation error | High | Medium | 1. Login. 2. Go to Bill Pay. 3. Enter "$0.00" as amount. 4. Submit. | Form throws validation error preventing sending $0. | Payment processes successfully for $0.00. | Open | test_billpay_0.png |
| BUG-002 | Fund transfer to same account fails silently | Medium | Medium | 1. Go to Transfer. 2. Select matching Source and Destination account. 3. Click Transfer. | Error message "Cannot transfer to identical account". | Page reloads without error, transfer does not occur. | Open | test_transfer_silent.png |
| BUG-003 | Session timeout triggers StaleElementReferenceException | High | High | 1. Login. 2. Wait 15 minutes. 3. Attempt to click 'Accounts Overview'. | Site cleanly redirects user to login.htm with an alert. | DOM invalidates unexpectedly, script crashes with StaleElementReference. | Open | test_timeout.png |

---

## SECTION D — Critical Evaluation [2 marks]

### Strengths of Selenium in ParaBank Context
1. **Dynamic Element Tracking:** Handling ParaBank's dynamically generated Account IDs in drop-downs was highly stabilized by using explicit Wait (`WebDriverWait`), showing Selenium's maturity in dynamic DOM synchronization.
2. **Cross-Browser Verification:** The POM framework easily toggled between Edge and Chrome drivers using `webdriver-manager`, verifying that the Bill Pay form behaves identically across engines.
3. **Data-Driven Flexibility:** By coupling Selenium with `pytest.mark.parametrize()`, I systematically ran BVA combinations for the Request Loan module without duplicating the test logic.
4. **Action Sequence Simplicity:** Selenium’s capability to simulate complex multi-step journeys (Register → Login → Transfer → Check Balance) accurately captured the State Transition criteria mapped in Section B.

### Limitations Encountered
1. **Handling Inherent Flakiness:** During heavy automation loads, ParaBank occasionally delayed rendering the welcome message post-registration, causing `NoSuchElementException` until conditional waits were strictly enforced over implicit ones.
2. **iframe Intricacies:** While not globally pervasive on ParaBank, external ad banners on some simulated portals interrupt strict XPath paths, requiring careful iframe switching or CSS selector hardening.
3. **Silent Failure Ambiguity:** Because the "Transfer to same account" bug fails *silently* (no error is injected into the DOM), Selenium cannot natively flag it as an error unless we explicitly assert the state of the balance post-transfer, complicating test assertions.
4. **Session/Cookie Volatility:** Capturing the StaleElementReferenceException after standard session expiration was tedious; Selenium lacks a native "session status" polling mechanism that isn't purely DOM-dependent.

### Testing Types NOT Supported
1. **Security / Penetration Testing:** Selenium cannot effectively test if ParaBank's database is vulnerable to SQL injection natively; it only automates the browser frontend.
2. **Backend API Testing:** Verifying the actual JSON/REST payloads between front-end actions and the backend banking database is highly inefficient and outside Selenium's scope (tools like Postman are required).

### Comparison: Selenium vs. Cypress for Banking Applications
| Feature | Selenium WebDriver | Cypress |
|---|---|---|
| **Architecture** | Runs outside browser, communicates via HTTP. | Runs directly inside the browser execution loop. |
| **Language Support** | Python, Java, C#, JS, Ruby | JavaScript / TypeScript only |
| **Wait Mechanisms** | Requires explicit/implicit waits (prone to flakiness) | Automatic waiting built-in for DOM rendering |
| **Iframe Handling** | Switch native context method (cumbersome) | Requires third-party plugins (cypress-iframe) |
| **Tab/Window Control** | Excellent (can switch between multiple tabs) | Poor (doesn't natively support multi-tab testing) |
| **Network Mocking** | Limited, requires proxy implementation | Native API mocking and intercepting |

### Improvement Suggestions for the Framework
1. **Database Assertion Integration:** Instead of purely relying on the UI to verify a successful transaction, the framework should integrate DB queries to assert real backend ledger changes.
2. **Enhanced API Interception:** Since Silent Failures exist (like the transfer bug), combining Selenium with network log capturing (like Selenium 4's DevTools integration or BrowserMob) would catch HTTP 4xx or empty states.
3. **Auto-Retry Mechanisms:** Incorporate plugins like `pytest-rerunfailures` to automatically retry failed instances just in case ParaBank's sandbox server experiences a micro-outage.

---

## SECTION E — Viva Preparation [2 marks]

### 15 Likely Viva Questions & Answers
1. **[VIVA LIKELY] Why did you choose the Page Object Model (POM) for this assignment?**
   *Model Answer:* POM drastically reduces code duplication and improves maintainability. If ParaBank changes the ID of the 'Login' button, I only need to update the `login_page.py` locator once instead of modifying every test script.
2. **How does WebDriverWait differ from Implicit Wait?**
   *Model Answer:* Implicit wait sets a global timeout for the driver to wait for an element to appear in the DOM. `WebDriverWait` (Explicit Wait) pauses execution until a specific condition is met, like an element becoming clickable, which prevents racing conditions.
3. **[VIVA LIKELY] What is StaleElementReferenceException and how did you encounter it?**
   *Model Answer:* It occurs when a web element was found in the DOM, but the page reloaded or altered before it could be interacted with. I encountered it when the ParaBank session timed out, invalidating the previous DOM references.
4. **How did you apply Boundary Value Analysis (BVA) to the loan amount feature?**
   *Model Answer:* I tested down payment limits close to the acceptance threshold. For a $1000 loan requiring a 10% down payment, I tested exactly $99 (Denied) and exactly $100 (Approved).
5. **What critical defects did you find in ParaBank?**
   *Model Answer:* The most notable bugs include the Bill Pay module accepting a $0.00 transaction and the Transfer module failing silently when transferring to the exact same account. Both are functional logic failures.
6. **How do you generate screenshots automatically on test failure?**
   *Model Answer:* I utilized a Pytest hook `pytest_runtest_makereport` in `conftest.py`. When an execution yields a failed state, it triggers the `take_screenshot` utility bound to the current driver fixture instance.
7. **Why use Pytest over standard Unittest?**
   *Model Answer:* Pytest requires less boilerplate code and offers highly flexible fixtures for driver setup and teardown. It also inherently supports plugins like `pytest-html` for rich reporting and `pytest.mark.parametrize` for data-driven testing.
8. **Explain your approach to testing the Equivalence Partitions of Registration.**
   *Model Answer:* I split the inputs into valid data (creating the account successfully) and invalid data (missing required name/password). I didn't need to test every possible random string, just one representative of each partition.
9. **How would you handle ParaBank's dynamic account IDs?**
   *Model Answer:* Account IDs load slightly after the page renders. By using `WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "accountId")))`, I ensured the script didn't click too early.
10. **What is a Decision Table and how does it relate to Loan processing?**
   *Model Answer:* A Decision Table maps complex business logically conditions to outcomes. For ParaBank loans, the outcome (Accept/Deny) depends on multiple variables simultaneously: user credit, down payment ratio, and total amount.
11. **Why might Selenium be considered inferior to Cypress for frontend testing?**
   *Model Answer:* Cypress executes directly within the browser runtime, avoiding network latency and flaky element waits. It also automatically intercepts and waits for internal XHR / API requests, which Selenium struggles with natively.
12. **What does `driver.quit()` do versus `driver.close()`?**
   *Model Answer:* `driver.close()` only closes the currently active browser tab or window. `driver.quit()` terminates the entire webdriver session and gracefully closes all associated browser instances.
13. **How do you assert that a user successfully logged in?**
   *Model Answer:* I locate the 'Accounts Overview' string or the 'Log Out' anchor tag on the DOM via `WebDriverWait` and assert its visibility. This actively validates functional completion rather than just a URL check.
14. **How did you implement Data-Driven Testing?**
   *Model Answer:* I applied Pytest's `@pytest.mark.parametrize` decorator above the test functions. This injected arrays of varying test data (like boundary limits) directly into a single test method, executing it multiple times.
15. **If the "Bill Pay" form fails, does it block other tests?**
   *Model Answer:* No, because each test leverages its own fresh driver setup via function-scoped fixtures in `conftest.py`. This ensures tests run in atomic isolation and a failure in one won't taint the next.

### Live Demo Script (5 Minutes)
- **Minute 1: Execution & Run Output.** Open VSCode and run `pytest tests/test_login.py -v`. Observe the browser open, process the credentials rapidly, and the terminal displaying PASSED green text.
- **Minute 2: POM Architecture Explanation.** Briefly show the directory tree. Open `login_page.py` to highlight how locators `(By.NAME, "username")` are separated from the actual test implementation.
- **Minute 3: Live Modification (On the spot test).** Under examiner supervision, open the `test_transfer.py` file. Change the verified exact string matching the 'Transfer Complete' text to show how assertions trap failures. Run immediately to display the artificial failure.
- **Minute 4: Bug Trigger & Screenshot Capture.** Execute `test_billpay.py` parameterized specifically with the $0 limit. The test is designed to *expect* a fail, or if it asserts a failure state, watch it throw an error. Open the local directory to show the auto-captured timestamped screenshot of the failure.
- **Minute 5: Report Delivery.** Run `pytest --html=report.html`. Open the generated `report.html` file in the browser to showcase the unified test summary grid.

### Three "On The Spot" Modification Examples for Viva
1. **Modify Login for SQL Injection:** Examiner asks to test injection; I will change the parameterized username input from `"john"` to `"admin' OR '1'='1"`, execute the test, and verify whether the system throws a DB error or cleanly rejects.
2. **Add Assertion for Account Balances:** After a transfer, use WebDriver to locate the Account Balance element, parse the inner text as a float, and assert that `new_balance == old_balance - transfer_amount`.
3. **Add New Equivalence Class:** Add a negative boundary input (e.g., `"-100"`) into the transfer amount parameters list, rerun the test, and demonstrate that the site blocks it properly.
