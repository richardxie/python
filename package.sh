#!/bin/bash
if [ -e 'src.tar.gz' ]; then
	echo 'remove previous package'
	rm src.tar.gz
fi
echo 'packaging'
tar -cvzf src.tar.gz app.py task.py supervisor.conf logging-conf.yaml uwsgi-conf.yaml encrypt.js default webservice/ conf/ yatang/ utils/ test/ cookies/ tzj/ 
