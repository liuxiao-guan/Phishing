import threading
import time

import os

from requests_html import HTMLSession
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import urllib.request
result = set()
subdomain = set()

def beautiful_soup(j,SubdomianName):
    # request_html(j)
    global soup

    result = set()
    url = 'http://www.baidu.com'
    key = True
    domain_url = set()

    res = set()
    #去除排除重复项 浪费时间没效果
    # filename = "D:\GuanXiaoLiu\Phishing\\brand_crawl\Result3\\" +SubdomianName
    # if os.path.exists(filename):
    #     if os.path.getsize(filename) > 0:
    #         df1 = pd.read_csv(filename, encoding="gbk", engine="python", header=None).values.tolist()
    #         df1 = [b for a in df1 for b in a]
    #         for i in df1:
    #             print(i)
    #             res.add(i)
    try:

        res = requests.get("http://www." + j,timeout=20)
        print(j)
        j = "http://www." + j
        soup = BeautifulSoup(res.text, 'lxml')
        if j not in res:
            result.add(j)
    except:
        try:
            res = requests.get("http://" + j,timeout=20)
            j = "http://" + j
            soup = BeautifulSoup(res.text, 'lxml')
            if j not in res:
                result.add(j)
        except:
            try:
                res = requests.get("https://www." + j, timeout=20)
                print(j)
                j = "https://www." + j
                soup = BeautifulSoup(res.text, 'lxml')
                if j not in res:
                    result.add(j)
                print(j + "能访问")
            except:
                try:
                    res = requests.get("https://" + j, timeout=20)
                    j = "https://" + j
                    soup = BeautifulSoup(res.text, 'lxml')
                    if j not in res:
                        result.add(j)
                    print(j + "能访问")
                except:
                    # print(j + "不能访问")
                    key = False
    if key == True:
        for b in soup.find_all('a'):
            try:
                ## 排除一些无效链接 比如点击没有反应的
                if str(b['href']).find("javascript:void(0)") ==-1  and b['href'] != "#":
                    if str(b['href']).find("http") == -1:
                        #因为搜到的是相对链接 所以要加
                        url = j + b['href']
                    else:
                        url = b['href']
                    print(url)
                    if(url.find("ecs") != -1):
                        print("kk")
                    domian = urllib.parse.urlparse(url).netloc
                    #排除非本域名 但是也不是登录或者注册的链接
                    #if domian not in subdomain and b['text'] != "登录" and b['text']!= "注册":
                    if domian not in subdomain and b.next_element != "登录" and b.next_element  != "注册":
                        continue
                    if url.find("?") != -1:
                        url1 = url.split("?")
                        if url1[0] not in domain_url:
                            domain_url.add(url1[0])
                        else:
                            continue

                    if url not in res:
                        result.add(url)
                    #result.add(j+b['href'])

            except:
                pass

    print("result:")
    print(len(result))
    print('*' * 100)
    result_csv = pd.DataFrame(list(result))
    result_csv.to_csv("D:\GuanXiaoLiu\Phishing\\brand_crawl\Result_oneforall1\\"+SubdomianName,index = False,mode='a',header=None)
def batch_files(start,end,BeianNameList):
    need_list = []
    f = open("D:\GuanXiaoLiu\Phishing\\brand_crawl\\result_zero_filename1.txt",'r',encoding="gbk")
    for i in f:
        need_list.append(i.strip())
    for i in range(len(BeianNameList)):
        subdomain.clear()


        if i < start:
            continue
        if i >= end:
            break

        if str(BeianNameList[i]).replace(".csv","") not in need_list:
            continue
        if BeianNameList[i].find("subdomain_count") != -1:
            continue
        print(BeianNameList[i])
        filename = 'D:\GuanXiaoLiu\Phishing\\brand_crawl\Subdomain_oneforall1\\' +BeianNameList[i]
        if not os.path.exists(filename):
            continue
        if os.path.getsize(filename) == 0:
            continue

        df = pd.read_csv(
            'D:\GuanXiaoLiu\Phishing\\brand_crawl\Subdomain_oneforall1\\' +BeianNameList[i],
            engine='python', encoding="UTF-8",
            header=0).values.tolist()
        # df= pd.read_csv("D:\GuanXiaoLiu\Phishing\\brand_crawl\Subdomain2\海通期货股份有限公司\海通期货股份有限公司.csv",encoding="gbk",engine="python",header=None).values.tolist()

        for x in df:
            subdomain.add(x[4])
        for j in df:
            # t = threading.Thread(target=beautiful_soup(), args=(j, BeianNameList[i],))
            # t.setDaemon(True)  # 把子线程设置为守护线程，必须在start()之前设置
            # thread_list.append(t)
            # t.start()
            if j[11] == 200:
                beautiful_soup(j[4],BeianNameList[i])

if __name__ == '__main__':
    session = HTMLSession()

    os.chdir('D:\GuanXiaoLiu\Phishing\\brand_crawl\Subdomain_oneforall1')
    BeianNameList = os.listdir()
    os.chdir('.\\..\\')
    k = 0
    thread_list = []
    #batch_files(0,35,BeianNameList)
    for i in range(5):
        t = threading.Thread(target=batch_files, args=(i*3,i*3+3,BeianNameList,))
        t.setDaemon(True)    #把子线程设置为守护线程，必须在start()之前设置
        thread_list.append(t)
        t.start()
    for j in thread_list:
        j.join()





# if __name__ == '__main__':
#     t=threading.Thread(target=run,args=('t1',))
#     t.setDaemon(True)    #把子线程设置为守护线程，必须在start()之前设置
#     t.start()
#     t.join()     #设置主线程等待子线程结束
#     print('end')
#
