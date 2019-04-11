# produce的二级目录设置

from django.conf.urls import url
from app.produce import produce_views

urlpatterns = [
    url(r'^producer_alter_personal',produce_views.producer_alter_personal),
    url(r'^producer_alter_farm',produce_views.producer_alter_farm),
    url(r'^sheep_state',produce_views.sheep_state),
    url(r'^fully_grown', produce_views.fully_grown),
    url(r'^input_sheep', produce_views.input_sheep),
    url(r'^test', produce_views.test),
]

