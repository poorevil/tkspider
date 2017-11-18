# -*- coding: utf-8 -*-

# Scrapy settings for tkspider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'tkspider'

SPIDER_MODULES = ['tkspider.spiders']
NEWSPIDER_MODULE = 'tkspider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tkspider (+http://www.yourdomain.com)'


USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'

CONCURRENT_REQUESTS = 20
#CONCURRENT_REQUESTS_PER_DOMAIN = 2

DOWNLOAD_DELAY = 2

EXTENSIONS = {
    'tkspider.extensions.HandleResult': 300,
}

# LOG_LEVEL ＝ 'ERROR'