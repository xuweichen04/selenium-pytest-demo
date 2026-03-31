# 注意：这里不需要 import driver，pytest 会自动从 conftest.py 加载
from time import sleep

import pytest
from selenium.webdriver.common.by import By


class TestBaidu:
    """百度搜索测试"""

    def test_open_baidu(self, driver):
        """打开百度首页"""
        print("\n[测试 1] 访问百度...")
        driver.get("https://www.baidu.com")

        title = driver.title
        print(f"页面标题：{title}")

        assert "百度一下" in title, f"标题不包含'百度一下': {title}"

    def test_search_selenium(self, driver):
        """搜索 Selenium"""
        print("\n[测试 2] 搜索 Selenium...")
        driver.get("https://www.baidu.com")
        sleep(2)
        # 定位搜索框并输入关键词
        search_box = driver.find_element(By.ID, "chat-textarea")
        search_box.send_keys("Selenium")

        # 点击搜索按钮
        search_btn = driver.find_element(By.ID, "chat-submit-button")
        search_btn.click()
        sleep(4)
        # 验证标题
        assert "Selenium" in driver.title
        print(f"✓ 搜索完成，标题：{driver.title}")

    def test_page_navigation(self, driver):
        """
        测试页面前进后退
        """
        print("\n[测试 3] 测试导航功能...")

        # 访问百度
        driver.get("https://www.baidu.com")
        baidu_url = driver.current_url
        sleep(2)
        # 访问淘宝
        driver.get("https://www.taobao.com")
        taobao_url = driver.current_url
        sleep(2)
        # 验证是两个不同的页面
        assert baidu_url != taobao_url

        # 后退到百度
        driver.back()
        back_url = driver.current_url

        # 验证回到了百度
        assert back_url == baidu_url
        print("✓ 测试 3 通过")

class TestTaobao:
    def test_refresh_page(self, driver):
        """
        测试页面刷新
        """
        print("\n[测试 4] 测试页面刷新...")
        driver.get("https://www.baidu.com")

        # 获取刷新前的标题
        title_before = driver.title

        # 刷新页面
        driver.refresh()
        sleep(2)
        # 获取刷新后的标题
        title_after = driver.title

        # 验证标题相同
        assert title_before == title_after
        print("✓ 测试 4 通过")