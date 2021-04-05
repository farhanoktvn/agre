import scrapy


class SiteSpider(scrapy.Spider):

    def __init__(self, category=None, *args, **kwargs):
        super(SiteSpider, self).__init__(*args, **kwargs)
        self.name = kwargs['name']
        self.start_urls = [kwargs['start_url']]
        self.allowed_domains = [kwargs['allowed_domain']]
        self.post_xpath = kwargs['post_xpath']
        self.title_xpath = kwargs['title_xpath']
        self.link_xpath = kwargs['link_xpath']
        self.crawl_time = kwargs['crawl_time']

    def parse(self, response):
        for post in response.xpath(self.post_xpath):
            yield {
                'title': post.xpath(self.title_xpath).get().strip(),
                'link': post.xpath(self.link_xpath).get(),
                'site': self.name
            }
