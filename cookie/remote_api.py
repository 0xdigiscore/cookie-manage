from django.http.response import JsonResponse
from cookie.models import AccountModel, WebModel
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


def get_account_info(request):
    accounts = AccountModel.objects.filter(web__half_or_auto_get_cookie='half', cookie='').order_by('?')
    if accounts:
        account = accounts.first()
        ac_dict = account.to_dict()
        ac_dict['code'] = 200
        ac_dict['message'] = "成功拿到一个需要协助登录的账号数据"
    else:
        return JsonResponse({'code':404,'message':'未发现对应的账号信息'}, status=404, json_dumps_params={'ensure_ascii': False})
    return JsonResponse(ac_dict, status=200, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def post_account_cookie_info(request):
    account_cookie_str = request.body.decode("utf8")
    account_cookie_dict = json.loads(account_cookie_str)
    if not account_cookie_dict:
        return JsonResponse({'code':404,'message':'未发现对应的账号信息'}, status=404, json_dumps_params={'ensure_ascii': False})
    id = account_cookie_dict['id']
    account = AccountModel.objects.filter(id=id).first()
    if not account:
        return JsonResponse({'code': 404, 'message': '未发现对应的账号信息'}, status=404,
                            json_dumps_params={'ensure_ascii': False})
    else:
        account.cookie = account_cookie_dict['cookie']
        account.save()
    return JsonResponse({'code':200,'message':'成功'}, status=200, json_dumps_params={'ensure_ascii': False})





def get_account_cookie_active_info(request):
    accounts = AccountModel.objects.filter(~Q(web__active_cookie_use_python_or_javascript_script='default'), ~Q(cookie='')).order_by('-opera_datetime')
    if accounts:
        account = accounts.first()
        ac_dict = account.cookie_to_dict()
        ac_dict['code'] = 200
        ac_dict['message'] = "成功拿到一个需要协助登录的账号数据"
    else:
        return JsonResponse({'code':404,'message':'未发现对应的账号信息'}, status=404, json_dumps_params={'ensure_ascii': False})
    return JsonResponse(ac_dict, status=200, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def post_account_cookie_active_info(request):
    account_cookie_str = request.body.decode("utf8")
    account_cookie_dict = json.loads(account_cookie_str)
    if not account_cookie_dict:
        return JsonResponse({'code':404,'message':'未发现对应的账号信息'}, status=404, json_dumps_params={'ensure_ascii': False})
    id = account_cookie_dict['id']
    account = AccountModel.objects.filter(id=id).first()
    if not account:
        return JsonResponse({'code': 404, 'message': '未发现对应的账号信息'}, status=404,
                            json_dumps_params={'ensure_ascii': False})
    else:
        account.cookie = account_cookie_dict['cookie']
        account.save()
    return JsonResponse({'code':200,'message':'成功'}, status=200, json_dumps_params={'ensure_ascii': False})