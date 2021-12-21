from celery import shared_task, task
import random, datetime, json, requests
from lxml import etree
from time import sleep
from django.utils.timezone import now
from cookie.models import AccountModel, WebModel, ActiveRecordModel
from django.db.models import Q


@task
def check_account_need_auto_get_cookie():
    accounts = AccountModel.objects.filter(cookie='')
    for ac in accounts:
        if ac.web.half_or_auto_get_cookie == 'auto':
            auto_get_cookie(ac)
        # print(ac)


@task
def auto_get_cookie(account):
    start_datetime = now()
    name = account.web.name
    if name=='shanzhi':
        from website.shanzhi.auto_get_cookie import main
        status, cookie = main(account.username, account.password)
        if status:
            account.cookie = cookie
            account.save()
        else:
            return False
    else:
        return False
    end_datetime = now()
    arm = ActiveRecordModel(account=account, opera='自动登录提取Cookie', start_datetime=start_datetime, end_datetime=end_datetime)
    arm.save()
    return True


@task
def check_account_cookie_need_active():
    accounts = AccountModel.objects.filter(Q(web__active_cookie_use_python_or_javascript_script='default'), ~Q(cookie='')).order_by('-opera_datetime')[:2]
    for ac in accounts:
        activate_cookie(ac)

@task
def activate_cookie(account):
    start_datetime = datetime.datetime.now()
    # print(account.cookie,'-------------')
    cookie_dict = json.loads(account.cookie)
    session = requests.Session()
    session.cookies = requests.utils.cookiejar_from_dict(cookie_dict)
    num = 1
    while num <= 5:
        response = session.get(account.web.indexurl)
        html = etree.HTML(response.text)
        links = html.xpath(".//a/@href")
        link = random.choice(links)
        if not link:
            end_datetime = datetime.datetime.now()
            arm = ActiveRecordModel(account=account, start_datetime=start_datetime, end_datetime=end_datetime)
            arm.save()
            return False
        session.get(link)
        sleep(random.randint(4, 20))
        num += 1
    cookies_dict = requests.utils.dict_from_cookiejar(session.cookies)
    cookies_str = json.dumps(cookies_dict)
    account.cookie = cookies_str
    account.save()
    end_datetime = datetime.datetime.now()
    arm = ActiveRecordModel(account=account, opera='活跃Cookie', start_datetime=start_datetime, end_datetime=end_datetime)
    arm.save()
    return True

