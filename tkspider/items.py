# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



u'''
is_baoyou       是否包邮
coupon_url      优惠券链接
coupon_price    优惠券金额
source_cid      商品分类id
title           商品标题
price           商品现价
old_price       商品原价
sell_pre        商品折扣
item_id         商品id
pic_url         图片链接

下面为新增字段
-------------------
cate_name       商品分类名称
seller_rate1    店铺描述打分
seller_rate2    店铺服务打分
seller_rate3    店铺物流打分
volume          销量数据
shop_type       商品类型（淘宝，天猫）
'''

u'''
    {
        "is_baoyou": true,                  是否包邮
        "source_cid": "50009032",           商品分类
        "seller_rates": [                   店铺动态评分
            {
                "highGap": "12.85",
                "score": "4.8 ",
                "name": "描述相符",
                "title": "描述相符"
            },
            {
                "highGap": "19.42",
                "score": "4.8 ",
                "name": "服务态度",
                "title": "服务态度"
            },
            {
                "highGap": "18.62",
                "score": "4.8 ",
                "name": "物流服务",
                "title": "发货速度"
            }
        ],
        "price": "49.00",                   现价
        "title": " 七匹狼皮带男士真皮正品休闲牛皮腰带 青年韩版针扣裤带中年皮带",     标题
        "old_price": "￥64",                 原价
        "volume": "14931",                  总销量
        "shop_type": 1,                     商品类型（0，unknow 1，tmall 2，taobao）
        "item_id": "530839948259",          商品id
        "pic_url": "http://img.alicdn.com/bao/uploaded/i3/TB1a.2jKVXXXXaNXpXXXXXXXXXX_!!0-item_pic.jpg_430x430q90.jpg"
    }
'''

class Item(scrapy.Item):
    item_id = scrapy.Field()                #item_id    
    coupon_activity_id = scrapy.Field()                     #优惠券id
    coupon_seller_id = scrapy.Field()                       #卖家id
    desc = scrapy.Field()                   #小编评语
    title = scrapy.Field()                  #商品标题


    # item_id = scrapy.Field()				#item_id	
    # pic_url = scrapy.Field()			
    # title = scrapy.Field()
    # desc = scrapy.Field()					#小编评语
    # location = scrapy.Field()               #商品所在地
    # has_sku = scrapy.Field()                #是否有sku

    # #优惠券
    # coupon_activity_id = scrapy.Field()						#优惠券id
    # coupon_seller_id = scrapy.Field()						#卖家id
    # coupon_title = scrapy.Field()							#优惠券标题
    # coupon_desc = scrapy.Field()							#优惠券描述
    # coupon_price = scrapy.Field()           				#优惠券价格
    # coupon_begin_time = scrapy.Field()						#优惠券开始时间
    # coupon_end_time = scrapy.Field()						#优惠券结束时间
    # coupon_limit = scrapy.Field()							#优惠券限领数量
    # coupon_total_amount = scrapy.Field()					#优惠券总数
    # coupon_received_amount = scrapy.Field()					#优惠券已领数量


    # #淘宝商品数据
    # price = scrapy.Field()					#现价
    # old_price = scrapy.Field()				#原价
    # is_baoyou = scrapy.Field()				#是否包邮 bool
    # cate_id = scrapy.Field()                #商品分类id
    # volume = scrapy.Field()                 #月销量数据
    # buy_support = scrapy.Field()                 #是否可以购买

    # #淘宝店铺数据
    # shop_id = scrapy.Field()					#店铺id
    # shop_name = scrapy.Field()					#店铺名称
    # seller_id = scrapy.Field() 					#卖家id
    # nick = scrapy.Field()						#卖家昵称
    # shop_type = scrapy.Field()              	#商品类型（淘宝，天猫）
    # shop_rate = scrapy.Field()					#店铺好评率
    # shop_follow_amount = scrapy.Field()			#店铺关注人数
    # dsr_desc_score = scrapy.Field()           	#店铺描述打分
    # dsr_service_score = scrapy.Field()           	#店铺服务打分
    # dsr_shipment_score = scrapy.Field()           	#店铺物流打分
    

    


