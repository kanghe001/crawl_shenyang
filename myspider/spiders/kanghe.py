# -*- coding: utf-8 -*-
import scrapy
import time


class KangheSpider(scrapy.Spider):
    name = "get_sy_fang"
    start_urls = (
        "http://www.syfc.com.cn/work/xjlp/new_building01.jsp?page=1",
    )
    key_fields = ["项目名称", "住宅平均价", "总幢数", "商业用房平均价", "座落",
                  "土地等级", "开盘时间", "联系电话", "入住时间", "开发商", "楼盘简介",
                  "设备装修", "配套设施", "周边交通", "绿化率", "容积率", "车位"]
    result_data = {}

    def parse(self, response):
        xiaoqu_list = response.xpath("//body/table[2]/tr/td[3]/table[3]/tr[2]/td/table/tr")
        for xiaoqu in xiaoqu_list:
            xiaoqu_detail_url = xiaoqu.xpath("./td[2]/a/@href").extract()[0]
            xiaoqu_detail_url = response.urljoin(xiaoqu_detail_url)
            yield scrapy.Request(xiaoqu_detail_url, callback=self.xiaoqu_detail)
        for page_num in range(2, 107):
            time.sleep(1)
            next_page = "http://www.syfc.com.cn/work/xjlp/new_building01.jsp?page=" + str(page_num)
            yield scrapy.Request(next_page, callback=self.parse)

    def xiaoqu_detail(self, response):
        x = 0
        xiaoqu_table = response.xpath("//body/table[2]/tr/td[2]/table/tr[2]/td/table")
        for element in xiaoqu_table:
            pro_name = element.xpath("./tr[1]/td[1]/table/tr[1]/td[2]/text()").extract_first()
            avg_price = element.xpath("./tr[1]/td[1]/table/tr[1]/td[4]/text()").extract_first()
            all_num = element.xpath("./tr[1]/td[1]/table/tr[2]/td[2]/text()").extract_first()
            shangye_avg_price = element.xpath("./tr[1]/td[1]/table/tr[2]/td[4]/text()").extract_first()
            zuoluo = element.xpath("./tr[1]/td[1]/table/tr[3]/td[2]/text()").extract_first()
            field_level = element.xpath("./tr[1]/td[1]/table/tr[4]/td[2]/text()").extract_first()
            start_time = element.xpath("./tr[1]/td[1]/table/tr[4]/td[4]/text()").extract_first()
            phone_num = element.xpath("./tr[1]/td[1]/table/tr[5]/td[2]/text()").extract_first()
            settle_time = element.xpath("./tr[1]/td[1]/table/tr[5]/td[4]/text()").extract_first()
            developer = element.xpath("./tr[1]/td[1]/table/tr[6]/td[2]/a/text()").extract_first()
            loupan_introduction = element.xpath("./tr[3]/td[1]/table/tr[1]/td[2]/a/text()").extract_first()
            device_maintain = element.xpath("./tr[3]/td[1]/table/tr[2]/td[2]/a/text()").extract_first()
            peitao_sheshi = element.xpath("./tr[3]/td[1]/table/tr[3]/td[2]/a/text()").extract_first()
            transportation = element.xpath("./tr[3]/td[1]/table/tr[4]/td[2]/a/text()").extract_first()
            lvhua = element.xpath("./tr[3]/td[1]/table/tr[5]/td[2]/a/text()").extract_first()
            rongjilv = element.xpath("./tr[3]/td[1]/table/tr[6]/td[2]/a/text()").extract_first()
            chewei = element.xpath("./tr[3]/td[1]/table/tr[7]/td[2]/a/text()").extract_first()

            data_lis = [
                all_num, pro_name, avg_price, shangye_avg_price, zuoluo, field_level, start_time, phone_num,
                settle_time, developer, loupan_introduction, device_maintain, peitao_sheshi, transportation,
                lvhua, rongjilv, chewei
            ]

            for key in data_lis:
                if key:
                    self.result_data[self.key_fields[x]] = key
                else:
                    self.result_data[self.key_fields[x]] = ""
                x += 1
            yield self.result_data
