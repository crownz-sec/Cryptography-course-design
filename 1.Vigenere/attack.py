# -*- coding: utf-8 -*-
import re
from Vigenere import *

#标准的频率表
freq = [0.082,0.015,0.028,0.043,0.127,0.022,0.02,
        0.061,0.07,0.002,0.008,0.04,0.024,0.06,
        0.075,0.019,0.001,0.06,0.063,0.091,0.028,
        0.01,0.023,0.001,0.02,0.001]

#列表去重函数
def simplifiy_list(alist):
    set_list=set(alist)     # 创建集合，无序不重复
    alist=[]
    for i in set_list:
        alist.append(i)
    return alist 

#定义列表元素求和函数
def add_the_list(alist):
    sum=0
    for i in range(len(alist)):
        sum=alist[i]+sum
    return sum

def sub_stdfre(fre):
    return abs(fre-0.06549669949999998)
def zip_flist(fre,n):
    return (n,fre)
def all_lower(c):
    return c.lower()

def get_keylen():   #猜解密钥长度
    flist=[]
    ave_flist=[]
    len_list=[]
    result=[]
    res=[]
    initial_text=open("/Users/crownz/Code/python/Crypto/1.Vigenere/cipher.txt","r")#读入文本
    simplified_text=initial_text.read()#防止len出错
    letter_cnt=len(simplified_text)#英文字母总个数
    simp_text=map(all_lower,simplified_text)#都换成小写字母
    text_list=list(simp_text)#将简化的文本列表化
    for key_len in range(2,50):   #在密钥可能的长度范围里面找
        len_list.append(key_len)    
        for i in range(key_len):
            templist=text_list[i::key_len]  #按密钥长度分组
            #print(templist)
            sqcnt_list=[]
            temp_len=len(templist)#分组字母个数
            once_list=simplifiy_list(templist)#对当前分组去重复
            for letter in range(len(once_list)):
                #对于非重复列表中的每一个字母，查找它在templist出现了多少次
                cnt=templist.count(once_list[letter])#字母在templist出现的次数
                sqcnt=cnt*(cnt-1)#我们假设文本数量足够大，不会出现cnt==1的情况
                sqcnt_list.append(sqcnt)#存放的都是sqcnt
            flist.append(add_the_list(sqcnt_list)/(temp_len*(temp_len-1)))
        ave_fre=add_the_list(flist)/len(flist)
        ave_flist.append(ave_fre)
    res=list(zip(len_list,(list(map(sub_stdfre,ave_flist)))))
    result=sorted(res, key=lambda x:x[1])
    print("最有可能的前十个密钥长度及其对应频率和0.065差值为：")
    for i in range(10):
        print(result[i])

# 根据密钥长度将密文分组 
def makelist(text,length): 
    textarray = []
    row = []
    index = 0
    for ch in text:
        row.append(ch)
        index += 1
        if index % length ==0:
            textarray.append(row)
            row = []
    return textarray

# 统计字母频度
def f_list(lis): 
    li = []
    alphabet = [chr(i) for i in range(65,91)]  #生成字母表,这里改成大写字母表
    for c in alphabet:
        count = 0
        for ch in lis:
            if ch == c:
                count+=1
            #print(count)
        li.append(count/len(lis))
    #print(li)
    return li

def Crack_key(text,length): 
    key = [] 
    array =makelist(text,length)
    #print(array)   这里没错    错误在于没有转换小写
    for i in range(length):
        flist = f_list([row[i] for row in array])
        #print(flist) 这里flist全部为0
        multi = [] 
        for j in range(26):
            Sum = 0.0
            for k in range(26):
                Sum += freq[k]*flist[k]
                #print(freq[k],flist[k])  这里flist全部为0
            multi.append(Sum)
            flist = flist[1:]+flist[:1]
        n = 100
        ch = ''
        #print(multi)
        for j in range(len(multi)):
             if abs(multi[j] - 0.065)<n: 
                 n = abs(multi[j] -0.065)
                 ch = chr(j+97)
        key.append(ch)
    return key

if __name__ == "__main__":    
    get_keylen()
    ciphertext=open("/Users/crownz/Code/python/Crypto/1.Vigenere/cipher.txt","r")
    ciphertext=ciphertext.read()
    length=int(input("请输入最有可能的密钥长度："))
    key=Crack_key(ciphertext,length)
    print("猜测的密钥为：",key)
    str_key="".join(key)
    print(decrypt(key))
