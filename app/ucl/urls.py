# quarantine的二级目录设置

from django.conf.urls import url
from app.ucl import ucl

urlpatterns = [

    # inquiry提交的是get请求
    url(r'^getUCL$', ucl.get_ucl),
]
