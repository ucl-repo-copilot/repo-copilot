from cache.element import Element

__cache : dict[str, Element] = {}

def get(key):
    if key in __cache:
        return __cache[key]
    else:
        KeyError(f"Key {key} not found in cache")

def set(key, value):
    __cache[key] = value
    
def delete(key):
    del __cache[key]
    
def clear():
    __cache.clear()

def get_size():
    return len(__cache)

def get_items():
    return __cache.items()

def get_keys():
    return __cache.keys()

def get_values():
    return __cache.values()