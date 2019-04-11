# user的二级目录设置

from django.conf.urls import url
from app.user import user_views
import Trace3.settings as settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    url(r'^register',user_views.register),
    url(r'^login',user_views.login),
    url(r'^fulfil',user_views.fulfil),
    url(r'^test', user_views.test),
    url(r'^update', user_views.update),  # 更改
    url(r'^origin/$', user_views.origin),  # 更改
    url(r'^img_fulfil', user_views.fulfil_img),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.QRCODE_ORIGIN_URL, document_root=settings.QRCODE_ORIGIN_ROOT)

