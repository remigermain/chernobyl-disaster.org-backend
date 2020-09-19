import json



lst = []

def gen_path(path, key):
    return f"{path}.{key}" if path else key

def depth_dict(path, element):
    if isinstance(element, dict):
        for key, value in element.items():
            depth_dict(gen_path(path, key), value)
    elif isinstance(element, str):
        lst.append([path, element])
    else:
        raise TypeError(f"file type error {type(element)}")


test = {
    'a': {
        'b': "lalalal",
        'c': 'fggggg',
        'd': {
            'd': 'ddd'
        }
    },
    'dd': [
        "eferfer"
    ]
}


depth_dict("", test)
print(lst)
print("--end--")