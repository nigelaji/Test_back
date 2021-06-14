#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
信息摘要: md5、sha256
"""
import hashlib
import hmac

__all__ = [
    'StdHash', 'HmacHash'
]


class StdHash:
    """
    标准哈希
    """

    @staticmethod
    def md5(message: str, salt: str = "") -> str:
        m = hashlib.md5()
        m.update(message.encode('utf-8'))
        m.update(salt.encode('utf-8'))
        return m.hexdigest()

    @staticmethod
    def sha256(message: str, salt: str = "") -> str:
        m = hashlib.sha256()
        m.update(message.encode('utf-8'))
        m.update(salt.encode('utf-8'))
        return m.hexdigest()


class HmacHash:
    """
    基于秘钥的哈希运算
    """

    @staticmethod
    def md5(key: str, message: bytes = None) -> str:
        key = bytes(key, encoding='utf-8')
        h = hmac.new(key, message, hashlib.md5)
        return h.hexdigest()

    @staticmethod
    def sha256(key: str, message: bytes = None) -> str:
        key = bytes(key, encoding='utf-8')
        h = hmac.new(key, message, hashlib.sha256)
        return h.hexdigest()


if __name__ == '__main__':
    print(HmacHash.sha256('123456'))
