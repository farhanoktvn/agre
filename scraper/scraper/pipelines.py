import json
import os
import pymongo

from itemadapter import ItemAdapter


def get_time_str(ctime):
    time_str = "{:02d}-{:02d}-{:02d}-{:02d}-{:02d}".format(
        ctime[0], ctime[1], ctime[2], ctime[3], ctime[4]
    )
    return time_str


class JsonWriterPipeline:

    def __init__(self, name, crawl_time):
        self.name = name
        self.crawl_time = crawl_time
        self.crawl_time_str = get_time_str(self.crawl_time)

    @classmethod
    def from_crawler(cls, crawler):
        spider = crawler.spider
        return cls(name=spider.name, crawl_time=spider.crawl_time)

    def open_spider(self, spider):
        base_name = 'scraper/json_out/{}/'.format(self.name)
        json_path = base_name + self.crawl_time_str + '.json'
        self.file = open(json_path, 'a')
        self.file.write('[\n')

    def close_spider(self, spider):
        self.file.write(']\n')
        self.file.close()

    def process_item(self, item, spider):
        post = ItemAdapter(item).asdict()
        post['crawl_time'] = self.crawl_time_str
        line = json.dumps(post, indent=4) + ",\n"
        self.file.write(line)
        return item


class MongoPipeline:

    def __init__(self, crawl_time, site):
        self.mongo_uri = os.environ.get('MONGO_URI')
        self.mongo_db = os.environ.get('MONGO_DB')
        self.crawl_time = crawl_time
        self.site = site

    @classmethod
    def from_crawler(cls, crawler):
        spider = crawler.spider
        return cls(crawl_time=spider.crawl_time, site=spider.name)

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db['site'].drop()

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        post = ItemAdapter(item).asdict()
        post['crawl_time'] = self.crawl_time
        if self.db[self.site].find({'link': post['link']}).count() > 0:
            pass
        else:
            self.db[self.site].insert_one(post)
        return item
