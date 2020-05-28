import json

from django.core import serializers
from django.http import JsonResponse
from django.views.generic.base import View

from goods.models import Goods


class GoodsListView(View):
    def get(self, request):
        """
        Implement product list page through django View
        :param request:
        :return:
        """
        goods = Goods.objects.all()[:10]

        json_data = serializers.serialize("json", goods)
        json_data = json.loads(json_data)

        return JsonResponse(json_data, safe=False)