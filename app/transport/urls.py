# transport的二级目录设置

from django.conf.urls import url
from app.transport import transport_views


urlpatterns = [
    # 运输人员申请
    url(r'^transpoter/apply/', transport_views.transpoter_apply),
    url(r'^transpoter/regis/', transport_views.transpoter_regis),

    # 商品信息扫码录入
    url(r'^product_enter/', transport_views.product_enter),
    url(r'^product_enter2/', transport_views.data_write),

    # 开始运输
    url(r'^start/', transport_views.Transport_start),

    # 到达终点
    url(r'^end/', transport_views.Transport_end),
]

