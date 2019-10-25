# coding;utf-8
import hashlib
from tp_app.config.config import SALT


# md5加盐加密
def _hashed_with_salt(info, salt):
    m = hashlib.md5()
    m.update(info.encode('utf-8'))
    m.update(salt)
    return m.hexdigest()


# 对密码进行加密
def encrypt_password(pwd):
    return _hashed_with_salt(pwd, SALT)


# 对密码进行解密
def decrypt_password(pwd):
    return
