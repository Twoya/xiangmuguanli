# -*- coding: utf-8 -*-

import pickle

steps ={
1:[
    {"mission":"需求调研", "flow":1,"leader":"baijingting","start":"2018-03-05","process": "100%", "teammates":["weidaxun"],"end":"2018-03-20",},
    {"mission":"文献查阅", "flow":1,"leader":"weidaxun","start":"2018-03-20","process": "100%", "teammates":"","end":"2018-03-30",},
    {"mission":"器材购买", "flow":2,"leader":"baijingting","start":"2018-04-01","process": "70%", "teammates":"","end":"2018-04-30",},
],
2:[
    {"mission":"需求调研", "flow":1,"leader":"baijingting","start":"2018-02-24","process": "100%", "teammates":["yangyang"],"end":"2018-03-21",},
    {"mission":"代码编写", "flow":2,"leader":"yangyang","start":"2018-03-20","process": "20%", "teammates":["sabeining","baijingting"],"end":"2018-05-20",},
],
3:[
    {"mission":"开题调研", "flow":1,"leader":"sabeining","start":"2017-11-08","process": "100%", "teammates":["yangyang"],"end":"2017-12-01",},
    {"mission":"器材购买", "flow":2,"leader":"yangyang","start":"2018-01-01","process": "100%", "teammates":["sabeining"],"end":"2018-01-05",},
    {"mission":"结题答辩", "flow":5,"leader":"sabeining","start":"2017-05-01","process": "100%", "teammates":["yangyang"],"end":"2018-05-02",},
],
4:[
    {"mission":"开题调研", "flow":1,"leader":"wangou","start":"2017-03-01","process": "100%", "teammates":["wuyingjie"],"end":"2017-04-01",},
],
}


with open("steps.pk", 'wb') as f:
    f.write(pickle.dumps(steps))