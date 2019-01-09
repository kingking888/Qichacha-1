import io
import random
import time

import selenium
from selenium.common.exceptions import WebDriverException
from Qichacha import chaojiying
import PIL.Image
from selenium.webdriver import ActionChains
from selenium import webdriver
class Login():
    
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.username = ''
        self.passwd = ''

    def input(self,login_url):
        self.browser.get(login_url)
        self.browser.find_element_by_id("normalLogin").click()
        time.sleep(2)
        # one = self.browser.find_element_by_xpath("//*[@id='nc_1__scale_text']/span")
        user = self.browser.find_element_by_id("nameNormal")
        user.send_keys(self.username)
        passwd = self.browser.find_element_by_id("pwdNormal")
        passwd.send_keys(self.passwd)
        time.sleep(1)

        return self.browser

    def sliding(self):
        # self.browser.find_element_by_id("nc_1_n1z").click()  # 点击显示滑块拼图
        time.sleep(1)
        tab = selenium.webdriver.ActionChains(self.browser)
        # 获取滑动按钮
        hua1 = self.browser.find_element_by_id("nc_1_n1z").click()
        # 使用随机数确定滑动位置后滑动
        l = [0.2,0.3,0.4,0.5]
        t = random.choice(l)
        time.sleep(t)
        S = [450,465,480,500,550]
        s = random.choice(S)
        tab.drag_and_drop_by_offset(hua1, s, 0).perform()
        tab.move_to_element(hua1).release()
        time.sleep(0.5)
        return self.browser

    def click(self):
        one = self.browser.find_element_by_id("nc_1__scale_text")
        print(one)
        location = one.location
        size = one.size
        print(location)
        print(size)
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        top = int(top)
        bottom = int(bottom)
        left = int(left)
        right = int(right)
        print('验证码位置', top, bottom, left, right)
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = PIL.Image.open(io.BytesIO(screenshot))
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save('上半部分.png')
        time.sleep(1)


        tow = self.browser.find_element_by_xpath("//*[@id='nc_1_clickCaptcha']")
        location = tow.location
        size = tow.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        top = int(top)
        bottom = int(bottom)
        left = int(left)
        right = int(right)
        print('验证码位置', top, bottom, left, right)
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = PIL.Image.open(io.BytesIO(screenshot))
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save('下半部分.png')


        top, bottom, left, right = 444, location['y'] + size['height'], 451, location['x'] + size['width']
        top = int(top)
        bottom = int(bottom)
        left = int(left)
        right = int(right)
        print('验证码位置', top, bottom, left, right)
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = PIL.Image.open(io.BytesIO(screenshot))
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save('整张.png')
        code = chaojiying.get_code()
        print(code)
        locations = [[int(number) for number in group.split(',')] for group in code]
        try:
            for location in locations:
                print(location)
                ActionChains(self.browser).move_to_element_with_offset(tow, location[0],location[1] - 35).click().perform()
        except WebDriverException:
            return self.click()
        time.sleep(1)
        sub = self.browser.find_element_by_xpath("//*[@id='user_login_normal']/button")
        print(sub)
        sub.click()
        time.sleep(1)
        return self.browser
        # input = self.browser.find_element_by_id("nc_1_captcha_input")
        # input.send_keys(code)
        # self.browser.find_element_by_id("nc_1_scale_submit").click()
        # time.sleep(1)
        # self.browser.find_element_by_xpath("//*[@id='user_login_normal']/button").click()
    def test(self,url):
        # 半道遇上验证码
        if '您的操作过于频繁' in self.browser.page_source:
            time.sleep(0.5)
            self.test_sliding()
        self.browser.get(url)
        time.sleep(1)
        return self.browser

    def test_sliding(self):
        tab = selenium.webdriver.ActionChains(self.browser)
        # 获取滑动按钮
        hua1 = self.browser.find_element_by_id("nc_1_n1z").click()
        # 使用随机数确定滑动位置后滑动
        l = [0.2, 0.3, 0.4, 0.5]
        t = random.choice(l)
        time.sleep(t)
        S = [450, 465, 480, 500, 550]
        s = random.choice(S)
        tab.drag_and_drop_by_offset(hua1, s, 0).perform()
        tab.move_to_element(hua1).release()
        time.sleep(1)
        self.test_click()
        return self.browser

    def test_click(self):

        one = self.browser.find_element_by_id("nc_1__scale_text")
        print(one)
        location = one.location
        size = one.size
        print(location)
        print(size)
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        top = int(top)
        bottom = int(bottom)
        left = int(left)
        right = int(right)
        print('验证码位置', top, bottom, left, right)
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = PIL.Image.open(io.BytesIO(screenshot))
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save('上半部分.png')
        time.sleep(2)
        #

        tow = self.browser.find_element_by_xpath("//*[@id='nc_1_clickCaptcha']")
        location = tow.location
        size = tow.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        top = int(top)
        bottom = int(bottom)
        left = int(left)
        right = int(right)
        print('验证码位置', top, bottom, left, right)
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = PIL.Image.open(io.BytesIO(screenshot))
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save('下半部分.png')

        top, bottom, left, right = 303, location['y'] + size['height'], 473, location['x'] + size['width']
        top = int(top)
        bottom = int(bottom)
        left = int(left)
        right = int(right)
        print('验证码位置', top, bottom, left, right)
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = PIL.Image.open(io.BytesIO(screenshot))
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save('整张.png')
        code = chaojiying.get_code()
        print(code)
        locations = [[int(number) for number in group.split(',')] for group in code]
        try:
            for location in locations:
                print(location)
                selenium.webdriver.ActionChains(self.browser).move_to_element_with_offset(tow, location[0],
                                                                                 location[1] - 35).click().perform()
        except WebDriverException:
            return self.test_click()
            # time.sleep(2)
            # sub = self.browser.find_element_by_xpath("//*[@id='user_login_normal']/button")
            # print(sub)
            # sub.click()

        time.sleep(2)
        sub = self.browser.find_element_by_xpath("//*[@id='verify']")
        sub.click()
        return self.browser

    def get_cookie(self):
        time.sleep(1)
        cookie = [item["name"] + "=" + item["value"] for item in self.browser.get_cookies()]
        cookietr = ';'.join(item for item in cookie)
        print(cookietr)
        return cookietr

    def close(self):
        time.sleep(10)
        self.browser.close()

def cookie():
    q = Login()
    q.input("https://www.qichacha.com/user_login")
    q.sliding()
    q.click()
    q.test("https://www.qichacha.com/search_index?key=%25E7%25A7%2591%25E6%258A%2580&ajaxflag=1&p=2&")
    cookie = q.get_cookie()
    q.close()
    return cookie

if __name__ == '__main__':
    cookie()
