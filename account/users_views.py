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
    _projects_dict = utils.get_projects(request.session['account'], is_pass)
    page_list = utils.get_pages(page, _projects_dict)
    projects_dict, page, project_id = utils.adjust_info(_projects_dict, page, project_id)
    return error_msg, page, page_list, projects_dict, project_id


def summary(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'accounts':
        return redirect("/index")
    error_msg = ''
    page = utils.get_page(args)  # 获取当前页面
    _projects_dict = utils.get_projects(request.session['account'])
    page_list = utils.get_pages(page, _projects_dict)
    projects_dict, page, project_id = utils.adjust_info(_projects_dict, page, 1)
    if request.method == 'GET':
        return render(request, 'user_projectsum.html',
                      {'projects_dict':projects_dict, "page_list":page_list, "page":page})
    if request.method == "POST":
        if request.POST.get("edit"):
            project_id = int(request.POST.get("edit"))
            for key, data in projects_dict:
                if key == project_id:
                    project_data = data
            return render(request, 'user_edit.html', {"project_id": project_id,
                "project_data":project_data, "error_msg":error_msg, "page":page,
            })


def new(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'accounts':
        return redirect("/index")
    error_msg = ''
    if request.method == 'GET':
        return render(request, 'user_projectnew.html', {"error_msg":error_msg})
    if request.method == 'POST':
        data = {
            "name": request.POST.get("name").strip(),
            "leader":request.POST.get("leader").strip(),
            "teammates":request.POST.get("teammates").strip().split(',')  if request.POST.get("teammates") else None,
            "budget":request.POST.get("budget").strip(),
        }
        data, error_msg = utils.check_error(data)
        if not request.FILES.get('file'):
            error_msg = "请上传文件"
        if error_msg:
            return render(request, 'user_projectnew.html', {"error_msg": error_msg})
        else:
            error_msg = '提交成功'
            id = utils.apply_project(data)
            utils.save_file(id, request, save_name="applyingFile",new=True)
            return render(request, 'user_projectnew.html', {"error_msg": error_msg})


def user_edit(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'accounts':
        return redirect("/index")
    error_msg = ''
    page = utils.get_page(args)  # 获取当前页面
    _projects_dict = utils.get_projects(request.session['account'])
    page_list = utils.get_pages(page, _projects_dict)
    projects_dict, page, project_id = utils.adjust_info(_projects_dict, page, 1)
    if request.method == 'POST':
        project_id = int(request.POST.get("project_id"))
        for key, data in projects_dict:
            if key == project_id:
                project_data = data
        data = {
            "name": request.POST.get("name").strip(),
            "leader": request.POST.get("leader").strip(),
            "teammates": request.POST.get("teammates").strip().split(',') if request.POST.get("teammates") else None
        }
        data, error_msg = utils.check_error(data, budget=False)
        if error_msg:
            return render(request, 'user_edit.html', {
                "project_id": project_id,
                "project_data": project_data, "error_msg": error_msg, "page": page,
            })
        else:
            if request.FILES.get('file'):
                utils.save_file(id, request, save_name="applyingFile", new=True)
            project_data['name'] = data['name']
            project_data['leader'] = data['leader']
            project_data['teammates'] = data['teammates']
            with open("database/projects.pk", 'rb') as f:
                _projects_dict = pickle.load(f)
            _projects_dict[project_id] = project_data
            with open("database/projects.pk", 'wb') as f:
                f.write(pickle.dumps(_projects_dict))
            return redirect("/account/summary&page=%d" % page)


def process(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'accounts':
        return redirect("/index")
    error_msg, page, page_list, projects_dict, project_id = initialize(args, request, True)
    if not project_id:
        return redirect('/account/summary')
    steps = utils.get_steps(project_id)
    step_path = utils.steps_path(utils.get_eva_info(project_id, top=True))
    if request.method == 'GET':
        return render(request, 'user_projectprocess.html',{"projects_dict": projects_dict, "project_id":project_id,
                    "steps":steps, "step_path":step_path, "page_list":page_list, "page":page, 'error_msg':error_msg})
    if request.method == "POST":
        data = {
            "mission" : request.POST.get("mission"),
            "flow": request.POST.get("flow"),
            "start" : request.POST.get("start"),
            "process" : request.POST.get("process"),
            "teammates": request.POST.get("teammates").strip().split(',') if request.POST.get("teammates") else None,
            "end" : request.POST.get("end"),
        }
        data, error_msg = utils.check_error(data, pro_name=False, budget=False)
        if not data.get("mission", None):
            error_msg = '请输入正确的任务名称'
        elif data.get("flow", None) not in ['1','2','3','4','5']:
            error_msg = '请输入正确的任务所属流程'
        # utils.add_steps(project_id, data)
        # return redirect("/account/process&id=%d&page=%d"%(project_id, page))
        if not error_msg:
            utils.add_steps(project_id, data)
            return redirect("/account/process&id=%d&page=%d" % (project_id, page))
        else:
            return render(request, 'user_projectprocess.html',
                          {"projects_dict": projects_dict, "project_id": project_id,
                           "steps": steps, "step_path": step_path, "page_list": page_list, "page": page,
                           'error_msg': error_msg})


def stop(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'accounts':
        return redirect("/index")
    error_msg = ''
    project_id = utils.get_id(args)
    page = utils.get_page(args)
    if request.method == "GET":
        for id, item in utils.get_projects(request.session['account']):
            if id == project_id:
                project_info = item
        return render(request, "user_projectstop.html", {"project_info":project_info, "project_id":project_id, "page":page , "error_msg": error_msg})
    if request.method == "POST":
        data = {
            "name": request.POST.get("name"),
            "leader": request.POST.get("leader"),
            "teammates": request.POST.get("teammates"),
            "start": request.POST.get("start"),
            "cost": request.POST.get("cost"),
        }
        if int(data['cost']) < 0:
            data['cost'] = '0'
        if not error_msg:
            error_msg = "项目申停成功"
            _projects_dict = utils.get_projects(request.session['account'])
            page_list = utils.get_pages(page, _projects_dict)
            projects_dict, page, project_id = utils.adjust_info(_projects_dict, page, project_id)
            steps = utils.get_steps(project_id)
            step_path = utils.steps_path(utils.get_eva_info(project_id, top=True))
            return render(request, "user_projectprocess.html",
                          {"projects_dict": projects_dict, "project_id": project_id,
                           "steps": steps, "step_path": step_path, "page_list": page_list, "page": page,
                           'error_msg': error_msg})


def evaluation(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'accounts':
        return redirect("/index")
    error_msg, page, page_list, projects_dict, project_id = initialize(args, request, True)
    if not project_id:
        return redirect('/account/summary')
    eva_info = utils.get_eva_info(project_id)
    steps = utils.get_steps(project_id)
    step_path = utils.steps_path(utils.get_eva_info(project_id, top=True))
    if request.method == 'GET':
        return render(request, 'user_evaluation.html',
                {"projects_dict": projects_dict, "project_id":project_id,
                 "eva_info": eva_info,
                 "steps": steps, "step_path": step_path,
                "page_list":page_list, "page":page, "error_msg":error_msg})
    if request.method == 'POST':
        for num in [1,2,3,4,5]:
            if request.FILES.get("file"+str(num)):
                with open("database/evaluation.pk", 'rb') as f:
                    eva = pickle.load(f)
                eva[project_id][num-1] = 1
                with open("database/evaluation.pk", 'wb') as f:
                    f.write(pickle.dumps(eva))
                utils.save_file(project_id, request, "file"+str(num), "evaluation%d"%num)
                return redirect("/account/evaluation&id=%d&page=%d"%(project_id, page))
        error_msg = '未选择文件'
        return render(request, 'user_evaluation.html',
                      {"projects_dict": projects_dict, "project_id": project_id, "eva_info": eva_info,
                       'page_list': page_list, 'page': page, 'error_msg': error_msg})


def finance(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'accounts':
        return redirect("/index")
    error_msg, page, page_list, projects_dict, project_id = initialize(args, request, True)
    if not project_id:
        return redirect('/account/summary')
    steps = utils.get_steps(project_id)
    step_path = utils.steps_path(utils.get_eva_info(project_id, top=True))
    if request.method == 'GET':
        with open("database/finance.pk", 'rb') as f:
            finance = pickle.load(f)
        records = enumerate(finance.get(project_id, []))
        return render(request, 'user_finance.html', {"records":records,"projects_dict": projects_dict, "project_id":project_id,
                     "steps": steps, "step_path": step_path,"page_list":page_list, "page":page, "error_msg":error_msg})


def new_finance(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'accounts':
        return redirect("/index")
    error_msg, page, page_list, projects_dict, project_id = initialize(args, request, True)
    if not project_id:
        return redirect('/account/summary')
    if request.method == 'GET':
        return render(request, 'user_financenew.html', {"projects_dict": projects_dict, "project_id":project_id,
                 "page_list":page_list, "page":page, 'error_msg':error_msg})
    if request.method == 'POST':
        data = {
            "name":request.POST.get("name"),
            "process": request.POST.get("process"),
            "where": request.POST.get("where"),
            "money": request.POST.get("money"),
            "time" : request.POST.get("time"),
            "consumer": request.POST.get("consumer"),
            "status": "审核中",
            "auditor": '',
        }
        if not request.FILES.get("file"):
            error_msg = '请上传发票证明'
            return render(request, 'user_financenew.html', {"projects_dict": projects_dict, "project_id": project_id,
                                                        "page_list": page_list, "page": page, 'error_msg': error_msg})
        else:
            with open("database/finance.pk", 'rb') as f:
                finance = pickle.load(f)
            if finance.get(project_id, None) is None:
                finance[project_id] = []
            finance[project_id].append(data)
            with open("database/finance.pk", 'wb') as f:
                f.write(pickle.dumps(finance))
            utils.save_file(project_id, request, save_name="record%d"%(len(finance[project_id])))
            return redirect("/account/finance&id=%d&page=%d" % (project_id, page))


def files(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'accounts':
        return redirect("/index")
    error_msg, page, page_list, projects_dict, project_id = initialize(args, request, True)
    if not project_id:
        return redirect('/account/summary')
    with open("database/files.pk", 'rb') as f:
        _files = pickle.load(f)
    file_record = _files.get(project_id, [None, None, None])
    if request.method == 'GET':
        return render(request, 'user_file.html', {"projects_dict": projects_dict, "project_id": project_id,
                            "file_record": file_record, "page_list": page_list, "page": page, 'error_msg': error_msg})
    if request.method == 'POST':
        _map = {"requirement": 0, "operation": 1, "inference": 2}
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
            return redirect("/account/files&id=%d&page=%d" % (project_id, page))

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
                return redirect("/account/files&id=%d&page=%d" % (project_id, page))
        else:
            error_msg = "未选择文件"
            return render(request, 'user_file.html', {"projects_dict": projects_dict, "project_id": project_id,
                                                      "file_record": file_record, "page_list": page_list, "page": page,
                                                      'error_msg': error_msg})


def user(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'accounts':
        return redirect("/index")
    if request.method == 'GET':
        return render(request, 'user.html', )

