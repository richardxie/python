#!/bin/bash
if [ -e 'src.tar.gz' ]; then
	echo 'remove previous package'
	rm src.tar.gz
fi
echo 'packaging'
tar -cvzf src.tar.gz app.py encrypt.js yatang/ utils/ test/ cookies/
