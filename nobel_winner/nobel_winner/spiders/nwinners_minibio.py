# -*- coding: utf-8 -*-
import scrapy


class NwinnersMinibioSpider(scrapy.Spider):
    name = 'nwinners_minibio'
    allowed_domains = ['https://ja.wikipedia.org/wiki/']
    start_urls = ['https://ja.wikipedia.org/wiki/%E5%9B%BD%E5%88%A5%E3%81%AE%E3%83%8E%E3%83%BC%E3%83%99%E3%83%AB%E8%B3%9E%E5%8F%97%E8%B3%9E%E8%80%85/']

    def parse(self, response):

        filename =

        pass
