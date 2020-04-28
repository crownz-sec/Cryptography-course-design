import sys
import random
import libnum
sys.path.append("/Users/crownz/Code/python/Crypto/3.DES")
sys.path.append("/Users/crownz/Code/python/Crypto/4.RSA")
sys.path.append("/Users/crownz/Code/python/Crypto/5.MD5")
from DES import *
from RSA import *
from MD5 import *
#私钥
d=117433164657064573975932937869022733817359465155456160439734294086416030414300271570752518188167092678660887423424109232866070659227835436554247060342856865343130697593105035828053549165332367588442049994642522027771394489249052079117956112660969275563291015374957299632588321781883874849438671630393755738393
#公钥
e=65537
n=121316813192673922739335691753056367631713729218511174305062602366705770665710318541156193894889685412465495658332348347142036803761324280103023212750670908854740964877013830283769124423719332312678853475739173446264598113342259176079343958003512081871807169472134435709922149129819535316989101978079482288319

# 生成随机对称密钥
def gen_key(): #num为希望产生伪素数的位数
    list = []
    for i in range(64):
        c = random.choice(['0','1'])
        list.append(c)
    #print(list)
    #res = int("".join(list),2)
    res = "".join(list)
    return res
# 读取明文
def read_out_file():
    try:
        f = open('/Users/crownz/Code/python/Crypto/6.Mix/文章.txt','r',encoding = 'utf-8')
        mess = f.read()
        f.close()
        print("读取成功！")
        return mess
    except IOError:
        print('读取错误！')

# 用对称密钥加密明文
def des_encrypt(key,plain):
    return encrypt_all(plain,key)

def des_decrypt(key,cipher):
    return decrypt_all(cipher,key)

# 非对称公钥加密对称密钥
def rsa_encrypt(e,plain_key):
    cipher_key = X_n_mod_P(plain_key, e, n)
    return cipher_key

def x_k_mod_n(x,e,n):
    return X_n_mod_P(x, e, n)

def Md5(e):
    return MD5(e)

if __name__ == "__main__":
    print("开始加密传输:")
    a=input()
    bin_key = gen_key()         #对称密钥
    int_key = int(bin_key,2)    
    print("产生对称密钥:",int_key)#这里是随机产生的对称密钥，即便泄漏被解密，下次也会不一样
                                #这样算是一种一次一密？

    a=input()
    plain = read_out_file()#明文
    #print(des_encrypt(bin_key, plain))#二进制
    bin_cipher = des_encrypt(bin_key, plain)#二进制加密值
    print("加密明文中...")

    a=input()
    cipher_key = X_n_mod_P(int_key, e, n)
    plain_key = X_n_mod_P(cipher_key, d,n)
    print("加密对称密钥:",cipher_key)

    #这里应该是加密 对称密钥加密和传输信息密文
    #检测传输信息是否出错，如果出错，直接
    a=input()
    #print(int_key,plain_key)
    MAC = MD5(str(cipher_key)+str(bin_cipher))
    print("加密'对称密钥加密和传输信息密文'得到的hash值:",MAC)

    a=input()
    flag = (MAC == MD5(str(cipher_key)+str(bin_cipher)))
    print("验证MAC:", flag)
    
    if(flag):
        a=input()
        cipher = bin_to_str(bin_cipher)
        bin_key = bin(int_key)[2:]
        print("解密传输内容:")
        print(libnum.b2s(des_decrypt(bin_key, cipher)))#还原明文
    else:
        print("传输信息出错,拒绝解密!")
        


