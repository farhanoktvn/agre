import os
import time
import pymongo

mongo_client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
mongo_db = mongo_client[os.environ.get('MONGO_DB')]

docs = ['antr', 'dtik', 'kmps', 'okzn', 'suar', 'trbn']


def get_all():
    news = {}
    try:
        for doc in docs:
            latest_news = list(mongo_db[doc].find().limit(10))
            for ln in latest_news:
                # Remove id from dictionary
                ln.pop('_id')

                # Change time to ISO-8601
                crawl_time = time.struct_time(ln['crawl_time'])
                ln['crawl_time'] = time.strftime(
                    '%Y-%m-%dT%H:%M:%S%z', crawl_time
                )
            news[doc] = latest_news
    except Exception as e:
        print(e)
        return (0, {})
    return (1, news)


def get_on(site_name):
    news = {}
    try:
        latest_news = list(mongo_db[site_name].find().limit(10))
        for ln in latest_news:
            # Remove id from dictionary
            ln.pop('_id')

            # Change time to ISO-8601
            crawl_time = time.struct_time(ln['crawl_time'])
            ln['crawl_time'] = time.strftime('%Y-%m-%dT%H:%M:%S%z', crawl_time)
        news[site_name] = latest_news
    except Exception as e:
        print(e)
        return (0, {})
    return (1, news)
