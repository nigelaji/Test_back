# coding;utf-8
import hashlib
from tp_app.config.config import SALT


# md5加盐加密密码，md5不可反解密，只能通过字典库去一个个查md5库，那登录时如何验证密码？看主函数内示例
def encrypt_with_salt(pwd, salt=SALT):
    m = hashlib.md5()
    m.update(salt.encode('utf-8'))
    m.update(pwd.encode('utf-8'))
    return m.hexdigest()


def check_password(pwd, pwd_hashed):        # 检查密码
    return encrypt_with_salt(pwd) == pwd_hashed


if __name__ == '__main__':
    # 假设有个密码是123456，过来登录，登录的时候获取到password
    pwd = '123456'
    # 数据库中存储的串是 3fbbef13e64846295fd4b22fee9b8735
    database_pwd = '3fbbef13e64846295fd4b22fee9b8735'
    # 开始判断
    if encrypt_with_salt(pwd, SALT) == database_pwd:
        print("通过用户输入的密码进行加密再和数据库比较，然后验证成功")

