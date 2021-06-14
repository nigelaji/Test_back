#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
对称加密: AES、DES
"""
from Crypto.Cipher import AES  # win：pip install pycryptodome
from pyDes import des, PAD_PKCS5, ECB

__all__ = [
    'encryptAES', 'decryptAES', 'encryptDES', 'decryptDES', 'AES_SECRET', 'DES_SECRET'
]
AES_SECRET = 's5e2n6s4e1l3in7ks5e2n6s4e1l3in7k'
DES_SECRET = 'bb635dd47e5861f717472df95652077356a8f38dea6347851c191f66b7cf9dc8'


def pkcs7padding(plaintext):
    """PKCS7填充方式: """
    bs = AES.block_size
    length = len(plaintext)
    bytes_length = len(plaintext.encode('utf-8'))
    padding_size = length if (bytes_length == length) else bytes_length
    padding = bs - padding_size % bs
    sign = chr(padding)
    padding_text = sign * padding
    # print(bs, length, bytes_length, padding_size, padding, sign)
    return plaintext + padding_text


def pkcs5padding(plaintext):
    """pkcs5填充方式"""
    pass


def customize_padding(plaintext):
    """自定义填充"""
    # print(text)
    # text = plaintext.encode('utf-8')  #  下面是自定义补位的逻辑
    # length = 32
    # count = len(text)
    # if count < length:
    #     add = (length - count)
    #     text = text + ('\x0f' * add).encode('utf-8')  # \x0f 是补位符
    # elif count > length:
    #     add = (length - (count % length))
    #     text = text + ('\x0f' * add).encode('utf-8')


def encryptAES(plaintext: str, key: str = AES_SECRET) -> str:
    """AES256加密
    :plaintext 明文
    key, mode, iv
    """
    key = key.encode('utf-8')
    mode = AES.MODE_CBC
    iv = bytes(AES.block_size)
    aes_obj = AES.new(key, mode, iv)
    text = pkcs7padding(plaintext)

    ciphertext = aes_obj.encrypt(text.encode('utf-8'))  # 生成密文
    return ciphertext.hex()


def decryptAES(ciphertext: str, key: str = AES_SECRET) -> str:
    """AES256解密
    :ciphertext 密文
    """
    key = key.encode('utf-8')
    text = bytes.fromhex(ciphertext)
    mode = AES.MODE_CBC
    iv = bytes(AES.block_size)
    aes_obj = AES.new(key, mode, iv)
    plain_text = aes_obj.decrypt(text)
    plain_text = str(plain_text, encoding='utf-8')
    sign = plain_text[-1]
    return plain_text.rstrip(sign)  # 不管啥填充，这个解密方法暂时未发现问题


def encryptDES(data: str, key: str = DES_SECRET) -> str:
    """DES加密
    :param data: 要加密的数据
    :param key: 密钥
    :return: 16进制字符串
    """
    des_obj = des("        ", ECB, padmode=PAD_PKCS5)
    des_obj.setKey(key)
    secret_bytes = des_obj.encrypt(data)
    return secret_bytes.hex()


def decryptDES(data: str, key: str = DES_SECRET) -> str:
    """DES解密
    :param data: 要解密的数据
    :param key: 密钥
    :return: 16进制字符串
    """
    secret_bytes = bytes.fromhex(data)
    des_obj = des("        ", ECB, padmode=PAD_PKCS5)
    des_obj.setKey(key)
    return str(des_obj.decrypt(secret_bytes), encoding='utf-8')


if __name__ == '__main__':
    print(encryptAES('12345678901234561234567890123456', AES_SECRET))
    print(decryptAES('6dcaa2916b424f0a6fc469962a662719b135c3f2967620117c28d69a771e4147ecde6ec42032b39cd284c727af141d7c',
                     AES_SECRET))
    print(encryptDES('123456', DES_SECRET))
    print(decryptDES('8f04bb2d77606d74', DES_SECRET))
