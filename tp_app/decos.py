from threading import Thread


def async_exec(f):   # 异步执行函数触发器
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
