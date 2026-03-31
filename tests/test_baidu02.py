import pytest
import json
from pathlib import Path
import allure
import yaml
import sys
from pathlib import Path
current_dir = Path(__file__).parent   # tests 目录

parent_dir = current_dir.parent       # 测试脚本 目录

sys.path.insert(0, str(parent_dir))   # 把 '测试脚本' 加入搜索路径


from pages.baidu_page import BaiduPage
"""
def load_test_data():
    # 获取当前文件所在目录的父目录（即项目根目录）下的 data/search_data.json
    data_file = Path(__file__).parent.parent / "data" / "search_data.json"
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)   # 直接返回 Python 列表
        """

def load_test_data():
    data_file = Path(__file__).parent.parent / "data" / "search_data.yaml"
    with open(data_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)  # 直接返回 Python 列表

@allure.feature("百度搜索")
@allure.story("基本搜索功能")
@pytest.mark.parametrize("test_data", load_test_data())
def test_search(driver, test_data):
    with allure.step(f"打开百度并搜索 {test_data["keyword"]}"):
        baidu = BaiduPage(driver)
        baidu.open().search(f"{test_data["keyword"]}")
    with allure.step("验证标题包含关键词"):
        assert test_data["keyword"] == test_data["expected_title"]
