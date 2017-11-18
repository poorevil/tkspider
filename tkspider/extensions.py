# -*- coding: utf-8 -*-


from scrapy import signals
import scrapy
import json
from datetime import datetime
from datetime import date

import urllib  
import urllib2

import datetime
import md5
import time

from tkspider.fetchItemDetail import FetchItemDetail
from tkspider.fetchShopCouponDetail import FetchShopCouponDetail

import socket
socket.setdefaulttimeout(60*5)

#处理结果 扩展
class HandleResult(object):

	result_array = []		#结果集合array

	@classmethod
	def from_crawler(cls, crawler):
		# if not crawler.settings.getbool('MYEXT_ENABLED'):
		# 	raise NotConfigured

		# # get the number of items from settings

		# item_count = crawler.settings.getint('MYEXT_ITEMCOUNT', 1000)

		# instantiate the extension object

		ext = cls()

		# connect the extension object to signals
		crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
		crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
		crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

		return ext

	def spider_opened(self, spider):
		print '============HandleResult===========spider_opened==================================='+spider.name

	def item_scraped(self, item, spider):
		
		# {
		#  'coupon_activity_id': u'8c6b6d086ad043e29cadaeff83b3a133',
		#  'coupon_seller_id': u'2860270208',
		#  'item_id': u'529715420715'
		# }
		itemDict = {}
		itemDict.update(item)

		for x in xrange(1,4):					#超时重试
			try :
				item_taobao_detail = FetchItemDetail(item['item_id']).fetchDetail()
				# print item_taobao_detail
				if item_taobao_detail is not None:
					itemDict.update(item_taobao_detail)
					break
			except Exception, e:
				print str(e)

		for x in xrange(1,4):					#超时重试
			try :
				shop_coupon_detail = FetchShopCouponDetail(item['coupon_activity_id'], item['coupon_seller_id']).fetchDetail()
				# print shop_coupon_detail
				if shop_coupon_detail is not None:
					itemDict.update(shop_coupon_detail)

				break
			except Exception, e:
				print str(e)

		#如果爬取结果有title，则覆盖淘宝的title
		if 'title' in item and item['title'] is not None and len(item['title']) > 0:
			itemDict['title'] = item['title'].replace('\n', '')

		#如果爬取结果有小编评语，则覆盖小编评语
		if 'desc' in item and item['desc'] is not None and len(item['desc']) > 0:
			itemDict['desc'] = item['desc'].replace('\n', '')

		self.result_array.append(itemDict)
		print "-------item_scraped-------\n%s "%(item['item_id'])
		time.sleep(0.5)

	def spider_closed(self, spider):
		print '============HandleResult===========spider_closed==================================='+spider.name

		# print json.dumps(self.result_array, indent=4)

		for x in xrange(1,10):
			try:
				# api_response = self.postResult(json.dumps(self.result_array, cls=CJsonEncoder), spider)
				api_response = self.postResult(json.dumps(self.result_array), spider)
				print '=========postResult=============='+api_response
				break
			except Exception, e:
				print str(e)

			time.sleep(2)


	def postResult(self, jsonStr, spider=None):
		print jsonStr

		u'''
		提交获取到的商品信息至服务器
		'''
		req = urllib2.Request('http://www.server.address/api/%s'%spider.name)
		req.add_header('Content-Type', 'application/x-www-form-urlencoded')
		data = {"commitData":jsonStr}
		data = urllib.urlencode(data)
		response = urllib2.urlopen(req, data, timeout=40)
		return response.read()



class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        # if isinstance(obj, datetime):
        #     return obj.strftime('%Y-%m-%d %H:%M:%S')
        # elif isinstance(obj, date):
        #     return obj.strftime('%Y-%m-%d')
        # el

        if isinstance(obj, scrapy.item.Item):
            return dict(obj)
        else:
            return json.JSONEncoder.default(self, obj)
