import pickle
a = {}

with open("stop.pk", 'wb') as f:
    f.write(pickle.dumps(a))