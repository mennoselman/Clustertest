from bs4 import BeautifulSoup 
import urllib2
import selenium
import signal
from contextlib import closing
#from selenium.webdriver import Firefox # pip install selenium
#from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from IPython import get_ipython
import platform
import time
import os
import requests
import sys


def init_phantomjs_driver(*args, **kwargs):

    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'

    driver =  webdriver.PhantomJS(*args, **kwargs)
    # driver.set_window_size(1400, 1000)

    return driver

class Crawler():
    def __init__(self):

        self.driver = init_phantomjs_driver(executable_path='phantomjs-2.1.1-linux-x86_64/bin/phantomjs')

        self.driver.implicitly_wait(10)  # seconds
        self.driver.set_page_load_timeout(30)

        self.starting()

    def subproducts(self, page_source, url):
        soup = BeautifulSoup(page_source)
        int_href_tags = soup.find_all(href=True)
        int_hrefs = []
        for t in int_href_tags:
            #if "producten/verse-kant-en-klaar-maaltijden-salades/" in str(t):
            if url + "/" in str(t):
                if "bonus" not in t.get("href"):
                    if "=" not in t.get("href"):
                        if t.get("href") not in int_hrefs:
                            int_hrefs.append(t.get("href"))
        return int_hrefs

    def get_category(self, var, set1, set2):
        su = 0
        count_i = -1
        while count_i < len(set1)-1 and su < var:
            count_j = -1
            count_i = count_i + 1
            while count_j < len(set2[count_i][:])-1 and su < var:
                count_j = count_j+1
                su = su + 1
                
        return set2[count_i][count_j]
    
    def subproducts2(self, page_source, url):
        soup = BeautifulSoup(page_source)
        int_href_tags = soup.find_all(href=True)
        int_hrefs = []
        for t in int_href_tags:
            #if "producten/verse-kant-en-klaar-maaltijden-salades/" in str(t):
            if "product/wi" in str(t):
                if "bonus" not in t.get("href"):
                    if "=" not in t.get("href"):
                        if t.get("href") not in int_hrefs:
                            int_hrefs.append(t.get("href"))
        return int_hrefs


    def starting(self):
        self.driver.get("https://www.ah.nl/producten")
        #wait = WebDriverWait(self.driver, 200)
        WebDriverWait(self.driver, timeout=30).until(
         lambda x: x.find_element_by_xpath("//div[@class='lane row product-category-navigation-lane  product-category-navigation-lane--ah']"))
        page_source = self.driver.page_source
        print(page_source)
        soup = BeautifulSoup(page_source)
        new_soup = (soup.find_all("a", class_="column grid-item category-link heading--9 link--2 link-color--dark small-12 medium-4 large-3 xlarge-2 xxlarge-2 color-white__bg--1"))
        hrefs1 = []
        for t in new_soup:
            if "producten" in str(t):
                hrefs1.append(t.get("href"))
        hrefs1
        results_subproducts = []
        count = -1
        while count < len(hrefs1)-1:
            # use firefox to get page with javascript generated content
            count = count + 1
            #with closing(Firefox()) as browser:
            url2 = "https://www.ah.nl" + hrefs1[count]
            self.driver.get(url2)
            time.sleep(4)
            # wait for the page to load
            WebDriverWait(self.driver, timeout=100).until(
                    lambda x: x.find_element_by_id('Filters'))
            # store it to string variable
            page_source = self.driver.page_source
            subs = self.subproducts(page_source, hrefs1[count])  
            results_subproducts.append(subs)
        count
        results_subproducts

    def quit(self):
            try:
                self.driver.service.process.send_signal(signal.SIGTERM)
                self.driver.quit()
            except:
                self.driver.quit()

Crawler().quit()
crawler = Crawler()