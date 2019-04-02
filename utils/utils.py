from functools import wraps
from PyQt4.QtCore import QString
import hashlib
import uuid

def singleton(cls):
    instances = {}
    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return getinstance

def get_uuid():
    return str(uuid.uuid1())

def to_python_str(from_str):
    if type(from_str) is QString:
        return str(unicode(from_str))
    else:
        return str(from_str)

def olt_con_hash_code(ip,port):
    str_key = ip + ':' + str(port)
    return hashlib.new('md5',str_key).hexdigest()

def onu_con_has_code(olt_has_code,slot_id,intf_id,onu_id):
    str_key = olt_has_code + str(slot_id) + str(intf_id) + str(onu_id)
    return hashlib.new('md5', str_key).hexdigest()