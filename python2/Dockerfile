FROM  ubuntu:14.04
MAINTAINER "richard" <richard_xieq@hotmail.com>

ENV VERSION 2.28
RUN apt-get update -q && \
	apt-get install -qy --no-install-recommends python3 python3-dev python3-pip \
	curl build-essential python-lxml tesseract-ocr \
	tesseract-ocr-dev python-opencv nginx supervisor sqlite3 ntpdate && \
	apt-get clean && \
	apt-get autoclean && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN locale-gen zh_CN.UTF-8 && \
	mv /etc/nginx/sites-available/default  /etc/nginx/sites-available/default.orginal && \
	echo "daemon off;" >> /etc/nginx/nginx.conf

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN pip install html5lib && \
	pip install lxml && \
	pip install BeautifulSoup && \
	pip install numpy && \
	pip install tesserpy && \
	pip install pyyaml && \
	pip install pymysql && \
	pip install Flask && \
	pip install uwsgi && \
	pip install SQLAlchemy && \
	pip install supervisor-stdout && \
	pip install python-crontab && \
	pip install redis && \
	pip install marshmallow


WORKDIR /usr/src/app/python

COPY default /etc/nginx/sites-available/
COPY supervisor.conf /etc/supervisor/conf.d/
COPY webapp /usr/share/nginx/html

EXPOSE 8082
CMD ["/usr/sbin/ntpdate","192.16.150.211"]
CMD ["nginx ", '-g', 'daemon off;']
#CMD ["supervisord", "-n"]
#ENTRYPOINT [ "bash" ]