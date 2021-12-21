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

def main(username, password):
    url = 'http://shanzhi.spbeen.com/login/'
    cb = webdriver.Chrome()
    cb.get(url)
    sleep(1)
    username_input = cb.find_element_by_xpath('.//input[@id="username"]')
    username_input.send_keys(username)
    password_input = cb.find_element_by_xpath('.//input[@id="MemberPassword"]')
    password_input.send_keys(password)
    sleep(2)
    submit_button = cb.find_element_by_xpath('.//button[@onclick="doLogin()"]')
    submit_button.click()
    sleep(2)

    cookies_list = cb.get_cookies()
    cookies_dict = { ck['name']:ck['value'] for ck in cookies_list }
    print(cookies_dict)
    with open("cookies_3_2.txt", 'a', encoding='utf8') as file:
        file.write(json.dumps(cookies_dict))
        file.write('\n')

    cb.quit()


if __name__ == "__main__":
    for user in users:
        username = user['username']
        password = user['password']
        main(username,password)
        # break