import pickle

with open("projects.pk", 'rb') as f:
    eva = pickle.load(f)

print eva