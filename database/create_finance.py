# -*- coding: utf-8 -*-

import pickle

finance = {

}

with open("finance.pk", 'wb') as f:
    f.write(pickle.dumps(finance))