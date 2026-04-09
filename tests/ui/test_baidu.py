import sys
from pathlib import Path
import allure
import pytest
# 获取当前文件（test_baidu.py）所在目录的父目录（即 '测试脚本' 目录）
current_dir = Path(__file__).parent.parent   # tests 目录
parent_dir = current_dir.parent       # 测试脚本 目录
sys.path.insert(0, str(parent_dir))   # 把 '测试脚本' 加入搜索路径
# 现在可以尝试导入
from pages.baidu_page import BaiduPage

@allure.feature("百度搜索")
@allure.story("基本搜索功能")
@pytest.mark.parametrize("keyword", ["selenium", "pytest", "python"])
def test_search_selenium(driver,keyword):
    """测试在百度搜索 selenium"""
    with allure.step(f"打开百度并搜索 {keyword}"):
     baidu = BaiduPage(driver)
     baidu.open().search(f"{keyword}是什么")
    with allure.step("验证标题包含关键词"):
     assert keyword in baidu.get_title()

    ## 记住这个万能命令
# Remove-Item .\allure-results\* -Recurse -Force; pytest tests/test_baidu02.py --alluredir=./allure-results -v

     """
     allure generate ./allure-results -o ./allure-report --clean
     allure open ./allure-report
     """