import requests
from bs4 import BeautifulSoup
import pandas as pd
url = "http://www.lilvb.com/gupiao/quanshang.htm"

res = requests.get(url, timeout=20)
res.encoding = "gbk"
soup = BeautifulSoup(res.text, 'lxml')
file_path = "D:\GuanXiaoLiu\Phishing\\brand_crawl\Client_Name\\"
file_name = "Securities_top50" + ".csv"
k = 0
result =set()


for b in soup.find_all('tr'):
    ## 因为有可能不存在这个标签

    try:
        for a in b.find_all('a'):
            print(a.next_element)
            #result.add(a.next_element)
    except:
        pass

result = pd.DataFrame(result)
result.to_csv(file_path + file_name,encoding="utf8",header=None,mode='w',index=False)