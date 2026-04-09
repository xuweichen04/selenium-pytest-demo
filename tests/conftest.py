import pytest
import allure
import requests
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
@pytest.fixture(scope="session")
def base_url():
    return "http://kdtx-test.itheima.net"


@pytest.fixture(scope="function")
def captcha_uuid(base_url):
    """
    验证码 UUID - function 级别
    每个测试都获取新的，避免过期或被重复使用
    """
    response = requests.get(f"{base_url}/api/captchaImage")
    assert response.status_code == 200, f"获取验证码失败: {response.text}"

    data = response.json()
    assert "uuid" in data, "响应中没有 uuid 字段"

    return data["uuid"]


@pytest.fixture(scope="function")
def auth_token(base_url, captcha_uuid):
    """
    登录 Token - function 级别
    依赖 captcha_uuid，保证每次登录都使用新鲜的验证码
    """
    payload = {
        "username": "admin",
        "password": "HM_2023_test",
        "uuid": captcha_uuid,
        "code": "2"
    }

    response = requests.post(f"{base_url}/api/login", json=payload)

    # 增加详细的断言，方便排查登录失败的原因
    assert response.status_code == 200, (
        f"登录请求失败\n状态码: {response.status_code}\n响应: {response.text}"
    )

    data = response.json()
    assert "token" in data, f"登录成功但未返回 token: {data}"

    return data["token"]

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