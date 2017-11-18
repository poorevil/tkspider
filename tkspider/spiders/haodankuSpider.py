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
# import json

from tkspider.items import Item

import time,urllib2
import urlparse

import socket
socket.setdefaulttimeout(60*5)

u'''
haodanku
http://www.haodanku.com/index/index/p/1.html


'''

#每次请求5页
max_page_amount = 3


class HaodankuSpider (Spider):
	name = "haodanku"
	allowed_domains = ["www.haodanku.com"]

	start_url_maps = []
	
	def __init__(self, page_amount=None,*args, **kwargs):
		super(HaodankuSpider, self).__init__(*args, **kwargs)

		if page_amount is not None :
			max_page_amount = page_amount
		
	def start_requests(self):  
		
		for idx in xrange(1,max_page_amount):
			item_list_interface_url = 'http://www.haodanku.com/index/index/p/%d.html'%idx

			request = Request(item_list_interface_url) 
			print '----------------------'+request.url
			yield request
			

	def parse(self, response):  
		
		try:
			# print response.body
			hxs = Selector(response)
			# goods_container_nodes = hxs.xpath('//div[@class="am-hide itemsdata"]')
			goods_container_nodes = hxs.xpath('//div[@class="public-commodity-size default-style library-list"]')
			# print goods_container_nodes

			for goods_node in goods_container_nodes:
				item = Item()

				item_url = goods_node.xpath('./div[@class="public-option"]/a/@href').extract()[0]
				print item_url
				# https://item.taobao.com/item.htm?id=537180158515
				# https://detail.tmall.com/item.htm?id=559026008988
				query = urlparse.parse_qs(urlparse.urlparse(item_url).query,True)
				item['item_id'] = query['id'][0]

				# item['item_id'] = goods_node.xpath('./@data-itemid').extract()[0]
				
				# item['title'] = goods_node.xpath('./@data-itemtitle').extract()[0]
				item['title'] = goods_node.xpath('./div[@class="commodity_name am-text-sm am-padding-bottom-sm"]/a[1]/span/text()').extract()[0]
				# item['desc'] = goods_node.xpath('./@data-itemdesc').extract()[0]

				# coupon_url = goods_node.xpath('./@data-couponurl').extract()[0]
				# http://shop.m.taobao.com/shop/coupon.htm?sellerId=2086961343&activityId=3a499ad0fcb14a478b08430075950543
				coupon_url = goods_node.xpath('./div[@class="commodity_name am-text-sm am-padding-bottom-sm"]/a[2]/@href').extract()[0]
				print coupon_url, item['item_id']
				
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
			



	


