from django.db import models
from django.utils.timezone import now


class WebModel(models.Model):
    name = models.CharField(default='', max_length=64, verbose_name="网站名称")
    loginurl = models.CharField(default='', max_length=255, verbose_name="登录网址")
    indexurl = models.CharField(default='', max_length=255, verbose_name="首页网址")

    HALF_OR_AUTO = (('auto', 'auto'), ('half', 'half'))
    half_or_auto_get_cookie = models.CharField(choices=HALF_OR_AUTO, default='auto', max_length=32,
                                               verbose_name="全自动或半自动获取Cookie")
    extract_cookie_script = models.TextField(default='', verbose_name="提取Cookie的Python脚本", blank=True, null=True)

    SCRIPT = (('python', 'python'), ('javascript', 'javascript'), ('default', 'default'))
    active_cookie_use_python_or_javascript_script = models.CharField(max_length=64, choices=SCRIPT, default='default',
                                                                     verbose_name="选择使用脚本")
    active_js_script = models.TextField(default='', verbose_name="活跃Cookie的JS脚本", blank=True, null=True)
    wait_exec_active_js_script = models.IntegerField(default=100, verbose_name="等待JS执行的时间")
    active_python_script = models.TextField(default='', verbose_name="活跃Cookie的Python脚本", blank=True, null=True)

    def __str__(self):
        return f"{self.name}网站，目前有{self.accounts.count()}个会员账号"


class AccountModel(models.Model):
    web = models.ForeignKey(to=WebModel, on_delete=models.CASCADE, related_name="accounts", verbose_name="归属网站")
    username = models.CharField(default='', max_length=64, verbose_name="账号")
    password = models.CharField(default='', max_length=64, verbose_name="密码")
    cookie = models.TextField(default='', verbose_name="Cookie", blank=True, null=True)
    opera_datetime = models.DateTimeField(verbose_name="操作时间", auto_now=True)

    @property
    def active_cookie_use_python_or_javascript_script(self):
        return self.web.active_cookie_use_python_or_javascript_script

    def __str__(self):
        return f"{self.username}账号归属于{self.web.name},当前Cookie：{self.cookie}"

    def to_dict(self):
        temp_dict = {
            'web': {
                'name': self.web.name,
                'loginurl': self.web.loginurl,
                'indexurl': self.web.indexurl,
            },
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'extract_cookie_script': self.web.extract_cookie_script,
        }
        return temp_dict

    def cookie_to_dict(self):
        temp_dict = {
            'web': {
                'name': self.web.name,
                'loginurl': self.web.loginurl,
                'indexurl': self.web.indexurl,
            },
            'id': self.id,
            'username': self.username,
            'cookie': self.cookie,
            'active_cookie_use_python_or_javascript_script': self.web.active_cookie_use_python_or_javascript_script,
            'active_js_script': self.web.active_js_script,
            'wait_exec_active_js_script': self.web.wait_exec_active_js_script,
            'active_python_script': self.web.active_python_script,
        }
        return temp_dict


class ActiveRecordModel(models.Model):
    account = models.ForeignKey(to=AccountModel, on_delete=models.CASCADE, related_name="active_record",
                                verbose_name="归属账号")
    opera = models.CharField(default='', verbose_name="操作", max_length=128, null=True, blank=True)
    start_datetime = models.DateTimeField(default=now, verbose_name="开始时间")
    end_datetime = models.DateTimeField(default=now, verbose_name="结束时间")

    def __str__(self):
        return f"{self.account.username}活跃记录，进行了{self.opera}操作，开始于{self.start_datetime}, 结束于{self.end_datetime}"
