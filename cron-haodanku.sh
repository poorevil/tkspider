#! /bin/sh
export PATH=$PATH:/usr/local/bin

cd /usr/local/src/tkspider
nohup scrapy crawl haodanku > /usr/local/src/tkspider/haodanku.log &