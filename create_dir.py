import os
import shutil


def create_dir():

    os.chdir("D:\GuanXiaoLiu\Download\\brand_logo")
    brand_name_list = os.listdir()
    base_file_path = "D:\GuanXiaoLiu\Phishing\\brand_logo\\"
    k = 0
    for brand_name in brand_name_list:

        print(brand_name)
        dir_file_path = base_file_path + brand_name
        os.makedirs(dir_file_path)
    #os.makedirs("D:\GuanXiaoLiu\Phishing\\brand_logo\\"+"aaa")
def copy_url():
    k = 0
    dist_path = "D:\GuanXiaoLiu\Phishing\\brand_logo"
    os.chdir(dist_path)
    brand_names = os.listdir()
    source_path = "D:\GuanXiaoLiu\Phishing\\brand_crawl\Temp_Result\Top5"
    for brand_name in brand_names:
        file_path = source_path + "\\"+brand_name+".txt"
        if not os.path.exists(file_path):
            print(file_path)
            continue
        shutil.copy(source_path + "\\"+brand_name+".txt",dist_path+"\\"+brand_name+"\\"+"url.txt")
def find_no_logo():
    base_path = "D:\GuanXiaoLiu\Phishing\\brand_logo_all"
    os.chdir(base_path)
    k = 0
    brand_names = os.listdir()
    with open("D:\GuanXiaoLiu\Phishing\\brand_crawl\\find_no_logo.txt","w",encoding='gbk') as fw:
        for brand_name in brand_names:
            file_path = base_path + "\\"+brand_name

            file_count = os.listdir(file_path)
            if len(file_count) <= 1 and brand_name != "误报":
                k = k + 1
                fw.write(brand_name+"\n")


    print(k)
if __name__ == "__main__":
   #create_dir()
   copy_url()
    #find_no_logo()