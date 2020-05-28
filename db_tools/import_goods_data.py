__author__ = 'seehow'

import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MxShop.settings')

import django
django.setup()

from goods.models import Goods, GoodsCategory, GoodsImage

from db_tools.data.product_data import row_data

for goods_detail in row_data:
    goods = Goods()
    goods.name = goods_detail['name']
    # get rid of symbols and characters and transfer into number
    goods.market_price = float(int(goods_detail["market_price"].replace("￥", "").replace("元", "")))
    goods.shop_price = float(int(goods_detail["sale_price"].replace("￥", "").replace("元", "")))
    goods.goods_brief = goods_detail["desc"] if goods_detail["desc"] else ""
    goods.goods_desc = goods_detail["goods_desc"] if goods_detail["goods_desc"] else ""
    goods.goods_front_image = goods_detail["images"][0] if goods_detail["images"] else ""

    category_name = goods_detail["categorys"][-1]
    # use filter instead of get here to avoid raising exceptions when there are none or more than one result
    category = GoodsCategory.objects.filter(name=category_name)
    if category:
        goods.category = category[0]
    else:
        category = GoodsCategory()
        category.name = category_name
        parent_name = goods_detail["categorys"][-2]
        category.parent_category = GoodsCategory.objects.filter(name=parent_name)[0]
        category.code = category_name
        category.category_type = 2
        category.save()
        goods.category = category
    goods.save()

    for goods_image in goods_detail['images']:
        goods_image_instance = GoodsImage()
        goods_image_instance.image = goods_image
        goods_image_instance.goods = goods
        goods_image_instance.save()