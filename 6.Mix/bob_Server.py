
import socket
from mix_crypto import *
from time import ctime

#私钥
d=117433164657064573975932937869022733817359465155456160439734294086416030414300271570752518188167092678660887423424109232866070659227835436554247060342856865343130697593105035828053549165332367588442049994642522027771394489249052079117956112660969275563291015374957299632588321781883874849438671630393755738393
#公钥
e=65537
n=121316813192673922739335691753056367631713729218511174305062602366705770665710318541156193894889685412465495658332348347142036803761324280103023212750670908854740964877013830283769124423719332312678853475739173446264598113342259176079343958003512081871807169472134435709922149129819535316989101978079482288319
name="bob"

server = socket.socket() #创建对象
server.bind(("localhost",6666))#绑定
server.listen()  #监听
#等待连接
print('Waiting connection...')
#接受请求，返回套接字对象和IP+端口号
con,addr = server.accept()  
con.send(bytes("Welcome connect!\n开始加密传输:\n","utf-8"))
con.recv(1024)

#验证alice身份
print("验证alice身份...")
a = input()
hash_name = con.recv(512).decode()
if hash_name == Md5("alice"):
    print("验证通过！")
    con.send(bytes("您通过了验证!","utf-8"))
else:
    print(hash_name,Md5("alice"))
    exit("验证错误！")
#送出自己身份hash
print("等待alice验证自身身份...")
hash_name = bytes(Md5(name),"utf-8")
con.send(hash_name)
con.recv(1024)
#送出公钥及相应hash
con.send(bytes(str(e),"utf-8"))
con.recv(1024)
hash_e = Md5(str(e))
con.send(bytes(hash_e,"utf-8"))

#传输过程
while True:
    #接收密钥
    buffer = []
    data = con.recv(1024)
    data = data.decode()#str
    int_key = int(data)
    print(int_key)

    print("-" * 20)
    con.send(b'1')

    #接收密文长度
    length = con.recv(1024)
    length = int(length.decode())

    #接收密文
    buffer = []
    size = 0

    while size < length:
        # 每次最多接收1k字节:
        dat = con.recv(1024)
        size += len(dat.decode())
        buffer.append(dat)
    data = b''.join(buffer)
    bin_cipher = data.decode()#接受信息


    print(bin_cipher)

    #解密密钥
    int_key = x_k_mod_n(int_key,d,n)

    #还原明文
    a=input()
    cipher = libnum.b2s(bin_cipher)
    bin_key = bin(int_key)[2:]
    print("解密传输内容:")
    print(libnum.b2s(des_decrypt(bin_key, cipher)))

    con.send(b'1')
    break

server.close()