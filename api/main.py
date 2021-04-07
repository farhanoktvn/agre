import api.service as service

from fastapi import FastAPI

app = FastAPI()


@app.get('/', status_code=200)
def index():
    return {
        'message': 'Hello from Agre!'
    }


@app.get('/api/news', status_code=200)
def get_news_all():
    response = {}

    news = service.get_all()

    if news[0] == 1:
        response['message'] = 'Success'
        response['sites'] = news[1]
    else:
        response['message'] = 'Request failed'

    return response


@app.get('/api/news/{site_name}', status_code=200)
def get_news_on(site_name: str):
    response = {}

    news = service.get_on(site_name)

    if news[0] == 1:
        response['message'] = 'Success'
        response['sites'] = news[1]
    else:
        response['message'] = 'Request failed'

    return response
