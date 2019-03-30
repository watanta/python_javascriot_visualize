# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import pymongo
from scrapy.conf import settings


class DropNonPersons(object):
    """個人でない受賞者を除外する"""

    def process_item(self, item, spider):
        if not item['gender']:
            raise DropItem("No gender for %s" % item['name'])  # 団体は性別がない除外される
        return item

class MongoDBPipeline(object):

    def __init__(self, mongo_server, mongo_port, mongo_db, mongo_collection):
        connection = pymongo.MongoClient(
            mongo_server,
            mongo_port
        )
        db = connection[mongo_db]
        self.collection = db[mongo_collection]

    @classmethod  # 引数にクラスがあるので、クラス変数にアクセスできる
    def from_crawler(cls, crawler):
        return cls(
            mongo_server=crawler.settings.get('MONGODB_SERVER'), # settings.py て定義した変数にアクセスする
            mongo_port=crawler.settings.get('MONGODB_PORT'),
            mongo_db=crawler.settings.get('MONGODB_DB'),
            mongo_collection=crawler.settings.get('MONGODB_COLLECTION')
        ) # def __init__ の引数になる

    def process_item(self, item, spider):

        self.collection.insert(dict(item))
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
