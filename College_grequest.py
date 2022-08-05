import time

import grequests
import pandas as pd
import tldextract
from bs4 import BeautifulSoup


def exception_handler(request,exception):
    print("出错"+str(request) + ":" + str(exception))

def read_file():
    result = set()
    domain_url = set()
    subdomain = set()
    file_path = "D:\GuanXiaoLiu\Phishing\\brand_crawl\BeianResults\hospital_top30\\"
    file_name = "复旦大学.csv"
    df = pd.read_csv(file_path+file_name,engine="python",encoding='utf8',header=None).values.tolist()
    df = [b for a in df for b in a ]
    for x in df:
        val = tldextract.extract(x)
        domian = val.domain + "." + val.suffix
        subdomain.add(domian)
    headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
    time1 = time.time()
    req_list = [grequests.get("http://www." +i,headers = headers) for i in df]
    result_set = grequests.map(req_list,size=100,exception_handler=exception_handler)
    time2 = time.time()
    print("复旦大学{}条花费的时间是{}秒".format(len(df),time2-time1))
    for res in result_set:
        if res == None:
            continue
        if res.status_code != 200:
            continue
        try:
            result.add(res.url)
            print(res.url)
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
                        if domian not in subdomain :
                            continue
                        if url.find("?") != -1:
                            url1 = url.split("?")
                            if url1[0] not in domain_url:
                                domain_url.add(url1[0])
                            else:
                                continue


                        result.add(url)

                        # result.add(j+b['href'])


                except Exception as e:
                    print(str(e))
        except:
            pass
    print(len(result))
    print('*' * 100)
    result_csv = pd.DataFrame(list(result))
    result_csv.to_csv("D:\GuanXiaoLiu\Phishing\\brand_crawl\Result\Insurance_top50\\" + "复旦大学.csv", index=False,
                      mode='a',
                      header=None)
    print("result:"+  str(result))
    print(subdomain)
if __name__ == "__main__":
    read_file()