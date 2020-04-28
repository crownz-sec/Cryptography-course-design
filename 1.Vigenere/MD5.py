# 实现MD5算法
import gmpy2
import math
import libnum

# 附加填充位
def preAppend(message):
    i = 0
    length = len(message)#二进制消息长度

    while True:     #附加1，0
        if len(message) % 512 == 448:
            break
        if i == 0:
            message = message + '1'
            i+=1
        message = message + '0'
    # 再附加消息长度
    rest_length = 64
    bin_len = bin(length)[2:]#消息长度化为二进制
    #print(bin_len)
    while len(bin_len) < 64:
        bin_len = '0'+bin_len
    for i in range(8):
        tmp = bin_len[56-i*8:64-i*8]
        #print(tmp)
        message = message + bin_len[56-i*8:64-i*8]
    #print(len(message))
    return  message

# 初始向量
A, B, C, D = (0x01234567,0x89ABCDEF,0xFEDCBA98,0x76543210)
A, B, C, D = ('0x67452301','0xefcdab89','98bacdfe','10325476') 

# 使用正弦函数产生的位随机数，也就是书本上的T[i]
T =  [int(math.floor(abs(math.sin(i + 1)) * (2 ** 32))) for i in range(64)]

# 循环左移的位数
l = [
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 
    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
]

# 循环左移
lrot = lambda x,n:(((x<<n)|(x>>(32-n)))&(0xffffffff))


# 步函数
def fac(bin_mes):
    global A,B,C,D
    #消息分为16个组，I代表一组32位
    w = []
    j = 0
    for i in range(16):
        wi = []
        for i in range(4):
            wi.append(bin_mes[j:j+32][0+8*i:8+8*i])
        for Wi in reversed(wi):
            w.append(int(Wi))
        j += 32

    # 将W中值倒序存放
    print((w))

    AA, BB, CC, DD = A, B, C, D
    #转换为十进制进行运算
    A, B, C, D = int(A,16), int(B,16), int(C,16), int(D,16)
    for i in range(64):
        if i < 16:
            f = (B & C) | ((~B) ^ D)
            flag = i    #标志处理到哪组
        elif i < 32:
            f = (B & D) | (C & (~D))
            flag = (5 * i +1) % 16
        elif i < 48:
            f = B ^ C ^ D
            flag = (3 * i + 5) % 16
        else:
            f = C ^ (B | (~D))
            flag = (7 * i ) % 16
        tmp = hex((f + A + w[flag] + T[i]) & 0xffffffff)#依次加上A,32比特消息分组,一个伪随机常数
        tmp = int(tmp, 16)
        tmp = lrot(tmp, l[i]) + B      #循环左移后,B+A
        A, B, C, D = D, tmp & 0xffffffff, B, C
        print(i,hex(A),hex(B),hex(C),hex(D))
    A = (int(AA,16) + A) & 0xffffffff
    B = (int(BB,16) + B) & 0xffffffff
    C = (int(CC,16) + C) & 0xffffffff
    D = (int(DD,16) + D) & 0xffffffff
    print(hex(A),hex(B),hex(C),hex(D))


if __name__ == "__main__":
    message = input("要MD5加密的信息:")
    bin_mes = libnum.s2b(message)
    #print(reverse_hex(A))
    message = preAppend(bin_mes).encode("utf-8")
    print(message)
    fac(message)
