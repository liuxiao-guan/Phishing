import time

import grequests
import pandas as pd
def exception_handler(request,exception):
    print("出错"+str(request) + ":" + str(exception))

def read_file():
    file_path = "D:\GuanXiaoLiu\Phishing\\brand_crawl\Subdomains\College_top50\\"
    file_name = "北京理工大学.csv"
    df = pd.read_csv(file_path+file_name,engine="python",encoding='utf8',header=None).values.tolist()
    df = [b for a in df for b in a ]
    headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
    time1 = time.time()
    req_list = [grequests.get("http://www." +i,headers = headers) for i in df]
    result = grequests.map(req_list,size=100,exception_handler=exception_handler)
    time2 = time.time()
    print("北京理工大学{}条花费的时间是{}秒".format(len(df),time2-time1))
    for re in result:
        try:
            print(str(re.url) + str(re.status_code))
        except:
            pass
if __name__ == "__main__":
    read_file()