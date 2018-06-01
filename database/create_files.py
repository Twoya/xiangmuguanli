# -*- coding: utf-8 -*-

import pickle

files = {

}

with open("files.pk", 'wb') as f:
    f.write(pickle.dumps(files))