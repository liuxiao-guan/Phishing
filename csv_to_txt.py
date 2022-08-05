import os

import pandas as pd
##这是将csv转为txt的程序
os.chdir('D:\GuanXiaoLiu\Phishing\\brand_crawl\Result\\Manufacturing_top50')

BeianNameList = os.listdir()
txt_path = "D:\GuanXiaoLiu\Phishing\\brand_crawl\Temp_Result\\Manufacturing_top50"
if not os.path.exists(txt_path):
    os.mkdir(txt_path)

os.chdir(txt_path)
txt_list= os.listdir()
for i in range(len(BeianNameList)):
    result = set()
    csv_filename= "D:\GuanXiaoLiu\Phishing\\brand_crawl\Result\\Manufacturing_top50\\"+BeianNameList[i]
    if BeianNameList[i].replace("csv","txt") in txt_list:
        continue
    if os.path.getsize(csv_filename) > 0:
        print(BeianNameList[i])
        df =pd.read_csv(csv_filename,encoding='utf8',engine='python',header=None).values.tolist()
        df = [b for a in df for b in a]
        txt_filename= "D:\GuanXiaoLiu\Phishing\\brand_crawl\Temp_Result\\Manufacturing_top50\\"+BeianNameList[i].replace("csv","txt")
        with open(txt_filename,'w',encoding='gbk') as f:
            for j in df:
                if j not in result:
                    result.add(j)
                    f.write(j+"\n")
        f.close()

