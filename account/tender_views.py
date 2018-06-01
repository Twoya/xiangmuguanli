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

def initialize(args, request, is_pass=False, tender=False):
    error_msg = ''
    project_id = utils.get_id(args)
    page = utils.get_page(args)  # 获取当前页面
    if is_pass:
        _projects_dict = utils.get_pass_projects()
    elif not tender:
        _projects_dict = utils.get_all_projects()
    else:
        _projects_dict = utils.get_tend_projects()
    page_list = utils.get_pages(page, _projects_dict)
    projects_dict, page, project_id = utils.adjust_info(_projects_dict, page, project_id)
    return error_msg, page, page_list, projects_dict, project_id

def summary(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'tender':
        return redirect("/index")
    error_msg = ''
    page = utils.get_page(args)  # 获取当前页面
    _projects_dict = utils.get_all_projects()
    page_list = utils.get_pages(page, _projects_dict)
    projects_dict, page, project_id = utils.adjust_info(_projects_dict, page, 1)
    if request.method == 'GET':
        return render(request, 'tender_projectsum.html',
                      {'projects_dict':projects_dict, "page_list":page_list, "page":page})



def process(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'tender':
        return redirect("/index")
    error_msg, page, page_list, projects_dict, project_id = initialize(args, request)
    steps = utils.get_steps(project_id)
    step_list = []
    for obj in steps:
        step_list.append(obj[1]['flow'])
    step_path = utils.steps_path(utils.get_eva_info(project_id, top=True))
    if request.method == 'GET':
        return render(request, 'tender_projcetprocess.html',{"projects_dict": projects_dict, "project_id":project_id,
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
            return redirect("/tender/process&id=%d&page=%d"%(project_id, page))
        else:
            return render(request, 'tender_projcetprocess.html',
                          {"projects_dict": projects_dict, "project_id": project_id,
                           "steps": steps, "step_path": step_path, "page_list": page_list, "page": page,
                           'error_msg': error_msg})


def check(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'tender':
        return redirect("/index")
    error_msg, page, page_list, projects_dict, project_id = initialize(args, request, tender=True)
    if request.method == 'GET':
        return render(request, 'tender_projectnew.html',
                      {'projects_dict':projects_dict, "page_list":page_list, "page":page})



def edit(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'tender':
        return redirect("/index")
    error_msg, page, page_list, projects_dict, project_id = initialize(args, request, tender=True)
    for key, data in projects_dict:
        if key == project_id:
            project_data = data
            break
    if request.method == 'GET':
        return render(request, "tender_edit.html", {"page":page, "project_data":project_data, "project_id":project_id})
    if request.method == 'POST':
        project_id = int(request.POST.get("project_id"))
        data = {
            "budget": utils.std_money(request.POST.get("budget").strip()),
            "tend": utils.std_money(request.POST.get("budget").strip())
        }
        if request.POST.get('pass'):
            # 立项审核通过
            data['status'] = "进行中"
            data['start'] = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        elif request.POST.get('reject'):
            # 立项审核未通过
            data['status'] = "未通过"
        with open("database/projects.pk", 'rb') as f:
            _projects_dict = pickle.load(f)
        for _key in data.keys():
            _projects_dict[project_id][_key] = data[_key]
        with open("database/projects.pk", 'wb') as f:
            f.write(pickle.dumps(_projects_dict))
        return redirect("/tender/check&page=%d" % page)





def evaluation(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'tender':
        return redirect("/index")
    error_msg, page, page_list, projects_dict, project_id = initialize(args, request)
    eva_info = utils.get_eva_info(project_id)
    if request.method == 'GET':
        return render(request, 'tender_evaluation.html',
                      {"projects_dict": projects_dict, "project_id":project_id, "eva_info": eva_info,
                                    'page_list':page_list, 'page':page, 'error_msg':error_msg})



def finance(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'tender':
        return redirect("/index")
    error_msg, page, page_list, projects_dict, project_id = initialize(args, request, True)
    if request.method == 'GET':
        return render(request, 'tender_finance.html', {"projects_dict": projects_dict,
               "project_id":project_id, "page_list":page_list, "page":page, 'error_msg':error_msg})
    if request.method == 'POST':
        project_id = int(request.POST.get("project_id"))
        tend = request.POST.get("tend")
        if tend.isdigit() and int(tend) > 0:
            tend = int(tend)
        else:
            error_msg = '请输入正确的招标金额'
            return render(request, 'tender_finance.html', {"projects_dict": projects_dict,
                                                           "project_id": project_id, "page_list": page_list,
                                                           "page": page, 'error_msg': error_msg})
        with open("database/projects.pk", 'rb') as f:
            projects = pickle.load(f)
        projects[project_id]["tend"] = tend
        with open("database/projects.pk", 'wb') as f:
            f.write(pickle.dumps(projects))
        return redirect("/tender/finance&page=%s" % page)


def files(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'tender':
        return redirect("/index")
    error_msg, page, page_list, projects_dict, project_id = initialize(args, request)
    if request.method == 'GET':
        return render(request, 'tender_filesum.html',
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
                return render(request, 'tender_file.html',
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
            return render(request, 'tender_file.html',
                          {"projects_dict": projects_dict, "project_id": project_id,
                           "file_record": _files[project_id], "page_list": page_list, "page": page,
                           'error_msg': error_msg})
        with open("database/files.pk", 'rb') as f:
            _files = pickle.load(f)
        file_record = _files.get(project_id, [None, None, None])
        return render(request, 'tender_file.html', {"projects_dict": projects_dict, "project_id": project_id,
                                                  "file_record": file_record, "page_list": page_list, "page": page,
                                                  'error_msg': error_msg})
