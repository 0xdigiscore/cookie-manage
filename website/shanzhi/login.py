import requests
from lxml import etree
from login_crypto import encrypto
from python_js_encrypto import js_encrypto


url = 'http://shanzhi.spbeen.com/login/'
headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Cookie": "_ga=GA1.2.501597955.1605090738; UM_distinctid=179501039c3702-0975e33b6b0ecf-103c6054-13c680-179501039c4594; sessionid=kf32dyeknblc7ix4znintduqed3n3qf1; csrftoken=5H9PDQ6TAxknuydbn6IVhmZfGmGwsC6hT1zFxlpCtZgaX7XJbubICPnOKmqyZ8Hg",
}

get_response = requests.get(url, headers=headers)

html = etree.HTML(get_response.text)
pk = html.xpath('.//input[@id="pk"]/@value')
pk = pk[0]
token = html.xpath('.//input[@name="csrfmiddlewaretoken"]/@value')
token = token[0]

print("公钥:", pk)

username = 'demo1234'
password = 'demo1234'

# miwen_password = encrypto(pk, password)
miwen_password = js_encrypto(pk, password)
print("密码：",password, "\n加密后：", miwen_password)


formdata = {
    'username':username,
    'password':miwen_password,
    'csrfmiddlewaretoken':token,
}
print(formdata)

post_response = requests.post(url,headers=headers, data=formdata)

# print(post_response.history[0].headers)

print(post_response, post_response.text)

if post_response.status_code >= 400:
    with open('error.html', 'wb') as file:
        file.write(post_response.content)


