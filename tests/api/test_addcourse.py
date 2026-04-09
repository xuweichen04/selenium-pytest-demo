import requests
import json
import pytest
import time

def test_add_course(base_url, auth_token):
    """
    测试添加课程接口
    接口地址: POST /api/clues/course
    """
    url = f"{base_url}/api/clues/course"
    unique_name = f"测试开发提升课_{int(time.time())}"
    # 准备请求数据
    payload = {
        "name": unique_name,
        "subject": "6",
        "price": 5000,
        "applicablePerson": "6",
        "info": "测试开发提升课01"
    }

    # 准备请求头（使用 fixture 提供的 token）
    headers = {
        'Authorization': auth_token,  # ← 自动注入登录后的 token
    }

    # 发送请求
    response = requests.post(url, json=payload,headers=headers)

    # 打印响应内容（调试用）
    print("\n状态码:", response.status_code)
    try:
        print("响应数据:", json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print("原始响应:", response.text)

    # 断言验证
    assert response.status_code == 200, f"请求失败，状态码: {response.status_code}"

    # 根据实际业务逻辑调整断言，例如检查返回的课程 ID 或成功标识
    data = response.json()
    assert data.get("code") == 200 or data.get("msg") == "success", f"业务逻辑失败: {data}"


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
