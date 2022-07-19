import os
import pandas as pd
import os
import shutil
from tablib import Dataset,Databook
def findBeianremain2():
    os.chdir("D:\GuanXiaoLiu\Phishing\\brand_crawl\Subdomain")
    BeianNameList = os.listdir()
    print(type(BeianNameList))
    filepath1 = "D:\GuanXiaoLiu\Phishing\\brand_crawl\Result"
    os.chdir(filepath1)
    result1 = os.listdir()
    filepath2 = "D:\GuanXiaoLiu\Phishing\\brand_crawl\Result0_91"
    os.chdir(filepath2)
    result2 = os.listdir()
    filepath2 = "D:\GuanXiaoLiu\Phishing\\brand_crawl\Subdomain"
    os.chdir(filepath2)
    result_remain = os.listdir()
    k = 0
    result = set()
    for i in result1:
       result.add(i)
    for i in result2:
        result.add(i)
    print("已经收集的数据："+str(len(result)))
    print("*"*100)
    remain = list()
    for BeianName in BeianNameList:
        if BeianName+".csv" not in result:
           remain.append(BeianName)
    print(len(remain))
    print(remain)
    with open("D:\GuanXiaoLiu\Phishing\\brand_crawl\\result_zero_filename2.txt","w",encoding='gbk') as fw:
        for i in remain:
            fw.write(i+"\n")
    fw.close()


    # src = filepath2
    # dest = "D:\GuanXiaoLiu\Phishing\\brand_crawl\Result4"
    # src_files = os.listdir(src)
    # for file_name in src_files:
    #     full_file_name = os.path.join(src, file_name)
    #     if os.path.isfile(full_file_name) and file_name in remain:
    #         shutil.copy(full_file_name, dest)
    #         os.remove(full_file_name)
    #     if file_name in result:
    #         os.remove(full_file_name)
    # print(k)

def findpdnszero():
    result_filepath = "D:\GuanXiaoLiu\Phishing\\brand_crawl\Result"
    os.chdir(result_filepath)
    result_list = os.listdir()
    beian_filepath = "D:\GuanXiaoLiu\Phishing\\brand_crawl\Subdomain"
    os.chdir(beian_filepath)
    beian_list = os.listdir()
    k = 0
    all_result = set()
    with open("D:\GuanXiaoLiu\Phishing\\brand_crawl\\result_zero_filename.txt",'w',encoding='gbk') as fw:
        for result in result_list:
            if os.path.getsize(result_filepath+"\\"+result) == 0:
                fw.write(result.replace(".csv","")+"\n")
                all_result.add(result.replace(".csv",""))
                k =  k+1
    fw.close()
    print(k)
    with open("D:\GuanXiaoLiu\Phishing\\brand_crawl\\result_zero_filename.txt",'a',encoding='gbk') as fw:
        for beian in beian_list:
            if beian.find("subdomain_count") != -1:
                continue
            beian_file = beian_filepath + "\\" + beian + "\\" + beian + ".csv"
            if not os.path.exists(beian_file):
                    if beian not in result:
                        fw.write(beian + "\n")
                        all_result.add(beian)
                        k = k+1
                    continue
            if os.path.getsize(beian_file) == 0 and beian not in result:
                fw.write(beian+"\n")
                all_result.add(beian+"\n")
                k = k +1
    fw.close()

    print(k)
def findnotoneforall():
    k = 0
    f = open("D:\GuanXiaoLiu\Phishing\\brand_crawl\\result_zero_filename.txt","r")
    subdomain_oneforall_file_path = "D:\GuanXiaoLiu\Phishing\\brand_crawl\Subdomain_oneforall"
    os.chdir(subdomain_oneforall_file_path)
    subdomain_list = os.listdir()
    result =set()
    for line in f:
        if line.replace("\n", "") + ".csv" not in subdomain_list:
            result.add(line)
            k = k + 1
    print(result)
    print(k)
    f.close()
    f=open("D:\GuanXiaoLiu\Phishing\\brand_crawl\\result_zero_filename1.txt","w")
    f.writelines(result)
def findthesecond():
    os.chdir("D:\GuanXiaoLiu\Phishing\\brand_crawl\Subdomain1")
    BeianNameList = os.listdir()
    print(len(BeianNameList))
    print(type(BeianNameList))
    filepath1 = "D:\GuanXiaoLiu\Phishing\\brand_crawl\Temp_Result_109"
    os.chdir(filepath1)
    result1 = os.listdir()
    for i in BeianNameList:
        if i.replace("csv","txt") not in result1:
            print(i)

if __name__ == '__main__':
    #findpdnszero()
    #findnotoneforall()
   findBeianremain2()
   #findthesecond()



