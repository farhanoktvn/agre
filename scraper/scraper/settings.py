BOT_NAME = 'scraper'
ROBOTSTXT_OBEY = True
ITEM_PIPELINES = {
    'scraper.pipelines.JsonWriterPipeline': 300
}
