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

import time,urllib2,urllib
import urlparse

import socket
socket.setdefaulttimeout(60*5)

u'''
大淘客
http://www.dataoke.com/qlist/?page=1


'''

#每次请求5页
max_page_amount = 3


class DataokeSpider (Spider):
	name = "dataoke"
	allowed_domains = ["www.dataoke.com"]

	start_url_maps = []
	
	def __init__(self, page_amount=None,*args, **kwargs):
		super(DataokeSpider, self).__init__(*args, **kwargs)

		if page_amount is not None :
			max_page_amount = page_amount
		
	def start_requests(self):  
		
		for idx in xrange(1,max_page_amount):
			item_list_interface_url = 'http://www.dataoke.com/qlist/?page=%d'%idx

			request = Request(item_list_interface_url) 
			# print '----------------------'+request.url
			yield request
			

	def parse(self, response):  
		
		try:
			# print response.body
			hxs = Selector(response)
			goods_container_nodes = hxs.xpath('//div[@class="goods-list clearfix"]/div')
			# print goods_container_nodes
			for goods_node in goods_container_nodes:
				
				item = Item()

				item['item_id'] = goods_node.xpath('.//@data_goodsid').extract()[0]
				print item['item_id']
				# item['title'] = goods_node.xpath('.//span[@class="goods-tit"]/a/text()').extract()[0]
				item['title'] = goods_node.xpath('.//div/div[2]/span[@class="goods-tit"]/a/text()').extract()[0]
				if item['title'] is not None :
					item['title'] = item['title'].replace('\t', '').replace('\n','')

				print item['title']
				#获取店铺优惠券信息
				goods_id = goods_node.xpath('.//@id').extract()[0]
				goods_id = goods_id.replace('goods-items_','')
				# print goods_id
				coupon_url = None

				try:
					# response = urllib2.urlopen('http://www.dataoke.com/gettpl?gid=%s&_=%d'%(goods_id,time.time()*1000),timeout=40)  
					# response = urllib2.urlopen('http://www.dataoke.com/detailtpl?gid=%s'%(goods_id),timeout=40)  

					values = {'gid' : goods_id}
					headers = { 'User-Agent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36" } 
					data = urllib.urlencode(values)
					req = urllib2.Request('http://www.dataoke.com/gettpl?gid=%s'%goods_id, headers=headers)
					response = urllib2.urlopen(req) 
					coupon_str = response.read() 
					# print coupon_str
					
					if coupon_str is not None and len(coupon_str) > 0:
						coupon_url = Selector(text='<html><body>%s</body></html>'%coupon_str).xpath('//a/@href').extract()[0]
						# print coupon_url
						if coupon_str.rfind('</a></br>') > 0:
							item['desc'] = u'%s'%coupon_str[coupon_str.rfind('</a></br>')+9:]
							# print item['desc']

				except Exception as e:
					print e
					pass

				if coupon_url is not None:
					query = urlparse.parse_qs(urlparse.urlparse(coupon_url).query,True)
					activity_id = query['activity_id'][0]
					seller_id = query['seller_id'][0]

					item['coupon_activity_id'] = activity_id						#优惠券id
					item['coupon_seller_id'] = seller_id 							#卖家id

				yield item

		except Exception, what :
			print "-----------",what
			



	


