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
taokezhushou
http://www.taokezhushou.com/?page=1


'''

#每次请求5页
max_page_amount = 3


class TaokezhushouSpider (Spider):
	name = "taokezhushou"
	allowed_domains = ["www.taokezhushou.com"]

	start_url_maps = []
	
	def __init__(self, page_amount=None,*args, **kwargs):
		super(TaokezhushouSpider, self).__init__(*args, **kwargs)

		if page_amount is not None :
			max_page_amount = page_amount
		
	def start_requests(self):  
		
		for idx in xrange(1,max_page_amount):
			item_list_interface_url = 'http://www.taokezhushou.com/?page=%d'%idx

			request = Request(item_list_interface_url) 
			print '----------------------'+request.url
			yield request
			

	def parse(self, response):  
		
		try:
			# print response.body
			hxs = Selector(response)
			goods_container_nodes = hxs.xpath('//div[@class="goods-a"]')
			# print goods_container_nodes

			for goods_node in goods_container_nodes:
				item = Item()

				detail_url = goods_node.xpath('./a/@href').extract()[0]

				if detail_url is not None and len(detail_url) > 0:
					try:
						response = urllib2.urlopen('http://www.taokezhushou.com%s'%detail_url)  
						coupon_str = response.read() 

						if coupon_str is not None and len(coupon_str) > 0:
							detail_hxs = Selector(text=coupon_str)
							# 淘宝商品详情
							taobao_detail_url = detail_hxs.xpath('//div[@class="goods-img fl"]/a/@href').extract()[0]
							try:
								if taobao_detail_url is not None:
									query = urlparse.parse_qs(urlparse.urlparse(taobao_detail_url).query,True)
									
									if 'id' in query:
										item['item_id'] = query['id'][0]

							except Exception as e:
								print e
							
							if item['item_id'] is None:
								continue

							coupon_url_container = detail_hxs.xpath('//div[@class="intro4-left fl"]')

							activity_id = None
							seller_id = None

							if coupon_url_container is not None:
								coupon_url_href_array = coupon_url_container.xpath('.//a/@href').extract()
								
								if coupon_url_href_array is not None:
									for coupon_url in coupon_url_href_array:
										try:
											if coupon_url is not None:
												# print coupon_url

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

											if item['coupon_activity_id'] is not None and item['coupon_seller_id'] is not None:
												break

										except Exception as e:
											print e
					except Exception as e:
						pass
				
				yield item

		except Exception, what :
			print "-----------",what



