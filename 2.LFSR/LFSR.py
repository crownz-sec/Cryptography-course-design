# -*- coding: utf-8 -*-
#选择一个15次以上的不可约多项式，
#编写一个线性反馈移位寄存器。验证生成序列的周期。
from multiprocessing import Pool
import time

def lfsr(init,tap):
    global init_
    array_init_bin = list(init)
    tap = list(tap)

    array_new = '0'*len(array_init_bin)
    array_new = list(array_new) #在初始化一个相同长度序列

    sum = 0
    for i in range(len(array_new)):
        if tap[i] == '1':
            sum += int(array_init_bin[i])
    #print(sum)
    for i in range(len(array_new)):
        if i == 0 :
            array_new[i] = str(sum % 2)#反馈函数
        else :
            array_new[i] = array_init_bin[i-1]
    init_ = "".join(array_new)


if __name__ == "__main__":   
    #选择32次不可约多项式，书上131页
    init = '1000000000000000'    #寄存初始序列
    init_ = '1000000000000000'    #初始序列
    tap =  '1000000000010101'     #特征多项式二进制

    #pool = multiprocessing.Pool(processes=4)
    for i in range(10000000000):
        #pool.apply_async(lfsr,(init_,tap))
        if init == init_ and i != 0 :
            print("第{0}次:".format(i),init_)
            print("序列周期为:",i)
            break
        print("第{0}次:".format(i),init_)
        lfsr(init_,tap)

    """p=Pool(4)
    for i in range(10000000000):
        if init == init_ and i != 0 :
            print("序列周期为:",i)
            break
        p.apply_async(lfsr,args=(init_,tap))
        p.close()
        p.join()
    print("所有进程执行完毕")"""
