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
judazhe
http://www.judazhe.com/index.php?page=1


'''

#每次请求5页
max_page_amount = 3


class JudazheSpider (Spider):
	name = "judazhe"
	allowed_domains = ["www.judazhe.com"]

	start_url_maps = []
	
	def __init__(self, page_amount=None,*args, **kwargs):
		super(JudazheSpider, self).__init__(*args, **kwargs)

		if page_amount is not None :
			max_page_amount = page_amount
		
	def start_requests(self):  
		
		for idx in xrange(1,max_page_amount):
			item_list_interface_url = 'http://www.judazhe.com/index.php?page=%d'%idx

			request = Request(item_list_interface_url) 
			print '----------------------'+request.url
			yield request
			

	def parse(self, response):  
		
		try:
			# print response.body
			hxs = Selector(response)
			# <a data-url="http://shop.m.taobao.com/shop/coupon.htm?activity_id=ec2eb60a7ca6487abb956023651e5c73&sellerId=354994457" 
			# title="三味纺车 老粗布圆柱颈椎枕头颈椎糖果枕颈椎枕修复保健护颈枕荞麦皮枕包邮" 
			# class="" target="_blank" 
			# href="http://uland.taobao.com/coupon/edetail?activityId=ec2eb60a7ca6487abb956023651e5c73&sellerId=354994457&itemId=542494138703&pid=mm_99317136_20310381_69314823&src=jdz_tkjd&dx=">
			goods_container_nodes = hxs.xpath('//div[@class="newyhq"]/a')
			# print goods_container_nodes

			for goods_node in goods_container_nodes:
				item = Item()

				href_pro = goods_node.xpath('./@href')
				if href_pro is not None and len(href_pro.extract()) > 0:
					url = href_pro.extract()[0]

					if url is not None and 'itemId=' in url:
						query = urlparse.parse_qs(urlparse.urlparse(url).query,True)
						item['item_id'] = query['itemId'][0]
					
						#寻找优惠券url
						data_url_pro = goods_node.xpath('./@data-url')
						if data_url_pro is not None and len(data_url_pro.extract()) > 0:
							coupon_url = data_url_pro.extract()[0]
							# print coupon_url
							
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
			



	


