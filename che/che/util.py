#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import hashlib
import execjs

def getresponsejson(response):
    if response._body[0] == '{' and response._body[-1] == '}':
        return response._body
    start = response._body.find('(') + 1
    bodystr = response._body[start:-2]
    # ret = json.loads(bodystr)
    return bodystr

def getHoney(t):  #####根据JS脚本破解as ,cp
    # t = int(time.time())  #获取当前时间
    # t=1534389637
    # print(t)
    e = str('%X' % t)  ##格式化时间
    # print(e)
    m1 = hashlib.md5()  ##MD5加密
    m1.update(str(t).encode(encoding='utf-8'))  ##转化格式
    i = str(m1.hexdigest()).upper()  ####转化大写
    # print(i)
    n = i[0:5]  ##获取前5位
    a = i[-5:]  ##获取后5位
    s = ''
    r = ''
    for x in range(0, 5):
        s += n[x] + e[x]
        r += e[x + 3] + a[x]
    eas = 'A1' + s + e[-3:]
    ecp = e[0:3] + r + 'E1'
    # print(eas)
    # print(ecp)
    return eas, ecp

def get_js():
    f = open(r"toutiao-TAC.sign", 'r')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    ctx = execjs.compile(htmlstr)
    f.close()
    return ctx.call('get_as_cp_signature')
