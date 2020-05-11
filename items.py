# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field,Item
from scrapy.loader.processors import MapCompose, TakeFirst, Join

def remove_nt(value):
    return value.replace("\n",' ').replace(" ","")

class PxItem(scrapy.Item):

    href = scrapy.Field()
    price = scrapy.Field(
        input_processor = MapCompose(str.strip,remove_nt),
        output_processor = TakeFirst()
    )
    location = scrapy.Field()
    title = scrapy.Field()
    ptype = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    floor_area = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    listing_url = scrapy.Field()
