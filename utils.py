import os.path
import time
import json


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.gua.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)

def translate_time(ltime):
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(ltime)
    dt = time.strftime(format, value)
    return dt
import os
BASE_DIR = os.path.dirname(__file__) #获取当前文件夹的绝对路径
print (BASE_DIR)