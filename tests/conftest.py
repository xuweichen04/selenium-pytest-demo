import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager

from pathlib import Path
import time

@pytest.fixture(scope="session")
def driver(request):
    """
    浏览器驱动 fixture
    scope="session" 表示整个测试会话共享同一个浏览器实例
    """
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        if headless:
            service = ChromeService(ChromeDriverManager().install())
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome(service=service, options=options)
        else:
            service = ChromeService(executable_path=r"C:\python\chromedriver.exe")
            driver = webdriver.Chrome(service=service, options=options)

    elif browser == "edge":
        service = EdgeService(executable_path=r"C:\python\msedgedriver.exe")
        options = EdgeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Edge(service=service, options=options)

    else:
        raise ValueError(f"不支持的浏览器：{browser}，请使用 chrome 或 edge")

    print("\n=== 启动浏览器（无头模式）" if headless else "\n=== 启动浏览器")
    driver.implicitly_wait(10)
    request.node.driver = driver

    yield driver

    print("\n=== 关闭浏览器 ===")
    driver.quit()


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="浏览器类型：chrome / edge")
    parser.addoption("--headless", action="store_true", default=False, help="是否以无头模式运行")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            screenshot_dir = Path("./screenshots")
            screenshot_dir.mkdir(exist_ok=True)
            timestamp = str(call.start).replace(".", "_")
            screenshot_path = f"screenshots/{item.name}_{timestamp}.png"
            driver.save_screenshot(screenshot_path)
            allure.attach.file(
                screenshot_path,
                name="失败截图",
                attachment_type=allure.attachment_type.PNG
            )


@pytest.fixture(autouse=True)
def log_test_name(request):
    print(f"\n当前测试用例名称：{request.node.name}")
    yield
    print(f"结束测试用例名称：{request.node.name}")


def pytest_runtest_setup(item):
    print(f"\n开始执行测试：{item.name}，时间：{time.strftime('%H:%M:%S')}")


def pytest_runtest_teardown(item):
    print(f"结束执行测试：{item.name}，时间：{time.strftime('%H:%M:%S')}")