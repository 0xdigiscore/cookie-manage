import json
import requests
from lxml import etree
from .login_crypto import encrypto
# from python_js_encrypto import js_encrypto


def main(username, password):
    url = 'http://shanzhi.spbeen.com/login/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    }
    session = requests.Session()
    get_response = session.get(url, headers=headers)
    html = etree.HTML(get_response.text)
    pk = html.xpath('.//input[@id="pk"]/@value')
    pk = pk[0]
    token = html.xpath('.//input[@name="csrfmiddlewaretoken"]/@value')
    token = token[0]
    # print("公钥:", pk)
    miwen_password = encrypto(pk, password)
    formdata = {
        'username': username,
        'password': miwen_password,
        'csrfmiddlewaretoken': token,
    }
    post_response = session.post(url, headers=headers, data=formdata)
    # print(post_response, post_response.text)
    cookies_dict = requests.utils.dict_from_cookiejar(session.cookies)
    cookies_str = json.dumps(cookies_dict)
    return True, cookies_str

if __name__ == "__main__":
    users = [
        {"username": "demo123", "password": "demo123"},
        {"username": "demo1234", "password": "demo1234"},
        {"username": "test1234", "password": "test1234"},
        {"username": "test123", "password": "test123"},
    ]
    for user in users:
        username = user['username']
        password = user['password']
        main(username,password)