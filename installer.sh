#!/bin/bash
VERSION="2.28"
apt-get update -q
apt-get install -qy curl python python-pip python-dev build-essential ngnix
pip install --upgrade pip
pip install --upgrade virtualenv 
pip install lxml
pip install html5lib
pip install beautifulsoup4
locale-gen zh_CN.UTF-8
cd /usr/local/src
echo "/vagrant/util-linux-$VERSION.tar.gz"
if [ -e "/vagrant/util-linux-2.28.tar.gz" ];
then
	tar -zxf /vagrant/util-linux-2.28.tar.gz
	ln -s util-linux-2.28 util-linux
	cd util-linux
	./configure --without-ncurses
	make LDFLAGS=-all-static nsenter
	cp nsenter /usr/local/bin
else
	ls -l /vagrant
fi

cp /vagrant/docker-enter /usr/local/bin
chmod a+x /usr/local/bin/docker-enter