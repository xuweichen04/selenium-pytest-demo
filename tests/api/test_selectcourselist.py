import requests
import json
import pytest


def test_select_course_list(base_url, auth_token):
    """
    测试查询课程列表接口
    接口地址: GET /api/clues/course/list
    """
    # 准备查询参数
    params = {
        "name": "测试开发提升课08"
    }

    # 准备请求头
    headers = {
        'Authorization': auth_token  # ← 使用 fixture 自动注入的 token
    }

    # 发送 GET 请求
    # 注意：GET 请求的参数通常放在 params 中，requests 会自动拼接到 URL 后面
    url = f"{base_url}/api/clues/course/list"
    response = requests.get(url, params=params, headers=headers)

    # 打印响应内容
    print("\n状态码:", response.status_code)
    try:
        print("响应数据:", json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print("原始响应:", response.text)

    # 断言验证
    assert response.status_code == 200, f"请求失败，状态码: {response.status_code}"

    data = response.json()
    # 假设 code 200 代表业务成功
    assert data.get("code") == 200, f"业务逻辑失败: {data}"


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
