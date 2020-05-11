import scrapy
from scrapy.loader import ItemLoader
from items import PxItem
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from urllib.parse import urljoin, urlencode
import json

class PropertyFinder(scrapy.Spider):

    # scraper name
    name = 'property'
    # custom settings
    custom_settings = {'FEED_FORMAT':'csv', 'FEED_URI':'propertyfound.csv'}
    
    #base_url = 'https://www.propertyfinder.bh/en/search?'
    
    headers = {
        'user-agent' : 
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36 '
    }

    def start_requests(self):
            # Starting url
            url = 'https://www.propertyfinder.bh/en/search?c=1&ob=mr&page=1'
            # crawl next page URL
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self,response):
        for card in response.xpath('//div[@class="card-list__item"]'):

            l = ItemLoader(item=PxItem(), selector=card, response=response)

            # Convert link to URL
            relative_url = card.xpath(".//a[@class='card card--clickable']/@href").get()
            domain = 'https://www.propertyfinder.bh'
            url = urljoin(domain, relative_url)

            # Attempt to extract geo coordinates
            try:
                script = json.loads(response.xpath('//script[@type="application/ld+json"]/text()').get())
            # loop over cards' JSON data
                for card in script[0]['itemListElement']:
                #print(card['url'])
                    if url == card['url']:
                        # "Add longitude and latitude 
                        l.add_value('longitude',card['mainEntity']['geo']['longitude'])
                        l.add_value('latitude',card['mainEntity']['geo']['latitude']))
            except Exception as e:
                print(e)
            
            l.add_xpath('href',".//a[@class='card card--clickable']/@href")
            l.add_xpath('price', ".//span[@class='card__price-value']/text()")
            l.add_xpath('location',".//p[@class='card__location']/text()")
            l.add_xpath('title',".//h2[@class='card__title card__title-link']/text()")
            l.add_xpath('ptype',".//p[@class='card__property-amenity card__property-amenity--property-type']/text()")
            l.add_xpath('bedrooms',".//p[@class='card__property-amenity card__property-amenity--bedrooms']/text()")
            l.add_xpath('bathrooms',".//p[@class='card__property-amenity card__property-amenity--bathrooms']/text()")
            l.add_xpath('floor_area',".//p[@class='card__property-amenity card__property-amenity--area']/text()")
            l.add_value('listing_url',url)
            yield l.load_item()
                            
        next_page = response.xpath("//a[@class='pagination__link pagination__link--next']/@href").get()

        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse)
                
# main driver
if __name__ == "__main__":
    # run scraper
    process = CrawlerProcess()
    process.crawl(PropertyFinder)
    process.start()
