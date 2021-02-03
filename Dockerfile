FROM alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories \
    && apk add py3-pip supervisor npm make \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple Django==3.1 elasticsearch==7.9.1 requests==2.23.0 \
    && npm config set registry https://registry.npm.taobao.org \
    && mkdir /var/pl-log-notic

COPY . /var/pl-log-notic/

EXPOSE 80
