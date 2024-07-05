import inspect
import hashlib
import json

def get_source_code_hash(func):
    source_code = inspect.getsource(func)
    hasher = hashlib.sha256()
    hasher.update(source_code.encode('utf-8'))
    hash_digest = hasher.hexdigest()
    return source_code, hash_digest, func.__name__


def get_json_obj_hash(obj):
    serialized_obj = json.dumps(obj).encode('utf-8')
    hasher = hashlib.sha256()
    hasher.update(serialized_obj)
    hash_digest = hasher.hexdigest()
    return hash_digest