# -*- coding: utf-8 -*-
import scrapy
from ..items import NWinnerItemBio

BASE_URL = 'https://ja.wikipedia.org'

class NwinnersMinibioSpider(scrapy.Spider):
    name = 'nwinners_minibio'
    allowed_domains = []
    start_urls = ['https://ja.wikipedia.org/wiki/%E5%9B%BD%E5%88%A5%E3%81%AE%E3%83%8E%E3%83%BC%E3%83%99%E3%83%AB%E8%B3%9E%E5%8F%97%E8%B3%9E%E8%80%85']


    custom_settings = {
        'ITEM_PIPELINES': {'nobel_winner.pipelines.NobelImagesPipeline': 1,
                           'nobel_winner.pipelines.MongoDBPipeline': 2},
        'MONGODB_SERVER': 'localhost',
        'MONGODB_PORT': 27017,
        'MONGODB_DB': 'nobel_prize',
        'MONGODB_COLLECTION': 'mini_bio'
    }
    def parse(self, response):

        filename = response.url.split('/')[-1]
        h4s = response.xpath('//h4')

        for h4 in h4s:
            country = h4.xpath('span[@class="mw-headline"]/text()').extract()
            if country:
                winners = h4.xpath('following-sibling::ol[1]')
                for w in winners.xpath('li'):
                    wdata = {}
                    wdata['link'] = BASE_URL + w.xpath('a/@href').extract()[0]
                    request = scrapy.Request(wdata['link'],
                                             callback=self.get_mini_bio,
                                             dont_filter=True)
                    request.meta['item'] = NWinnerItemBio(**wdata)
                    yield request


    def get_mini_bio(self, response):

        item = response.meta['item']
        item['image_urls'] = []
        img_src = response.xpath('//table[contains(@class, "infobox")]//img/@src')
        if img_src:
            item['image_urls'] = ['https:' + img_src[0].extract()]
        mini_bio = response.xpath('//*[@id="mw-content-text"]/div/div[@id="toc"]/preceding-sibling::p/descendant-or-self::text()').extract()

        item['mini_bio'] = ''.join(mini_bio)
        yield item

