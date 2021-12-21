import json
from selenium import webdriver
from time import sleep
# selenium python -m pip install selenium
# chrome 浏览器，注意版本号
# chromedriver 驱动文件，对应chrome版本号  搜索taobao chromedriver
# macos /usr/local/bin/chromedriver
# win chromedriver.exe放在python.exe旁边
# linux 大佬自己处理


users = [
    {"username":"demo123", "password":"demo123"},
    {"username":"demo1234", "password":"demo1234"},
    {"username":"test1234", "password":"test1234"},
    {"username":"test123", "password":"test123"},
]


# 程序将预处理的内容，全部处理好
# 浏览器放着等用户处理
# 用户处理的同时，程序一直监听
# 直到用户直接关闭了浏览器，程序发现监听异常，继续往下执行
def wait_cookie(browser):
    num = 1
    while True:
        try:
            cookies_list = browser.get_cookies()
            cookies_dict = {ck['name']: ck['value'] for ck in cookies_list}
            print(num, cookies_dict)
        except:
            with open("cookies_3_3.txt", 'a', encoding='utf8') as file:
                file.write(json.dumps(cookies_dict))
                file.write('\n')
            break
        sleep(3)
        num += 1

        # browser.quit()


def main(username, password):
    url = 'http://shanzhi.spbeen.com/login/'
    cb = webdriver.Chrome()
    cb.get(url)
    sleep(1)

    # 程序能主动处理的部分，尽量主动处理
    username_input = cb.find_element_by_xpath('.//input[@id="username"]')
    username_input.send_keys(username)
    password_input = cb.find_element_by_xpath('.//input[@id="MemberPassword"]')
    password_input.send_keys(password)
    sleep(2)

    # 如果登录的时候，弹出一个行为验证的验证框，那登录就还没有成功
    # submit_button = cb.find_element_by_xpath('.//button[@onclick="doLogin()"]')
    # submit_button.click()
    # sleep(2)

    wait_cookie(cb)




if __name__ == "__main__":
    for user in users:
        username = user['username']
        password = user['password']
        main(username,password)
        # break