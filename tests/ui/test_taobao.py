
import sys
from pathlib import Path

# 获取当前文件（test_baidu.py）所在目录的父目录（即 '测试脚本' 目录）
current_dir = Path(__file__).parent.parent   # tests 目录
print("当前目录:", current_dir)
parent_dir = current_dir.parent       # 测试脚本 目录
print("父目录:", parent_dir)
sys.path.insert(0, str(parent_dir))   # 把 '测试脚本' 加入搜索路径
print("sys.path:", sys.path)
# 现在可以尝试导入
from pages.taobao_page import TaobaoPage


def test_search_selenium(driver):
    taobao = TaobaoPage(driver)
    taobao.open()
    assert "淘宝" in taobao.get_title()


