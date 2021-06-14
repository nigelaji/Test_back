# coding:utf-8
from functools import wraps
import time
from threading import Thread


def async_exec(func):  # 异步执行函数触发器
    @wraps(func)
    def wrapper(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


def times_count(func):  # 统计接口被访问次数装饰器
    count = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        f = func(*args, **kwargs)
        nonlocal count
        count += 1
        return f

    return wrapper


def execution_time(func):  # 统计函数执行时长
    @wraps(func)
    def wrapper(*args, **kwargs):
        st = time.time()
        f = func(*args, **kwargs)
        et = time.time()
        print(st - et)
        return f

    return wrapper


class Auth:

    def required(self):
        return