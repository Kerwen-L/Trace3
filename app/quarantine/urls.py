# quarantine的二级目录设置

from django.conf.urls import url
from app.quarantine import quarantine_views


urlpatterns = [

    url(r'^quarantine/submit', quarantine_views.quarantine_submit),
    # inquiry提交的是get请求
    url(r'^quarantine/inquiry$', quarantine_views.quarantine_inquiry),
    url(r'^quarantiner/inquiry$', quarantine_views.quarantiner_inquiry),
    url(r'^quarantine/registry', quarantine_views.quarantiner_registry),
    url(r'^quarantiner/alter', quarantine_views.quarantiner_alter),
    url(r'^quarantiner/application$', quarantine_views.qurarantiner_application)
]
