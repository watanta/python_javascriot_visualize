# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NobelWinnerItem(scrapy.Item):
    country = scrapy.Field()
    name = scrapy.Field()
    link_text = scrapy.Field()
    category = scrapy.Field()
    date_of_birth = scrapy.Field()
    date_of_death = scrapy.Field()
    gender = scrapy.Field()
    link = scrapy.Field()
    place_of_birth = scrapy.Field()
    place_of_death = scrapy.Field()
    text = scrapy.Field()
    year = scrapy.Field()

    pass
