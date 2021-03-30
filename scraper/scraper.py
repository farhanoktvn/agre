import configparser
from scraper.spiders import site_spider

from twisted.internet import reactor, defer
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

spider_conf = configparser.ConfigParser()
spider_conf.read('scraper/spider.cfg')

settings = get_project_settings()
settings.update({
    'BOT_NAME': 'agrescraper',
    'ROBOTSTXT_OBEY': True,
    'ITEM_PIPELINES': {
        'scraper.pipelines.JsonWriterPipeline': 100
    }
})
runner = CrawlerRunner(settings)


@defer.inlineCallbacks
def crawl():
    for site in spider_conf.sections():
        site_conf = spider_conf[site]
        yield runner.crawl(
            site_spider.SiteSpider,
            name=site_conf['name'],
            start_url=site_conf['start_url'],
            allowed_domain=site_conf['allowed_domain'],
            post_xpath=site_conf['post_xpath'],
            title_xpath=site_conf['title_xpath'],
            link_xpath=site_conf['link_xpath']
        )
        # yield spider_obj
    reactor.stop()

if __name__ == '__main__':
    crawl()
    reactor.run()
