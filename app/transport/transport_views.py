from __future__ import unicode_literals
from django.shortcuts import HttpResponse, render, redirect
from app import models
from django.shortcuts import render_to_response
import json
from datetime import date
from datetime import datetime


class ComplexEncoder(json.JSONEncoder):                             #时间解析函数
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


'''运输员队列生成'''
transpoter_list = []
def transporter_list_generate():
    templist = models.TransporterRegistry.objects.filter(Flag=0)                   # 从运输数据库中取出所有空闲记录
    if templist:
        for temp in templist:                                                   # 取出这些记录的生产内容id并形成list返回
            tempid = temp.ConsumerId
            transpoter_list.append(tempid)
        print("运输员队列已生成")
        print(transpoter_list)
    else:
        print("运输员忙")


'''运输员状态释放，根据运输人员ID'''
def transpoter_release(number):
    models.TransporterRegistry.objects.filter(ConsumerId=number).update(Flag=0)

'''运输员选择'''
def transpoter_select_inproduct():                                          #返回运输员的记录，由前端决定显示的具体内容
    print("调用运输员选择函数")
    if transpoter_list.__len__() == 0:
        transporter_list_generate()
        print("运输员列表已从0更新")
    id = transpoter_list[0]                                                 #选择第一个运输员
    if models.TransporterRegistry.objects.filter(ConsumerId=id).update(Flag=1):     #修改标志位
        print("运输员标志位已经修改")
    transpoter_recorder = models.TransporterRegistry.objects.get(ConsumerId=id) #查找记录
    if transpoter_recorder:
        print("找到运输员的信息")
    info_str = transpoter_recorder.to_front()                            #获取字符串形式的信息给前端
    print("运输员的姓名" + transpoter_recorder.ConsumerName)
    del transpoter_list[0]                                                  #从队列中删除
    return info_str                                                         #返回信息字符串



def transpoter_regis(request):
    if request.method == "POST":
        models.TransporterRegistry(**json.loads(request.body)).save()
        print("运输员添加成功")
    return HttpResponse("运输员添加成功")





'''运输人员申请'''
def transpoter_apply(request):
    print("运输员申请与分配函数")
    if request.method=="POST":
        person_info = transpoter_select_inproduct()
        return HttpResponse(person_info)                    #返回选择运输人员的全部信息

'''商品信息扫码录入  前端发送生产内容id和人员id'''
def product_enter(request):
    if request.method=="POST":
        dict_get = json.loads(request.body)             #获得字典
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
        Flag=1,
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
    transpoter_release(peoson_id)                                                      # 运输人员状态释放
    return HttpResponse("终点数据上传完成")
