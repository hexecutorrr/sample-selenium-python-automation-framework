from selenium.webdriver.common.by import By
from base.base_driver import BaseDriver
from utilities.utils import Utils


class SearchResult(BaseDriver):
    log = Utils.custom_logger()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    MORE_FLIGHTS_FIELD = "//div[@class='timing-det v-aligm-t pull-left']"
    FILTER_BY_ONE_STOP = "//p[@class='font-lightgrey bold'][normalize-space()='1']"
    FILTER_BY_TWO_STOP = "//p[@class='font-lightgrey bold'][normalize-space()='2']"
    FILTER_BY_NON_STOP = "//p[@class='font-lightgrey bold'][normalize-space()='0']"
    SEARCH_FLIGHT_RESULT = "//span[contains(text(),'Non Stop') or contains(text(),'1 Stop') or contains(text()," \
                           "'2 Stop')] "

    def get_more_flights_field(self):
        return self.wait_for_presence_of_all_elements(By.XPATH, self.MORE_FLIGHTS_FIELD)

    def get_filter_by_one_stop(self):
        return self.driver.find_element(By.XPATH, self.FILTER_BY_ONE_STOP)

    def get_filter_by_two_stop(self):
        return self.driver.find_element(By.XPATH, self.FILTER_BY_TWO_STOP)

    def get_filter_by_non_stop(self):
        return self.driver.find_element(By.XPATH, self.FILTER_BY_NON_STOP)

    def get_filtered_search_result(self):
        return self.wait_for_presence_of_all_elements(By.XPATH, self.SEARCH_FLIGHT_RESULT)

    def show_more_flights(self):
        all_more_flights = self.get_more_flights_field()
        for flight in all_more_flights:
            self.driver.execute_script("arguments[0].scrollIntoView();", flight)
            self.driver.execute_script("arguments[0].click();", flight)
        self.log.info("Open all \"more flights\" field is successfully")

    def flight_filters_by_stop(self, stop):
        if stop == "1 Stop":
            self.get_filter_by_one_stop().click()
            self.log.info("Selected flights with \"1 stop\"")
        elif stop == "2 Stops":
            self.get_filter_by_two_stop().click()
            self.log.info("Selected flights with \"2 stops\"")
        elif stop == "Non Stop":
            self.get_filter_by_non_stop().click()
            self.log.info("Selected flights with \"Non stop\"")
        else:
            self.log.warning("Provide valid filter options")
