# -*- coding: utf-8 -*-
import scrapy


class InstrumentsSpider(scrapy.Spider):
    name = 'instruments'
    # allowed_domains = ['musicianfriends.com']

    def start_requests(self):
        homepage = 'https://www.musiciansfriend.com/'
        yield scrapy.Request(homepage, callback=self.parse_homepage)

    # Parse the home page to get the sub categories
    def parse_homepage(self, response):
        for category_url in response.css('div.dropdownDeptLinks a::attr(href)').extract():
            yield scrapy.Request('https://www.musiciansfriend.com/{}'.format(category_url), callback=self.parse_category)

    # Through the category page, we can get the items in the page, as well as the next page
    def parse_category(self, response):
        for item_url in response.css('div.productGrid a::attr(href)').extract():
            yield scrapy.Request('https://www.musiciansfriend.com/{}'.format(item_url),
                                 callback=self.parse_item)


        # Since Scrapy will send request to a link only once, so we can get the related pages without worrying about duplicate
        for page in response.css('a.page-link::attr(href)').extract():
            yield scrapy.Request('https://www.musiciansfriend.com/{}'.format(page),
                                 callback=self.parse_category)

    # Parse Items
    def parse_item(self, response):
        price_item = response.css('span.productPrice::text').extract()
        price = float(''.join(price_item).strip().replace(',',''))
        # price = float( ''.joinresponse.css('span.productPrice::text').extract_first().replace(',',''))
        name = response.css('title::text').extract_first().split('|')[0].strip() # The title contains the page and | ...
        description = ''.join(response.css('div.details *::text').extract()).replace('\n', '')
        # We can also get more info here if needed. If we need to store this to a Database, we can build an item in items.py.
        yield {
            'price': price,
            'name': name,
            'description': description,
        }