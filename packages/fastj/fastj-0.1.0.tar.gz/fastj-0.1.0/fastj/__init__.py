import json


def jd(d):
    return json.dumps(d)


def jl(d):
    return json.loads(d)


def jw(file_path, object, indent=4):
    with open(file_path, 'w') as j:
        json.dump(object, j, indent=indent)


def jr(file_path):
    with open(file_path, 'r') as j:
        return json.load(j)
