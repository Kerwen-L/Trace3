from __future__ import unicode_literals
from django.shortcuts import HttpResponse, render, redirect
from app import models
from django.shortcuts import render_to_response
import json
from datetime import date
from datetime import datetime
from app.ucl import ucl

'''运输员队列生成'''
transpoter_list = []
def transporter_list_generate():
    flag = 0    #
    templist = models.TransporterRegistry.objects.filter(Flag=0)                # 从运输数据库中取出所有空闲记录
    if templist:
        for temp in templist:                                                   # 取出这些记录的生产内容id并形成list返回
            tempid = temp.ConsumerId
            transpoter_list.append(tempid)
        flag = 1
        print("运输员队列已生成，包含以下id")
        print(transpoter_list)
    else:
        flag = 0
    return flag


'''运输员状态释放，根据运输人员ID'''
def transpoter_release(number):
    models.TransporterRegistry.objects.filter(ConsumerId=number).update(Flag=0)


'''运输员选择'''
def transpoter_select_inproduct():                                          #返回运输员的记录，由前端决定显示的具体内容
    print("调用运输员选择函数")
    if transpoter_list.__len__() == 0:
        have_people = transporter_list_generate()                           #队列有内容，返回1，队列为空，返回0
        if have_people==1:
            print("运输员列表已从0更新")
        else:
            print("all busy")
    #20190410修改
    if transpoter_list.__len__() >0:
        id = transpoter_list[0]                                                         #选择第一个运输员
        if models.TransporterRegistry.objects.filter(ConsumerId=id).update(Flag=1):     #修改标志位
            print("运输员标志位已经修改")
        transpoter_recorder = models.TransporterRegistry.objects.get(ConsumerId=id)     #查找记录
        if transpoter_recorder:
            print("找到运输员的信息")
        info_str = transpoter_recorder.to_front()                                       #获取字符串形式的信息给前端
        print("运输员的姓名" + transpoter_recorder.ConsumerName)
        del transpoter_list[0]                                                          #从队列中删除
        return info_str  # 返回信息字符串
    else:
        return HttpResponse("没有运输员处于空闲状态，请等待。。。")                    # 返回信息字符串

def transpoter_regis(request):
    if request.method == "POST":
        models.TransporterRegistry(**json.loads(request.body)).save()
        print("运输员添加成功")
    return HttpResponse("运输员添加成功")


'''运输员信息修改'''
'''如果id和password匹配的话进行修改'''
def transpoter_info_alter(request):
    if request.method == "POST":
        dict_get = json.loads(request.body)             # 获得字典
        peoson_id = dict_get['ConsumerId']
        temp_people = models.TransporterRegistry.objects.filter(ConsumerId=peoson_id)
        if temp_people.Password == dict_get['Password'] and dict_get['NewPwd'] != dict_get['NewPwdAgain']:
            temp_people.update( ConsumerName=dict_get['ConsumerName'],
                                ConsumerId=dict_get['ConsumerId'],
                                ContactNo=dict_get['ContactNo'],
                                TransportCounts=dict_get['TransportCounts'],
                                RoadTransportQCNo=dict_get['RoadTransportQCNo'],
                                Password=dict_get['NewPwd']
                              )
        elif dict_get['NewPwd'] != dict_get['NewPwdAgain']:
            return HttpResponse("新密码不一致")
        elif temp_people.Password != dict_get['Password']:
            return HttpResponse("密码输入错误")


'''运输人员申请'''
def transpoter_apply(request):
    print("运输员申请与分配函数")
    if request.method=="GET":
        person_info = transpoter_select_inproduct()
        return HttpResponse(person_info)                    #返回选择运输人员的全部信息

'''商品信息扫码录入  前端发送生产内容id和人员id'''
def product_enter(request):#20190412
    if request.method=="POST":
        dict_get0 = json.loads(request.body)
        PackedUcl = dict_get0['ucl']
        serialnumber = dict_get0['serialnumber']
        productionId = dict_get0['productionId']                                            #
        flag = dict_get0['flag']

        dict_get,path = ucl.unpack(PackedUcl, 'transport',productionId,serialnumber)       #解包，返回解包地址
        New_Recorder = models.TransportData.objects.create(**dict_get)  # 新增记录'''
        if New_Recorder:
            print(dict_get)
            print(path)
            return HttpResponse("OK")
        else:
            return HttpResponse("录入失败")

        # 以下内容正常 没有ucl
        #temp_person = models.TransporterRegistry.objects.filter(ConsumerId=data['TransactionPersonID'])
        # if temp_person:
        #     print(temp_person[0].ConsumerName)
        #     models.TransportData.objects.create(**data)
        #     return HttpResponse("录入完毕")
        # else:
        #     print("查无此人")
        #     return HttpResponse("查无此人")

'''
@运输数据 开始
1、收到前端推送的运输数据
2、解析出运输人员id
3、在运输数据表中 把与该运输员id匹配且标志为0 的商品
4、填写运输数据表（来源、去向、开始时间、商品标志）
5、生成环节标志、运输批次、流通编号（生产内容id+环节标志）
'''
def Transport_start(request):#20190412
    if request.method=="POST":
        dict_get = json.loads(request.body)                                                # 获得字典

        PackedUcl = dict_get['ucl']
        serialnumber = dict_get['serialnumber']
        productionId = dict_get['productionId']                                            #
        flag = dict_get['flag']

        dict_get,Beginpath = ucl.unpack(PackedUcl, 'transport',productionId,serialnumber)       #解包，返回解包地址
        print("path:"+Beginpath)
        person_id=dict_get['TransactionPersonID']                                          # 解析运输人员id
        print("personid是：  "+person_id)

    temp_person = models.TransporterRegistry.objects.filter(ConsumerId=dict_get['TransactionPersonID'])
    if temp_person:
        print("运输员的名字为: "+temp_person[0].ConsumerName)
        flag = models.TransportData.objects.filter(TransactionPersonID=person_id,State=0)
        if flag:
            models.TransportData.objects.filter(TransactionPersonID=person_id,State=0).update(      # 更新前端推送内容到运输数据表
                From=dict_get['From'],
                To=dict_get['To'],
                TransactionStartTime=dict_get['TransactionStartTime'],
                State=1,
                Flag=2,
            )
            if dict_get['From'].find("牧场") >= 0:                                                 #模糊查询 说明运输员在生产运输阶段
                print("开始更新生产数据 环节标志30")
                list1 = models.TransportData.objects.filter(TransactionPersonID=person_id,State=1)  #取出本次运输的全部生产商品记录
                for record in list1:
                    models.TransportData.objects.filter(ProductionID=record.ProductionID).update(  #填写流通编号
                        TransactionID=record.ProductionID + '30',
                        Transport_Flag=30,
                        Flag=2,
                        TransactionStartUCLLink=Beginpath,)
                    #在这里打包
                    #uclstr, path = ucl.pack(jsonstr, flag, record.ProductionID, TotalDict['tag'])#ucl字符串，环节标志、生产id、顺序号

            elif dict_get['From'].find("检疫") >= 0:                                               #模糊查询 说明运输员在检疫运输阶段
                print("开始更新检疫数据 环节标志31")
                list1 = models.TransportData.objects.filter(TransactionPersonID=person_id,State=1)  #取出本次运输的全部检疫商品记录
                for record in list1:
                    models.TransportData.objects.filter(ProductionID=record.ProductionID).update(  #填写流通编号
                        TransactionID=record.ProductionID + '31',
                        Transport_Flag=31,
                        Flag=2,
                        TransactionStartUCLLink=Beginpath,)

            elif dict_get['From'].find("加工") >= 0:                                               #模糊查询 说明运输员在加工运输阶段
                print("开始更新加工数据 环节标志32")
                list1 = models.TransportData.objects.filter(TransactionPersonID=person_id,State=1)  #取出本次运输的全部加工商品记录
                for record in list1:
                    models.TransportData.objects.filter(ProductionID=record.ProductionID).update(  #填写流通编号
                        TransactionID=record.ProductionID + '32',
                        Transport_Flag=32,
                        Flag=2,
                        TransactionStartUCLLink=Beginpath,)
            else:
                print("数据填写不规范")

            return HttpResponse("起点数据填写完成")
        else:
            return HttpResponse("该运输员没有运输数据，请确认已经扫码录入完毕")
    else:
        return HttpResponse("信息填写错误，没有这个运输员")

'''
@运输数据 到达
1、收到前端推送的运输数据(运输人员id和到达时间)
2、解析出运输人员id
3、在运输数据表中 检索与该运输员id匹配且标志为1的商品
4、填写运输数据表（到达时间）
'''
def Transport_end(request):#20190412
    dict_get0 = json.loads(request.body)                                                # 获得字典
    PackedUcl = dict_get0['ucl']
    serialnumber = dict_get0['serialnumber']
    productionId = dict_get0['productionId']  #
    flag = dict_get0['flag']

    dict_get, path = ucl.unpack(PackedUcl, 'transport', productionId, serialnumber)  # 解包，返回解包地址
    print(dict_get)
    peoson_id=dict_get['TransactionPersonID']                                        # 解析运输人员id
    transpoter_release(peoson_id)  # 运输人员状态释放
    RelatedRecorder = models.TransportData.objects.filter(TransactionPersonID=peoson_id,State=1).update(TransactionEndTime=dict_get['TransactionEndTime'],
                                                         State=2,TransactionEndUCLLink=path)
    if RelatedRecorder:
            # str = Recorder.toJSON()
            # uclstr,EndPath = ucl.pack(str,flag,Recorder.ProductionID,serialnumber)
            # Recorder.objects.update(TransactionEndUCLLink=EndPath)
            # print(uclstr)
        return HttpResponse("终点数据上传完成")
    else:
        return HttpResponse("终点数据上传失败")


