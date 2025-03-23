import re
import scrapy
from urllib.parse import urljoin, unquote
import requests
from scrapy.selector import Selector
import time
import random

class PropertiesSpider(scrapy.Spider):
    name = 'properties'
    allowed_domains = ['divar.ir']
    start_urls = ['https://divar.ir/s/tehran/buy-apartment']


    def extract_floor_number(self, text):
        if not text:
            return 0
        
        if match := re.search(r'(\d+)\s*از\s*\d+', text):
            return int(match.group(1))

        if match := re.search(r'\+(\d+)', text):
            return f">{match.group(1)}"
        
        if text.isdigit():
            return int(text)
        
        return 0
    
    def extract_construction_date(self, text):
         if "قبل" in text:
              return 1369
         return int(text)

    def extract_room_number(self, text):
            if "بدون" in text:
                return 0
            return int(text)

    def parse(self, response):
        hrefs = response.xpath('//*[@id="post-list-container-id"]/div[1]/div/div//a/@href').getall()

        for href in hrefs:
            # try:
                url = urljoin(response.url, href)
                request = requests.get(url)
                request = Selector(text=request.text)
                time.sleep(random.randint(10,30))
                
                area = request.xpath('//*[@id="app"]/div[2]/div/main/article/div/div[1]/section[1]/div[4]/table[1]/tbody/tr/td[1]/text()').get()
                construction_date = request.xpath('//*[@id="app"]/div[2]/div/main/article/div/div[1]/section[1]/div[4]/table[1]/tbody/tr/td[2]/text()').get()
                number_of_rooms = request.xpath('//*[@id="app"]/div[2]/div/main/article/div/div[1]/section[1]/div[4]/table[1]/tbody/tr/td[3]/text()').get()

                extra_details = request.xpath('//td[contains(@class, "kt-group-row-item__value")]/text()').getall()
                elevator = 1 if "آسانسور" in extra_details else 0
                parking = 1 if "پارکینگ" in extra_details else 0
                storage_room = 1 if "انباری" in extra_details else 0

                total_price = request.xpath('//*[@id="app"]/div[2]/div/main/article/div/div[1]/section[1]').xpath(
                    '//p[contains(text(), "قیمت کل")]/../../div[@class="kt-base-row__end kt-unexpandable-row__value-box"]/p/text()').get()
                floor_number = request.xpath('//*[@id="app"]/div[2]/div/main/article/div/div[1]/section[1]').xpath(
                    '//p[contains(text(), "طبقه")]/../../div[@class="kt-base-row__end kt-unexpandable-row__value-box"]/p/text()').get()
                neighborhood = request.xpath('//div[contains(text(), "پیش در")]/text()').get()

                print("*"*100, flush=True)
                print(url)
                yield {
                    "area": int(area) if area else 0,
                    "construction_date": self.extract_construction_date(construction_date) if construction_date else 0,
                    "number_of_rooms": self.extract_room_number(number_of_rooms) if number_of_rooms else 0,
                    "elevator": elevator,
                    "parking": parking,
                    "storage_room": storage_room,
                    "floor_number": self.extract_floor_number(floor_number),
                    "total_price": total_price,
                    "neighborhood": neighborhood}
            # except:
                # print("///"*50)