# -*- coding: utf-8 -*-

from common.mymako import render_mako_context
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
import utils

user_info = {
    "is_login": False,
    "username": '',
    "user_type": None,
}

def index(request):
    """登录界面"""
    error_msg = ''
    if request.method == 'GET':
        return render(request, 'index.html', {'error_msg': error_msg})
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        login_data = utils.validation(username, password)
        if not login_data['is_login']:
            return render(request, 'index.html', {'error_msg': login_data['error_msg']})
        else:
            request.session['is_login'] = True
            request.session['username'] = login_data['username']
            request.session['account'] = username
            request.session['user_type'] = login_data['user_type']
            if login_data['user_type'] == 'accounts':
                return redirect('/account/summary')
            elif login_data['user_type'] == 'information':
                return redirect('/info/summary')
            elif login_data['user_type'] == 'finance':
                return redirect('/finance/summary')
            elif login_data['user_type'] == 'tender':
                return redirect('/tender/summary')
            elif login_data['user_type'] == 'admin':
                return redirect('/admin/summary')

def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/home.html')


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')
