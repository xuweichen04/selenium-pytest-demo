import requests
import pytest
from pathlib import Path


def test_upload_file(base_url, auth_token):
    """
    测试文件上传接口
    接口地址: POST /api/common/upload
    """
    url = f"{base_url}/api/common/upload"

    # 准备请求头
    headers = {
        'Authorization': auth_token
    }

    # 准备文件路径（建议使用相对路径或项目内的固定路径，避免依赖桌面路径）
    # 假设我们在项目根目录下创建一个 test_data 文件夹存放测试文件
    file_path = Path(__file__).parent.parent.parent / "data" / "apitest.txt"

    # 确保文件存在，如果不存在可以先创建一个用于测试
    if not file_path.exists():
        file_path.parent.mkdir(exist_ok=True)
        file_path.write_text("This is a test file for API automation.", encoding="utf-8")
        print(f"已自动创建测试文件: {file_path}")

    # 准备文件数据
    # 格式: {'字段名': ('文件名', 文件对象, 'MIME类型')}
    with open(file_path, 'rb') as f:
        files = {
            'file': ('apitest.txt', f, 'text/plain')
        }

        # 发送请求
        response = requests.post(url, headers=headers, files=files)

    # 打印响应内容
    print("\n状态码:", response.status_code)
    print("响应数据:", response.text)

    # 断言验证
    assert response.status_code == 200, f"上传失败，状态码: {response.status_code}"

    data = response.json()
    # 根据实际返回结构调整，通常上传成功会返回文件 URL 或 ID
    assert data.get("code") == 200 or data.get("msg") == "操作成功", f"业务逻辑失败: {data}"


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
