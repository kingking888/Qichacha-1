import ast
import json
import time
import requests
from urllib.parse import quote
from lxml import etree
from pymongo import MongoClient
import logging
from config import *
# from Qichacha.常规登录 import cookie
class qichacha():

    def __init__(self):
        self.cookie = cookie()
        self.headers = {
            'cookie': self.cookie,
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

        self.base_url = BASE_URL
        self.max_count = MAX_COUNT
        self.proxy_url = PROXY_URL
        self.proxy = None
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB]
        self.item = {}
        self.logger = logging.getLogger(__name__)

    def get_proxy(self,PROXY_POOL_URL):
        try:
            response = requests.get(PROXY_POOL_URL)
            if response.status_code == 200:
                return response.text
            else:
                return None
        except ConnectionError:
            self.logger.debug('连接出错')
            return None

    def get_html(self,url, count=1):
        self.logger.debug('Crawling', url)
        if count > self.max_count:
            self.logger.debug('trying too many count 5')
            return None
        try:
            if self.proxy:
                proxies = {
                    'http': 'http://' + self.proxy}
                response = requests.get(url, allow_redirects=False, headers=self.headers, proxies=proxies)
            else:
                response = requests.get(url, allow_redirects=False, headers=self.headers)

            if response.status_code == 200:
                return response.text
            else:
                return None
        except ConnectionError as e:
            self.logger.debug('Error Occurred', e.args)
            self.proxy = self.get_proxy(self.proxy_url)
            count += 1
            return self.get_html(url, count)

    def parse(self,html):

        doc = etree.HTML(html)
        trs = doc.xpath("//*[@id='search-result']/section[@id='result-list']/tr")
        self.logger.debug('页中企业数',len(trs))
        for tr in trs:
            print(tr)
            name = tr.xpath("./td[2]/a//text()")
            self.item['name'] = ''.join(name) if len(name) > 0 else None
            # if IS_KEY in self.item['name']:
            email_pl = tr.xpath("./td[2]/p[2]//text()")
            self.item['email'] = tr.xpath("./td[2]/p[2]//text()")[0] if len(email_pl) > 0 else None
            self.item['tel'] = tr.xpath("./td[2]/p[2]//text()")[1] if len(email_pl) > 0 else None
            corporate = tr.xpath("./td[2]/p[1]/a/text()")
            self.item['corporate'] = corporate[0] if len(corporate) > 0 else None
            capital_time = tr.xpath("./td[2]/p[1]/span/text()")
            self.item['capital'] =capital_time[0] if len(capital_time) > 0 else None
            self.item['time'] = capital_time[1] if len(capital_time) > 0 else None
            addr = tr.xpath("./td[2]/p[3]/text()")
            self.item['addr'] = addr[0] if len(addr) else None
            link = tr.xpath("./td[2]/a/@href")
            self.item['link'] = self.base_url + link[0] if len(link) > 0 else None
            state = tr.xpath("./td[3]/span/text()")
            self.item['state'] = state[0] if len(state) > 0 else None
            # print(self.item)
            # self.save_to_mongo(self.item)
        # yield self.item
            # enterprise_html = self.get_enterprise(link)
            # self.parse_enterprise(enterprise_html)
            # self.save_to_mongo(self.item)

    def get_enterprise(self,link):
        try:
            response = requests.get(link,headers=self.headers)
            if response.status_code == 200:
                data_html = response.text
                return data_html
        except requests.ConnectionError:
            self.logger.debug('连接出错')
            return False

    def parse_enterprise(self,html):
        pass

    def save_to_mongo(self,data):
        if self.db['qi'].update({'name': data['name']}, {'$set': data}, True):
            self.logger.debug('Save to Mongo', data['name'])
            print('Save to Mongo', data['name'])
        else:
            self.logger.debug('Saved to Mongo Failed', data['name'])

    def main(self):
        for key in KEYWORD:
            print('当前关键字',key)
            #  getSearchPage(6,"1","11");  js加载的翻页,如果使用ｊｓ语句执行的话，也可以对接splash,或者selenium执行js代码
            for page in range(1,6):
                url = 'https://www.qichacha.com/search_index?key={key}&ajaxflag=1&p={page}&'.format(key=quote(key),page=str(page))
                html = self.get_html(url)
                if html:
                    self.parse(html)
                    time.sleep(4)
                    # for data in self.parse(html):
                    #     self.save_to_mongo(data)

if __name__ == '__main__':
    q = qichacha()
    while 1:
        q.main()
        time.sleep(5)
        if q.main() == []:
            print(time.time())
            break
