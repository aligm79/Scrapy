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

    def parse(self, response):
        hrefs = response.xpath('//*[@id="post-list-container-id"]/div[1]/div/div//a/@href').getall()

        for href in hrefs:
            # try:
                url = urljoin(response.url, href)
                request = requests.get(url)
                request = Selector(text=request.text)
                time.sleep(random.randint(10,15))
                
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
                print(extra_details)
                print(area, elevator, parking, storage_room, total_price, floor_number, neighborhood)
                print(url)
                yield {
                    "area": int(area) if area else 0,
                    "construction_date": int(construction_date) if construction_date else 0,
                    "number_of_rooms": int(number_of_rooms) if number_of_rooms else 0,
                    "elevator": elevator,
                    "parking": parking,
                    "storage_room": storage_room,
                    "floor_number": int(floor_number[0]) if floor_number else 0,
                    "total_price": total_price,
                    "neighborhood": neighborhood}
            # except:
                # print("///"*50)