import threading
import time

import os

import grequests
import tldextract
from requests_html import HTMLSession
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import urllib.request



def exception_handler(request,exception):
    print("出错"+str(request) + ":" + str(exception))

def grequest(subdomain,df,SubdomianName):
    domain_url = set()
    result =set()
    headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
    time1 = time.time()
    req_list = [grequests.get("http://www." + i, headers=headers) for i in df]
    map_result = grequests.map(req_list, size=100, exception_handler=exception_handler)
    time2 = time.time()
    for res in map_result:
        try:
            print(str(res.url) + str(res.status_code))
            soup = BeautifulSoup(res.text, 'lxml')
            for b in soup.find_all('a'):
                try:
                    ## 排除一些无效链接 比如点击没有反应的
                    if str(b['href']).find("javascript:void(0)") == -1 and b['href'] != "#":
                        if str(b['href']).find("http") == -1:
                            # 因为搜到的是相对链接 所以要加
                            url = res.url + b['href']
                        else:
                            url = b['href']
                        print(url)
                        # domian = urllib.parse.urlparse(url).netloc
                        val = tldextract.extract(url)
                        domian = val.domain + "." + val.suffix
                        # 排除非本域名 但是也不是登录或者注册的链接
                        # if domian not in subdomain and b['text'] != "登录" and b['text']!= "注册":
                        if domian not in subdomain:
                            continue
                        if url.find("?") != -1:
                            url1 = url.split("?")
                            if url1[0] not in domain_url:
                                domain_url.add(url1[0])
                            else:
                                continue

                        result.add(url)
                except Exception as e:
                    print(str(e))
        except Exception as e:
            print(str(e))
    print(len(result))
    print('*' * 100)
    result_csv = pd.DataFrame(list(result))
    result_csv.to_csv("D:\GuanXiaoLiu\Phishing\\brand_crawl\Result\Manufacturing_top50\\" + SubdomianName, index=False, mode='a',
                      header=None)

def batch_files(start, end, BeianNameList):

    brand = []
    for i in range(len(BeianNameList)):
        subdomain = set()
        BeianName_url =[]
        # if os.path.getsize("D:\GuanXiaoLiu\Phishing\\brand_crawl\Subdomains\Manufacturing_top50\\"+BeianNameList[i]) >= 2048:
        #     continue
        mtime = os.path.getmtime("D:\GuanXiaoLiu\Phishing\\brand_crawl\Subdomains\Manufacturing_top50\\"+BeianNameList[i])
        # if time.localtime(mtime).tm_mday <13 :
        #     continue
        filename = "D:\GuanXiaoLiu\Phishing\\brand_crawl\Result\Manufacturing_top50\\" + BeianNameList[i]

        if i < start:
            continue
        if i >= end:
            break

        if BeianNameList[i].find("subdomain_count") != -1:
            continue

        filename = 'D:\GuanXiaoLiu\Phishing\\brand_crawl\Subdomains\Manufacturing_top50\\' +BeianNameList[i]
        if not os.path.exists(filename):
            continue
        if os.path.getsize(filename) == 0:
            continue
        print(BeianNameList[i])
        ### 将域名保存到subdomain 以便筛选
        df = pd.read_csv(
            'D:\GuanXiaoLiu\Phishing\\brand_crawl\Subdomains\Manufacturing_top50\\' +BeianNameList[i]  ,
            engine='python', encoding="UTF-8",
            header=None).values.tolist()
        # df= pd.read_csv("D:\GuanXiaoLiu\Phishing\\brand_crawl\Subdomain2\海通期货股份有限公司\海通期货股份有限公司.csv",encoding="gbk",engine="python",header=None).values.tolist()
        df = [b for a in df for b in a]
        for x in df:
            val = tldextract.extract(x)
            domian = val.domain + "." + val.suffix
            subdomain.add(domian)
        for j in df:
            if j[-1] == ".":
                j = j[:-1]
                BeianName_url.append(j)

            #beautiful_soup(j,BeianNameList[i])
        grequest(subdomain,df,BeianNameList[i])





if __name__ == '__main__':
    session = HTMLSession()

    os.chdir('D:\GuanXiaoLiu\Phishing\\brand_crawl\Subdomains\Manufacturing_top50')
    BeianNameList = os.listdir()
    os.chdir('.\\..\\')
    k = 0
    thread_list = []

    #batch_files(0,5,BeianNameList)
    for i in range(5):

        t = threading.Thread(target=batch_files, args=(i+50,i*10+60,BeianNameList,))
        t.setDaemon(True)    #把子线程设置为守护线程，必须在start()之前设置
        thread_list.append(t)
        t.start()
    for j in thread_list:
        j.join()
    #     t.start()
    #     t.join()     #设置主线程等待子线程结束
            #beautiful_soup(j,BeianNameList[i])
      #chrome_driver(j)


# if __name__ == '__main__':
#     t=threading.Thread(target=run,args=('t1',))
#     t.setDaemon(True)    #把子线程设置为守护线程，必须在start()之前设置
#     t.start()
#     t.join()     #设置主线程等待子线程结束
#     print('end')
#
