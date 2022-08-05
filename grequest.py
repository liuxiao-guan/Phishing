import grequests
from bs4 import BeautifulSoup
headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
urls = [
    # 'http://www.baidu.com',
    'http://www.qq.com',
    'http://www.163.com',
    'http://www.zhihu.com',
    'http://www.toutiao.com',
    'http://www.douban.com'
]
rs = (grequests.get(u,headers=headers) for u in urls)
print(rs)
#print(grequests.map(rs))  # [<Response [200]>, None, <Response [200]>, None, None, <Response [418]>]
for idx in grequests.map(rs,size = 5,):
    idx.encoding = "utf8"
    soup = BeautifulSoup(idx.text, 'lxml')
    print("url:"+ str(idx.url))
    print(soup)
    for b in soup.find_all("a"):
        try:
            print(b['href'])
        except Exception as e:
            print(str(e))

# # 异常处理
# def exception_handler(request, exception):
#     print("请求出错")
#
#
# reqs = [
#     grequests.get('http://httpbin.org/delay/1', timeout=0.001),
#     grequests.get('http://fakedomain/'),
#     grequests.get('http://httpbin.org/status/500')
# ]
#print(grequests.map(reqs, exception_handler=exception_handler))