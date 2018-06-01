# -*- coding: utf-8 -*-

import pickle

detail = {
    1:{
        1:{"name": "预付款", "money": 20000, "account":"魏大勋","date":"2018-03-01","grant":"财务处"},
        2:{"name":"中期拨款", "money": 20000,"account":"魏大勋","date":"2018-04-01","grant":"财务处" },
    },
    2:{
        1:{"name": "预付款", "money": 20000, "account":"白敬亭","date":"2018-04-02","grant":"财务处"},
        2:{"name":"交通报销", "money": 20000,"account":"白敬亭","date":"2018-04-18","grant":"财务处" },
    },
    3:{
        1:{"name": "预付款", "money": 20000, "account":"撒贝宁","date":"2017-11-08","grant":"财务处"},
        2:{"name":"项目尾款", "money": 20000,"account":"撒贝宁","date":"2018-03-18" ,"grant":"财务处"},
        3:{"name":"项目维护", "money": 15000,"account":"撒贝宁","date":"2018-04-20","grant":"财务处" },
        4:{"name":"项目维护", "money": 15000,"account":"撒贝宁","date":"2018-05-20" ,"grant":"财务处"},
    },
    4:{
        1:{"name": "预付款", "money": 4000, "account":"王鸥","date":"2017-05-20","grant":"财务处"},
        2:{"name": "项目尾款", "money": 16000, "account":"王鸥","date":"2017-12-25","grant":"财务处"},
    },
}

with open("detail.pk", 'wb') as f:
    f.write(pickle.dumps(detail))