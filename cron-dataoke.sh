#! /bin/sh
export PATH=$PATH:/usr/local/bin

cd /usr/local/src/tkspider
nohup scrapy crawl dataoke > /usr/local/src/tkspider/dataoke.log &