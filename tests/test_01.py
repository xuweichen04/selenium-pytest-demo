from time import sleep
from selenium.webdriver.common.by import By




def test_baidu(driver):
    driver.get("https://www.baidu.com")
    print("打开百度成功！")

    # 等待页面完全加载
    driver.implicitly_wait(5)
    # 用断言检测打开页面是否是百度
    assert driver.find_element(By.CSS_SELECTOR, "#csaitab").text == "文心"
    print("✅ 检测文心成功！")
    # 百度真实搜索框 ID = kw
    driver.find_element(By.ID, "chat-textarea").send_keys("openai")
    sleep(2)
    # 百度真实搜索按钮 ID = su
    driver.find_element(By.ID, "chat-submit-button").click()
    sleep(7)
    print("✅✅✅ 百度搜索 完 全 成 功！！！")
def test_taobao(driver):
    driver.get("https://www.taobao.com")