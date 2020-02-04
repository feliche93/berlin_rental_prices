# -*- coding: utf-8 -*-
import scrapy


class ImmoScraperSpider(scrapy.Spider):
    name = 'immo_scraper'
    allowed_domains = ['immowelt.de']
    start_urls = ['http://immowelt.de/']

    def parse(self, response):
        pass
