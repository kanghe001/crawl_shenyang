# -*- coding: utf-8 -*-
import scrapy
import time
import base64
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class KmhouseSpiderSpider(scrapy.Spider):
    name = "kmhouse_spider"
    start_urls = (
        'http://www.kmhouse.org/lqt/SellLicenseDisp.asp/',
    )
    driver = webdriver.Firefox()
    driver.set_page_load_timeout(5) #throw a TimeoutException when thepage load time is more than 5 seconds.

    def parse(self, response):
        """模拟浏览器实现翻页，并解析每一个话题列表页的url_list
        """
        url_set = set() #话题url的集合
        self.driver.get(response.url)
        while True:
            wait = WebDriverWait(self.driver, 2)
            # wait.until(lambda driver:driver.find_element_by_xpath('//ul[@class="post-list"]/li[@class]/a'))#VIP，内容加载完成后爬取
            # sel_list = self.driver.find_elements_by_xpath('//ul[@class="post-list"]/li[@class]/a')
            # url_list = [sel.get_attribute("href") for sel in sel_list]
            # url_set |= set(url_list)
            try:
                 wait =WebDriverWait(self.driver, 2)
                 wait.until(lambda driver:driver.find_element_by_xpath('//form[@id="FrmTurn"]/input[3]'))#VIP，内容加载完成后爬取
                 next_page =self.driver.find_element_by_xpath('//form[@id="FrmTurn"]/input[3]')
                 next_page.click() #模拟点击下一页
            except:
                 print "#####Arrive thelast page.#####"
                 break
#        with open('url_set.txt', mode='w') as f:
#            f.write(repr(url_set))
        # for url in url_set:
        result_data = {}
        x = 0
        key_field = ["项目名称", "项目座落", "开发商", "发证机构", "预售许可证号", "发证日期", "预售面积"]
        fields = response.xpath("//body/div/table[2]/tr[3]/td/table/tr")
        for field in fields:
            pro_name = field.xpath("./td/table/tr[1]/td/text()").extract_first()[5:]
            pro_addr = field.xpath("./td/table/tr[2]/td[1]/text()").extract_first()[5:]
            developer = field.xpath("./td/table/tr[2]/td[2]/text()").extract_first()[4:]
            fazheng_company = field.xpath("./td/table/tr[3]/td[1]/text()").extract_first()[5:]
            ys_allow = field.xpath("./td/table/tr[3]/td[2]/text()").extract_first()[7:]
            fz_date = field.xpath("./td/table/tr[4]/td[1]/text()").extract_first()[5:]
            ys_area = field.xpath("./td/table/tr[4]/td[2]/text()").extract_first()[5:]
            value_lis = [pro_name, pro_addr, developer, fazheng_company, ys_allow, fz_date, ys_area]

            for val in value_lis:
                if val:
                    result_data[key_field[x]] = val
                else:
                    result_data[key_field[x]] = ""
                x += 1

            yield result_data

"""
        result_data = {}
        x = 0
        key_field = ["项目名称", "项目座落", "开发商", "发证机构", "预售许可证号", "发证日期", "预售面积"]
        fields = response.xpath("//body/div/table[2]/tr[3]/td/table/tr")
        for field in fields:
            pro_name = field.xpath("./td/table/tr[1]/td/text()").extract_first()[5:]
	    pro_addr = field.xpath("./td/table/tr[2]/td[1]/text()").extract_first()[5:]
            developer = field.xpath("./td/table/tr[2]/td[2]/text()").extract_first()[4:]
            fazheng_company = field.xpath("./td/table/tr[3]/td[1]/text()").extract_first()[5:]
            ys_allow = field.xpath("./td/table/tr[3]/td[2]/text()").extract_first()[7:]
            fz_date = field.xpath("./td/table/tr[4]/td[1]/text()").extract_first()[5:]
            ys_area = field.xpath("./td/table/tr[4]/td[2]/text()").extract_first()[5:]
        value_lis = [pro_name, pro_addr, developer, fazheng_company, ys_allow, fz_date, ys_area]

        for val in value_lis:
            if val:
                result_data[value_lis[x]] = val
            else:
                result_data[value_lis[x]] = ""
            x += 1
        yield result_data
"""


