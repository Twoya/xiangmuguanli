# -*- coding: utf-8 -*-
import pickle
import re, os, shutil
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def check_contain_chinese(check_str):
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False



def check_error(data, teammates=True, pro_name=True, leader=True, budget=True):
    error_msg = ''
    # 队友
    if teammates:
        if not data.get("teammates", None):
            data["teammates"] = " "
        else:       # 如果有队友，就对队友进行账户合法性检测
            for key, name in enumerate(data["teammates"]):
                if check_contain_chinese(name):
                    username = get_account(name)
                    if not username:
                        error_msg = "用户 %s 不存在" % data["teammates"][key]
                        break
                    data["teammates"][key] = username
                elif not get_username(name):
                    error_msg = "用户 %s 不存在" % name
    # 项目名
    if pro_name:
        if not data.get("name", None):      # 检查项目名称是否合法
            error_msg = "请输入正确项目名"
    # 负责人
    if leader:
        if not data.get("leader", None):    # 检查负责人是否为空
            error_msg = "请输入正确负责人"
        elif check_contain_chinese(data['leader']):     # 检查负责人账户是否合法
            username = get_account(data['leader'])
            if not username:
                error_msg = "用户 %s 不存在" % data['leader']
            data['leader'] = username
        elif not get_username(data['leader']):
            error_msg = "用户 %s 不存在" % data['leader']
    # 检查预算
    if budget:
        if not data.get("budget", None):
            error_msg = "请输入正确预算"
        else:
            data['budget'] = std_money(data['budget'])
    return data, error_msg



def std_money(money):
    # if type(money) == str:
    #     if money.encode('gbk')[-1] == u"万":
    #         money = float(money.encode('gbk')[:-1]) * 10000
    return int(float(money))


def validation(username, password):
    # 模拟数据库操作
    # accounts 和 administor都是字典
    data = {
        "username": username,
        "is_login": False,
        "user_type": None,
        "error_msg": '',
    }
    with open("database/users_db.pk", 'rb') as f:
        users = pickle.load(f)
    for user_dict in users:
        if users[user_dict].get(username, None) is not None:
            if users[user_dict][username][0] != password:
                data['error_msg'] = '密码错误'
                break
            else:
                data['is_login'] = True
                data['user_type'] = user_dict
                data['username'] = users[user_dict][username][1]
    if not data['is_login'] and data['error_msg'] == '':
        data['error_msg'] = '用户不存在'
    return data


def get_username(username):
    with open("database/users_db.pk", 'rb') as f:
        users = pickle.load(f)
    for user_dict in users:
        if users[user_dict].get(username, None) is not None:
            return users[user_dict][username][1]
    return ''


def get_account(username):
    with open("database/users_db.pk", 'rb') as f:
        users = pickle.load(f)
    for item in users['accounts'].values():
        if item[1] == username:
            return item[0]
    return ''


def get_id(args):
    id = None
    for item in args:
        if item is not None and "id=" in item and len(item) > 4:
            id = int(item[4:])
            break
    return id


def get_page(args):
    current_page = None
    for item in args:
        if item is not None and "page=" in item and len(item) > 6:
            current_page = item[6:]
            break
    if not current_page or int(current_page) < 1:
        current_page = 1
    return int(current_page)


def get_projects(username, is_pass=False):
    with open("database/projects.pk", 'rb') as f:
        projects = pickle.load(f)
    pro_dict = {}
    for key in projects.keys():
        if (username in projects[key]["teammates"] or username == projects[key]["leader"]) \
                and (not is_pass or projects[key]['status'] in ['进行中', '已结题', '使用中'] ):
            pro_dict[key] = projects[key].copy()
            pro_dict[key]['leader'] = get_username(pro_dict[key]['leader'])
            try:
                for _key, teammate in enumerate(pro_dict[key]['teammates']):
                    pro_dict[key]['teammates'][_key] = get_username(pro_dict[key]['teammates'][_key])
                pro_dict[key]['teammates'] = ','.join(pro_dict[key]['teammates'])
                if pro_dict[key]['teammates'].count(',') > 1:
                    pro_dict[key]['teammates'] = pro_dict[key]['teammates'].replace(',','',pro_dict[key]['teammates'].count(',')-1)
            except:
                pass
            for __key in pro_dict[key]:
                if pro_dict[key][__key] is None or type(pro_dict[key][__key]) == str and pro_dict[key][__key].strip()=='':
                    pro_dict[key][__key] = ''
    pro_dict = pro_dict.items()
    pro_dict.sort()
    return pro_dict


def get_steps(id):
    if type(id) != int:
        id = int(id)
    with open("database/steps.pk", 'rb') as f:
        steps = pickle.load(f)
    steps_dict = []
    if steps.get(id, None) is not None:
        for key, step in enumerate(steps[id]):
            steps_dict.append((key, step))
    return steps_dict


def steps_path(current_step):
    res = []
    for key, value in enumerate(["需求分析", "立项审核", "前期成果", "中期成果", "项目结题"]):
        if key < int(current_step):
            res.append(('king-pearl done', key+1, value))
        else:
            res.append(('king-pearl', key+1, value))
    return res


def apply_project(data):
    with open("database/projects.pk", 'rb') as f:
        projects = pickle.load(f)
    id = max(projects.keys())+1
    projects[id]={"name": data['name'], "leader": data['leader'],
       "teammates": data['teammates'], "budget": data['budget'], "start": ' ', "process": "0%",
       "status": "审核中","left":0, "real":0, "year":0, "maintain": 0, "remitted":0, "tend":0}
    with open("database/projects.pk", 'wb') as f:
        f.write(pickle.dumps(projects))
    with open("database/evaluation.pk", 'rb') as f:
        eva = pickle.load(f)
    eva[id] = [0,0,0,0,0]
    with open("database/evaluation.pk", 'wb') as f:
        f.write(pickle.dumps(eva))
    return id


def save_file(id, request, file_name="file", save_name=None, new=False):
    if request.FILES.get(file_name):
        if not os.path.exists("database/files/%d" % id):    # 如果没有文件夹，就新建一个
            os.mkdir("database/files/%d" % id)
        elif new:   # 覆盖原有的文件
            shutil.rmtree("database/files/%d" % id)
        obj = request.FILES.get(file_name)
        if not save_name:   # 如果没指定保存名
            save_name = obj.name
        else:     # 拼接文件名后缀
            save_name += '.'+obj.name.split('.')[-1]
        with open("database/files/%d/%s" % (id, save_name), "wb") as f:
            for i in obj.chunks():
                f.write(i)


def get_pages(page, info_list):
    # 每页显示五条数据
    # page是当前
    each_page = 6       # 每页显示的数据条数
    page_showed = 2     # 当前页面的前后显示多少页
    page_list = ""
    page_start, page_end = 0, 0     # 页码起始，页码结尾
    try:
        page = 0 if page < 1 else int(page)
    except:
        page = 1
    all_page, c = divmod(len(info_list), each_page)
    if c > 0:
        all_page += 1
    if all_page > page_showed * 2 + 1:
        if page <= page_showed:
            page_start, page_end = 1, 2*page_showed + 1
        elif page >= all_page - page_showed:
            page_start, page_end = all_page - 2*page_showed, all_page
        else:
            page_start, page_end = page - page_showed, page + page_showed
    else:
        page_start, page_end = 1, all_page
    return list(range(page_start, page_end+1))


def adjust_info(projects_dict, page, project_id):
    each_page = 6  # 每页显示的数据条数
    all_page, c = divmod(len(projects_dict), each_page)
    if c > 0:
        all_page += 1
    if page > all_page:
        page = all_page
    projects_dict = projects_dict[each_page * (page - 1): each_page * page]
    id_list = []
    for item in projects_dict:
        id_list.append(item[0])
    if project_id not in id_list and id_list != []:
        project_id = id_list[0]
    return projects_dict, page, project_id


def add_steps(id, data):
    with open("database/steps.pk", 'rb') as f:
        steps = pickle.load(f)
    if not steps.get(id, None):
        steps[id] = []
    steps[id].append(data)
    with open("database/steps.pk", 'wb') as f:
        f.write(pickle.dumps(steps))


def apply_stop(id, data):
    with open("database/stop.pk", 'rb') as f:
        stop = pickle.load(f)
    stop[id] = data
    with open("database/steps.pk", 'wb') as f:
        f.write(pickle.dumps(stop))


def get_eva_info(id, top=False):
    with open("database/evaluation.pk", 'rb') as f:
        eva = pickle.load(f)
    if not eva.get(id, None):
        eva[id] = [0,0,0,0,0]
        with open("database/evaluation.pk", 'wb') as f:
            f.write(pickle.dumps(eva))
    res = eva.get(id, None)
    if top:
        for key, i in enumerate(res):
            if i != 2:
                return key
        return 5
    return res


def get_all_projects():
    with open("database/projects.pk", 'rb') as f:
        projects = pickle.load(f)
    pro_dict = {}
    for key in projects.keys():
        if projects[key]['status']  not in ['未通过']:
            pro_dict[key] = projects[key]
            pro_dict[key]['leader'] = get_username(pro_dict[key]['leader'])
            try:
                for _key, teammate in enumerate(pro_dict[key]['teammates']):
                    pro_dict[key]['teammates'][_key] = get_username(teammate)
                pro_dict[key]['teammates'] = ','.join(pro_dict[key]['teammates'])
                if pro_dict[key]['teammates'].count(',') > 1:
                    pro_dict[key]['teammates'] = pro_dict[key]['teammates'].replace(',', '',
                                                    pro_dict[key]['teammates'].count(',') - 1)
            except:
                pass
            for __key in pro_dict[key]:
                if pro_dict[key][__key] is None or type(pro_dict[key][__key]) == str and pro_dict[key][__key].strip() == '':
                    pro_dict[key][__key] = ''
    pro_dict = pro_dict.items()
    pro_dict.sort()
    return pro_dict

def get_pass_projects():
    with open("database/projects.pk", 'rb') as f:
        projects = pickle.load(f)
    pro_dict = {}
    for key in projects.keys():
        if projects[key]['status'] in ['进行中', '已结题', '使用中']:
            pro_dict[key] = projects[key]
            pro_dict[key]['leader'] = get_username(pro_dict[key]['leader'])
            try:
                for _key, teammate in enumerate(pro_dict[key]['teammates']):
                    pro_dict[key]['teammates'][_key] = get_username(teammate)
                pro_dict[key]['teammates'] = ','.join(pro_dict[key]['teammates'])
                if pro_dict[key]['teammates'].count(',') > 1:
                    pro_dict[key]['teammates'] = pro_dict[key]['teammates'].replace(',', '',
                                                    pro_dict[key]['teammates'].count(',') - 1)
            except:
                pass
            for __key in pro_dict[key]:
                if pro_dict[key][__key] is None or type(pro_dict[key][__key]) == str and pro_dict[key][__key].strip() == '':
                    pro_dict[key][__key] = ''
    pro_dict = pro_dict.items()
    pro_dict.sort()
    return pro_dict


def get_tend_projects():
    with open("database/projects.pk", 'rb') as f:
        projects = pickle.load(f)
    pro_dict = {}
    for key in projects.keys():
        if projects[key]['status'] in ['审核中...']:
            pro_dict[key] = projects[key]
            pro_dict[key]['leader'] = get_username(pro_dict[key]['leader'])
            try:
                for _key, teammate in enumerate(pro_dict[key]['teammates']):
                    pro_dict[key]['teammates'][_key] = get_username(teammate)
                pro_dict[key]['teammates'] = ','.join(pro_dict[key]['teammates'])
                if pro_dict[key]['teammates'].count(',') > 1:
                    pro_dict[key]['teammates'] = pro_dict[key]['teammates'].replace(',', '',
                                                    pro_dict[key]['teammates'].count(',') - 1)
            except:
                pass
            for __key in pro_dict[key]:
                if pro_dict[key][__key] is None or type(pro_dict[key][__key]) == str and pro_dict[key][__key].strip() == '':
                    pro_dict[key][__key] = ''
    pro_dict = pro_dict.items()
    pro_dict.sort()
    return pro_dict