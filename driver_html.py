import urllib
import pandas as pd
from selenium import webdriver
#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
#browser = webdriver.Chrome(chrome_options=chrome_options)
#browser.get(url)
from selenium.webdriver.chrome.service import Service
def driver(url,brand_name):

    path = r'D:/GuanXiaoLiu/Phishing/brand_crawl/chromedriver.exe'
    s= Service(executable_path=path)
    browser = webdriver.Chrome(service =s)
    # 设置隐式等待,最多等待10s
    browser.implicitly_wait(20)
    browser.get(url)
    result = []
    domain = urllib.parse.urlparse(url).netloc
    for link in browser.find_elements_by_tag_name('a'):
        print(link.get_attribute('href'))
        all_link = link.get_attribute('href')
        link_domain = urllib.parse.urlparse(all_link).netloc

        if all_link == None:
            continue
        if all_link.find( "javascript:void(0)")!= -1:
            continue
        result.append(all_link)

    result =  pd.DataFrame(result)
    result.to_csv("D:\GuanXiaoLiu\Phishing\\brand_crawl\Result\Top5\\" + brand_name+".csv",mode = "w",index=False,header=None)

if __name__ == '__main__':
    driver("https://www.hfbank.com.cn/","恒丰银行股份有限公司")

