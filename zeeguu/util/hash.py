# -*- coding: utf8 -*-
from hashlib import sha1


def text_hash(text):
    """
    :param text: str or binary. if str, it is converted to binary.
    :return: str
    """
    if isinstance(text, str):
        text = text.encode("utf8")
    return sha1(text).digest()


def password_hash(password, salt):
    """
    
    :param password: str
    :param salt: binary, utf-8 encoded
    :return: str
    """
    password = password.encode("utf8")
    for i in range(1000):
        password = text_hash(password + salt)
    return password
