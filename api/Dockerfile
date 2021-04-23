FROM python:3.7.10-buster

LABEL MAINTAINER="Muhammad Oktavian farhanoktvn@gmail.com"

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/

ADD ./api /var/www/
ADD ./requirements.txt /var/www/requirements.txt
ADD ./.env /var/www/.env
RUN pip install -r requirements.txt

RUN addgroup -gid $GROUP_ID www
RUN adduser -u $USER_ID --group www --shell /bin/sh

USER www

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]