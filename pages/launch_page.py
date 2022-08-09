import time
from datetime import date, timedelta
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from base.base_driver import BaseDriver
from pages.search_results_page import SearchResult
from pages.authorization_page import Authorization
from utilities.utils import Utils


class LaunchPage(BaseDriver):
    log = Utils.custom_logger()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    GOING_FROM_FIELD = "//input[@id='BE_flight_origin_city']"
    GOING_TO_FIELD = "//input[@id='BE_flight_arrival_city']"
    GOING_TO_RESULTS_LIST = "//div[@class='viewport']//div[1]/li"
    SELECT_DATE_FIELD = "//input[@id='BE_flight_origin_date']"
    ALL_DATES = "//div[@id='monthWrapper']//tbody//td[@class!='inActiveTD']"
    SEARCH_BUTTON = "//input[@value='Search Flights']"
    MY_ACCOUNT = "//a[contains(text(),'My Account')]"
    LOGIN_BUTTON = "//a[@id='signInBtn']"

    def get_going_from_field(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.GOING_FROM_FIELD)

    def get_going_to_field(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.GOING_TO_FIELD)

    def get_going_to_results(self):
        return self.wait_for_presence_of_all_elements(By.XPATH, self.GOING_TO_RESULTS_LIST)

    def get_departure_date_field(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.SELECT_DATE_FIELD)

    def get_all_dates_field(self):
        return self.wait_for_presence_of_all_elements(By.XPATH, self.ALL_DATES)

    def get_search_button(self):
        return self.driver.find_element(By.XPATH, self.SEARCH_BUTTON)

    def get_my_account(self):
        return self.driver.find_element(By.XPATH, self.MY_ACCOUNT)

    def get_login_button(self):
        return self.driver.find_element(By.XPATH, self.LOGIN_BUTTON)

    def enter_going_from_location(self, going_from_location):
        self.get_going_from_field().click()
        self.log.info("Click on \"going from\" field")
        self.get_going_from_field().send_keys(going_from_location)
        self.log.info("Add text in \"going from\" field is successfully")
        self.get_going_from_field().send_keys(Keys.ENTER)
        self.log.info("Select result from \"going from\" field is successful")
        time.sleep(1)

    def enter_going_to_location(self, going_to_location, location_name):
        self.get_going_to_field().click()
        self.log.info("Click on \"going to\" field")
        time.sleep(1)
        self.get_going_to_field().send_keys(going_to_location)
        self.log.info("Add text in \"going to\" field is successfully")
        time.sleep(1)
        search_result = self.get_going_to_results()
        for res in search_result:
            if location_name in res.text:
                res.click()
                break
        self.log.info("Select result from \"going to\" field is successful")

    def enter_departure_date(self, number_days):
        date_generator = (date.today() + timedelta(days=int(number_days))).strftime("%d/%m/%Y")
        self.get_departure_date_field().click()
        self.log.info("Click on \"departure date\" field is successful")
        all_dates = self.get_all_dates_field()
        for day in all_dates:
            if day.get_attribute("data-date") == date_generator:
                day.click()
                break
        self.log.info("Select \"departure date\" is successful")

    def click_search_flights_button(self):
        self.get_search_button().click()
        self.log.info("Click on \"search flights\" button is successful")
        time.sleep(3)

    def my_account_field(self):
        my_account = self.get_my_account()
        ac = ActionChains(self.driver)
        ac.move_to_element(my_account).perform()
        self.log.info("Open \"My Account\" is successful")

    def click_login_button(self):
        self.get_login_button().click()
        self.log.info("Click on \"Login\" button is successful")
        time.sleep(3)

    def search_flights(self, going_from_location, going_to_location, location_name, number_days):
        self.enter_going_from_location(going_from_location)
        self.enter_going_to_location(going_to_location, location_name)
        self.enter_departure_date(number_days)
        self.click_search_flights_button()
        return SearchResult(self.driver)

    def login_authorization(self):
        self.my_account_field()
        self.click_login_button()
        return Authorization(self.driver)
