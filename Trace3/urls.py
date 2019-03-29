"""Trace3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
# from django.contrib import admin

urlpatterns = [
    # 多级url
    # 指向user的urls文件
    url(r'^user/', include('app.user.urls')),
    # 指向produce的urls文件
    url(r'^produce/', include('app.produce.urls')),
    # 指向quarantine的urls文件
    url(r'^quarantine/', include('app.quarantine.urls')),
    # 指向transport的urls文件
    url(r'^transport/', include('app.transport.urls')),
    # 指向process的urls文件
    url(r'^process/', include('app.process.urls')),
    # 指向sell的urls文件
    url(r'^sell/', include('app.sell.urls'))


]
