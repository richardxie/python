FROM  ubuntu:14.04
MAINTAINER "richard" <richard_xieq@hotmail.com>

ENV VERSION 2.28
RUN apt-get update -q && \
	apt-get install -qy python python-dev python-pip \
	curl build-essential python-lxml && \
	apt-get clean && \
	apt-get autoclean && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install html5lib && \
	pip install BeautifulSoup && \
	mkdir -p /usr/src/app/python/cookies

WORKDIR /usr/src/app/python
ADD yt_buy.py .
ADD cookies/richardxieqCookie.txt  ./cookies
ADD pyv8.tar.gz .
EXPOSE 80
#CMD ["bash"]
ENTRYPOINT [ "python", "yt_buy.py" ]