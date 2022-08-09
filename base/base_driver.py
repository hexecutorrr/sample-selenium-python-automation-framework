import time
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class BaseDriver:
    def __init__(self, driver):
        self.driver = driver

    def scroll_page(self):
        page_length = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var "
                                                 "pageLength=document.body.scrollHeight;return pageLength;")
        match = False
        while not match:
            last_count = page_length
            time.sleep(1)
            page_length = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var "
                                                     "pageLength=document.body.scrollHeight;return pageLength;")
            if last_count == page_length:
                match = True
        time.sleep(1)

    def wait_for_presence_of_all_elements(self, locator_type, locator):
        wait = WebDriverWait(self.driver, 5)
        list_of_elements = wait.until(ec.presence_of_all_elements_located((locator_type, locator)))
        return list_of_elements

    def wait_until_element_is_clickable(self, locator_type, locator):
        wait = WebDriverWait(self.driver, 5)
        element = wait.until(ec.element_to_be_clickable((locator_type, locator)))
        return element
