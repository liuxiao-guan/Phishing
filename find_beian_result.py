import threading
import urllib.request

import requests
from bs4 import BeautifulSoup
import pandas as pd
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


                    result.add(url)
                    #result.add(j+b['href'])

            except:
                pass

    print("result:")
    print(len(result))
    print('*' * 100)
    result_csv = pd.DataFrame(list(result))
    result_csv.to_csv("D:\GuanXiaoLiu\Phishing\\brand_crawl\Result_nologo\\"+SubdomianName+".csv",index = False,mode='a',header=None)
def batch_files(start,end,brand_list):
    for i in range(len(brand_list)):
        if i < start:
            continue
        if i >= end:
            break
        beian_path = "D:\GuanXiaoLiu\Phishing\\brand_crawl\BeianResult_all" + "\\" + brand_list[i]+".csv"
        df = pd.read_csv(beian_path, engine="python", encoding="utf-8", header=None).values.tolist()
        df = [b for a in df for b in a]
        for x in df:
            subdomain.add(x)
        for link in df:
           beautiful_soup(link,brand_list[i])
if __name__ == "__main__":
    brand_names = open("D:\GuanXiaoLiu\Phishing\\brand_crawl\\find_no_logo.txt", 'r')
    brand_list = []
    thread_list = []
    for brand_name in brand_names:
        brand_list.append(brand_name.strip())
    beian_base_path = "D:\GuanXiaoLiu\Phishing\\brand_crawl\BeianResult_all"
    for i in range(6):
        t = threading.Thread(target=batch_files, args=(i*6, i*6+6  , brand_list,))
        t.setDaemon(True)  # 把子线程设置为守护线程，必须在start()之前设置
        thread_list.append(t)
        t.start()
    for j in thread_list:
        j.join()


           # beautiful_soup(link,brand_list[i])