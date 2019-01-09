import time

import requests
from lxml import etree
from Qichacha.常规登录 import Login
def get_html(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'UM_distinctid=167980d79419ef-08c6ac64388c66-3c720356-1fa400-167980d7943a93; zg_did=%7B%22did%22%3A%20%22167980d795d138-09097ecdfc470a-3c720356-1fa400-167980d795e1e%22%7D; _uab_collina=154444428026665112646301; saveFpTip=true; acw_tc=7160b5a615444442933874398eb4b4ec168f78f7399d84643caa034a84; QCCSESSID=h3v1t5ac6pqsrnh97aruv7fop0; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1544683694,1545205175,1545214685,1545214713; CNZZDATA1254842228=2089637536-1544439362-null%7C1545460724; hasShow=1; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201545461818348%2C%22updated%22%3A%201545463495383%2C%22info%22%3A%201545205174893%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22ce4370992a5bf4fde0ad76a28bab828c%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1545463496',
        'Host': 'www.qichacha.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    r = requests.session()
    proxies = {'http':'http://127.0.0.1:1080'}
    res = r.get(url,headers=headers,proxies=proxies)
    return res.text
  
def parse(html,item):
    doc = etree.HTML(html)
    trs = doc.xpath("//*[@id='search-result']/section[@id='result-list']/tr")
    # print(trs)
    for tr in trs:
        print(tr)
        name = tr.xpath("./td[2]/a/text()")
        item['name'] = ''.join(name) if len(name) > 0 else None
        # if IS_KEY in item['name']:
        #
        item['email'] = tr.xpath("./td[2]/p[2]/text()")
        item['pl'] = tr.xpath("./td[2]/p[2]/span/text()")
        fa = tr.xpath("./td[2]/p[1]/a/text()")
        item['fa'] = tr.xpath("./td[2]/p[1]/a/text()")[0] if len(fa) > 0 else None
        capital_time = tr.xpath("./td[2]/p[1]/span/text()")
        item['capital'] = capital_time[0] if len(capital_time) > 0 else None
        item['time'] = capital_time[1] if len(capital_time) > 0 else None
        addr = tr.xpath("./td[2]/p[3]/text()")
        item['addr'] = addr[0].strip('\n').strip(' ').strip('\n') if len(addr) else None
        link = tr.xpath("./td[2]/a/@href")
        item['link'] = 'https://www.qichacha.com' + link[0] if len(link) > 0 else None
        tag = tr.xpath("./td[2]/p[4]/em/text()")
        item['tag'] = tag[0] if len(tag) > 0 else None
        state = tr.xpath("./td[3]/span/text()")
        item['state'] = state[0] if len(state) > 0 else None
        # print(item)

def main():
    for i in ['金融','市场','销售','电脑','门窗','机构']:
        for page in range(1,6):
            url = 'https://www.qichacha.com/search_index?key={}&ajaxflag=1&p={}&'.format(i,str(page))
            html = get_html(url)
            item = {}
            parse(html,item)
            time.sleep(1.5)

if __name__ == '__main__':
    while 1:
        main()
        time.sleep(2)
        if main() == []:
            print(time.time())
            break
