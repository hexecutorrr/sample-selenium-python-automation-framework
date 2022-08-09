import pytest
import softest
from asserts.asserts import Asserts
from pages.launch_page import LaunchPage
from utilities.utils import Utils
from ddt import ddt, data, unpack


@pytest.mark.usefixtures("setup")
@ddt
class TestAuthorization(softest.TestCase):
    log = Utils.custom_logger()

    @pytest.fixture(autouse=True)
    def class_setup(self):
        self.lp = LaunchPage(self.driver)
        self.asrt = Asserts()

    @data(*Utils.read_from_csv(Utils.path()+"\\testdata\\login_validation.csv"))
    @unpack
    def test_login_validation(self, login, value):
        open_login = self.lp.login_authorization()
        open_login.enter_login(login)
        item_text = open_login.get_validation_info()
        self.log.info(f'Validation info: {item_text.text}')
        self.asrt.assert_item_text(item_text, value)
        self.log.info("------------Test finished successful------------")
