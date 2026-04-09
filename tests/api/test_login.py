import requests
import json
import pytest


def test_login_success(base_url,captcha_uuid):
    """
    测试登录成功
    """
    url = f"{base_url}/api/login"

    payload = {
        "username": "admin",
        "password": "HM_2023_test",
        "code": "2",
        "uuid": captcha_uuid
    }

    # 发送请求（方式一：推荐）
    response = requests.post(url, json=payload)

    # 打印状态码
    print("\n状态码:", response.status_code)

    # 打印美化后的响应
    try:
        response_data = response.json()
        print("响应数据:")
        print(json.dumps(response_data, indent=2, ensure_ascii=False))
    except Exception as e:
        print("解析失败:", e)
        print("原始内容:", response.text)
        raise  # ← 如果解析失败，直接让测试报错
    # 断言验证
    assert response.status_code == 200, f"期望状态码200，实际得到 {response.status_code}"

    response_data = response.json()
    assert "token" in response_data, "登录成功应返回 token"
    assert response_data["code"] == 200, f"业务码应为200，实际为 {response_data.get('code')}"

    print(f"\n✅ 登录成功！Token: {response_data['token'][:30]}...")


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
