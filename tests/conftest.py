import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from pathlib import Path
import time
import logging

@pytest.fixture(scope="session")
def driver(request):
    """
    创建一个浏览器驱动实例
    scope="module" 表示整个 Python 文件的所有测试共享同一个浏览器实例

    这个 fixture 放在 conftest.py 中，
    同一目录下的所有测试文件都可以直接使用，无需 import
    """
    browser = request.config.getoption("--browser")
    #无头模式
    headless = request.config.getoption("--headless")

    if browser == "chrome":

     # 配置 Chrome 选项
     service=ChromeService(executable_path=r"C:\python\chromedriver.exe")
     options = ChromeOptions()
     if headless:
         options.add_argument("--headless")
         options.add_argument("--no-sandbox")  # 无头模式必需
         options.add_argument("--disable-dev-shm-usage")  # 防止内存不足
     options.add_argument("--start-maximized")  # 窗口最大化
     driver = webdriver.Chrome(service=service,options=options)
    elif browser == "edge":

     # 配置 Edge 选项
     service=EdgeService(executable_path=r"C:\python\msedgedriver.exe")
     options = EdgeOptions()
     if headless:
         options.add_argument("--headless")
         options.add_argument("--no-sandbox")
         options.add_argument("--disable-dev-shm-usage")
     options.add_argument("--start-maximized")  # 窗口最大化
     driver = webdriver.Edge(service=service,options=options)
    else:
        raise ValueError(f"不支持的浏览器：{browser}")

    # 创建浏览器实例
    print("\n=== 启动浏览器（无头模式）" if headless else "\n=== 启动浏览器")
    driver.implicitly_wait(10)# 设置隐式等待 10 秒
    request.node.driver = driver

    yield driver  # yield 之前的代码是 setup，之后的代码是 teardown

    # 所有测试结束后关闭浏览器
    print("\n=== 关闭浏览器 ===")
    driver.quit()

# 命令行参数选择浏览器
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="浏览器类型：chrome / edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="是否以无头模式运行（不显示浏览器界面）"
    )

# 失败截图钩子
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """当测试失败时，自动截图并附加到 Allure 报告"""
    outcome = yield
    report = outcome.get_result()

    # 仅在测试失败且是执行阶段（不是 setup/teardown）时截图
    if report.when == "call" and report.failed:

            # 获取 driver 对象
            driver=item.funcargs.get("driver", None)

            # 确保 screenshots 目录存在
            screenshot_dir = Path("./screenshots")
            screenshot_dir.mkdir(exist_ok=True)

            # 生成带时间戳的文件名
            timestamp = str(call.start).replace(".", "_")
            screenshot_path = f"screenshots/{item.name}_{timestamp}.png"

            # 截图并保存为文件
            driver.save_screenshot(screenshot_path)

            # 附加到 Allure 报告
            allure.attach.file(
                    screenshot_path,
                    name="失败截图",
                    attachment_type=allure.attachment_type.PNG
                )
@pytest.fixture(autouse=True)
def log_test_name(request):
    """自动打印每个测试用例的名称"""
    print(f"\n当前测试用例名称：{request.node.name}")
    yield
    print(f"结束测试用例名称：{request.node.name}")

def pytest_runtest_setup(item):
    print(f"\n开始执行测试：{item.name}，时间：{time.strftime('%H:%M:%S')}")


def pytest_runtest_teardown(item):
    print(f"结束执行测试：{item.name}，时间：{time.strftime('%H:%M:%S')}")

