from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class DriverFactory:
    @staticmethod
    def get_driver():
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless') # Uncomment for headless execution
        options.add_argument('--window-size=1920,1080')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        return driver
