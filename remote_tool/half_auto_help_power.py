from selenium import webdriver # pypeteer,selenium都可以抓取web数据
from time import sleep
import requests, json

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

url = 'http://127.0.0.1:8000/remote/api/get_account_info/'
post_url = 'http://127.0.0.1:8000/remote/api/post_account_cookie_info/'

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
    python_script = account_info['extract_cookie_script']
    python_script = python_script.format(account_info['username'], account_info['password'])
    print(python_script)
    cb = webdriver.Chrome(options=options)
    with open('./stealth.min.js') as f:
        js = f.read()
    cb.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })
    sleep(2)

    cb.get(account_info['web']['loginurl'])
    exec(python_script)
    num = 1
    while True:
        print("当前第{}轮".format(num))
        try:
            cookies_list = cb.get_cookies()
            cookies_dict = {ck['name']: ck['value'] for ck in cookies_list}
        except:
            account_info['cookie'] = json.dumps(cookies_dict)
            post_response = requests.post(post_url, data=json.dumps(account_info))
            print(post_response, post_response.text)
            break
        sleep(2)
        num += 1
