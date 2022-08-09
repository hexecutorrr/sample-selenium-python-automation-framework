import pytest
import softest
from selenium.common import TimeoutException
from asserts.asserts import Asserts
from pages.launch_page import LaunchPage
from utilities.utils import Utils
from ddt import ddt, data, unpack, file_data


@pytest.mark.usefixtures("setup")
@ddt
class TestSearchAndVerifyFilter(softest.TestCase):
    log = Utils.custom_logger()

    @pytest.fixture(autouse=True)
    def class_setup(self):
        self.lp = LaunchPage(self.driver)
        self.asrt = Asserts()

    # @data(("New Delhi", "New", "New York (JFK)", 4, "1 Stop"))
    # @unpack
    # @file_data('../testdata/testdata.yaml')
    # @file_data('../testdata/testdata.json')
    # @data(*Utils.read_from_excel(Utils.path()+"\\testdata\\testdata.xlsx", "Sheet1"))
    @data(*Utils.read_from_csv(Utils.path()+"\\testdata\\testdata.csv"))
    @unpack
    def test_search_flights_by_stops(self, going_from, going_to, going_to_name, number_days, stop):
        search_result = self.lp.search_flights(going_from, going_to, going_to_name, number_days)
        self.lp.scroll_page()
        search_result.flight_filters_by_stop(stop)
        try:
            search_result.show_more_flights()
        except TimeoutException:
            self.log.warning("\"More flights\" button not found!")
        filtered_stops = search_result.get_filtered_search_result()
        self.log.info(f'Number of filtered flights: {len(filtered_stops)}')
        self.asrt.assert_list_items_text(filtered_stops, stop)
        self.log.info("------------Test finished successful------------")
