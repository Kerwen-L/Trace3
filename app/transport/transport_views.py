from __future__ import unicode_literals
from django.shortcuts import HttpResponse, render, redirect
from app import models
from django.shortcuts import render_to_response


'''
添加了一部分内容

'''
import json
from datetime import date
from datetime import datetime
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
def toJSON(self):
    return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]),cls=ComplexEncoder)

'''运输人员申请'''
def transpoter_apply(request):
    person_info = models.transpoter_select_inproduct()
    return HttpResponse(person_info)                    #返回选择运输人员的全部信息

'''商品信息扫码录入  前端发送生产内容id和人员id'''
def product_enter(request):
    if request.method=="POST":
        dict_get = json.loads(request.body)             # 获得字典
        models.TransportData.objects.create(**dict_get) #新增记录
    return HttpResponse("录入完毕")


'''模拟扫码  两个id'''
def data_write(request):
    dict_get = json.loads(request.body)
    models.TransportData.objects.create(**dict_get)
    return HttpResponse("保存完毕")

'''
@运输数据 开始
1、收到前端推送的运输数据
2、解析出运输人员id
3、在运输数据表中 把与该运输员id匹配且标志为0 的商品
4、填写运输数据表（来源、去向、开始时间、商品标志）
5、生成环节标志、运输批次、流通编号（生产内容id+环节标志）
'''
def Transport_start(request):
    if request.method=="POST":
        dict_get = json.loads(request.body)                                                # 获得字典
        peoson_id=dict_get['TransactionPersonID']                                          # 解析运输人员id
    models.TransportData.objects.filter(TransactionPersonID=peoson_id,Flag=0).update(      # 更新前端推送内容到运输数据表
        From=dict_get['From'],
        To=dict_get['To'],
        TransactionStartTime=dict_get['TransactionStartTime'],
        flag=1,
    )
    if dict_get['From'].find("牧场") >= 0:                                                 #模糊查询 说明运输员在生产运输阶段
        print("开始更新生产数据 环节标志03")
        list1 = models.TransportData.objects.filter(TransactionPersonID=peoson_id,Flag=1)  #取出本次运输的全部生产商品记录
        for record in list1:
            models.TransportData.objects.filter(ProductionID=record.ProductionID).update(  #填写流通编号
                TransactionID=record.ProductionID + '03',
                TransactionStartUCLLink="UCL_product_begin",)

    elif dict_get['From'].find("检疫") >= 0:                                               #模糊查询 说明运输员在检疫运输阶段
        print("开始更新检疫数据 环节标志13")
        list1 = models.TransportData.objects.filter(TransactionPersonID=peoson_id,Flag=1)  #取出本次运输的全部检疫商品记录
        for record in list1:
            models.TransportData.objects.filter(ProductionID=record.ProductionID).update(  #填写流通编号
                TransactionID=record.ProductionID + '13',
                TransactionStartUCLLink = "UCL_quarantine_begin",)


    elif dict_get['From'].find("加工") >= 0:                                               #模糊查询 说明运输员在加工运输阶段
        print("开始更新加工数据 环节标志23")
        list1 = models.TransportData.objects.filter(TransactionPersonID=peoson_id,Flag=1)  #取出本次运输的全部加工商品记录
        for record in list1:
            models.TransportData.objects.filter(ProductionID=record.ProductionID).update(  #填写流通编号
                TransactionID=record.ProductionID + '23',
                TransactionStartUCLLink="UCL_process_begin",)


    elif dict_get['From'].find("超市") >= 0:                                               #模糊查询 说明运输员在销售运输阶段
        print("开始更新销售数据 环节标志43")
        list1 = models.TransportData.objects.filter(TransactionPersonID=peoson_id,Flag=1)  #取出本次运输的全部销售商品记录
        for record in list1:
            models.TransportData.objects.filter(ProductionID=record.ProductionID).update(  #填写流通编号
                TransactionID=record.ProductionID + '43',
                TransactionStartUCLLink="UCL_sell_begin",)
    else:
        print("数据填写不规范")

    return HttpResponse("起点数据填写完成")

'''
@运输数据 到达
1、收到前端推送的运输数据(运输人员id和到达时间)
2、解析出运输人员id
3、在运输数据表中 检索与该运输员id匹配且标志为1的商品
4、填写运输数据表（到达时间）
'''
def Transport_end(request):
    dict_get = json.loads(request.body)                                                # 获得字典
    peoson_id=dict_get['TransactionPersonID']                                          # 解析运输人员id
    models.TransportData.objects.filter(TransactionPersonID=peoson_id,Flag=1).update(  # 更新前端推送内容的到达时间
        TransactionEndTime=dict_get['TransactionEndTime'],
        Flag=2,                                                                        # 标志商品到达环节终点
    )
    models.transpoter_release(peoson_id)                                               # 运输人员状态释放
