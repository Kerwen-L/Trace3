from __future__ import unicode_literals
from django.shortcuts import HttpResponse, render, redirect
from app import models
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.template import Context
# from django.utils import simplejson
import json
# Create your views here.


# 人员-查询
def Processor_Inquiry(request):
    if request.method == "GET":
        consumer_id = request.GET.get("consumer_id")  # 获得加工人员的processor_idTrace2@223.3.79.211
        try:
            temp1 = models.ProcessorRegistry.objects.get(ConsumerId=consumer_id)
            demo = model_to_dict(temp1)
            demo.pop("id")
            demo.pop("consumerregistry_ptr")
            return HttpResponse(json.dumps(demo,cls=models.DateEncoder,ensure_ascii = False),content_type="application/json",charset="utf-8")
        except ObjectDoesNotExist:
            return HttpResponse("未查询到符合条件的数据")


# 人员-删除
def Processor_Delete(request):
    if request.method == "POST":
        consumer_id = request.GET.get("consumer_id")  #获得id
        temp=models.ProcessorRegistry.objects.get(ConsumerId=consumer_id)
        temp.delete()
        print("加工人员数据删除成功!")
    return HttpResponse("加工人员数据删除成功!")


# 人员-更改
def Processor_Update(request):
    if request.method == "POST":
        try:
            demo = json.loads(request.body)  # 前台传入的数据 demo
            id = demo.get("ConsumerId")  # 获得传入加工人员的processor_id
            temp1 = models.ProcessorRegistry.objects.get(ConsumerId=id)  # 在数据库查找对象temp1
            temp1.ConsumerName = demo.get("ConsumerName")  # 更改姓名
            temp1.IDNo = demo.get("IDNo")  # 更改身份证号
            temp1.ContactNo = demo.get("ContactNo")  # 更改联系电话
            temp1.WorkPlaceID = demo.get("WorkPlaceID")  # 更改工作单位ID
            temp1.PhotoSrc = demo.get("PhotoSrc")  # 更改证件照
            temp1.HC4foodCertificationNo = demo.get("HC4foodCertificationNo")  # 更改食品从业人员健康证明编号
            temp1.HC4foodCertificationSrc = demo.get("HC4foodCertificationSrc")  # 更改食品从业人员健康证明图片
            temp1.Password = demo.get("Password")  # 更改密码
            temp1.save()
            print("加工人员数据更改成功")
            return HttpResponse("加工人员数据更改成功")
        except ObjectDoesNotExist:
            return HttpResponse("未查询到符合条件的数据")


# 结果-添加
def ProcessData_Add(request):
    if request.method == "POST":
        try:
            models.ProcessData(**json.loads(request.body)).save()
            demo1 = json.loads(request.body)
            person = demo1.get("ProcessPersonID")
            temp1 = models.ProcessorRegistry.objects.get(ConsumerId = person)  # 在数据库查找对象temp1
            temp1.ProcessorCounts = temp1.ProcessorCounts + 1 #对应的加工人员的加工次数+1
            temp1.save()
            print("加工数据添加成功")
            return HttpResponse("加工数据上传数据库成功!")
        except ObjectDoesNotExist:
            return HttpResponse("加工数据添加失败")
    else:
        return HttpResponse("Error：上传失败！")


# 结果-查询
def ProcessData_Inquiry(request):
    if request.method == "GET":  # 这里用get比post方便，因为羊id直接就在URL里了
        production_id = request.GET.get("production_id")  # 获得加工结果的process_id
        temp = models.ProcessData.objects.filter(ProductionID=production_id)
        ret=[]
        if(temp):
            for sample in temp:
                i = model_to_dict(sample)
                i.pop("id")
                ret.append(json.dumps(i,cls=models.DateEncoder,ensure_ascii = False))
            return HttpResponse(ret, content_type="application/json",charset="utf-8")
        else:
            return HttpResponse("未查询到符合条件的数据")
