# -*- coding: utf-8 -*-

import pickle

projects = {
    1:{"name":"人脸识别系统",
        "leader": "weidaxun", "teammates":["baijingting", "sabeining"],"start": "2018-03-05", "process": "40%",
       "status": "进行中", "budget": 100000, "left":30000, "real":70000, "year":0, "maintain": 0,"remitted":40000, "tend":0
        },
    2:{"name":"项目管理系统",
        "leader": "baijingting", "teammates":["yangyang", "sabeining"],"start": "2018-02-10", "process": "60%",
       "status": "进行中", "budget": 100000, "left":60000, "real":40000, "year":0, "maintain": 0,"remitted":40000, "tend":0
        },
    3:{"name":"景观照明控制系统",
        "leader": "sabeining", "teammates":["baijingting", "yangyang"],"start": "2017-11-08", "process": "100%",
        "status": "使用中", "budget": 100000, "left":0, "real":100000, "year":2, "maintain": 30000,"remitted":100000, "tend":0
        },
    4: {"name": "海洋生物生态调研",
        "leader": "wuyingjie", "teammates": ["wangou", "yangyang"], "start": "2017-2-05", "process": "100%",
        "status": "已结题", "budget": 20000, "left": 0, "real": 20000, "year": 0, "maintain": 0,"remitted":20000, "tend":0
        },
}

with open("projects.pk", 'wb') as f:
    f.write(pickle.dumps(projects))