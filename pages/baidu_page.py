import sys
from pathlib import Path

current_dir = Path(__file__).parent   # tests 目录
parent_dir = current_dir.parent       # 测试脚本 目录
sys.path.insert(0, str(parent_dir))   # 把 '测试脚本' 加入搜索路径
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
class BaiduPage(BasePage):
    """百度首页的页面对象"""

    # 元素定位器（集中管理，便于维护）
    INPUT_SEARCH = (By.ID, "chat-textarea")
    BUTTON_SUBMIT = (By.ID, "chat-submit-button")

    def open(self):
       #打开百度首页
       self.driver.get("https://www.baidu.com")
       return self

    def search(self, keyword: str):
        #在搜索框输入关键词并点击搜索
       self.input_text(self.INPUT_SEARCH, keyword)
       self.click(self.BUTTON_SUBMIT)
       self.wait_for_element((By.CSS_SELECTOR, "#page > div"))
       return self

    def get_title(self) -> str:
        """获取当前页面标题"""
        return self.driver.title