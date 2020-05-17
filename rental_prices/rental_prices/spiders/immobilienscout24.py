# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import FormRequest, Request


class Immobilienscout24Spider(scrapy.Spider):
    name = 'immobilienscout24'
    allowed_domains = ['immobilienscout24.de']
    start_urls = [
        'https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-mieten']
    custom_settings = {
        'ITEM_PIPELINES': {
            'rental_prices.pipelines.DuplicatesPipeline': 150,
            'rental_prices.pipelines.SQLLitePipeline': 300
        },
        'ROBOTSTXT_OBEY': 'False',
        # 'DOWNLOAD_DELAY': 3,
        # 'FEED_FORMAT': 'csv',
        # 'FEED_URI': 'test.csv',
    }

    def parse(self, response):
        base_url = 'https://www.immobilienscout24.de'
        listings = response.xpath('//li[@class="result-list__listing "]')
        for listing in listings:
            url = listing.xpath('.//a/@href').extract_first()
            url = base_url + url
            yield scrapy.Request(url=url, callback=self.parse_ad)

        next_page = response.xpath(
            '//div[@class="grid-item align-right"]//@href').extract_first()

        if next_page is not None:
            next_page = base_url + next_page
            yield response.follow(next_page, callback=self.parse)

    def parse_ad(self, response):
        url_dict = {'Url': response.url}

        general_infos = response.xpath(
            '//div[@class="criteriagroup "]')[0].xpath('.//text()').extract()

        general_infos = [info.strip() for info in general_infos]
        general_infos = [info for info in general_infos if info not in [
            '']]
        general_infos_dict = {'Titel': general_infos[0]}

        pricings = response.xpath(
            '//div[@class="criteriagroup "]')[1].xpath('.//text()').extract()
        pricings = [pricing.strip().replace('\xad', '')
                    for pricing in pricings]
        pricings = [pricing for pricing in pricings if pricing not in [
            '', 'Umzugskosten', 'Berechnung starten', 'Mieten ohne Kaution', '+', 'Mit lokalem Mietspiegel vergleichen', 'Kaution später zahlen']]
        pricings_dict = dict(zip(pricings[:: 2], pricings[1:: 2]))

        details = response.xpath(
            '//div[@class="criteriagroup criteria-group--two-columns"]//text()').extract()
        details = [detail.strip() for detail in details]
        details = [detail for detail in details if detail not in [
            '', 'Bonitätsauskunft', 'erforderlich', 'SCHUFA-BonitätsCheck anfordern']]
        details_dict = dict(zip(details[::2], details[1::2]))

        features = response.xpath(
            '//div[@class="criteriagroup boolean-listing padding-top-l"]//text()').extract()
        features = [feature for feature in features if feature != ' ']
        features_dict = {feature: True for feature in features}

        energy_infos = response.xpath(
            '//div[@class="criteriagroup criteria-group--border criteria-group--two-columns criteria-group--spacing"]//text()').extract()
        energy_infos = [info.strip().replace('\xad', '')
                        for info in energy_infos if info != ' ']
        energy_infos = [info for info in energy_infos if info not in [
            'Energieverbrauch für Warmwasser enthalten']]
        energy_infos_dict = dict(zip(energy_infos[:: 2], energy_infos[1:: 2]))

        address = response.xpath(
            '//div[@class="address-block"]')[0].xpath('.//text()').extract()

        address = ' '.join([e.strip() for e in address if e != ' '])
        address_dict = {
            'Adreese': address}

        ad_publisher_infos = response.xpath(
            '//div[@class="grid-item desk-one-third lap-one-half palm-one-whole padding-vertical"]//text()').extract()
        ad_publisher_infos = [info.strip()
                              for info in ad_publisher_infos if info != ' ']
        ad_publisher_infos = ' '.join(ad_publisher_infos)
        ad_publisher_infos_dict = {'Anbieter': ad_publisher_infos}

        timestamp_dict = {'Timestamp': pd.Timestamp.now()}

        final_dict = {**general_infos_dict, **url_dict, **pricings_dict, **details_dict,
                      **features_dict, **energy_infos_dict, **ad_publisher_infos_dict, **address_dict, **timestamp_dict}

        # print(final_dict)
        print(final_dict.keys())
        print(final_dict)

        yield final_dict


# scrapy crawl immobilienscout24 -s JOBDIR=crawls/immobilienscout24
