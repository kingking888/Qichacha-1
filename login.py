import lxml.etree
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import requests
import logging
from config import *
class getCookie():
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.logger = logging.getLogger(__name__)

    def Login(self):
        self.browser.get("https://www.qichacha.com/user_login")
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='normalLogin']"))).click()
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "btn-qq"))).click()
        except NoSuchElementException:
            self.close()
        time.sleep(2)
        self.browser.switch_to.frame(self.browser.find_elements_by_tag_name("iframe")[0])
        links = self.browser.find_elements_by_tag_name("a")
        for link in links:
            # print(f"linkText1 = {link.text}, link = {link}")
            if link.text == '帐号密码登录':
                link.click()
                time.sleep(3)
        try:
            user = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='u']")))
            user.clear()
            user.send_keys(USER)
            passwd = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='p']")))
            passwd.send_keys(PASSWD)
            submit = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='login_button']")))
            submit.click()
        except Exception:
            pass
        # time.sleep(3)
        # cookie = [item["name"] + "=" + item["value"] for item in browser.get_cookies()]
        # cookietr = ';'.join(item for item in cookie)
        # print(cookietr)
        # browser.switch_to.frame(browser.find_elements_by_tag_name("iframe")[0])
        time.sleep(2)
        self.browser.get('https://www.qichacha.com/search_index?key=keji&ajaxflag=1&p=1&')
        # time.sleep(3)
        time.sleep(2)
        cookie = [item["name"] + "=" + item["value"] for item in self.browser.get_cookies()]
        cookietr = ';'.join(item for item in cookie)
        return cookietr
    def get_html(self,cookie):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'cookie': cookie,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'referer': 'https://www.qichacha.com/',
            'upgrade-insecure-requests': '1'}
        try:
            URL = 'https://www.qichacha.com/search_index?key=keji&ajaxflag=1&p=4&'
            response = requests.get(URL,headers=headers)

            # 加个判断条件
            if response.status_code == 200:
                # return response.text
                if '立即登录' in response.text:
                    self.logger.debug('登录失败,cookies不可用')
                    print('登录失败,未登录')
                    print(response.text)
                    return None
                elif '您的操作过于频繁' in response.text:
                    print('出现验证码，可能是太频繁了')
                    return None
                    # 出现验证码 这里是点触验证码 一般使用打码平台
                    # 这里是一个点触验证码函数
                else:
                    self.logger.debug('获取cookies成功')
                    return cookie
            else:
                self.logger.debug('状态码异常')
                return None
        except ConnectionError:
            self.logger.debug('连接出错')
            return None

    # def parse(self):
    #     doc = lxml.etree.HTML(self.browser.page_source)
    #     trs = doc.xpath("//*[@id='search-result']/tr/td[2]/a")
    #     for tr in trs:
    #         print(tr.xpath("./text()"))
    # def next_page(self):
    #     js = 'getSearchPage(3,"1","11");'
    #     self.browser.execute_script(js)
    #     self.parse()
    def close(self):
        self.browser.close()

    def run(self):
        cookie = self.Login()
        if cookie:
            if self.get_html(cookie):
                print(cookie)
                print(type(cookie))
                return cookie
        # self.parse()
        # self.next_page()
        self.close()


if __name__ == '__main__':
    c = getCookie()
    c.run()
