import logging
import logging.handlers
import os
import sys
import textwrap
from tp_app.config import LOG_BASE_DIR

"""
filename：   用指定的文件名创建FiledHandler（后边会具体讲解handler的概念），这样日志会被存储在指定的文件中。
filemode：   文件打开方式，在指定了filename时使用这个参数，默认值为“a”还可指定为“w”。
format：      指定handler使用的日志显示格式。
datefmt：    指定日期时间格式。
level：        设置rootlogger（后边会讲解具体概念）的日志级别
stream：     用指定的stream创建StreamHandler。可以指定输出到sys.stderr,sys.stdout或者文件，默认为sys.stderr。
                  若同时列出了filename和stream两个参数，则stream参数会被忽略。
https://docs.python.org/zh-cn/3/library/logging.html#logrecord-attributes
"""
log_colors = {
    logging.DEBUG: "\033[1;34m",  # blue
    logging.INFO: "\033[1;32m",  # green
    logging.WARNING: "\033[1;35m",  # magenta
    logging.ERROR: "\033[1;31m",  # red
    logging.CRITICAL: "\033[1;41m",  # red reverted
}

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname_c)-8s %(message)s',  # 下面定制了levelname_c
    datefmt='%m-%d %H:%M:%S',
    stream=sys.stdout
)

orig_record_factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
    record = orig_record_factory(*args, **kwargs)
    record.levelname_c = "{}{}{}".format(log_colors[record.levelno], record.levelname, "\033[0m")  # 定制LogRecord属性
    record.message_shorten = "{}".format(textwrap.shorten(record.msg, width=1000, placeholder='...'))
    return record


logging.setLogRecordFactory(record_factory)

if not os.path.exists(LOG_BASE_DIR):
    os.mkdir(LOG_BASE_DIR)

limit_file_handler = logging.handlers.RotatingFileHandler(
    filename=os.path.join(LOG_BASE_DIR, 'tp_app.log'),
    mode='a+',
    maxBytes=1024 * 1024 * 3,
    backupCount=9,
    encoding='utf-8',
)
my_fmt = logging.Formatter(
    fmt='%(asctime)s %(pathname)s[line:%(lineno)d] %(name)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger()

limit_file_handler.setLevel(logging.WARNING)
limit_file_handler.setFormatter(my_fmt)

logger.addHandler(limit_file_handler)  # 禁止在其他脚本非__main__区域

if __name__ == '__main__':
    logger.debug("这是一条调试")
    logger.info("这是一条信息")
    logger.warning("这是一条警告")
    logger.error("这是一条错误")
    logger.critical("这是一条批判")
