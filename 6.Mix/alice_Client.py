
import socket
import time
from mix_crypto import *

name = "alice"

client = socket.socket()
client.connect(('localhost',6666)) # 发起连接请求

#初始化
data = client.recv(1024)
print(str(data,"utf-8"),end="")
client.send(b'1')

#送出自己身份hash
print("等待bob验证自身身份...")
hash_name = bytes(Md5(name),"utf-8")
client.send(hash_name)
print(client.recv(1024).decode())
#接收bob身份hash并验证
print("验证bob身份...",end="")
a=input()
hash_name = client.recv(1024).decode()
client.send(b'1')
if hash_name == Md5("bob"):
    print("验证通过!")
else:
    print(hash_name,Md5("bob"))
    exit("验证错误!")

#获取公钥 
a = input()
e = int(client.recv(1024))
print("获取公钥:", e)
client.send(b'1')
hash_e = client.recv(1024).decode()
if hash_e == Md5(str(e)):
    print("公钥正确!\n开始传输数据:")
else:
    exit("公钥错误!")

while True:
    a=input()
    bin_key = gen_key()         #生成对称密钥
    int_key = int(bin_key,2)    
    print("产生对称密钥:",int_key)
    
    a=input()
    plain = read_out_file()#明文
    bin_cipher = des_encrypt(bin_key, plain)#二进制加密值
    print("加密明文中...")
    
    a=input()
    cipher_key = X_n_mod_P(int_key, e, n)
    plain_key = X_n_mod_P(cipher_key, d,n)
    print("加密对称密钥...")

    #传输密钥
    a=input()
    print("传输密钥中...")
    client.sendall(bytes(str(int_key),"utf-8"))

    client.recv(512)

    #传输密文大小
    length = str(len(bin_cipher))
    length = bytes(length,"utf-8")
    client.send(length)

    #传输密文
    a=input()
    print("传输密文中...")
    client.sendall(bytes(str(bin_cipher),"utf-8"))

    client.recv(512)
    break


client.close()