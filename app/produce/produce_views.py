from __future__ import unicode_literals
from django.shortcuts import HttpResponse, render, redirect
from app import models
from django.shortcuts import render_to_response
from django.template import Context
# from django.utils import simplejson
from django.core import serializers
import json
import datetime
from PIL import Image
import qrcode


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
    #temp = models.ProducerRegistry.objects.get(ConsumerId=ConsumerId)
    temp.ContactNo = dicttemp["ContactNo"]  # 更改电话号码
    temp.Password = dicttemp["Password"]  # 更改密码
    temp.save()
    dict_ = {"ConsumerId": ConsumerId}
    return HttpResponse(json.dumps(dict_, ensure_ascii=False),
                        content_type="application/json")  # 返回ID


# 传给我要修改的生产者的ID
def producer_alter_farm(request):  # 只能改CompanyName OperatingPlace，即农场名，农场地址
    dicttemp = json.loads(request.body.decode())
    ConsumerId = dicttemp["ConsumerId"]
    CompanyName = dicttemp["CompanyName"]
    OperatingPlace = dicttemp["OperatingPlace"]
    temp_consumer = models.ProducerRegistry.objects.get(ConsumerId=ConsumerId)
    # temp_consumer.producerregistry.companyregistry.CompanyName=dicttemp["CompanyName"]#实际上不允许这样改的，因为这是一对多，怎么可能直接改1的值，应该在company里面搜索
    # 有没有要改的新的公司，如果有，外键对应上，如果没有，新创建一个，但是怎么确保这个公司不是乱填的呢？？？我的想法是：确保的时候可能需要查询一下公司表里有木有营业许可证啥的
    temp_company = models.CompanyRegistry.objects.filter(CompanyName=CompanyName)
    temp_place = models.CompanyRegistry.objects.filter(OperatingPlace=OperatingPlace)
    if temp_company.exists() and temp_place.exists() and temp_company[0].id == temp_place[0].id:  # 数据库里有新的企业名称和经营地址且匹配
        # temp_consumer.producerregistry.companyregistry_id = temp_company[0].id  # 将生产者的外键指向新的农场
        # temp_consumer.save()
        temp_consumer.companyregistry = temp_company[0]  # 将生产者的外键指向新的农场
        temp_consumer.save()

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
    import random

    dic = json.loads(request.body.decode())
    RecordID = dic["RecordID"]
    ConsumerId = dic["ConsumerId"]

    uuid_temp = models.UUID_Sheep.objects.filter(RecordID=RecordID, PB_Flag=1)
    UUID = uuid_temp.first().UUID  # 在中间表找到该羊对应的项圈ID
    base_data = models.BaseStationData.objects.filter(UUID=UUID, SheepID=RecordID)  # 这里应该有很多条数据
    for obj in base_data:
        HealthState = int(random.choice("01"))
        GPSLocation = "朔州"
        ActiveDis = round(random.uniform(20, 80), 3)  # 精度为3位
        Weight = round(random.uniform(40, 70), 3)
        BodyTemperature = round(random.uniform(20, 30), 3)
        models.ProductionData.objects.create(RecordID=RecordID, MonitorId=UUID, GPSLocation=GPSLocation,
                                             State=0, HealthState=HealthState, ActiveDis=ActiveDis, Weight=Weight, BodyTemperature=BodyTemperature,
                                                MonitorRecordTime=obj.Time)  # 这里应该是BodyTemperature=obj.Data1,但是Data1布吉岛是什么鸡巴，只能写死呵呵
    sheep_final = models.ProductionData.objects.filter(RecordID=RecordID)
    data = serializers.serialize("json", sheep_final)
    return HttpResponse(data, content_type="application/json")  # 直接不管三七二十一将queryset序列化成json给前端





    # sheep_primarykey = uuid_temp.first().id  # 找到当前羊的主键id
    # UUID = uuid_temp.first().UUID
    # base_data = models.BaseStationData.objects.filter(UUID=UUID, Sheep_Id_id=sheep_primarykey)  # 找到对应羊ID在基站中的数据
    # for obj in base_data:
    #     models.ProductionData.objects.create(RecordID=RecordID, MonitorId=UUID, BodyTemperature=obj.Data1,
    #                                          MonitorRecordTime=obj.Time)
    # sheep_final = models.ProductionData.objects.filter(RecordID=RecordID)
    # data = serializers.serialize("json", sheep_final)
    # return HttpResponse(data, content_type="application/json")  # 直接不管三七二十一将queryset序列化成json给前端










def fully_grown(request):
    sheep_id = request.GET.get("SheepID")
    temp = models.ProductionData.objects.filter(RecordID=sheep_id)
    for obj in temp:
        if obj.State == 0:
            obj.State = 1
            obj.save()
        else:
            return HttpResponse("出栏失败")
    return HttpResponse("出栏成功")


idcountsheep = 0  # 羊的自增全局变量


def input_sheep(request):
    dic = json.loads(request.body.decode())
    UUID = dic["UUID"]
    PB_Flag = 1
    ConsumerId = dic["ConsumerId"]  # 用来确认羊是哪个生产者录入的,实际上数据里羊和生产者并没有串起来
    # RecordID:  7位：企业Id X（8 + 2）位：生产内容Id + 00 8位：日期
    # 生产内容ID是怎么生成的
    # ProductionId = "假设还是2位省份+6位自增全局变量"
    # models.UUID_Sheep.objects.create(UUID=UUID, PB_Flag=PB_Flag, ProductionId=ProductionId)

    import random
    province = str(random.randint(1, 34)).zfill(2)  # 随机生成省份，占两位
    global idcountsheep
    # RecordID = province + str(idcountsheep).zfill(6)
    # idcountsheep += 1
    RecordID = province + str(random.randint(1, 999999)).zfill(6)
    RecordID += "00000000"

    temp = models.UUID_Sheep.objects.filter(UUID=UUID, PB_Flag=1)
    print(temp)
    for obj in temp:
        obj.PB_Flag = 0  # 将之前项圈对应的羊的flag置为0，因为项圈换羊戴了
        obj.save()

    models.UUID_Sheep.objects.create(UUID=UUID, PB_Flag=PB_Flag, RecordID=RecordID)
    dic2 = {}
    dic2["RecordID"] = RecordID
    dic2["ConsumerId"] = ConsumerId
    img = qrcode.make(str(dic2))  # eval(str)
    img.save("qrcode_origin/"+RecordID+".png")
    url = "http://223.3.79.211:8000/user/qrcode_origin/"+RecordID+".png"
    models.sheep_url.objects.create(RecordID=RecordID, qr_code=url)  # 把羊和该羊的二维码对应起来
    return HttpResponse(url)
    # http://223.3.79.211:8000/user/qrcode_origin/RecordID.png

def test(request):
    global idcountsheep
    print(idcountsheep)
    idcountsheep += 1
    print(idcountsheep)
    return HttpResponse("test ing")


























