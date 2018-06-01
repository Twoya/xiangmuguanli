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
    if not request.session.get('is_login', False) or request.session['user_type'] != 'information':
        return redirect("/index")
    error_msg = ''
    page = utils.get_page(args)  # 获取当前页面
    _projects_dict = utils.get_all_projects()
    page_list = utils.get_pages(page, _projects_dict)
    projects_dict, page, project_id = utils.adjust_info(_projects_dict, page, 1)
    if request.method == 'GET':
        return render(request, 'Administrators_projectsum.html',
                      {'projects_dict':projects_dict, "page_list":page_list, "page":page})
    if request.method == "POST":
        if request.POST.get("edit"):
            project_id = int(request.POST.get("edit"))
            for key, data in projects_dict:
                if key == project_id:
                    project_data = data
            return render(request, 'Administrators_edit.html', {"project_id": project_id,
                "project_data":project_data, "error_msg":error_msg, "page":page,
            })

def edit(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'information':
        return redirect("/index")
    error_msg = ''
    page = utils.get_page(args)  # 获取当前页面
    _projects_dict = utils.get_all_projects()
    page_list = utils.get_pages(page, _projects_dict)
    projects_dict, page, project_id = utils.adjust_info(_projects_dict, page, 1)
    if request.method == 'POST':
        project_id = int(request.POST.get("project_id"))
        for key, data in projects_dict:
            if key == project_id:
                project_data = data
        data = {
            "name": request.POST.get('name'),
            "leader": request.POST.get("leader").strip(),
            "teammates": request.POST.get("teammates").strip().split(',') if request.POST.get("teammates") else None,
            "start": request.POST.get("start").strip(),
            "status": request.POST.get("status").strip(),
            "process": request.POST.get("process").strip(),
            "budget": int(request.POST.get("budget").strip()),
            "real": int(request.POST.get("real").strip()),
        }
        data, error_msg = utils.check_error(data, budget=False)
        if error_msg:
            return render(request, 'Administrators_edit.html', {
                "project_id": project_id,
                "project_data": project_data, "error_msg": error_msg, "page": page,
            })
        if request.POST.get('pass'):
            # 立项审核通过
            data['status'] = "审核中..."
            data['left'] = data['budget'] - data['real']
        elif request.POST.get('reject'):
            # 立项审核未通过
            data['status'] = "未通过"
        elif request.POST.get('edit'):
            data['left'] = data['budget'] - data['real']
        with open("database/projects.pk", 'rb') as f:
            _projects_dict = pickle.load(f)
        for _key in data.keys():
            _projects_dict[project_id][_key] = data[_key]
        with open("database/projects.pk", 'wb') as f:
            f.write(pickle.dumps(_projects_dict))
        return redirect("/info/summary&page=%d" % page)


def process(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'information':
        return redirect("/index")
    error_msg, page, page_list, projects_dict, project_id = initialize(args, request)
    steps = utils.get_steps(project_id)
    step_list = []
    for obj in steps:
        step_list.append(obj[1]['flow'])
    step_path = utils.steps_path(utils.get_eva_info(project_id, top=True))
    if request.method == 'GET':
        return render(request, 'Administrators_process.html',{"projects_dict": projects_dict, "project_id":project_id,
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
            return redirect("/info/process&id=%d&page=%d"%(project_id, page))
        else:
            return render(request, 'Administrators_process.html',
                          {"projects_dict": projects_dict, "project_id": project_id,
                           "steps": steps, "step_path": step_path, "page_list": page_list, "page": page,
                           'error_msg': error_msg})


def evaluation(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'information':
        return redirect("/index")
    error_msg, page, page_list, projects_dict, project_id = initialize(args, request)
    eva_info = utils.get_eva_info(project_id)
    if request.method == 'GET':
        return render(request, 'Administrators_evaluation.html',
                      {"projects_dict": projects_dict, "project_id":project_id, "eva_info": eva_info,
                                    'page_list':page_list, 'page':page, 'error_msg':error_msg})
    if request.method == 'POST':
        for num in [1,2,3,4,5]:
            if request.POST.get("pass"+str(num)):
                with open("database/evaluation.pk", 'rb') as f:
                    eva = pickle.load(f)
                eva[project_id][num-1] = 2
                with open("database/evaluation.pk", 'wb') as f:
                    f.write(pickle.dumps(eva))
                return redirect("/info/evaluation&id=%d&page=%d"%(project_id, page))
            if request.POST.get("complete"):
                with open("database/projects.pk", 'rb') as f:
                    _projects_dict = pickle.load(f)
                if request.POST.get("complete")=="结束项目":
                    status, maintain = "已结题", 0
                else:
                    status, maintain = "使用中", int(_projects_dict[project_id]["budget"] * 0.1)
                _projects_dict[project_id]['status'] = status
                _projects_dict[project_id]['maintain'] = maintain
                _projects_dict[project_id]["end"] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                with open("database/projects.pk", 'wb') as f:
                    f.write(pickle.dumps(_projects_dict))
                return redirect("/info/evaluation&id=%d&page=%d"%(project_id, page))
        return render(request, 'Administrators_evaluation.html',
                      {"projects_dict": projects_dict, "project_id": project_id, "eva_info": eva_info,
                       'page_list': page_list, 'page': page, 'error_msg': error_msg})


def capitalpool(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'information':
        return redirect("/index")
    _projects_dict = utils.get_pass_projects()
    projects_dict = {}
    years_info = {}
    current_year = int(time.strftime('%Y', time.localtime(time.time())))
    current_date = int(time.strftime('%m%d', time.localtime(time.time())))
    for key, item in _projects_dict:
        item['year'] = 0
        if item.get('start', None) and item['start'][:4].isdigit:
            year = int(item['start'][:4])
            if year not in projects_dict:
                projects_dict[year] = []
            projects_dict[year].append((key, item))
            if year not in years_info:
                years_info[year] = {
                    "total": 0,
                    "use": 0,
                }
            years_info[year]['total'] += item['budget']
            years_info[year]['use'] += item['real']
            years_info[year]['left'] = years_info[year]['total'] - years_info[year]['use']
        if item.get('end', None) and item['end'][:4].isdigit and item.get("status", None) == "使用中":
            end_year = int(item['end'][:4])
            end_date = int(item['end'][5:7]+item['end'][8:])
            for year in range(end_year+1, current_year+1):
                if year not in projects_dict:
                    projects_dict[year] = []
                projects_dict[year].append((key, item))
                if year not in years_info:
                    years_info[year] = {
                        "total": 0,
                        "use": 0,
                    }
                item['year'] = current_year - end_year
                years_info[year]['total'] += item['maintain']
                if year < current_year or end_date < current_date:
                    years_info[year]['use'] += item['maintain']
                else:
                    item['year'] -= 1
                years_info[year]['left'] = years_info[year]['total'] - years_info[year]['use']
    year = None
    for item in args:
        if item is not None and "year=" in item and len(item) > 6:
            year = int(item[6:])
            break
    if not year or year not in years_info.keys():
        year = max(years_info.keys())
    years_info = years_info.items()
    years_info.sort(reverse=True)
    if request.method == "GET":
        return render(request, 'Administrators_capitalpool.html',
                      {"projects_dict": projects_dict[year], "years_info":years_info, "year":year, "stryear":str(year)})


def finance(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'information':
        return redirect("/index")
    error_msg, page, page_list, projects_dict, project_id = initialize(args, request,True)
    if request.method == 'GET':
        with open("database/finance.pk", 'rb') as f:
            finance = pickle.load(f)
        records = enumerate(finance.get(project_id, []))
        return render(request, 'Administrators_finance.html', {"records":records,"projects_dict": projects_dict,
               "project_id":project_id, "page_list":page_list, "page":page, 'error_msg':error_msg})
    if request.method == 'POST':
        if request.POST.get('pass'):
            id = int(request.POST.get("id"))
            with open("database/finance.pk", 'rb') as f:
                finance = pickle.load(f)
            finance[project_id][id]['status'] = "已通过"
            finance[project_id][id]['auditor'] = request.session["username"]
            with open("database/finance.pk", 'wb') as f:
                f.write(pickle.dumps(finance))
            return redirect("/info/finance&id=%d&page=%d" % (project_id, page))



def files(request, *args, **kwargs):
    if not request.session.get('is_login', False) or request.session['user_type'] != 'information':
        return redirect("/index")
    error_msg, page, page_list, projects_dict, project_id = initialize(args, request)
    if request.method == 'GET':
        return render(request, 'Administrators_filesum.html',
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
                return redirect("/info/files&id=%d&page=%d" % (project_id, page))

        project_id = int(request.POST.get("project_id"))
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
            return render(request, 'Administrators_file.html',
                          {"projects_dict": projects_dict, "project_id": project_id,
                           "file_record": _files[project_id], "page_list": page_list, "page": page,
                           'error_msg': error_msg})
        with open("database/files.pk", 'rb') as f:
            _files = pickle.load(f)
        file_record = _files.get(project_id, [None, None, None])
        return render(request, 'Administrators_file.html', {"projects_dict": projects_dict, "project_id": project_id,
                                                  "file_record": file_record, "page_list": page_list, "page": page,
                                                  'error_msg': error_msg})
