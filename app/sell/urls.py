# sell的二级目录设置

from django.conf.urls import url
from app.sell import sell_views


urlpatterns = [

    # 增加销售人员信息，仅测试时使用
    url(r'^add_seller/', sell_views.add_seller),
    # 查询销售人员信息
    url(r'^inquiry_seller/$', sell_views.inquiry_seller),
    # 修改销售人员信息
    url(r'^alter_seller/$', sell_views.alter_seller),
    # 完善销售人员信息
    # url(r'^complete_seller/', sell_views.complete_seller),
    # 增加超市信息，仅测试时使用
    url(r'^add_supermarket/', sell_views.add_supermarket),
    # 查询销售人员信息
    url(r'^inquiry_supermarket/$', sell_views.inquiry_supermarket),
    # 修改超市信息
    url(r'^alter_supermarket/$', sell_views.alter_supermarket),
    # 完善超市信息
    # url(r'^complete_supermarket/', sell_views.complete_supermarket),
    # 录入商品信息
    url(r'^register_commodity/', sell_views.register_commodity),
    # 查询商品信息
    url(r'^sell_state/$', sell_views.sell_state),
    # 按产地查询，测试
    url(r'^sell_state_bylocation/$', sell_views.sell_state_bylocation),
    # 修改商品信息
    url(r'^alter_sell_state/', sell_views.alter_sell_state)
]
