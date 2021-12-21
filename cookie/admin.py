from django.contrib import admin
from cookie.models import AccountModel, WebModel, ActiveRecordModel


class AccountModelAdmin(admin.ModelAdmin):
    # 需要显示的字段信息
    list_display = ('id', 'username', 'opera_datetime','active_cookie_use_python_or_javascript_script','cookie')
    # 设置哪些字段可以点击进入编辑界面，默认是第一个字段
    list_display_links = ('id', 'username')

admin.site.register(WebModel)
admin.site.register(AccountModel, AccountModelAdmin)
admin.site.register(ActiveRecordModel)
