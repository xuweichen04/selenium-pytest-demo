from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TaobaoPage:
    """百度首页的页面对象"""

    # 元素定位器（集中管理，便于维护）
    INPUT_SEARCH = (By.CSS_SELECTOR, "#q")
    BUTTON_SUBMIT = (By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open(self):
        """打开淘宝首页"""
        self.driver.get("https://www.taobao.com")
        return self

    def search(self, keyword: str):
        """在搜索框输入关键词并点击搜索"""
        input_elem = self.driver.find_element(*self.INPUT_SEARCH)
        input_elem.clear()
        input_elem.send_keys(keyword)
        self.driver.find_element(*self.BUTTON_SUBMIT).click()


        wait = WebDriverWait(self.driver, 10)
        iframe = wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "#baxia-dialog-content"
            ))
        )
        return self

    def get_title(self) -> str:
        """获取当前页面标题"""
        return self.driver.title