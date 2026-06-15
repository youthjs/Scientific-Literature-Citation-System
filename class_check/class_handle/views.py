from django.shortcuts import render, redirect
from .models import ClassCheckModel, UserInfoModel
from utils.model_check import check_handle
from django.http import JsonResponse



def index(request):
    return render(request, 'index.html')


def check(request):
    return render(request, 'check.html')


def show(request):
    return render(request, "show.html")

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        # 用户登录
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not (username or password):
            return JsonResponse({'code': 400, 'message': '缺少必传的参数'})
        user = UserInfoModel.objects.filter(username=username, password=password).first()
        if not user:
            return JsonResponse({'code': 400, 'message': '账号或密码错误'})
        request.session['login_in'] = True
        request.session['username'] = user.username
        request.session['user_id'] = user.id
        return JsonResponse({'code': 200})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not (username or password1 or password2):
            return JsonResponse({'code': 400, 'message': '缺少必传的参数'})

        if password1 != password2:
            return JsonResponse({'code': 400, 'message': '两次输入的密码不一致！'})

        flag = UserInfoModel.objects.filter(username=username).first()
        if flag:
            return JsonResponse({'code': 400, 'message': '该用户名已存在'})
        UserInfoModel.objects.create(
            username=username,
            password=password1,
        )
        return JsonResponse({'code': 200})


def logout(request):
    # 退出登录
    flag = request.session.clear()
    return redirect('/')



def news_check(request):
    news_text = request.POST.get('check_news')
    if news_text:
        news_text = str(news_text).replace(' ', '')
    else:
        return JsonResponse({'code': 400, 'message': '缺少必传的参数'})
    result = check_handle(news_text)
    ClassCheckModel.objects.create(news_text=news_text, check_result=result)
    data = {
        'pred_name': result
    }
    return JsonResponse({'code': 200, 'data': data})
