import time
import requests
import json
import random
from datetime import datetime
from pathlib import Path

# ================= 配置区域 =================
BASE_URL = "http://kdtx-test.itheima.net"
INTERVAL_SECONDS = 5  # 测试间隔（秒）
LOG_FILE = "monitor_log.txt"

# 账号信息
USERNAME = "admin"
PASSWORD = "HM_2023_test"
# ===========================================

def get_auth_token():
    """
    步骤1：获取最新的 Token
    先获取验证码，再登录
    """
    try:
        # 1. 获取验证码 UUID
        captcha_resp = requests.get(f"{BASE_URL}/api/captchaImage", timeout=10)
        captcha_resp.raise_for_status()
        uuid = captcha_resp.json()["uuid"]

        # 2. 调用登录接口
        login_payload = {
            "username": USERNAME,
            "password": PASSWORD,
            "uuid": uuid,
            "code": "2"
        }
        login_resp = requests.post(f"{BASE_URL}/api/login", json=login_payload, timeout=10)
        login_resp.raise_for_status()

        token_data = login_resp.json()
        if token_data.get("code") == 200:
            return token_data["token"]
        else:
            raise Exception(f"登录业务失败: {token_data.get('msg')}")

    except Exception as e:
        raise Exception(f"获取 Token 失败: {str(e)}")

def run_test(token):
    """
    步骤2：执行随机查询课程列表测试
    """
    # 随机生成 01 到 10 的后缀
    random_num = random.randint(1, 10)
    # 使用 :02d 确保数字是两位数，例如 1 变成 "01"
    course_name = f"测试开发提升课{random_num:02d}"

    url = f"{BASE_URL}/api/clues/course/list"
    headers = {'Authorization': token}
    params = {"name": course_name}

    start_time = time.time()
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        duration = time.time() - start_time

        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 200:
                course_count = len(data.get("rows", []))
                # 在日志中记录这次随机查的是哪个词
                return "PASS", f"查询[{course_name}] | 耗时: {duration:.2f}s | 结果数: {course_count}"
            else:
                return "FAIL", f"查询[{course_name}] 业务错误: {data.get('msg')}"
        else:
            return "FAIL", f"HTTP 状态码异常: {response.status_code}"

    except Exception as e:
        return "ERROR", f"请求异常: {str(e)}"

def log_result(status, message):
    """记录日志到文件和控制台"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{now}] [{status}] {message}\n"

    print(log_line.strip())

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line)

def main():
    print(f"🚀 启动 24h 随机监控程序 (目标: {BASE_URL})")
    print(f"⏱️  间隔: {INTERVAL_SECONDS}s | 📝 日志: {LOG_FILE}")

    count = 0
    try:
        while True:
            count += 1
            print(f"\n--- 第 {count} 轮检测 ({datetime.now().strftime('%H:%M')}) ---")

            # 1. 刷新 Token
            print("正在获取最新 Token...")
            try:
                token = get_auth_token()
            except Exception as e:
                log_result("ERROR", str(e))
                time.sleep(10)
                continue

            # 2. 执行业务测试
            status, message = run_test(token)
            log_result(status, message)

            # 3. 等待
            time.sleep(INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\n🛑 监控已手动停止。")

if __name__ == "__main__":
    main()
