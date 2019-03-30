# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class DropNonPersons(object):
    """個人でない受賞者を除外する"""

    def process_item(self, item, spider):
        if not item['gender']:
            raise DropItem("No gender for %s" % item['name'])  # 団体は性別がない除外される
        return item


class NobelImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):

        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if image_paths:
            item['bio_image'] = image_paths[0]

        return item
