# -*- coding: utf-8 -*-

import pickle

evaluation = {
    1: [2,2,1,0,0],
    2: [2,2,2,0,0],
    3: [2,2,2,2,2],
    4: [2,2,2,2,2],
}
with open("evaluation.pk", 'wb') as f:
    f.write(pickle.dumps(evaluation))