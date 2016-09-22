FROM  ubuntu:14.04
MAINTAINER "richard" <richard_xieq@hotmail.com>

ENV VERSION 2.28
RUN apt-get update -q && \
	apt-get install -qy python python-dev python-pip \
	curl build-essential python-lxml tesseract-ocr tesseract-ocr-dev python-opencv && \
	apt-get clean && \
	apt-get autoclean && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN locale-gen zh_CN.UTF-8

RUN pip install html5lib && \
	pip install lxml && \
	pip install BeautifulSoup && \
	pip install numpy && \
	pip install tesserpy && \
	mkdir -p /usr/src/app/python/cookies && \
	mkdir -p /usr/src/app/python/images

WORKDIR /usr/src/app/python
ADD src.tar.gz .
ADD pyv8.tar.gz .
EXPOSE 80
#CMD ["bash"]
ENTRYPOINT [ "python", "app.py" ]