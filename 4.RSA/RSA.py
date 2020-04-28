# RSA算法
import random
import math
import gmpy2
import libnum
# 生成伪素数
def gen_bin(num): #num为希望产生伪素数的位数
    list = []
    list.append('1')    #最高位为1
    for i in range(num-2):
        c = random.choice(['0','1'])
        list.append(c)
    list.append('1')    #最低位为1
    #print(list)
    res = int("".join(list),2)
    return res

# 计算x的n次方模p,快速计算模幂
def X_n_mod_P(x,n,p):
    res = 1
    n_bin = bin(n)[2:]
    for i in range(0,len(n_bin)):
        res = res**2 % p
        if n_bin[i] == '1':
            res = res * x % p
    return res


# 费马测试,没通过,一定不是素数;通过，可能是素数
# 如果n是一个素数，a是小于n的任意正整数，
# 那么a的n次方与a模n同余
def fermat_test(a,n):
    if n == 1:
        return False
    if n == 2:
        return True
    res = X_n_mod_P(a,n-1,n)  #   以2为底
    return res == 1

# 二次探测,进一步判断n是否为素数
def MillerRabin(n):
    a = random.randint(2,n-2)#随机选择 2-n-2
    if fermat_test(a,n) == 1:#p经过判断，可能为素数
        d = n-1 #初始的d
        sum = 0 #d中因子2的次数
        while (d%2) == 0:
            sum += 1
            d = d>>1
        
        x=X_n_mod_P(a,d,n)
        for i in range(sum):
            new_x = X_n_mod_P(x,2,n)
            if new_x == 1 and x != 1 and x != n-1:
                return False
            x = new_x
        
        if x != 1:
            return False
        else:
            return True


# 增加测试轮数，来提升精确度
def testMillerRabin(n,k):#n为待测试奇数，k为测试次数
    while k > 0:
        if not MillerRabin(n):
            return False
        k = k - 1
    return True

# 产生512位的素数
def gen_512():
    while 1:
        d = gen_bin(512)
        for i in range(50):  # 伪素数附近50个奇数都没有真素数的话，重新再产生一个伪素数
            flag = testMillerRabin(d+2*i,5)# 增加测试轮数，来提升精确度
            if flag:
                b = d + 2*i#这个数通过检验
                break
            else:
                continue
        if flag:
            return b
        else:
            continue

# 求最大公约数
def gcd(a,b):
    a=max(a,b)
    b=min(a,b)
    while (b != 0):
        tmp = a%b
        a = b
        b = tmp
    return a

# 求模逆,这里就是求私钥
# 模逆存在的前提是两者互素
def invert(e,phi):
    a_list = []
    m = phi
    n = e
    tmp = m % n

    while(tmp != 0):
        a = (m - tmp)/n
        a_list.append(a)
        m = n
        n = tmp
        tmp = m % n
    a_list.reverse()
    b_list = []
    b_list.append(1)    #倒数第二个式子,互素得到为1
    b_list.append(a_list[0])
    for i in range(len(a_list)-1):
        b = b_list[-1] * a_list[i+1] + b_list[-2]
        b_list.append(b)
    print(a_list)
    print(b_list)
    if len(a_list) % 2 == 0:#list数目为偶数
        return int(b_list[-1])
    else:                   #list数目为奇数
        return int(phi-b_list[-1])
# 拓展欧几里得算法,
def ext_euclid(a, b):
    old_s,s=1,0
    old_t,t=0,1
    old_r,r=a,b
    if b == 0:
        return 1, 0, a
    else:
        while(r!=0):
            q=old_r//r
            old_r,r=r,old_r-q*r
            old_s,s=s,old_s-q*s
            old_t,t=t,old_t-q*t
    return old_s, old_t, old_r

if __name__ == "__main__":
    print("Loading...")
    while 1:
        p = gen_512()
        q = gen_512()
        n = p*q
        if (len(bin(n)[2:])) == 1024:
            break
    phi = (p-1)*(q-1)
    e=65537
    d=gmpy2.invert(e,phi)
    d2=invert(e,phi)# 错的
    print("d:",d)
    print("e:",e)
    print("n:",n)
    print("---------")
    m=libnum.s2n("i love cumt!")#明文数字
    c=X_n_mod_P(m,e,n)    #密文
    m=X_n_mod_P(c,d,n)    #明文数字
    print("明文:",libnum.n2s(m))


    """print(invert(31,105))
    str="ilovecumt"
    m=libnum.s2n(str)
    print(m)
    c=pow(m,e,n)    #密文
    m=pow(c,d,n)    #明文
    print(libnum.n2s(m))#明文字符串
    print(X_n_mod_P(2,3,3))"""