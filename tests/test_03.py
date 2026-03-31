from time import sleep

from selenium.webdriver.common.by import By             # 元素定位
from selenium.webdriver.support.ui import WebDriverWait # 显式等待
from selenium.webdriver.support import expected_conditions as EC


class TestTaobao:
    """淘宝测试"""

    def test_open_taobao(self, driver):
        """打开淘宝首页"""
        print("\n[测试 3] 访问淘宝...")
        driver.get("https://www.taobao.com")

        title = driver.title
        print(f"页面标题：{title}")

        assert "淘宝" in title, f"标题不包含'淘宝': {title}"

    def test_check_search(self, driver):
        """检查搜索框是否存在"""
        print("\n[测试 4] 检查搜索框...")
        driver.get("https://www.taobao.com")
        """
        # 等待弹窗出现
        wait = WebDriverWait(driver, 15)
        login_iframe = wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "body > div.J_MIDDLEWARE_FRAME_WIDGET > iframe"
            ))
        )
        assert login_iframe.is_displayed(), "账号输入框未显示"
        print("✓ 登录弹窗已出现")
        driver.switch_to.frame(login_iframe)
         # 步骤 2：在弹窗中查找账号输入框
        print("查找账号输入框...")
        search_box = wait.until(
                           EC.visibility_of_element_located((By.CSS_SELECTOR, "#fm-login-id"))
                  )

        # 验证元素显示
        assert search_box.is_displayed(), "账号输入框未显示"
        print("✓ 账号输入框存在且可见")
        """
        # 检查搜索框是否存在
        search_box = driver.find_element(By.CSS_SELECTOR, "#q")
        assert search_box.is_displayed(), "搜索框未显示"
        print("搜索框找到了")
    def test_input(self, driver):
        #driver.switch_to.default_content()
        print("\n[测试 5] 检查输入...")
        driver.find_element(By.CSS_SELECTOR, "#q").send_keys("男装")
        driver.find_element(By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button").click()
        sleep(10)
        print("✓搜索成功")


