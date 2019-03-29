# transport的二级目录设置

from django.conf.urls import url
from app.transport import transport_views


urlpatterns = [
    # 运输人员申请
    url(r'^Product/transpoter/apply/', transport_views.transpoter_apply),

    # 商品信息扫码录入
    url(r'^product_enter/', transport_views.product_enter),
    url(r'^product_enter/', transport_views.data_write),

    # 开始运输
    url(r'^start/', transport_views.Transport_start),

    # 到达终点
    url(r'^end/', transport_views.Transport_end),
]

