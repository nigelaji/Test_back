#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
非对称加密: RSA
"""
import rsa

__all__ = [
    'RsaUtil'
]


class RsaUtil:

    def __init__(self, _hex_pubkey_e, _hex_pubkey_n):
        self.hex_pubkey_e = _hex_pubkey_e
        self.hex_pubkey_n = _hex_pubkey_n

    def populate_public_key(self):
        """通过rsa包依据模数和指数生成公钥，实现加密
        :return:
        """
        rsa_hex_pubkey_e = int(self.hex_pubkey_e, 16)
        rsa_hex_pubkey_n = int(self.hex_pubkey_n, 16)
        rsa_pubkey = rsa.PublicKey(rsa_hex_pubkey_n, rsa_hex_pubkey_e)
        return rsa_pubkey

    @staticmethod
    def _pad_for_encryption(message, key_length):
        """
        RSA加密常用的填充方式
        1.RSA_PKCS1_PADDING 填充模式，最常用的模式
        要求: 输入：必须 比 RSA 钥模长(hex_pubkey_n) 短至少11个字节, 也就是　RSA_size(rsa) – 11
        如果输入的明文过长，必须切割，　然后填充
        输出：和hex_pubkey_n一样长
        根据这个要求，对于512bit的密钥，　block length = 512/8 – 11 = 53 字节

        :kwargs message:
        :kwargs key_length:
        :return:
        """
        message = message[::-1]
        # print(message)
        # max_message_length = key_length - 11
        message_length = len(message)

        padding = b''
        padding_length = key_length - message_length - 3
        # print(padding_length, message_length)
        for i in range(padding_length):
            padding += b'\x00'
        # print(padding)
        # print(b''.join([b'\x00\x00', padding, b'\x00', message]))
        return b''.join([b'\x00\x00', padding, b'\x00', message])

    def _encrypt(self, message, pub_key):
        key_length = rsa.common.byte_size(pub_key.n)
        padded = self._pad_for_encryption(message, key_length)

        payload = rsa.transform.bytes2int(padded)
        encrypted = rsa.core.encrypt_int(payload, pub_key.e, pub_key.n)
        block = rsa.transform.int2bytes(encrypted, key_length)

        return block

    def encrypt_by_public_key(self, message):
        """加密公钥
        :kwargs message:
        :return:
        """
        rsa_pubkey = self.populate_public_key()
        crypto = self._encrypt(message.encode(), rsa_pubkey)
        return crypto.hex()

    @staticmethod
    def encryptRSA(empoent, module, message):
        """rsa加密
        :kwargs empoent:
        :kwargs module:
        :kwargs message:
        :return: str
        """
        rsa_obj = RsaUtil(empoent, module)
        rsa_msg = rsa_obj.encrypt_by_public_key(message)
        return rsa_msg

# if __name__ == '__main__':
#     hex_pubkey_n = "ac1152d6bbf4c27cff54877059af22402eadbfa852201d66412af1fce9de704e92df84315b28eaa9e1be8dc69c450bc9f5f1bdce6a954dc4233a79c4a4be53c91d0d938bd9611bfe7f4c15edcffe6896ddc12e71e63663bacdc7d379051f2c18a5ca4c3db94cad53b399e8679de9049fb45b27ba205a1f40da269a56af454f6b"
#     hex_pubkey_e = "10001"
#     print(RsaUtil.encryptRSA(hex_pubkey_e, hex_pubkey_n, "123456"))
