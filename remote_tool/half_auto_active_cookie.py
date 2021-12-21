from selenium import webdriver # pypeteer,selenium都可以抓取web数据
from time import sleep
from lxml import etree
import requests, json
import random

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

url = 'http://127.0.0.1:8000/remote/api/get_account_cookie_active_info/'
post_url = 'http://127.0.0.1:8000/remote/api/post_account_cookie_active_info/'

while True:
    response = requests.get(url)
    print(response)
    account_info = json.loads(response.text)
    if account_info['code'] == 200:
        print(account_info['message'])
    elif account_info['code'] == 404:
        print(account_info['message'], '睡眠15秒，等待下一次请求数据')
        sleep(15)
        continue
    cb = webdriver.Chrome(options=options)
    with open('./stealth.min.js') as f:
        js = f.read()
    cb.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })
    sleep(2)

    cb.get(account_info['web']['indexurl'])# 载入Cookie，必须先访问页面
    cookies = json.loads(account_info['cookie'])
    for k,v in cookies.items():
        cb.add_cookie({
            "name": k,
            "value": v,
        })
    cb.get(account_info['web']['indexurl'])

    cookies_list = cb.get_cookies()
    cookies_dict = {ck['name']: ck['value'] for ck in cookies_list}
    try:
        if account_info['active_cookie_use_python_or_javascript_script'] == 'python':
            exec(account_info['active_python_script'])# 自行携带睡眠
        elif account_info['active_cookie_use_python_or_javascript_script'] == 'javascript':
            cb.execute_script(account_info['active_js_script'])
            sleep(account_info['wait_exec_active_js_script'])# js是异步执行的，不受py程序控制，所以主动睡眠
        else:
            print("脚本信息获取异常，不执行脚本处理")
        cookies_list = cb.get_cookies()
        cookies_dict = {ck['name']: ck['value'] for ck in cookies_list}
    except Exception as e:
        print("出现异常，先跳过")
    cb.quit()
    account_info['cookie'] = json.dumps(cookies_dict)
    post_response = requests.post(post_url, data=json.dumps(account_info))
    print("处理完一个，休息30秒~~~~~~~~~~")
    sleep(30)



