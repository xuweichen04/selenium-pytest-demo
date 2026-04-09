import pytest
import requests


def test_get_captcha_image(base_url):
    """
    测试获取验证码图片接口
    接口地址: GET http://kdtx-test.itheima.net/api/captchaImage
    """
    # 1. 准备测试数据
    url = f"{base_url}/api/captchaImage"
    payload = {}

    # 2. 发送请求
    response = requests.request("GET", url, json=payload)

    # 3. 打印响应内容（调试用，-s 参数可见）
    print("状态码:", response.status_code)
    print("响应内容:", response.json())

    # 4. 断言验证
    assert response.status_code == 200, f"期望状态码200，实际得到 {response.status_code}"

    # 如果返回的是 JSON，可以进一步验证
    try:
        data = response.json()
        print("解析后的JSON:", data)
        # 根据你的实际响应结构调整断言
        assert "uuid" in data and "img" in data, "响应中应包含验证码相关字段"
    except Exception as e:
        print("响应不是JSON格式:", e)
        raise

if __name__ == "__main__":
    # 建议：在 main 中使用 pytest 运行，这样才能自动注入 base_url
    pytest.main(["-v", "-s", __file__])

