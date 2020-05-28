__author__ = 'seehow'

import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MxShop.settings')

import django
django.setup()

from goods.models import GoodsCategory

from db_tools.data.category_data import row_data


for lvl1_cat in row_data:
    lvl1_instance = GoodsCategory()
    lvl1_instance.code = lvl1_cat["code"]
    lvl1_instance.name = lvl1_cat["name"]
    lvl1_instance.category_type = 1
    lvl1_instance.save()

    for lvl2_cat in lvl1_cat["sub_categorys"]:
        lvl2_instance = GoodsCategory()
        lvl2_instance.code = lvl2_cat["code"]
        lvl2_instance.name = lvl2_cat["name"]
        lvl2_instance.category_type = 2
        lvl2_instance.parent_category = lvl1_instance
        lvl2_instance.save()

        for lvl3_cat in lvl2_cat["sub_categorys"]:
            lvl3_instance = GoodsCategory()
            lvl3_instance.code = lvl3_cat["code"]
            lvl3_instance.name = lvl3_cat["name"]
            lvl3_instance.category_type = 3
            lvl3_instance.parent_category = lvl2_instance
            lvl3_instance.save()