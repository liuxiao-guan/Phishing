import os
import time

import pandas as pd
import random
def select_much(file_path,file_size):

    os.chdir(file_path)
    subdomain_list = os.listdir()
    k =0
    for subdomain in subdomain_list:

        file_name = file_path+"\\"+subdomain
        delete_set = set()
        if os.path.getsize(file_name) < file_size:
            continue
        print(subdomain)
        df =pd.read_csv(file_name,engine='python',encoding='utf8',header=None).values.tolist()
        df = [b for a in df for b in a]
        randon_nums = set()
        ## 得到五个不同的随机数
        while len(randon_nums) < 7 :
            a = random.randint(1,10)
            randon_nums.add(a)

        length = len(df)
        i = 0
        while i < length:
            for j in randon_nums:
                if j + i < length:
                    delete_set.add(df[j + i])
            i = i + 10
        ## 将删除一半的数据再写入csv文件
        result_set = pd.DataFrame(delete_set)
        result_set.to_csv(file_name,mode='w',index=False,header=None)

def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)
if __name__ == "__main__":
    file_path = "D:\GuanXiaoLiu\Phishing\\brand_crawl\Result\Manufacturing_top50"
    file_size = 1024*13
    select_much(file_path,file_size)

    # time1 = TimeStampToTime(1479264792)
    # print(type(time1))
    # print(time1)
    #
    # hour = time.localtime(1479264792).tm_mday
    # print(hour)