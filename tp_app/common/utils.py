# coding:utf-8
from functools import wraps
import time
from tp_app.common.send_email2 import send_mail


# 验证码生成
def verification_code():
    return


def times_count(func):  # 统计接口被访问次数装饰器
    count = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        f = func(*args, **kwargs)
        nonlocal count
        count += 1
        # print(count)
        # if count % 50 == 0:
        #     send_mail("有内容传输过来了".encode('utf-8'), recipients=['838863149@qq.com'])
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
