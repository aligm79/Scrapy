import scrapy


class DivarItem(scrapy.Item):
    neighborhood = scrapy.Field()
    area = scrapy.Field()
    construction_date = scrapy.Field()
    floor_number = scrapy.Field()
    total_price = scrapy.Field()
    number_of_rooms = scrapy.Field()
    elevator = scrapy.Field()
    parking = scrapy.Field()
    storage_room = scrapy.Field()