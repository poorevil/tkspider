# -*- coding: utf-8 -*-
#!/usr/bin/env python
u'''
Created on 2015年3月25日
获取优惠券详情
@author: evil
'''

import urllib2, json, re

from scrapy.selector import Selector

import socket
socket.setdefaulttimeout(40)


class FetchShopCouponDetail(object):
	'''
	根据num_iid获取淘宝详细信息
	'''
	def __init__(self, activity_id=None, seller_id=None):
		self.activity_id = activity_id
		self.seller_id = seller_id

	def fetchDetail(self):
		itemTobeSave = None					#获取结果

		# try:
		#https://shop.m.taobao.com/shop/coupon.htm?seller_id=2267803127&activity_id=a9304782a9c548faa89949fffddc115f
		headers = {}
		headers['accept-encoding'] = 'deflate, br'
		headers['accept-language'] = 'zh-CN,zh;q=0.8,en;q=0.6'
		headers['pragma'] = 'no-cache'
		headers['user-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
		headers['accept'] = 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
		headers['cache-control'] = 'no-cache'

		#openssl s_client -connect hws.m.taobao.com:443
		req = urllib2.Request('http://shop.m.taobao.com/shop/coupon.htm?seller_id=%s&activity_id=%s'%(self.seller_id, self.activity_id))
		for k, v in headers.iteritems():
			req.add_header(k, v)

		response = urllib2.urlopen(req,timeout=40)
		coupon_str = response.read() 

		hxs = Selector(text=coupon_str)

		coupon_info_div = hxs.xpath('//div[@class="coupon-info"]')
		if coupon_info_div is not None and len(coupon_info_div) > 0:
			# print coupon_info_div

			itemTobeSave = {}

			itemTobeSave['coupon_title'] = coupon_info_div.xpath('//dl/dt/text()').extract()[0].strip()		#标题
			
			#价格
			if itemTobeSave['coupon_title'] is not None:
				result = re.compile(u'([\d]+)元优惠券').findall(itemTobeSave['coupon_title'])
				if result is not None and len(result) > 0:
					itemTobeSave['coupon_price'] = result[0]


			rest = hxs.xpath('//span[@class="rest"]/text()').extract()[0].strip()			#剩余
			count = hxs.xpath('//span[@class="count"]/text()').extract()[0].strip()			#已领取

			itemTobeSave['coupon_total_amount'] = int(rest)+int(count)						#优惠券总数
			itemTobeSave['coupon_received_amount'] = int(count)								#优惠券已领数量

			dd_ele_array = coupon_info_div.xpath('//dl/dd/text()').extract()
			itemTobeSave['coupon_desc'] = dd_ele_array[len(dd_ele_array)-2].strip()			#描述 单笔满69元可用，每人限领1 张

			#限领数量
			if itemTobeSave['coupon_desc'] is not None:
				result = re.compile(u'每人限领(\d+) 张').findall(itemTobeSave['coupon_desc'])
				if result is not None and len(result) > 0:
					itemTobeSave['coupon_limit'] = result[0]

			during = dd_ele_array[len(dd_ele_array)-1].strip()			#有效期:2017-02-20至2017-02-28
			if during is not None:
				result = re.compile(u'([\d]{4}-[\d]{2}-[\d]{2})至([\d]{4}-[\d]{2}-[\d]{2})').findall(during)
				if result is not None and len(result) > 0:
					itemTobeSave['coupon_begin_time'] = result[0][0]					#优惠券开始时间
					itemTobeSave['coupon_end_time'] = result[0][1]						#优惠券结束时间


		else:
			#找不到，可能是过期了
			pass



		# except Exception as e:
		# 	print e

		return itemTobeSave

if __name__ == '__main__' :
	#seller_id=2107594711&activity_id=2cb1dc713bfa429c91f54bf68e918c15
	# 无效的 seller_id=1673502867 activity_id=80219fb27a064eb6b120640b632c3a22
	mFetchItemDetail = FetchShopCouponDetail('80219fb27a064eb6b120640b632c3a22', '1673502867')
	print json.dumps(mFetchItemDetail.fetchDetail())


