# -*- coding:UTF-8 -*-
import re
# 编码字母
s = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

# 明文处理
"""
作用是对明文进行预处理，去除非字母字符和转换大小写
return: 经过预处理的明文字符串
"""
def PreTreat():
    with open("/Users/crownz/Code/python/Crypto/1.Vigenere/plain.txt","r") as f:
        plaintext = f.read()
    pattern = re.compile('[\n]|\d|\W')  #匹配非字母
    f_plain = re.sub(pattern,'',plaintext).lower()
    return f_plain

#密钥字符串转换为数字列表
def key_to_num(key):
    key_list=list(key)
    num_key_list=[]
    for key in key_list:
        num_key=ord(key)-97
        num_key_list.append(num_key)
    return num_key_list

#加密过程
def encrypt(key):
    """
    主要作用是对处理后的明文进行加密
    return: 密文
    """
    plaintext = PreTreat()
    num_key_list = key_to_num(key)
    ciphertext=''
    k=0
    for p in plaintext:
        if k == len(num_key_list):
            k = 0
        num_p = ord(p)-97
        cipher = (num_p+num_key_list[k]) % 26
        cipher = chr(cipher+97-32)
        ciphertext = ciphertext + cipher
        k += 1
    #write_txt(ciphertext,'crypt.txt')
    return ciphertext

#解密前变换
def de_change(cipher,num):
    """
    作用是根据密文字符和密钥还原明文字符,对单个字符处理
    cipher: 密文字符
    num: 密钥编码
    return: 明文字符
    """
    result = ord(cipher)-97 - num
    if result < 0:
        result = 26 + result
    return result

#解密过程
def decrypt(key):
    """
    decryption函数的主要作用是将密文解密成明文
    key: 密钥
    return: 明文
    """
    with open("/Users/crownz/Code/python/Crypto/1.Vigenere/cipher.txt") as f:
        ciphertext = f.read().lower()
        #print(ciphertext)
    num_key = key_to_num(key)
    plaintext=''
    k = 0
    for c in ciphertext:
        if k == len(num_key):
            k = 0
        result = ord(c)-97 - num_key[k]
        if result < 0:
            result = 26 + result
        plain = result
        #print(plain)
        plain = chr(plain+97)
        #print(plain)
        plaintext = plaintext + plain
        k += 1
    #write_txt(plaintext,'result.txt')
    return plaintext

if __name__ == "__main__":
    key='ilovecumt'
    key_to_num(key)
    #print(key_to_num(key))
    #print(encrypt(key))
    with open("/Users/crownz/Code/python/Crypto/1.Vigenere/cipher.txt","w") as f:
        f.write(encrypt(key))
    print()
    print(decrypt(key))
    #with open("/Users/crownz/编程/python/Crypto/plain.txt","w") as f:
        #f.write(decrypt(key))