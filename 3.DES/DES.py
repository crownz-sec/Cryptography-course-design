# 实现DES加解密
import re
from DES_BOX import * 

# 字符转为二进制流
def str_to_bin(str) :
    res = ""
    for i in str :   #对每个字符进行二进制转化
        tmp = bin(ord(i))[2:]   #字符转成ascii，再转成二进制，并去掉前面的0b
        for j in range(0,8-len(tmp)) : #补齐8位
            tmp = '0' + tmp
        res += tmp
    return res

# 二进制流转为字符
def bin_to_str(bin_str) :
    res = ""
    tmp = re.findall(r'.{8}',bin_str)
    for i in tmp :
        res += chr(int(i,2))
    return res

# 初始IP置换
def IP(init_str) :  
    res = ""
    for i in IP_Sub:
        res += init_str[i-1]
    return res

# IP逆置换
def IP_re(final_str) :
    res = ""
    for i in IP_re_Sub:
        res += final_str[i-1]
    return res

# 轮函数，包含4步
# ①E盒扩展 将32位明文拓展为48位
def Expan(bin_str) :
    res = ""
    for i in E :
        res += bin_str[i-1]
    return res

# ②密钥加,即异或
def Xor(str,key) :
    res = ""
    for i in range(0,len(str)) :
        xor_res = int(str[i],10) ^ int(key[i],10)
        if xor_res == 1 :
            res += '1'
        elif xor_res == 0 :
            res += '0'
    return res

# ③S盒代换
def Sub(xor_str) :
    res = ""
    count = 0     #用来计数S盒，共8个
    for i in range(0,len(xor_str),6) :  #每6个分一组，循环8次
        now_str = xor_str[i:i+6]    #将第i个分组，切片处理
        row = int(now_str[0] + now_str[5],2)    #int是把后面参数进制转化为十进制，这是是把二进制数转为十进制
        col = int(now_str[1:5],2)

        # S盒的第count个表,row*16是因为用一维列表存入矩阵值
        num = bin(S[count][row*16 + col])[2:]   #利用bin输出有可能不是4位str类型的值，下面的循环加上字符0
        for i in range(0,4-len(num)) :
            num = '0' + num
        res += num
        count += 1
    return res

# ④P盒置换
def PSub(sub_str) :
    res = ""
    for i in P :
        res += sub_str[i-1]
    return res

# fin f函数实现
def fac(bin_str,key) :
    first = Expan(bin_str)  #位选择函数将32位待加密str拓展位48位
    second = Xor(first,key) #将48位结果与子密钥Ki按位模2加 
    third = Sub(second)     #每组6位缩减位4位   S盒置换
    last = PSub(third)      #P盒换位处理  得到f函数的最终值
    return last

# 查看密钥是否为64位
def input_key_judge(bin_key):
    ans = len(bin_key)
    if len(bin_key) < 64:
        if ans % 64 != 0:
            for i in range(64 - (ans % 64)):  # 不够64位补充0
                bin_key += '0'
    # else:
    #     bin_key = bin_key[0:64]    #秘钥超过64位的情况默认就是应该跟密文一样长 直接将密钥变为跟明文一样的长度，安全性会有所下降
    return bin_key

# 密钥PC_1置换
def PC1(key) :
    res = ""
    for i in PC_1 :
        res += key[i-1]
    return res

# 密钥PC_2置换
def PC2(key) :
    res = ""
    for i in PC_2 :
        res += key[i-1]
    return res

# 密钥循环左移操作
def left_shift(bin_str,num) :
    left_res = bin_str[num:len(bin_str)]    #列表切片，第一位取，最后一位不取
    left_res = left_res + bin_str[0:num]    #例，l[2:7],2取，7不取，2和7在这里是列表元素序号
    return left_res

# 密钥生成
def gen_key(key) :
    key_list = []
    key_change1 = PC1(key)
    key_C0 = key_change1[0:28]
    key_D0 = key_change1[28:]
    for i in Shift :
        key_c = left_shift(key_C0,i)
        key_d = left_shift(key_D0,i)
        key_output = PC2(key_c + key_d)
        key_list.append(key_output)
    return key_list

# 一次完整加密过程
def encrypt_one(bin_plain,bin_key): #64位二进制加密
    mes_ip_bin = IP(bin_plain)    #初始IP置换
    key_list = gen_key(bin_key)
    mes_left = mes_ip_bin[0:32]
    mes_right = mes_ip_bin[32:]
    for i in range(0,15):
        mes_tmp = mes_right     #暂存右边32位
        f_res = fac(mes_tmp,key_list[i])    #轮函数处理
        mes_right = Xor(mes_left,f_res)     #右边f后，与左边密钥加
        mes_left = mes_tmp  #初始右边32位放左边

    f_res = fac(mes_right,key_list[15])
    mes_fin_left = Xor(mes_left,f_res)
    mes_fin_right = mes_right
    bin_cipher = IP_re(mes_fin_left+mes_fin_right)
    return bin_cipher       #返回二进制 

# 一次完整解密过程
def decrypt_one(bin_cipher,bin_key):
    cipher_ip_bin = IP(bin_cipher)
    key_list = gen_key(bin_key)
    lst = range(1,16)   #循环15次
    cipher_left = cipher_ip_bin[0:32]
    cipher_right = cipher_ip_bin[32:]

    for i in lst[::-1]:   #表示逆转列表调用
        mes_tmp = cipher_right
        f_result = fac(cipher_right,key_list[i])
        cipher_right = Xor(cipher_left,f_result)
        cipher_left = mes_tmp
    
    f_result = fac(cipher_right,key_list[0])
    mes_fin_left = Xor(cipher_left,f_result)
    mes_fin_right = cipher_right
    bin_plain = IP_re(mes_fin_left + mes_fin_right)
    return bin_plain    #返回二进制 

# 二进制明文位数调整为64的倍数
def deal_mess(bin_mess):
    ans = len(bin_mess)
    if ans % 64 != 0:
        for i in range( 64 - (ans%64)):           #不够64位补充0
            bin_mess += '0'
    return bin_mess

# 对整个明文字符串加密
def encrypt_all(message,key):
    res = ""
    bin_plain = deal_mess(str_to_bin(message)) #得到明文的二进制比特流  64的倍数
    bin_key = input_key_judge(str_to_bin(key))   #得到密钥的二进制比特流 64的倍数
    tmp = re.findall(r'.{64}',bin_plain)    #单词加密只能实现8个字符，匹配为每64一组的列表
    for i in tmp:
        res += encrypt_one(i,bin_key)  #将每个字符加密后的结果再连接起来
    return res

# 对整个密文字符串解密
def decrypt_all(message,key):
    res = ""
    bin_cipher = deal_mess(str_to_bin(message))
    bin_key = input_key_judge(str_to_bin(key))
    tmp = re.findall(r'.{64}',bin_cipher)
    for i in tmp :
        res += decrypt_one(i,bin_key)
    return res

# 因为输入输出会有字符转换，会有乱码，也不知道该复制哪些加密后去解密，所以用文件来操作
# 写入加密结果
def write_in_file(str_mess):
    try:
        f = open('/Users/crownz/Code/python/Crypto/3.DES/DES.txt','w',encoding='utf-8')
        f.write(str_mess)
        f.close()
        print("文件输出成功！")
    except IOError:
        print('文件加解密出错！')

# 读取加密结果
def read_out_file():
    try:
        f = open('/Users/crownz/Code/python/Crypto/3.DES/DES.txt','r',encoding = 'utf-8')
        mess = f.read()
        f.close()
        print("文件读取成功！")
        return mess
    except IOError:
        print('文件加解密出错！')

def main():
    print("1.加密")
    print("2.解密")
    print("3.退出")
    mode = input()
    if mode == '1':
        plain = input("请输入要加密的字符串:")
        key = input("请输入密钥：")
        print("-----加密前-----")
        print("二进制:",str_to_bin(plain))
        print("字符串:",plain)

        bin_cipher = encrypt_all(plain,key) #加密结果二进制
        cipher = bin_to_str(bin_cipher)     #加密结果字符串
        print("-----加密后-----")
        print("二进制:",bin_cipher)
        print("字符串:",cipher)

        write_in_file(cipher)       #写入加密后的字符串
    elif mode == '2':
        key = input("请输入你的秘钥：")
        message = read_out_file()       #读取加密后的字符串
        bin_plain = decrypt_all(message, key)   #字符串解密二进制
        plain = bin_to_str(bin_plain)
        print("-----解密后-----")
        print("二进制:",bin_plain)
        print("字符串:",plain)
    elif mode == '3':
        exit()
    else:
        print("请重新输入!")

if __name__ == "__main__" :
    print("欢迎使用DES算法,输入序号选择加密、解密或退出:")
    while True:
        main()
