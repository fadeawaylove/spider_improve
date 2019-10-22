# 注意：pip.conf文件为了解决，pip安装时可能出现的如certificate verify failed的错误

FROM python:3.6.5-stretch
COPY pip.conf /root/.config/pip/

RUN pip install ipython

RUN pip install requests &&\
    pip install aiohttp &&\
    pip install tornado &&\
    pip install gevent &&\
    pip install incremental &&\
    pip install twisted[tls] &&\
    pip install eventlet &&\
    pip install dnspython &&\
    pip install celery[redis]
