from __future__ import unicode_literals
from django.shortcuts import HttpResponse, render, redirect
from app import models
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from app.ucl import ucl
from django.shortcuts import render_to_response
import json
from PIL import Image
import qrcode #导入包
# Create your views here.
#定义二维码格式
qr = qrcode.QRCode(
    version=1, #控制二维码的大小，（1-40）
    error_correction=qrcode.constants.ERROR_CORRECT_L, #控制二维码的纠错功能
    box_size=10, #二维码的每个格子包含的像素数
    border=4,    #控制边框包含的格子数
)

# 加工人员查询
def Processor_Inquiry(request):
    if request.method == "GET":
        consumer_id = request.GET.get("ConsumerId")  # 获得加工人员的processor_idTrace2@223.3.79.211
        print(consumer_id)
        try:
            temp1 = models.ProcessorRegistry.objects.get(ConsumerId=consumer_id)
            demo = model_to_dict(temp1)
            demo.pop("id")
            demo.pop("consumerregistry_ptr")
            demo.pop("imgID")
            demo.pop("imgwork")
            demo.pop("imgquality")
            print("加工人员信息查询成功")
            return HttpResponse(json.dumps(demo, cls=models.DateEncoder, ensure_ascii=False), content_type="application/json", charset="utf-8")
        except ObjectDoesNotExist:
            return HttpResponse("未查询到符合条件的数据")
    else:
        return HttpResponse("mothod应该为GET")

# 人员-删除
def Processor_Delete(request):
    if request.method == "POST":
        consumer_id = request.GET.get("ConsumerId")  #获得id
        temp = models.ProcessorRegistry.objects.get(ConsumerId=consumer_id)
        temp.delete()
        print("加工人员数据删除成功!")
        return HttpResponse("加工人员数据删除成功!")
    else:
        return HttpResponse("mothod应该为POST")

# 人员-更改
def Processor_Update(request):
    if request.method == "POST":
        try:
            demo = json.loads(request.body)  # 前台传入的数据 demo
            demo_id = demo.get("ConsumerId")  # 获得传入加工人员的processor_id
            temp1 = models.ProcessorRegistry.objects.get(ConsumerId=demo_id)  # 在数据库查找对象temp1
            temp1.ConsumerName = demo.get("ConsumerName")  # 更改姓名
            temp1.IDNo = demo.get("IDNo")  # 更改身份证号
            temp1.ContactNo = demo.get("ContactNo")  # 更改联系电话
            temp1.WorkPlaceID = demo.get("WorkPlaceID")  # 更改工作单位ID
            temp1.PhotoSrc = demo.get("PhotoSrc")  # 更改证件照
            temp1.HC4foodCertificationNo = demo.get("HC4foodCertificationNo")  # 更改食品从业人员健康证明编号
            temp1.HC4foodCertificationSrc = demo.get("HC4foodCertificationSrc")  # 更改食品从业人员健康证明图片
            temp1.Password = demo.get("Password")  # 更改密码
            temp1.CharacterFlag = 3
            temp1.save()
            print("加工人员数据更改成功")
            return HttpResponse("加工人员数据更改成功")
        except ObjectDoesNotExist:
            return HttpResponse("未查询到符合条件的数据")
    else:
        return HttpResponse("mothod应该为POST")

# 结果-添加
def ProcessData_Add(request):
    if request.method == "POST":
        try:
            # UCL解包
            data = json.loads(request.body)
            print(data)
            uclstr = data['ucl']
            flag = data['flag']
            serialnumber = data['serialnumber']
            productionId = data['productionId']
            print("uclStrBase64:" + uclstr)
            [contentdict, uclpath] = ucl.unpack(uclstr, flag, productionId, serialnumber)
            print(contentdict)
            print(uclpath)
#            models.SellData(**contentdict).save()
            models.ProcessData(**contentdict).save()
#            models.ProcessData(**json.loads(request.body)).save()

            # 加工人员对应加工次数+1
            demo1 = contentdict
#            demo1 = json.loads(request.body)
            person = demo1.get("ConsumerId")
            temp1 = models.ProcessorRegistry.objects.get(ConsumerId=person)  # 在数据库查找对象temp1
            temp1.ProcessorCounts = temp1.ProcessorCounts + 1
            temp1.save()


            # 生成记录对应的二维码
            img = qrcode.make('{ProductionID:'+demo1.get("ReproductionID")+'}')
            img.save("qrcode_process/"+demo1.get("ReproductionID")+".png")
            url1 = "223.3.93.189"

            # 图片对应的地址
            src = "http://"+url1+":8000/process/qrcode_process/"+demo1.get("ReproductionID")+".png"
            print("src is %s"%(src))

            # 加工数据表添加QRcode
            ddd = models.ProcessData.objects.get(ReproductionID=demo1.get("ReproductionID"))
            print(demo1.get("ReproductionID"))
            ddd.QRCodeLink = demo1.get("ReproductionID")
            ddd.save()

            print("加工数据添加成功")
            return HttpResponse(src)
        except ObjectDoesNotExist:
            return HttpResponse("加工数据添加失败")
    else:
        return HttpResponse("mothod应该为POST")


# 结果-查询
def ProcessData_Inquiry(request):
    if request.method == "GET":  # 这里用get比post方便，因为羊id直接就在URL里了
        production_id = request.GET.get("ProductionID")  # 获得加工结果的process_id
        temp = models.ProcessData.objects.filter(ProductionID=production_id)
        ret = []
        if(temp):
            for sample in temp:
                i = model_to_dict(sample)
                i.pop("id")
                ret.append(json.dumps(i, cls=models.DateEncoder, ensure_ascii = False))
            print("加工结果查询成功")
            return HttpResponse(ret, content_type="application/json", charset="utf-8")
        else:
            return HttpResponse("未查询到符合条件的数据")
    else:
        return HttpResponse("mothod应该为GET")
