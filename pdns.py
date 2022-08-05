import json
import requests
import logging
import os
import pandas as pd
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s[%(filename)s|%(funcName)s|%(lineno)d]%(levelname)s: %(message)s")
logger = logging.getLogger()

import csv
# 全局资源，深圳生产环境接口，需要深圳vpn
PDNS_URL = "http://10.75.5.101/dnsdb/v2/"
PDNS_API_KEY = "bf0e43d642bcdd580529e462b250729405084bfceda34d29554dc16411b87c00"
PDNS_RESULT_LIMIT = 20000
PDNS_MAX_OFFSET = 20000
PDNS_RETRY_SIZE = 2


class DNSResult(object):
    """
    遍历结果，有些域名结果集非常大不能一次返回，需要分块返回
    """
    def __init__(self, url, is_sou=False):
        """
        只针对pdns查询结果遍历
        :param url: 查询的url，不能包含limit和offset
        """
        self._headers = {
            "X-API-Key": PDNS_API_KEY
        }
        if is_sou:
            self._url = url
        else:
            if "?" in url:
                self._url = url+"&limit={l}".format(l=PDNS_RESULT_LIMIT)
            else:
                self._url = url+"?limit={l}".format(l=PDNS_RESULT_LIMIT)
        self._offset = 0
        self._is_end = False
        self.read_size = 0
        # 是否按原始接口请求
        self._is_sou = is_sou

    def is_end(self):
        return self._is_end

    def get_next_dns(self):
        """
        获取下一个分块的记录
        :return: 结果集
        """
        if self._is_end:
            return None
        try:
            if self._is_sou:
                ret = requests.get(url=self._url, headers=self._headers, timeout=(10, 800))
            else:
                ret = requests.get(url=self._url+"&offset={n}".format(n=self._offset),
                                   headers=self._headers, timeout=(10, 800))
        except Exception as err:
            logger.warning(err)
            return None
        if not ret or ret.status_code != 200:
            logger.warning("get dns fail, code: {c}".format(c=ret.status_code))
            self._is_end = True
            return None
        result = []
        for dns_info in ret.text.split("\n"):
            if not dns_info:
                continue
            json_data = json.loads(dns_info)
            if "obj" in json_data:
                result.append(json_data["obj"])
            elif "cond" in json_data and json_data["cond"] == "succeeded":
                self._is_end = True
        self._offset += PDNS_RESULT_LIMIT
        if self._offset >= PDNS_MAX_OFFSET:
            self._is_end = True
        self.read_size += len(result)
        return result

    def __iter__(self):
        return self

    def next(self):
        retry = 0
        while retry < PDNS_RETRY_SIZE:
            retry += 1
            result = self.get_next_dns()
            if not result and self.is_end():
                raise StopIteration
            if not result:
                continue
            return result
        else:
            # 重试都失败就认为完成
            self._is_end = True
            raise StopIteration

    def __next__(self):
        return self.next()


class PassiveDNSClient(object):
    """
    查询pdns记录客户端
    """
    @staticmethod
    def merge_date_range(date_range=None):
        """
        将时间数据合并为参数形式
        :param date_range: 查询记录时间限制
        :return: http参数形式
        """
        date_param = ""
        if date_range:
            for k, v in date_range.items():
                temp_param = k + "=" + str(v)
                if date_param:
                    date_param += ("&" + temp_param)
                else:
                    date_param += temp_param
        return date_param

    @staticmethod
    def get_domain_dns(domain, dns_type=None, date_range=None):
        """
        查询指定域名dns记录
        :param domain: 查询的域名，如：test.com,*.test.com,test.*
                       如果要获取所有域名可以使用*来全局匹配，但不是绝对的，不增加时间范围限定看起好像可以
                       如果增加了时间范围，需要使用*.com来获取这一时间段的所有.com域名
        :param dns_type: 要查询的记录类型，如A,AAAA,NS等，如果未指定将查询所有
                         ANY-DNSSEC查询所有DNSSEC记录，DNSSEC是dns的安全验证扩展
        :param date_range：指定时间范
                       {
                                   "time_first_before": 123,#只匹配首次观察到记录时间之前的数据
                                   "time_first_after": 123,#只匹配首次观察到记录时间之后的数据
                                   "time_last_before": 123,#只匹配最后观察到记录时间之前的数据
                                   "time_last_after": 123,#只匹配最后观察到记录时间之后的数据
                               }
            :return: 查询结果
            """
        request_param = "lookup/rrset/name/{domain}{type}".format(domain=domain,
                                                                  type="/" + dns_type if dns_type else "")
        # 增加时间限制
        date_param = PassiveDNSClient.merge_date_range(date_range=date_range)
        if date_param:
            request_param += ("?" + date_param)
        return DNSResult(url=PDNS_URL + request_param)

    @staticmethod
    def get_ip_dns(ip, dns_type=None, date_range=None):
        request_param = "lookup/rdata/ip/{ip}{type}".format(ip=ip, type="/" + dns_type if dns_type else "")
        # 增加时间限制
        date_param = PassiveDNSClient.merge_date_range(date_range=date_range)
        if date_param:
            request_param += ("?" + date_param)
        return DNSResult(url=PDNS_URL + request_param)

    @staticmethod
    def get_domain_dns_regex(regex, dns_type=None, date_range=None):
        request_param = "regex/rrnames/{regex}{type}".format(regex=regex, type="/" + dns_type if dns_type else "")
        # 增加时间限制
        date_param = PassiveDNSClient.merge_date_range(date_range=date_range)
        if date_param:
            request_param += ("?" + date_param)
        return DNSResult(url=PDNS_URL + request_param)

    @staticmethod
    def get_domain_count_summarize(domain, dns_type=None, max_count=None):
        request_param = "summarize/rrset/name/{name}{type}".format(name=domain, type="/" + dns_type if dns_type else "")
        # 增加最大数量的限制
        if max_count:
            request_param += ("?" + "max_count=" + str(max_count))
        return DNSResult(url=PDNS_URL + request_param, is_sou=True)
if __name__ == "__main__":
    test = PassiveDNSClient()
    os.chdir('D:\GuanXiaoLiu\Phishing\\brand_crawl\BeianResults\Manufacturing_top50')
    BeianNameList = os.listdir()
    os.chdir('.\\..\\')
    result_set = set()
    df_sub_count = pd.read_csv('D:\GuanXiaoLiu\Phishing\\brand_crawl\Subdomains\Manufacturing_top50\\' + "subdomain_count.csv", engine='python', encoding='gbk',
                               header=0).values.tolist()
    for j in df_sub_count:
        result_set.add(j[0])
    for i in range(len(BeianNameList)):

        result = set()
        # if not os.path.exists('.\\Subdomain1\\' + BeianNameList[i].replace('.csv', '')):
        #     os.mkdir('.\\Subdomain1\\' + BeianNameList[i].replace('.csv', ''))
        if os.path.getsize('D:\GuanXiaoLiu\Phishing\\brand_crawl\BeianResults\Manufacturing_top50\\' + BeianNameList[i]) == 0:
            continue
        if (BeianNameList[i].replace('.csv', '') not in result_set):
            print(BeianNameList[i].replace('.csv', ''))
            df = pd.read_csv('D:\GuanXiaoLiu\Phishing\\brand_crawl\BeianResults\Manufacturing_top50\\' + BeianNameList[i], engine='python', encoding='UTF-8',
                             header=None).values.tolist()
            df = [b for a in df for b in a]
            for j in df:

                data = test.get_domain_dns(domain="*." + j)

            # data = test.get_domain_dns_regex(regex="[a-z\\-0-9]+\\.baidu\\.com", dns_type="A")
            for info in data:
                for s in info:
                    # print(s)
                    if(str(s['rrname']).find("*") == -1):
                        rrname = str(s["rrname"])
                        if rrname[-1] == ".":
                            rrname = rrname[:-1]
                        print(rrname)
                        result.add(rrname)
            df = pd.DataFrame(result)
            df.to_csv(
                'D:\GuanXiaoLiu\Phishing\\brand_crawl\Subdomains\Manufacturing_top50\\' +  BeianNameList[i].replace('.csv','') + ".csv",
                header=None, index=False, mode='w')

            # print(result)
            print(BeianNameList[i])
            print("resulit:" + str(len(result)))
            result_map = {"company": BeianNameList[i].replace('.csv', ''), "subdomain_count": str(len(result)),
                          "status": 1}
            with open('D:\GuanXiaoLiu\Phishing\\brand_crawl\Subdomains\Manufacturing_top50\\' + "subdomain_count.csv", "a", newline='') as fw:
                writer = csv.writer(fw)
                writer.writerow(result_map.values())