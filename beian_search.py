# -*- coding: utf-8 -*-
import csv
import random
import threading

import pandas as pd
import requests
import hashlib
import time
import base64
import cv2
import os

os.environ['no_proxy'] = '*' #避免因系统代理设置导致请求失败


#提前获取要查询的对象信息，以免Token失效（Token有效时间为3分钟）
#print("项目地址：https://github.com/wongzeon/ICP-Checker\n")
#print("版本：V1.1 可用测试：2021-7-27\n")
#print("以企业名称查询的，需要输入企业全称\n")
#print("以域名查询的，请不要输入“http/www”等域名外的字符\n")
def beian_search_api(info,title):
    requests.adapters.DEFAULT_RETRIES = 5
    info_data = {
        'pageNum':'',
        'pageSize':'',
        'unitName':info
    }
    # proxies = {
    #     "http": "http://750277410108624896:m0CbTwXl@http-dynamic-S02.xiaoxiangdaili.com:10030",
    #     "https": "https://750277410108624896:m0CbTwXl@http-dynamic-S02.xiaoxiangdaili.com:10030"
    # }
    proxies = {
        "http": "http://750277410108624896:m0CbTwXl@http-dynamic-S02.xiaoxiangdaili.com:10030"
    }
    #构造AuthKey
    timeStamp = int(round(time.time()*1000))
    authSecret = 'testtest' + str(timeStamp)
    authKey = hashlib.md5(authSecret.encode(encoding='UTF-8')).hexdigest()
    #获取Cookie
    cookie_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.42'
    }
    cookie = requests.utils.dict_from_cookiejar(requests.get('https://beian.miit.gov.cn/',headers=cookie_headers).cookies)['__jsluid_s']
    #请求获取Token
    t_url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/auth'
    t_headers = {
        'Host': 'hlwicpfwc.miit.gov.cn',
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Microsoft Edge";v="90"',
        'Accept': '*/*',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46',
        'Origin': 'https://beian.miit.gov.cn',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://beian.miit.gov.cn/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': '__jsluid_s=' + cookie
    }
    data = {
        'authKey': authKey,
        'timeStamp': timeStamp
    }
    requests.packages.urllib3.disable_warnings()
    t_response = requests.post(t_url,data=data,headers=t_headers,proxies=proxies,verify=False)

    try:
        get_token = t_response.json()['params']['bussiness']
    except:
        print('\n'"请求被禁止，请稍后或更换头部与IP后再试，状态码：",t_response.status_code)
        return False

    #获取验证图像、UUID
    p_url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/image/getCheckImage'
    p_headers = {
        'Host': 'hlwicpfwc.miit.gov.cn',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Microsoft Edge";v="90"',
        'Accept': 'application/json, text/plain, */*',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46',
        'token': get_token,
        'Origin': 'https://beian.miit.gov.cn',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://beian.miit.gov.cn/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': '__jsluid_s=' + cookie
    }
    p_request = requests.post(p_url,data='',headers=p_headers)
    try:
        p_uuid = p_request.json()['params']['uuid']
        big_image = p_request.json()['params']['bigImage']
        small_image = p_request.json()['params']['smallImage']
    except KeyError:
        print("请重试，请求状态码：",p_request.status_code)
        return False

    #解码图片，写入并计算图片缺口位置
    with open('bigImage.jpg','wb') as f:
        f.write(base64.b64decode(big_image))
        f.close()
    with open('smallImage.jpg','wb') as f:
        f.write(base64.b64decode(small_image))
        f.close()
    background_image = cv2.imread('bigImage.jpg',cv2.COLOR_GRAY2RGB)
    fill_image = cv2.imread('smallImage.jpg',cv2.COLOR_GRAY2RGB)
    background_image_canny = cv2.Canny(background_image, 100, 200)
    fill_image_canny = cv2.Canny(fill_image, 100, 300)
    position_match = cv2.matchTemplate(background_image, fill_image, cv2.TM_CCOEFF_NORMED)
    min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(position_match)
    position = max_loc
    mouse_length = position[0]+1
    os.remove('bigImage.jpg')
    os.remove('smallImage.jpg')
    #通过拼图验证，获取sign
    check_url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/image/checkImage'
    check_headers = {
        'Host': 'hlwicpfwc.miit.gov.cn',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'Content-Length': '60',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Microsoft Edge";v="90"',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.42',
        'token': get_token,
        'Content-Type': 'application/json',
        'Origin': 'https://beian.miit.gov.cn',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://beian.miit.gov.cn/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': '__jsluid_s=' + cookie
    }
    check_data = {
        'key':p_uuid,
        'value':mouse_length
    }
    check_request = requests.post(check_url,json=check_data,headers=check_headers)
    try:
        sign = check_request.json()['params']
    except Exception:
        print('\n'"请求被禁止，请稍后或更换头部与IP后再试，状态码：",check_request.status_code)
        return False

    #获取备案信息
    info_url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/icpAbbreviateInfo/queryByCondition'
    info_headers = {
        'Host': 'hlwicpfwc.miit.gov.cn',
        'Connection': 'keep-alive',
        'Content-Length': '78',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Microsoft Edge";v="90"',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'uuid': p_uuid,
        'token': get_token,
        'sign': sign,
        'Origin': 'https://beian.miit.gov.cn',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://beian.miit.gov.cn/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': '__jsluid_s=' + cookie
    }
    info_request = requests.post(info_url,json=info_data,headers=info_headers)
    domain_total = info_request.json()['params']['total']
    page_total = info_request.json()['params']['lastPage']
    page_size = info_request.json()['params']['pageSize']
    start_row = info_request.json()['params']['startRow']
    end_row = info_request.json()['params']['endRow']

    csv_list = []
    os.system('cls')
    print("\n查询对象",title,"共有",domain_total,"个备案域名",'\n')
    #print("域名具体信息如下：")
    for i in range(1,page_total+1):
        for k in range(start_row,end_row+1):
            info_base = info_request.json()['params']['list'][k]
            domain_name = info_base['domain']
            domain_type = info_base['natureName']
            domain_licence = info_base['mainLicence']
            domain_web_licence = info_base['serviceLicence']
            domain_status = info_base['limitAccess']
            domain_approve_date = info_base['updateRecordTime']
            domain_owner = info_base['unitName']
            try:
                domain_content_approved = info_base['contentTypeName']
                if not bool(domain_content_approved):
                    domain_content_approved = "无"
            except KeyError:
                domain_content_approved = "无"
            #print("\n域名主办方：",domain_owner,'\n')
            print("域名：",domain_name,'\n')
            csv_list.append(domain_name)
            #print("备案许可证号：",domain_licence,'\n')
            #print("网站备案号：",domain_web_licence,'\n')
            #print("域名类型：",domain_type,'\n')
            #print("网站前置审批项：",domain_content_approved,'\n')
            #print("是否限制接入：",domain_status,'\n')
            #print("审核通过日期：",domain_approve_date,'\n')
        info_data_page = {
            'pageNum':i+1,
            'pageSize':'10',
            'unitName':info
        }
        if info_data_page['pageNum'] > page_total:
            print("查询完毕",'\n')
            break
        else:
            info_request = requests.post(info_url,json=info_data_page,headers=info_headers)
            start_row = info_request.json()['params']['startRow']
            end_row = info_request.json()['params']['endRow']
            time.sleep(3)
    df = pd.DataFrame(csv_list)
    title = str(title)

    title.replace('//','')
    title = title.replace('|', ' ')
    title  = title.replace('&', '')
    title = title.strip()
    dir_path = "D:\GuanXiaoLiu\Phishing\\brand_crawl\BeianResults\Medicine_top50"
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    df.to_csv(dir_path+"\\" + title + ".csv", header=None, index=False, mode='w')
    return True
    #os.system('pause')
def batch_resolve(start,end,name_list):
    for i in range(len(name_list)):
        if i < start:
            continue
        if i >= end:
            break
        a = random.randint(10, 25)
        time.sleep(a)
        beian_search_api(name_list[i],name_list[i])

    pass
if __name__ == '__main__':

    os.chdir("D:\GuanXiaoLiu\Phishing\\brand_crawl\BeianResults")
    BeianResults = os.listdir()
    df = pd.read_csv("D:\GuanXiaoLiu\Phishing\\brand_crawl\Client_Name\Medicine_top50.csv",engine = "python",encoding="gbk",header=None,usecols=[0]).values.tolist()
    df = [b for a in df for b in a]
    print(df)
    # name_list = []
    # thread_list = []
    # for j in df:
    #     print(j)
    #     name_list.append(j)
    # for i in range(5):
    #     t = threading.Thread(target=batch_resolve, args=(i*5, i*5+5, name_list,))
    #     t.setDaemon(True)  # 把子线程设置为守护线程，必须在start()之前设置
    #     thread_list.append(t)
    #     t.start()
    # for j in thread_list:
    #     j.join()

    # i  = 0
    # for j in df[50:70]:
    #
    #     if j in BeianResults:
    #         continue
    #     if j == "nan":
    #         continue
    #
    #     print(j)
    #     #print(j[0])
    #     a = random.randint(10, 25)
    #     time.sleep(a)
    #     beian_search_api(j,j)
    beian_search_api("中国兵器装备集团有限公司","中国兵器装备集团有限公司")

#中国石油化工股份有限公司