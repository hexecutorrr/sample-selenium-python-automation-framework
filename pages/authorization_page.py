from selenium.webdriver.common.by import By
from base.base_driver import BaseDriver
from utilities.utils import Utils


class Authorization(BaseDriver):
    log = Utils.custom_logger()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    LOGIN_INPUT = "//input[@id='login-input']"
    CONTINUE_BUTTON = "//button[@id='login-continue-btn']"
    VALIDATION_INFO = "//p[@id='login-title']"

    def get_login_input(self):
        return self.driver.find_element(By.XPATH, self.LOGIN_INPUT)

    def get_continue_button(self):
        return self.driver.find_element(By.XPATH, self.CONTINUE_BUTTON)

    def get_validation_info(self):
        return self.driver.find_element(By.XPATH, self.VALIDATION_INFO)

    def enter_login(self, login):
        self.get_login_input().send_keys(login)
        self.log.info("Enter \"login\" is successful")
        self.get_continue_button().click()
        self.log.info("Click \"Continue\" button is successful")

