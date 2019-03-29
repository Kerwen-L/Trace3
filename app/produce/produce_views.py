from __future__ import unicode_literals
from django.shortcuts import HttpResponse, render, redirect
from app import models
from django.shortcuts import render_to_response
from django.template import Context
# from django.utils import simplejson
from django.core import serializers
import json
import datetime

# Create your views here.

'''
def register(request):
    characterflag = request.GET.get("characterFlag")
    print(characterflag)
    def producer():
        models.ProducerRegistry(**json.loads(request.body)).save()  # 可以直接存，没传进来的表项数据里默认为空
    def trans():
        models.TransporterRegistry(**json.loads(request.body)).save()  # 可以直接存，没传进来的表项数据里默认为空
    def quaratine():
        models.QuarantineRegistry(**json.loads(request.body)).save()
    def processor():
        models.ProcessorRegistry(**json.loads(request.body)).save()
    def seller():
        models.SellerRegistry(**json.loads(request.body)).save()
    def company():
        models.CompanyRegistry(**json.loads(request.body)).save()
    def consumer():
        models.ConsumerRegistry(**json.loads(request.body)).save()
    switcher={
        "0":producer(),
        "1":trans(),
        "2":quaratine(),
        "3":producer(),
        "4":seller(),
        "5":consumer(),
        "6":company()
    }
    switcher.get(characterflag,"error")()#替代switch/case,Expression is not callable

    return {
        "0":producer(),
        "1":trans(),
        "2":quaratine(),
        "3":producer(),
        "4":seller(),
        "5":consumer(),
        "6":company()
        }.get(characterflag, 'error')  # 'error'为默认返回值，可自设置

    return HttpResponse("注册成功！")
'''


def DateEncoder(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.strftime('%Y-%m-%d')


# 传给我要修改的生产者的ID
def producer_alter_personal(request):  # 只能改ContactNo和Password,
    dicttemp = json.loads(request.body.decode())
    ConsumerId = dicttemp["ConsumerId"]
    temp = models.ConsumerRegistry.objects.get(ConsumerId=ConsumerId)
    temp.ContactNo = dicttemp["ContactNo"]  # 更改电话号码
    temp.Password = dicttemp["Password"]  # 更改密码
    temp.save()
    # models.ConsumerRegistry.objects.filter(user='yangmv').update(pwd='520')
    dict_ = {"ConsumerId": ConsumerId}
    return HttpResponse(json.dumps(dict_, ensure_ascii=False),
                        content_type="application/json")  # 返回ID


# 传给我要修改的生产者的ID
def producer_alter_farm(request):  # 只能改CompanyName OperatingPlace，即农场名，农场地址
    dicttemp = json.loads(request.body.decode())
    ConsumerId = dicttemp["ConsumerId"]
    CompanyName = dicttemp["CompanyName"]
    OperatingPlace = dicttemp["OperatingPlace"]
    temp_consumer = models.ConsumerRegistry.objects.get(ConsumerId=ConsumerId)
    # temp_consumer.producerregistry.companyregistry.CompanyName=dicttemp["CompanyName"]#实际上不允许这样改的，因为这是一对多，怎么可能直接改1的值，应该在company里面搜索
    # 有没有要改的新的公司，如果有，外键对应上，如果没有，新创建一个，但是怎么确保这个公司不是乱填的呢？？？我的想法是：确保的时候可能需要查询一下公司表里有木有营业许可证啥的
    temp_company = models.CompanyRegistry.objects.filter(CompanyName=CompanyName)
    temp_place = models.CompanyRegistry.objects.filter(OperatingPlace=OperatingPlace)
    if temp_company.exists() and temp_place.exists() and temp_company[0].id == temp_place[0].id:  # 数据库里有新的企业名称和经营地址且匹配
        temp_consumer.producerregistry.companyregistry = temp_company[0].id  # 将生产者的外键指向新的农场
        # producerregistry是父类通过子类的小写表明访问子类的数据
        # dict_ = {"ConsumerId": ConsumerId}
        # return HttpResponse(json.dumps(dict_, ensure_ascii=False),content_type="application/json")  # 返回ID
        return HttpResponse("修改成功！")

    if temp_company.exists() and temp_place.exists() and temp_company[0].id != temp_place[0].id:
        return HttpResponse("该企业名称和经营地址不匹配！")

    if temp_company.exists() and temp_place.count() == 0:
        return HttpResponse("该经营地址不存在")
    if temp_place.exists() and temp_company.count() == 0:
        return HttpResponse("该企业名称不存在")
    if temp_place.count() == 0 and temp_company.count() == 0:
        return HttpResponse("该企业名称和经营地址均不存在")


def sheep_state(request):
    temp = models.ProductionData.objects.all()
    data = serializers.serialize("json", temp)
    return HttpResponse(data, content_type="application/json")  # 直接不管三七二十一将queryset序列化成json给前端


def fully_grown(request):
    sheep_id = request.GET.get("Sheep_Id")
    temp = models.ProductionData.objects.filter(RecordID__contains=sheep_id).first()
    if temp.State == 0:
        temp.State = 2
        temp.save()
        return HttpResponse("出栏成功！")
    else:
        return HttpResponse("出栏失败！")


























