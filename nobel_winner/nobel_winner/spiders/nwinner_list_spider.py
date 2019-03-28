# -*- coding: utf-8 -*-
import scrapy
from ..items import NobelWinnerItem
import re
BASE_URL = 'https://ja.wikipedia.org/wiki/'

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

                    wdata = process_winner_li(w, country[0])
                    yield NobelWinnerItem(
                        country=wdata['country'],
                        name=wdata['name'],
                        text=wdata['text'],
                        year=wdata['year'],
                        category=wdata['category'],
                    )
        pass



def process_winner_li(w, country=None):
    """受賞者の<li>タグを処理する"""
    wdata = {}
    wdata['link'] = BASE_URL + w.xpath('a/@href').extract()[0]
    text = ''.join(w.xpath('descendant-or-self::text()').extract())
    wdata['name'] = text.split('、')[0].strip()

    year = re.findall('/d{4}', text) #4桁の文字列は年度である
    if year:
        wdata['year'] = int(year[0])
    else:
        wdata['year'] = 0
        print('no year')

    category = re.findall('文学賞|化学賞|物理学賞|生理学・医学賞|平和賞|経済学賞', text)
    if category:
        wdata['category'] = category[0]
    else:
        wdata['category'] = ''
        print('no category')

    if country:
        wdata['country'] = country
        wdata['born_in'] = ''

    wdata['text'] = text
    return wdata

