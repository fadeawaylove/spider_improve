FROM python:alpine3.6
# 安装python模块
RUN pip install --upgrade pip && \
    pip install requests && \
    pip install aiohttp && \
    pip install tornado && \
    pip install selenium && \
    pip install appium-python-client

# 安装gcc编译环境
RUN apk add --no-cache gcc musl-dev

# 安装需要gcc编译环境的python包
RUN pip install twisted && pip install gevent

# 安装scrapy
# ubuntu下依赖：libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
RUN apk add --no-cache libxml2-dev libxslt-dev zlib-dev libffi-dev openssl-dev &&\
    pip install scrapy

# 安装pyspider
# ubuntu下的依赖：libcurl4-openssl-dev libxml2-dev libxslt1-dev libssl-dev zlib1g-dev
RUN apk add --no-cache curl-dev openssl-dev libxml2-dev libxslt-dev zlib-dev &&\
    pip install pyspider

RUN pip install websocket-client

RUN pip install redis &&\
    pip install pymysql &&\
    pip install sqlalchemy &&\
    pip install six &&\
    pip install w3lib
RUN pip install simhash

RUN pip install u-msgpack-python

# 编译安装 confluent-kafka-python
RUN apk add --no-cache libc-dev pcre-dev zlib-dev jemalloc-dev &&\
    apk --update add git openssh && \
    apk --update --no-cache add bash &&\
    apk add --update --no-cache g++ &&\
    apk add --update --no-cache make &&\
    rm -rf /var/lib/apt/lists/* && \
    rm /var/cache/apk/*
RUN git clone https://github.com/edenhill/librdkafka.git &&\
    cd librdkafka &&\
    ./configure &&\
    make &&\
    make install &&\
    pip install confluent-kafka

#RUN pip install pika
RUN pip freeze

