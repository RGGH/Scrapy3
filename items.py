# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field, Item
from scrapy.loader.processors import MapCompose, Compose, TakeFirst, Join
import re

def remove_nt(value):
    return value.replace("\n",' ').replace(" ","")

def filter_num(value):
    if value.isalnum():
        return value[0]
    else:
    	return "8"

def remove_text(value):
    return re.sub("[^0-9]", "", value)
    
class PxItem(scrapy.Item):

    href = scrapy.Field()
    
    price = scrapy.Field(
        input_processor = MapCompose(str.strip, remove_nt),
        output_processor = TakeFirst()
    )
    
    location = scrapy.Field()
    title = scrapy.Field()
    ptype = scrapy.Field()
    
    bedrooms = scrapy.Field(    	
    	default=0,
        input_processor=MapCompose(str.strip,filter_num),
        output_processor=TakeFirst())
    
    bathrooms = scrapy.Field(        
    	default=0,
        input_processor=MapCompose(remove_nt,filter_num),
        output_processor=TakeFirst())

    floor_area = scrapy.Field(
    	default=0,
        input_processor=MapCompose(str.strip,remove_text),
        output_processor=TakeFirst())
    
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    listing_url = scrapy.Field()
