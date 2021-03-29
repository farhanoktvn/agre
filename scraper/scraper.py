import configparser

import site_spider
from scrapy.crawler import CrawlerProcess

config = configparser.ConfigParser()
config.read('scraper/spider.cfg')
process = CrawlerProcess(settings={
    "FEEDS": {
        "scraper/items.json": {"format": "json"},
    },
})

for site in config.sections():
    site_conf = config[site]
    process.crawl(
        site_spider.SiteSpider,
        name=site_conf['name'],
        start_url=site_conf['start_url'],
        allowed_domain=site_conf['allowed_domain'],
        post_xpath=site_conf['post_xpath'],
        title_xpath=site_conf['title_xpath'],
        link_xpath=site_conf['link_xpath']
    )

process.start()
