# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItems



class DropNonPersons(object):
    """個人でない受賞者を除外する"""

    def process_item(self, item, spider):
        if not item['gender']:
            raise DropItems("No gender for %s" % item['name']) #団体は性別がない除外される
        return item
