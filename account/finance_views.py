# -*- coding: utf-8 -*-

# from account.accounts import Account
# from account.decorators import login_exempt
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
import os
import time
import utils
import pickle

def initialize(args, request, is_pass=False):
    error_msg = ''
    project_id = utils.get_id(args)
    page = utils.get_page(args)  # 获取当前页面
    if is_pass:
        _projects_dict = utils.get_pass_projects()
    else:
        _projects_dict = utils.get_all_projects()
    page_list = utils.get_pages(page, _projects_dict)
    projects_dict, page, project_id = utils.adjust_info(_projects_dict, page, project_id)
    return error_msg, page, page_list, projects_dict, project_id

def summary(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'finance':
        return redirect("/index")
    error_msg = ''
    page = utils.get_page(args)  # 获取当前页面
    _projects_dict = utils.get_all_projects()
    page_list = utils.get_pages(page, _projects_dict)
    projects_dict, page, project_id = utils.adjust_info(_projects_dict, page, 1)
    if request.method == 'GET':
        return render(request, 'financeoff_projectsum.html',
                      {'projects_dict':projects_dict, "page_list":page_list, "page":page})




def process(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'finance':
        return redirect("/index")
    error_msg, page, page_list, projects_dict, project_id = initialize(args, request)
    steps = utils.get_steps(project_id)
    step_list = []
    for obj in steps:
        step_list.append(obj[1]['flow'])
    step_path = utils.steps_path(utils.get_eva_info(project_id, top=True))
    if request.method == 'GET':
        return render(request, 'financeoff_projectprocess.html',{"projects_dict": projects_dict, "project_id":project_id,
                    "steps":steps, "step_path":step_path, "page_list":page_list, "page":page, 'error_msg':error_msg})
    if request.method == "POST":
        data = {
        "mission" : request.POST.get("mission"),
        "flow": request.POST.get("flow"),
        "leader": request.POST.get("leader"),
        "start" : request.POST.get("start"),
        "process" : request.POST.get("process"),
        "teammates" : request.POST.get("teammates"),
        "end" : request.POST.get("end"),
        }
        if not data.get("mission", None):
            error_msg = '请输入正确的任务名称'
        elif data.get("flow", None) not in ['1','2','3','4','5']:
            error_msg = '请输入正确的任务所属流程'
        # utils.add_steps(project_id, data)
        # return redirect("/account/process&id=%d&page=%d"%(project_id, page))
        if not error_msg:
            utils.add_steps(project_id, data)
            return redirect("/admin/process&id=%d&page=%d"%(project_id, page))
        else:
            return render(request, 'financeoff_projectprocess.html',
                          {"projects_dict": projects_dict, "project_id": project_id,
                           "steps": steps, "step_path": step_path, "page_list": page_list, "page": page,
                           'error_msg': error_msg})


def evaluation(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'finance':
        return redirect("/index")
    error_msg, page, page_list, projects_dict, project_id = initialize(args, request)
    eva_info = utils.get_eva_info(project_id)
    if request.method == 'GET':
        return render(request, 'financeoff_evaluation.html',
                      {"projects_dict": projects_dict, "project_id":project_id, "eva_info": eva_info,
                                    'page_list':page_list, 'page':page, 'error_msg':error_msg})



def finance(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'finance':
        return redirect("/index")
    error_msg, page, page_list, projects_dict, project_id = initialize(args, request, True)
    if request.method == 'GET':
        return render(request, 'financeoff_finance.html', {"projects_dict": projects_dict,
               "project_id":project_id, "page_list":page_list, "page":page, 'error_msg':error_msg})



def detail(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'finance':
        return redirect("/index")
    error_msg, page, page_list, projects_dict, project_id = initialize(args, request, True)
    with open("database/detail.pk", 'rb') as f:
        detail = pickle.load(f)
    if detail.get(project_id, None) is None:
        detail[project_id] = {}
        with open("database/detail.pk", 'wb') as f:
            f.write(pickle.dumps(detail))
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    if request.method == 'GET':
        return render(request, 'financeoff_financedetail.html',
                      {"projects_dict": projects_dict,"project_id":project_id, "page_list":page_list,
                       "detail" : detail[project_id].items(), "page":page, 'error_msg':error_msg,
                       "date": date,})
    if request.method == 'POST':
        data = {
            "name": request.POST.get("name"),
            "money":request.POST.get("money"),
            "account":request.POST.get("account"),
            "date":request.POST.get("date"),
            "grant:":request.POST.get("grant"),
        }
        if not data.get("name", None):  # 检查项目名称是否合法
            error_msg = "请输入正确的款项名"
        # 负责人
        if not data.get("account", None):  # 检查负责人是否为空
            error_msg = "请输入正确负责人"
        elif utils.check_contain_chinese(data["account"]):  # 检查负责人账户是否合法
            username = utils.get_account(data["account"])
            if not username:
                error_msg = "用户 %s 不存在" % data['account']
            data['leader'] = username
        elif not utils.get_username(data["account"]):
            error_msg = "用户 %s 不存在" % data['account']
        # 检查预算
        if not data.get("money", None):
            error_msg = "请输入正确预算"
        else:
            data['money'] = utils.std_money(data['money'])
        if error_msg:
            return render(request, 'financeoff_financedetail.html',
                          {"projects_dict": projects_dict, "project_id": project_id, "page_list": page_list,
                           "detail": detail[project_id].items(), "page": page, 'error_msg': error_msg,
                           "date": date, })
        else:
            with open("database/detail.pk", 'rb') as f:
                detail = pickle.load(f)
            if detail.get(project_id, None) is None:
                detail[project_id] = {}
            try:
                detail[project_id][max(detail[project_id].keys())+1] = data
            except:
                detail[project_id][1] = data
            with open("database/detail.pk", 'wb') as f:
                f.write(pickle.dumps(detail))
            with open("database/projects.pk", 'rb') as f:
                projects = pickle.load(f)
            projects[project_id]["remitted"] += data['money']
            with open("database/projects.pk", 'wb') as f:
                f.write(pickle.dumps(projects))
            return render(request, 'financeoff_financedetail.html',
                          {"projects_dict": projects_dict, "project_id": project_id, "page_list": page_list,
                           "detail": detail[project_id].items(), "page": page, 'error_msg': error_msg,
                           "date": date, })




def files(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'finance':
        return redirect("/index")
    error_msg, page, page_list, projects_dict, project_id = initialize(args, request)
    if request.method == 'GET':
        return render(request, 'financeoff_filesum.html',
                      {'projects_dict':projects_dict, "page_list":page_list, "page":page})
    if request.method == "POST":
        _map = {"requirement": 0, "operation": 1, "inference": 2}
        for file_name in _map.keys():
            if request.FILES.get(file_name):
                with open("database/files.pk", 'rb') as f:
                    _files = pickle.load(f)
                if _files.get(project_id, None) is None:
                    _files[project_id] = [None, None, None]
                _files[project_id][_map[file_name]] = {"person":request.session["username"],
                                                       "date": time.strftime('%Y-%m-%d',time.localtime(time.time()))}
                with open("database/files.pk", 'wb') as f:
                    f.write(pickle.dumps(_files))
                utils.save_file(project_id,request,file_name,file_name)
                return render(request, 'financeoff_file.html',
                              {"projects_dict": projects_dict, "project_id": project_id,
                               "file_record": _files[project_id], "page_list": page_list, "page": page,
                               'error_msg': error_msg})
        if request.POST.get('delete'):
            target = request.POST.get('delete')
            for file_name in os.listdir("database/files/%d" % project_id):
                if target in file_name:
                    os.remove("database/files/%d/%s" % (project_id, file_name))
            with open("database/files.pk", 'rb') as f:
                _files = pickle.load(f)
            _files[project_id][_map[target]] = None
            with open("database/files.pk", 'wb') as f:
                f.write(pickle.dumps(_files))
            return render(request, 'financeoff_file.html',
                          {"projects_dict": projects_dict, "project_id": project_id,
                           "file_record": _files[project_id], "page_list": page_list, "page": page,
                           'error_msg': error_msg})
        with open("database/files.pk", 'rb') as f:
            _files = pickle.load(f)
        file_record = _files.get(project_id, [None, None, None])
        return render(request, 'financeoff_file.html', {"projects_dict": projects_dict, "project_id": project_id,
                                                  "file_record": file_record, "page_list": page_list, "page": page,
                                                  'error_msg': error_msg})
