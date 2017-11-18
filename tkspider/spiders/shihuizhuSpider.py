#-*- coding:UTF-8 -*-
#!/usr/bin/env python

from __future__ import absolute_import

import sys    
reload(sys)
sys.setdefaultencoding('UTF-8')  

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http.request import Request  
import re
import json

from tkspider.items import Item

import time,urllib2
import urlparse

import socket
socket.setdefaulttimeout(60*5)

u'''
shihuizhu
http://www.shihuizhu.com/search/?page=2


'''

#每次请求5页
max_page_amount = 3


class ShihuizhuSpider (Spider):
	name = "shihuizhu"
	allowed_domains = ["www.shihuizhu.com"]

	start_url_maps = []
	
	def __init__(self, page_amount=None,*args, **kwargs):
		super(ShihuizhuSpider, self).__init__(*args, **kwargs)

		if page_amount is not None :
			max_page_amount = page_amount
		
	def start_requests(self):  
		
		for idx in xrange(1,max_page_amount):
			item_list_interface_url = 'http://www.shihuizhu.com/search/?page=%d'%idx

			request = Request(item_list_interface_url) 
			print '----------------------'+request.url
			yield request
			

	def parse(self, response):  
		
		try:
			# print response.body
			hxs = Selector(response)
			goods_container_nodes = hxs.xpath('//div[@class="col list-item"]')
			# print goods_container_nodes

			for goods_node in goods_container_nodes:
				item = Item()

				item['item_id'] = goods_node.xpath('./@data-info').extract()[0]
				
				#寻找优惠券url
				intro_contents = goods_node.xpath('.//div[@class="intro"]/text()').extract()
				# print json.dumps(intro_contents, indent=4)

				coupon_url = None
				if intro_contents is not None and len(intro_contents) > 0:
					pattarn = re.compile(r'.*?((https|http)://shop\.m\.taobao\.com/shop/coupon\.htm\?[a-zA-Z=&0-9]+).*')
					for content in intro_contents:
						result = re.findall(pattarn, content)
						#[(u'https://shop.m.taobao.com/shop/coupon.htm?sellerId=3010348893&activityId=6aeb6abfb2e04be39367d4f19d6db323', u'https')]
						if result is not None and len(result) > 0:
							coupon_url = result[0][0]

					desc = intro_contents[len(intro_contents)-1]
					if desc is not None:
						item['desc'] = u'%s'%desc
						# print item['desc']
				
				try:
					if coupon_url is not None:
						query = urlparse.parse_qs(urlparse.urlparse(coupon_url).query,True)
						
						if 'activity_id' in query:
							activity_id = query['activity_id'][0]
						elif 'activityId' in query:
							activity_id = query['activityId'][0]

						if 'seller_id' in query:
							seller_id = query['seller_id'][0]
						elif 'sellerId' in query:
							seller_id = query['sellerId'][0]

						item['coupon_activity_id'] = activity_id						#优惠券id
						item['coupon_seller_id'] = seller_id 							#卖家id
				except Exception as e:
					print e
				
				yield item

		except Exception, what :
			print "-----------",what
			



	


