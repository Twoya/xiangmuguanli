# -*- coding: utf-8 -*-

import pickle

accounts = {
    "baijingting": ["baijingting", "白敬亭"],
    "weidaxun": ["weidaxun", "魏大勋"],
    "sabeining": ["sabeining", "撒贝宁"],
    "yangyang": ["yangyang", "杨洋"],
    "wangou": ["wangou", "王鸥"],
    "wuyingjie": ["wuyingjie", "吴映洁"],
    "liyingying": ["liyingying", "二丫"],
}
administor = {
    "admin": ["admin", "管理员"],
}
information = {
    'information': ['information', "信息办"],
}
finance = {
    "finance": ["finance", "财务处"],
}
tender = {
    "tender": ["tender", "采招办"],
}
users = {
    "accounts": accounts,
    "admin": administor,
    "information": information,
    "finance": finance,
    "tender": tender,
}

with open("users_db.pk", 'wb') as f:
    f.write(pickle.dumps(users))
