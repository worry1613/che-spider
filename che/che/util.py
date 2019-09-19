import execjs
import time
import math
import hashlib
from functools import partial
# from settings import signature_js_func,signature_js_path


signature_js_path = 'javascript/signature.js'
signature_js_func = 'get_sign'


ascp_js_path = './javascript/ascp.js'
ascp_js_func = 'ascp'


def getresponsejson(response):
    if response._body[0] == '{' and response._body[-1] == '}':
        return response._body
    start = response._body.find('(') + 1
    bodystr = response._body[start:-1]
    # ret = json.loads(bodystr)
    return bodystr


def get_js(js_file_path,mode='r'):

    f = open(js_file_path,mode)
    line = f.readline()
    result = ''
    while line:
        result +=  line
        line = f.readline()
    return result

def py_to_js(js_file_path,js_func,*params):

    js_script = get_js(js_file_path)
    JsContext = execjs.compile(js_script)
    result = JsContext.call(js_func,*params)
    return result

def get_ascp():

    t = int(math.floor(time.time()))
    e = hex(t).upper()[2:]
    m = hashlib.md5()
    m.update(str(t).encode(encoding='utf-8'))
    i = m.hexdigest().upper()
    if len(e) != 8:
        AS = '479BB4B7254C150'
        CP = '7E0AC8874BB0985'
        return AS,CP
    n = i[0:5]
    a = i[-5:]
    s = ''
    r = ''
    for o in range(5):
        s += n[o] + e[o]
        r += e[o + 3] + a[o]
    AS = 'A1' + s + e[-3:]
    CP = e[0:3] + r + 'E1'
    return AS,CP

def payload_for_get( id, mode, max_behot_time):

    _signature = py_to_js(signature_js_path, signature_js_func, id, max_behot_time)
    # ascp = py_to_js(ascp_js_path,ascp_js_func)
    _as,_cp = get_ascp()
    return {
        # 'page_type': mode,
        # 'user_id': id,
        # 'max_behot_time': max_behot_time,
        # 'count':'20',
        'as': _as,
        'cp': _cp,
        '_signature': _signature
    }

signature_func = partial(py_to_js,signature_js_path,signature_js_func)

