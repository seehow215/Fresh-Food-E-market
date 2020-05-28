"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.static import serve
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

import xadmin
from MxShop.settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, CategoryViewSet, BannerViewSet, IndexCategoryViewSet, HotSearchsViewset
from trade.views import ShoppingCartViewSet, OrderViewSet, AlipayView
from user_operation.views import UserFavViewSet, LeavingMessageViewSet, AddressViewSet
from users.views import SmsCodeViewSet, UserViewSet

router = DefaultRouter()

# configure goods url
router.register(r'goods', GoodsListViewSet, basename='goods')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'banners', BannerViewSet, basename='banners')
router.register(r'indexcategories', IndexCategoryViewSet, basename='indexcategories')
router.register(r'hotsearchs', HotSearchsViewset, basename="hotsearchs")
# config users url
router.register(r'codes', SmsCodeViewSet, basename='codes')
router.register(r'users', UserViewSet, basename='users')
# config user operations url
router.register(r'userfavs', UserFavViewSet, basename='userfavs')
router.register(r'messages', LeavingMessageViewSet, basename='messages')
router.register(r'addresses', AddressViewSet, basename='addresses')
# config trades url
router.register(r'shopcarts', ShoppingCartViewSet, basename='shopcarts')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    # use re to get the path of the image
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    path('ueditor/', include('DjangoUeditor.urls')),

    url(r'^index/', TemplateView.as_view(template_name="index.html"), name="index"),

    # product list page
    url(r'^', include(router.urls)),
    url(r'docs/', include_docs_urls(title="Muxue Seafood")),

    # drf token authentication
    url(r'^api-token-auth/', views.obtain_auth_token),
    # jwt authentication
    url(r'^login/$', obtain_jwt_token),
    # third-parties
    path('alipay/return/', AlipayView.as_view()),
    url('', include('social_django.urls', namespace='social'))
]
