import os
from pathlib import Path

MAX_LOGIN_FAIL = 5  # 最大登录失败次数

SALT = 'n~1!i@6#d$8^a&y*e'  # 密码加密的盐
SECRET_KEY = '12138'  # token的盐
# MySQL_URI = "mysql://username:password@hostname/database"
# Postgres_URI = "postgresql://username:password@hostname/database"
SQLite_URI = "sqlite:///my_blog.db"

# 邮件服务器配置
EMAIL_HOST = 'smtp.qq.com'  # 如果是 163 改成 smtp.163.com
EMAIL_PORT = 465
EMAIL_HOST_USER = '838863149@qq.com'  # 在这里填入您的QQ邮箱账号
EMAIL_HOST_PASSWORD = 'ubzdpogpyhsgbajh'  # 请在这里填上您自己邮箱的授权码
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_SSL = True

# 日志存储目录
LOG_BASE_DIR = os.path.join(Path(__file__).resolve().parent.parent, 'logs')

if __name__ == '__main__':
    print(LOG_BASE_DIR)
