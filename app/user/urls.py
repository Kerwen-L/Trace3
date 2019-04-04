# user的二级目录设置

from django.conf.urls import url
from app.user import user_views
import Trace3.settings as settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    url(r'^register',user_views.register),
    url(r'^login',user_views.login),
    url(r'^fulfil',user_views.fulfil),
    url(r'^fulfil_img', user_views.fulfil_img),
    #消费者更改密码
    url(r'^update/$',user_views.update),
    #消费者溯源
    url(r'^origin/$', user_views.origin),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

