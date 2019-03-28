# -*- coding: utf-8 -*-
import scrapy
from ..items import NobelWinnerItem


class NwinnerListSpiderSpider(scrapy.Spider):
    name = 'nwinner_list_spider'
    allowed_domains = ['https://ja.wikipedia.org/wiki/']
    start_urls = ['https://ja.wikipedia.org/wiki/%E5%9B%BD%E5%88%A5%E3%81%AE%E3%83%8E%E3%83%BC%E3%83%99%E3%83%AB%E8%B3%9E%E5%8F%97%E8%B3%9E%E8%80%85']

    def parse(self, response):
        h4s = response.xpath('//h4')
        for h4 in h4s:
            country = h4.xpath('span[@class="mw-headline"]/text()').extract()
            if country:
                winners = h4.xpath('following-sibling::ol[1]')
                for w in winners.xpath('li'):
                    text = w.xpath('descendant-or-self::text()').extract()
                    yield NobelWinnerItem(
                        country = country,
                        name = text[0],
                        link_text = ''.join(text)
                    )
        pass
