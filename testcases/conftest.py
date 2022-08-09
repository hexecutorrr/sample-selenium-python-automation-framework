import os
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from utilities.utils import Utils

log = Utils.custom_logger()
driver = None


# pytest --html=reports/report1.html
@pytest.fixture(autouse=True)
def setup(request, browser, url):
    global driver
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
        log.info("Select browser is Chrome")
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("start-maximized")
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver = webdriver.Firefox(options=options, service=FirefoxService(GeckoDriverManager().install()))
        log.info("Select browser is Firefox")
    elif browser == "edge":
        options = webdriver.EdgeOptions()
        options.add_argument("start-maximized")
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver = webdriver.Edge(options=options, service=EdgeService(EdgeChromiumDriverManager().install()))
        log.info("Select browser is Edge")
    else:
        log.warning("No enter browser, default browser is Chrome")
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
        log.info("Select browser is Chrome")
    driver.get(url)
    request.cls.driver = driver
    yield
    driver.close()


def pytest_addoption(parser):
    parser.addoption("--browser")
    parser.addoption("--url", default="https://www.yatra.com/")


@pytest.fixture(scope="class", autouse=True)
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="class", autouse=True)
def url(request):
    return request.config.getoption("--url")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call":
        # always add url to report
        extra.append(pytest_html.extras.url("http://www.yatra.com/"))
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # only add additional html on failure
            report_directory = Utils.path() + "\\reports\\screenshots\\"
            file_name = report.nodeid.replace("::", "_").replace('testcases/', "") + ".png"
            destination_file = os.path.join(report_directory, file_name)
            driver.save_screenshot(destination_file)
            html = '<div><img src="%s" alt="screenshot" style="width:300px;height=200px" ' \
                   'onclick="window.open(this.src)" align="right"/></div>' % ("screenshots\\" + file_name)
            extra.append(pytest_html.extras.html(html))
        report.extra = extra


def pytest_html_report_title(report):
    report.title = "Automation Report"
