import tablib
import pandas as pd
import os
def get_pdns_zero_names():
    os.chdir('D:\GuanXiaoLiu\Phishing\\brand_crawl\Subdomain')
    SubdoaminList = os.listdir()
    for i in range(len(SubdoaminList)):
        filename = "D:\GuanXiaoLiu\Phishing\\brand_crawl\Subdomain\\"+ SubdoaminList[i]+"\\"+SubdoaminList[i]+".csv"
        if SubdoaminList[i].find("csv") != -1:
            continue
        pdns_zero_filename = "D:\GuanXiaoLiu\Phishing\\brand_crawl\pdns_zero_filename0.txt"
        if not os.path.exists(filename):
            continue
        if os.path.getsize(filename) == 0:
            with open(pdns_zero_filename, 'a', encoding='utf-8') as f:
                f.write(SubdoaminList[i].replace(".csv","")+"\n")
                f.close()

def get_result_zero_names():
    os.chdir('D:\GuanXiaoLiu\Phishing\\brand_crawl\Result4')
    SubdoaminList = os.listdir()
    for i in range(len(SubdoaminList)):
        filename = "D:\GuanXiaoLiu\Phishing\\brand_crawl\Result4\\"  + SubdoaminList[i]
        pdns_zero_filename = "D:\GuanXiaoLiu\Phishing\\brand_crawl\\result_zero_filename.txt"
        if not os.path.exists(filename):
            continue
        if os.path.getsize(filename) == 0:
            with open(pdns_zero_filename, 'a', encoding='utf-8') as f:
                print(SubdoaminList[i])
                f.write(SubdoaminList[i].replace(".csv", "") + "\n")
                f.close()
def get_logo_zero():
    base_path = "D:\GuanXiaoLiu\Phishing\\brand_logo\\"
    os.chdir(base_path)
    name_list = os.listdir()
    for name in name_list:
        file_path = base_path + name
        files = os.listdir(file_path)
        if len(files) <= 1:
            print(name)

if __name__ == '__main__':
   #get_result_zero_names()
   get_logo_zero()