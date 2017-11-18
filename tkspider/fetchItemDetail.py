# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 2015年3月25日

@author: evil
'''

'''

curl 'https://detail.m.tmall.com/item.htm?id=527098750576' \
   -H 'accept-encoding: gzip, deflate, br' \
   -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8' \
   -H 'upgrade-insecure-requests: 1' \
   -H 'user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Mobile Safari/537.36' \
   -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' \
   -H 'authority: detail.m.tmall.com' \
   -H 'cookie: cna=oUSDEovSA3gCAXlFC/gfLwkF; ucn=unzbyun; uc3=sg2=WvcRxTd8eRK9swepX%2BIo2CC17H3JVNZU%2BLD6VQpOj5o%3D&nk2=r5MaXHXs&id2=UNGR7KLwbonKWw%3D%3D&vt3=F8dBzLOQ8kVpfKffuBk%3D&lg2=VT5L2FSpMGV7TQ%3D%3D; uss=VyyY5d413Y1czENXDiHMInvg7XpfF0sEjQ%2FsrvE0YWgdoMcEVszCQsp6tQ%3D%3D; t=8e4194dbaa3a3f7119f0014a8a7c83cd; tracknick=%5Cu5510%5Cu671D%5Cu83DC; lgc=%5Cu5510%5Cu671D%5Cu83DC; _tb_token_=ec7b45c119874; cookie2=1d562a38dc33f14e4b29963fcab5f597; _m_h5_tk=9103e77c37e4004f875f42c290652614_1510805618935; _m_h5_tk_enc=a6aa9b93b6d67ed6973daa690d87c06c; tkmb=e=3RK_w2w40nWN66h0wm-m15s3ceIC0tyUKVqHT2ved8Iy_GvxSzyNfi_IAR7ok-npC9ESIF8JDzfo2G2NesUrtxakgVc6i1DDIQEzO6yoPYS9GAJfbX073aUshHhzsr6M3dACyc-zO3YsQSI6e9P2_YolYnKKv5OXahOeZxDaYYbtLRitWNd0q1qv6VXvBkcMdVq0UU97bIgMYUrxpqsXDQ2Hj5AnhcrDPQQUCf0KvVV64auo6JaTWSKKbxKe-VTQD_PxggW57RS4x5YtRK7brm66Avkwm5Osbre-v5DaPTTDG_1N5hlzNg&iv=0&et=1510803378; isg=AhQUw4lqMsomr6X0vBHtcq0E5VRGxSfScz4ORa71oB8imbTj1n0I58ob66v-' --compressed
'''


import urllib2, json

import socket
socket.setdefaulttimeout(40)


class FetchItemDetail(object):
	'''
	根据num_iid获取淘宝详细信息
	'''
	def __init__(self, num_iid=None):
		self.num_iid = num_iid
		
	def fetchDetail(self):
		itemTobeSave = None					#获取结果

		if self.num_iid is not None:
			response = urllib2.urlopen('http://hws.m.taobao.com/cache/wdetail/5.0/?id=%s' % self.num_iid,timeout=40)  
			jsonStr = response.read() 
			
			resultObj = json.loads(jsonStr)

			if 'SUCCESS' in resultObj['ret'][0] :
				itemTobeSave = {}

				'''
				{
					"api": "wdetail",
					"v": "5.0",
					"ret": [
						"SUCCESS::调用成功"
					],
					"data": {
						"apiStack": [
							{
								"name": "esi",
								"value": "...."
							}
						],
					...
				'''

				#获取原价、现价、是否包邮
				apiStackObj = json.loads(resultObj['data']['apiStack'][0]['value'])
				if 'SUCCESS' not in apiStackObj['ret'][0] :
					raise Exception("fetch item apiStackObj detail failed!")
				
				#获取 原价、现价
				# -------------------
				itemInfoModelObj = apiStackObj['data']['itemInfoModel']	
				priceUnitsObj = itemInfoModelObj['priceUnits']

				price = None							#原价
				old_price = None						#现价
				for unit in priceUnitsObj :
					# "priceUnits": [
		   #              {
		   #                  "name": "上新价",
		   #                  "rangePrice": "125.00-208.00",
		   #                  "price": "125.00-208.00",
		   #                  "display": "1"
		   #              },
		   #              {
		   #                  "name": "价格",
		   #                  "price": "388.00-458.00",
		   #                  "display": "3"
		   #              }
		   #          ],

					#display==1,现价   !=1 原价
					if cmp(unit['display'], '1') == 0:
						price = unit['price']
					else:
						old_price = unit['price']

					if price is not None and old_price is not None:
						break

				itemTobeSave['price'] = price
				itemTobeSave['old_price'] = old_price
					
				# -------------------
				itemTobeSave['volume'] = itemInfoModelObj['totalSoldQuantity']  # 月销量
				# quantity = itemInfoModelObj['quantity']  # 库存
	
				#是否包邮
				# -------------------
				is_baoyou = False
	
				deliveryObj = apiStackObj['data']['delivery']
				if deliveryObj is not None :
					deliveryFees = deliveryObj['deliveryFees'][0]
					try:
						if deliveryFees.index(u'卖家包邮') >= 0 :
							is_baoyou = True
					except Exception as e:
						print str(e)
				
				itemTobeSave['is_baoyou'] = is_baoyou
	

				#在售状态
				#-------------
				'''
				  \"itemControl\": {
			            \"unitControl\": {
			                \"cartSupport\": \"false\",
			                \"buySupport\": \"false\",
			                \"buyText\": \"立即购买\",
			                \"cartText\": \"加入购物车\",
			                \"errorMessage\": \"已下架\",
			                \"hintBanner\": {
			                    \"text\": \"已下架\",
			                    \"bgColor\": \"#666666\"
			                },
			                \"submitText\": \"已下架\"
			            }
			        },
				'''
				buySupport = False
				try:
					itemControlObj = apiStackObj['data']['itemControl']
					buySupportStr = itemControlObj['unitControl']['buySupport']
				except Exception as e:
					print str(e)
				
				buySupport = True if cmp('true',buySupportStr) == 0 else False
				itemTobeSave['buy_support'] = buySupport


				# -------------------
				# 获取商品基本信息
				# -------------------
	
				itemInfoModelObj = resultObj['data']['itemInfoModel']
	
				itemTobeSave['title'] = itemInfoModelObj['title']  # 标题
				itemTobeSave['pic_url_array'] = itemInfoModelObj['picsPath']  # 图片地址，数组！
				itemTobeSave['location'] = itemInfoModelObj['location']  # 产品所在地
				itemTobeSave['has_sku'] = itemInfoModelObj['sku']  # 是否有sku信息 true\false
				itemTobeSave['cate_id'] = itemInfoModelObj['categoryId']  # 对应淘宝类目id
				# if 'itemTypeName' in itemInfoModelObj :
				# 	itemTobeSave['shop_type'] = itemInfoModelObj['itemTypeName']  # 淘宝还是天猫  taobao tmall
				# else:
				# 	itemTobeSave['shop_type'] = 'taobao'
	
				# 店铺信息
				# -------------------
				'''
					"seller": {
					"userNumId": "213712821",
					"type": "C",
					"nick": "手心纪",
					"creditLevel": "14",
		"goodRatePercentage": "99.85%",
					"shopTitle": "手心纪",
					"shopId": "57951032",
					"weitaoId": "2058689331",
					"fansCount": "66005",
					"fansCountText": "6.6万",
		"evaluateInfo": [
			{
				"title": "发货速度",
				"score": "4.8 ",
				"highGap": "37.37"
			},
			{
				"title": "服务态度",
				"score": "4.9 ",
				"highGap": "38.03"
			},
			{
				"title": "描述相符",
				"score": "4.8 ",
				"highGap": "34.81"
			}
		],
					"bailAmount": "1000元",
					"picUrl": "http://gw.alicdn.com/bao/uploaded//30/5d/TB1KkanFpXXXXXVbVXXSutbFXXX.jpg",
					"starts": "2009-04-21 18:03:23",
					"certificateLogo": "http://gw.alicdn.com/tps/i2/TB1bHe7FVXXXXbJXpXX4LN0JXXX-82-96.png",
					"actionUnits": [
						{
							"name": "全部宝贝",
							"value": "100",
							"url": "http://shop.m.taobao.com/goods/index.htm?shop_id=57951032",
							"track": "Button-AllItem"
						},
						{
							"name": "上新",
							"value": "1",
							"url": "http://h5.m.taobao.com/weapp/view_page.htm?page=shop/new_item_list&userId=213712821",
							"track": "Button-NewItem"
						},
						{
							"name": "关注人数",
							"value": "6.6万"
						}
					]
				},
				'''

				# 商品详情页面地址
				if 'descInfo' in resultObj['data'] and 'h5DescUrl2' in resultObj['data']['descInfo']:
					descInfoObj = resultObj['data']['descInfo']
					itemTobeSave['item_detail_url'] = descInfoObj['h5DescUrl2']
	
				sellerObj = resultObj['data']['seller']
				itemTobeSave['seller_id'] = sellerObj['userNumId']  # 卖家id
				itemTobeSave['shop_type'] = sellerObj['type']  # 店铺类型，C B
				itemTobeSave['nick'] = sellerObj['nick']  # 卖家昵称
				itemTobeSave['shop_name'] = sellerObj['shopTitle']  # 店铺名称
				itemTobeSave['shop_id'] = sellerObj['shopId']  # 店铺id
				itemTobeSave['shop_follow_amount'] = sellerObj['fansCount']  # 店铺关注人数
				if 'picUrl' in sellerObj:
					itemTobeSave['shop_icon'] = sellerObj['picUrl']  # 店铺icon
	
	
				#店铺动态评分
				evaluateInfoObjs = sellerObj['evaluateInfo']
				for scoreMap in evaluateInfoObjs :
					try :
						score = scoreMap['score'].lstrip().rstrip()
						name = scoreMap['name']

						if cmp(u'描述相符', name)==0:
							itemTobeSave['dsr_desc_score'] = score
						elif cmp(u'服务态度', name)==0:
							itemTobeSave['dsr_service_score'] = score
						elif cmp(u'物流服务', name)==0:
							itemTobeSave['dsr_shipment_score'] = score

					except Exception as e :
						print str(e)
	
	
				#好评率
				goodRatePercentage = sellerObj['goodRatePercentage']
				if goodRatePercentage is not None :
					try:
						itemTobeSave['shop_rate'] = float(goodRatePercentage[:goodRatePercentage.index('%')])	
					except Exception as e :
						print str(e)
		
		return itemTobeSave
			
			
if __name__ == '__main__' :
	mFetchItemDetail = FetchItemDetail('531511040464')
	print mFetchItemDetail.fetchDetail()
	
	
		