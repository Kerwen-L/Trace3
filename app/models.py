from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from datetime import date
import datetime
import json

# Create your models here.


class Uni_Manager(models.Manager):
    def update(self,registry,company,**kwargs):
        com = CompanyRegistry.objects.filter(CompanyName=company)
        if com.count() == 0:  # 公司表里没有这个公司
            return 0
        else:
            comid = com.first().id
            aaa = registry(**kwargs,companyregistry_id=comid)
            aaa.save()
            return aaa


    def create(self,company,**kwargs):
        #kwargs.update(classroom_ptr_id=temp.id,c_id=temp.c_id,c_number=temp.c_number)
        # if company==-1:#表示是=售员的个人信息完善
        #     super().create(consumerregistry_ptr_id=temp.id, ConsumerId=temp.ConsumerId, ConsumerName=temp.ConsumerName,
        #                    ContactNo=temp.ContactNo, RegisterTimeConsumer=temp.RegisterTimeConsumer,
        #                    SearchCounts=temp.SearchCounts, VIP=temp.VIP, Password=temp.Password,
        #                    **kwargs)
        # else:
        #     com=CompanyRegistry.objects.filter(CompanyName=company)
        #     if com.count()==0:#公司表里没有这个公司
        #         return 0
        #     else:
        #         comid=com.first().id
        #         super().create(consumerregistry_ptr_id=temp.id,ConsumerId=temp.ConsumerId,ConsumerName=temp.ConsumerName,
        #                    ContactNo=temp.ContactNo,RegisterTimeConsumer=temp.RegisterTimeConsumer,
        #                    SearchCounts=temp.SearchCounts,VIP=temp.VIP,Password=temp.Password,companyregistry_id=comid,
        #                    **kwargs)
        com = CompanyRegistry.objects.filter(CompanyName=company)
        if com.count()==0:#公司表里没有这个公司
            return 0
        else:
            comid=com.first().id
            # super().create(ConsumerId=temp.ConsumerId,ConsumerName=temp.ConsumerName,
            #            ContactNo=temp.ContactNo,RegisterTimeConsumer=temp.RegisterTimeConsumer,
            #            SearchCounts=temp.SearchCounts,VIP=temp.VIP,Password=temp.Password,companyregistry_id=comid,
            #            **kwargs)
            super().create(companyregistry_id=comid,**kwargs,RegisterTime=date.today)


# 消费者注册表
class ConsumerRegistry(models.Model):
    ConsumerId = models.CharField(max_length=10,unique=True)            # 消费者注册ID
    ConsumerName = models.CharField(max_length=10)                      # 姓名
    ContactNo = models.CharField(max_length=11)                         # 联系方式
    RegisterTimeConsumer = models.DateField(default=date.today)       # 消费者注册时间
    SearchCounts = models.IntegerField(default=0)                       # 查询次数
    VIP = models.BooleanField(default=False)                            # 会员标志位
    Password = models.CharField(max_length=30)                          # 登陆密码
    CharacterFlag = models.IntegerField(default=1)                      # 角色属性

    def __str__(self):  # print的时候好看，类似于C++的重载<<
        return self.ConsumerId

    # model的内部写一个函数返回json
    def toJSON(self):
        import json
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]),cls=DateEncoder)


# 企业组织注册表
class CompanyRegistry(models.Model):
    CompanyID = models.CharField(max_length=7)                                          # 企业注册ID(企业唯一标识)
    CompanyName = models.CharField(max_length=40)                                       # 企业名称
    CorporateName = models.CharField(max_length=10)                                     # 法人姓名
    CorporateIDNo = models.CharField(max_length=18)                                     # 企业法人身份证号
    CorporateContactNo = models.CharField(max_length=11,null=True,blank=True)           # 企业法人联系方式
    RegisterTime = models.DateTimeField(default=date.today)                             # 企业注册时间
    OperatingPlace = models.CharField(max_length=30)                                    # 经营地址
    OperatingKind = models.IntegerField(default=0)                                      # 经营类型
    InvestigateRes = models.IntegerField(default=0)                                     # 生产地实地考察结果
    BLicenseRegisterNo = models.CharField(max_length=20)                                # 营业执照注册号
    BLicenseSrc = models.CharField(max_length=50)                                       # 营业执照图片地址
    BLicenseDeadline = models.DateField(default=date.today)                               # 营业执照经营期限
    PLicenseNo = models.CharField(max_length=30)                                        # 生产许可证编号
    PLicenseSrc = models.CharField(max_length=40)                                       # 生产许可证图片地址
    PLicenseDeadline = models.DateField(default=date.today)                             # 生产许可证生产期限
    AEPCertificateNo = models.CharField(max_length=30,null=True,blank=True)             # 动物防疫条件合格证号(农场)
    AEPCertificateSrc = models.CharField(max_length=50)                                 # 动物防疫条件合格证图片地址(农场)
    TaxRCNo = models.CharField(max_length=30,null=True,blank=True)                      # 税务登记证编号
    TaxRCSrc = models.CharField(max_length=50)                                          # 税务登记证图片地址
    FoodDistributionLicenseNo = models.CharField(max_length=30,null=True,blank=True)    # 食品流通许可证编号
    FoodDistributionLicenseSrc = models.CharField(max_length=50)                        # 食品流通许可证图片地址
    FoodHygienePermitNo = models.CharField(max_length=30,null=True,blank=True)          # 食品卫生许可证编号
    FoodHygienePermitSrc = models.CharField(max_length=50)                              # 食品卫生许可证图片地址
    OrganizationCodeCertificateNo = models.CharField(max_length=30,null=True,blank=True)# 组织机构代码证编号
    OrganizationCodeCertificateSrc = models.CharField(max_length=50)                    # 组织机构代码证图片地址
    RoadTransportBusinessLicenseNo = models.CharField(max_length=30,null=True,blank=True)# 道路运输经营许可证编号
    RoadTransportBusinessLicenseSrc = models.CharField(max_length=50)                   # 道路运输经营许可证图片地址
    AnimalEpidemicPCNo = models.CharField(max_length=30,null=True,blank=True)           # 动物防疫合格证编号(农场)
    AnimalEpidemicPCSrc = models.CharField(max_length=50)                               # 动物防疫合格证图片地址(农场)
    SecretKeys = models.CharField(max_length=2048)                                      # 密钥对
    Password = models.CharField(max_length=35)                                          # 登陆密码(需加密保存)

    def __str__(self):  # print的时候好看，类似于C++的重载<<
        return self.CompanyID

    # model的内部写一个函数返回json
    def toJSON(self):
        import json
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]),cls=DateEncoder)


# 生产者注册表
class ProducerRegistry(ConsumerRegistry):
    #ProducerId=models.CharField(max_length=10)#唯一标识生产者；2位省份，8位人员编号
    #ProducerName=models.CharField(max_length=10)
    IDNo=models.CharField(max_length=18)                       # 生产人员身份证号，18位
    #ContactNo=models.BigIntegerField()
    # RegisterTime=models.DateField(default=date.today)
    RegisterTime = models.DateField(default=date.today)
    ProductionPlace=models.CharField(max_length=30,null=True)
    ProductionKind=models.IntegerField(default=0,null=True)
    ProductionScale=models.CharField(max_length=100,null=True)#这里存json
    InvestigateRes=models.IntegerField(default=0,null=True)
    SecretKeys=models.CharField(max_length=100,null=True)#这里存json
    #Password=models.CharField(max_length=30)
    CompanyName=models.CharField(max_length=15,null=True)
    imgID=models.ImageField(upload_to='images/',default="")
    imgwork = models.ImageField(upload_to='images/',default="")
    companyregistry=models.ForeignKey("CompanyRegistry",on_delete=models.CASCADE,related_name="producer",null=True)#一个农场有好多生产者
    #这里
    inherit=Uni_Manager()

    def __str__(self):  # print的时候好看，类似于C++的重载<<
            return self.ConsumerId

    # model的内部写一个函数返回json
    def toJSON(self):
            return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))


# 运输员注册表
class TransporterRegistry(ConsumerRegistry):
    #TransporterId=models.CharField(max_length=15)
    #TransporterName=models.CharField(max_length=10)
    IDNo=models.CharField(max_length=18)                       # 运输人员身份证号，18位
    #ContactNo=models.BigIntegerField()
    RegisterTime=models.DateField(default=date.today)
    WorkPlaceID=models.CharField(max_length=30)
    PhotoSrc=models.CharField(max_length=40)
    RoadTransportQCNo=models.BigIntegerField()
    RoadTransportQCSrc=models.CharField(max_length=40)
    TransportCounts=models.IntegerField(default=0)
    Flag = models.IntegerField(default=0)
    #Password=models.CharField(max_length=30)
    imgID = models.ImageField(upload_to='images/', default="")
    imgwork = models.ImageField(upload_to='images/', default="")
    imgquality = models.ImageField(upload_to='images/', default="")
    companyregistry = models.ForeignKey("CompanyRegistry", on_delete=models.CASCADE,
                                        related_name="transporter",null=True)  # 一个农场有好多生产者
    inherit = Uni_Manager()
    def __str__(self):  # print的时候好看，类似于C++的重载<<
            return self.ConsumerId

    def to_front(self):
        listtemp = [f.name for f in self._meta.fields]
        listtemp.remove('consumerregistry_ptr')
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in listtemp]), cls=DateEncoder)

    # model的内部写一个函数返回json
    def toJSON(self):
            return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))

    def to_front(self):#20190410新增
        templist = []
        for key in self._meta.fields:
            templist.append(key.name)  # 获得属性域

        templist.remove('consumerregistry_ptr')
        templist.remove('companyregistry')
        templist.remove('imgwork')
        templist.remove('imgquality')
        templist.remove('imgID')

        return json.dumps(dict([(attr, getattr(self, attr)) for attr in templist]),cls=DateEncoder)


# 检疫员注册表
class QuarantineRegistry(ConsumerRegistry):
    QuarantinePersonID = models.CharField(max_length=15)
    #Password = models.CharField(max_length=128)
    QuarantinerName = models.CharField(max_length=16)
    IDNo = models.CharField(max_length=18)
    #ContactNo = models.BigIntegerField(null=True, blank=True)
    RegisterTime = models.DateField(default=date.today)
    WorkPlaceID = models.CharField(max_length=10)
    PhotoSrc = models.CharField(max_length=100, null=True, blank=True)
    CertificateNo = models.CharField(max_length=32, null=True, blank=True)
    CertificateSrc = models.CharField(max_length=100, null=True, blank=True)
    LicensedVeterinaryQCNo = models.CharField(max_length=32, null=True, blank=True)
    LicensedVeterinaryQCSrc = models.CharField(max_length=32, null=True, blank=True)
    QuarantineCounts = models.IntegerField(default=0)
    imgID = models.ImageField(upload_to='images/', default="")
    imgwork = models.ImageField(upload_to='images/', default="")
    imgquality1 = models.ImageField(upload_to='images/', default="")
    imgquality2 = models.ImageField(upload_to='images/', default="")
    companyregistry = models.ForeignKey("CompanyRegistry", on_delete=models.CASCADE,
                                        related_name="quarantine",null=True)  # 一个农场有好多生产者
    inherit = Uni_Manager()
'''
    def __unicode__(self):
        return self.ConsumerId
'''


# 加工员注册表
class ProcessorRegistry(ConsumerRegistry):
    #ProcessorId = models.CharField(max_length=30)                                #加工员注册ID
    #ProcessorName = models.CharField(max_length=10)                       #姓名
    IDNo = models.CharField(max_length=18)                                 #身份证号
    #ContactNo = models.BigIntegerField()                                  #联系方式
    RegisterTime = models.DateField(default=date.today)                   #注册时间
    WorkPlaceID = models.CharField(max_length=50, null=True)                         #工作单位ID
    PhotoSrc = models.CharField(max_length=50,null=True,blank=True)       #加工人员证件照地址
    HC4foodCertificationNo = models.BigIntegerField(null=True)                     #食品从业人员健康证明编号
    HC4foodCertificationSrc = models.CharField(max_length=50,null=True)             #食品从业人员健康证明图片地址
    ProcessorCounts = models.IntegerField(default=0,null=True)                      #加工操作次数
    #Password = models.CharField(max_length=30)
    imgID = models.ImageField(upload_to='images/', default="")
    imgwork = models.ImageField(upload_to='images/', default="")
    imgquality = models.ImageField(upload_to='images/', default="")
    companyregistry = models.ForeignKey("CompanyRegistry", on_delete=models.CASCADE,
                                        related_name="processor",null=True)  # 一个农场有好多生产者
    inherit = Uni_Manager()
    def __unicode__(self):  # print的时候好看，类似于C++的重载<<
        return self.ConsumerId
    # model的内部写一个函数返回json
    #def toJSON(self):
     #   return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]),cls=DateEncoder)


# 销售员注册表
class SellerRegistry(ConsumerRegistry):
    # SellerID = models.IntegerField()                        #销售人员注册ID(唯一的标识销售人员)
    # SellerID = models.CharField(max_length=20,unique=True,null=True,blank=True)  # 销售人员注册ID(唯一的标识销售人员)
    # SellerName = models.CharField(max_length=10)  # 姓名
    # SellerName = ConsumerRegistry.ConsumerName
    # IDNo = models.BigIntegerField()                         #身份证号
    IDNo = models.CharField(max_length=18)                          # 身份证号
    # ContactNo = models.BigIntegerField()                    #联系方式
    # RegisterTime = models.DateTimeField()  # 销售人员注册时间
    RegisterTime = models.DateField(default=date.today)             # 销售人员注册时间
    WorkPlaceID = models.CharField(max_length=50)                   # 工作单位ID(企业注册ID)
    PhotoSrc = models.CharField(max_length=100)                     # 销售人员证件照地址
    # Password = models.CharField(max_length=30)              #登陆密码(需加密保存)
    imgID = models.ImageField(upload_to='images/', default="")
    imgwork = models.ImageField(upload_to='images/', default="")    # 销售员没有工作单位
    companyregistry = models.ForeignKey("CompanyRegistry", on_delete=models.CASCADE,
                                        related_name="seller", null=True)  # 一个农场有好多生产者
    inherit = Uni_Manager()


# 生产内容数据表
class ProductionData(models.Model):
    RecordID=models.CharField(max_length=25)
    # MonitorId=models.BigIntegerField()
    MonitorId = models.CharField(max_length=25)
    State=models.IntegerField()
    HealthState=models.SmallIntegerField()
    GPSLocation=models.CharField(max_length=50)#json存经纬度
    ActiveDis=models.FloatField()#活动距离
    Weight=models.FloatField()
    BodyTemperature=models.FloatField()
    UCLLink=models.CharField(max_length=50)
    MonitorRecordTime=models.TimeField()#timestamp()
    Flag = models.IntegerField(default=0)
    def __str__(self):  # print的时候好看，类似于C++的重载<<
            return self.RecordID

            # model的内部写一个函数返回json

    def toJSON(self):
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))


# 生产监测器数据表
'''
    暂时缺省
'''


# 基站数据表
class BaseStationData(models.Model):
    UUID = models.CharField(max_length=50,default='',blank=True)  # 终端编号
    Time = models.DateTimeField(default=date.today)
    Index = models.IntegerField()
    Data1 = models.CharField(max_length=20,default='',blank=True)
    Data2 = models.CharField(max_length=20,default='',blank=True)
    Sheep_Id = models.ForeignKey('ProductionData')
    SheepID = models.CharField(max_length=20,default='',blank=True)


# ID绑定表
class UUID_Sheep(models.Model):
    UUID = models.CharField(max_length=50, null=True)
    RecordID = models.CharField(max_length=25, null=True)
    PB_Flag = models.IntegerField(default=0, null=True)


# UCL数据表
class UCLData(models.Model):
    ProductionId = models.CharField(max_length=16)      # 产品编号
    UCLPack = models.CharField(max_length=1024)         # UCL包（UCL包字符串形式，Base64编码）
    Flag = models.IntegerField()                        # 环节标识（表明UCL存储在哪个环节的服务器时）
    isLatest = models.IntegerField()                    # 分支标识（标识是否该ProductionId对应的最新的UCL包）
    SerialNum = models.IntegerField()                   # 顺序号（溯源树的层数，与ProductionId结合，唯一标识一个UCL包）
    UCLSrc = models.CharField(max_length=255)           # UCL存储地址（在各个服务器上的存储地址）
    RelatedUCLId = models.IntegerField()                # 关联UCL的id


# 检疫数据表
class QuarantineData(models.Model):
    QuarantineID = models.CharField(max_length=10, null=True, blank=True)
    ProductionId = models.CharField(max_length=16)
    QuarantinerName = models.CharField(max_length=16, null=True, blank=True)
    QuarantinePersonID = models.CharField(max_length=10)
    QuarantineLocation = models.CharField(max_length=100)
    QuarantineRes = models.CharField(max_length=100)
    QuarantineLink = models.CharField(max_length=100, null=True, blank=True)
    # QuarantineTime = models.DateField(default=date.today)
    QuarantineTime = models.DateTimeField(default=timezone.now())
    QuarantineBatch = models.CharField(max_length=50)
    QuarantineUCLLink = models.CharField(max_length=100, null=True, blank=True)
    Applicant = models.CharField(max_length=30)
    Flag = models.IntegerField(default=1)

    def __unicode__(self):
        return self.QuarantineID

    def toJSON(self):
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]), cls=DateEncoder)


# 加工数据表
class ProcessData(models.Model):
    ProcessID = models.CharField(max_length=22, null=True, blank=True)   #加工编号(屠宰点编号7+生产内容ID10+屠宰点宰杀顺序)
    ProductionID = models.CharField(max_length=16)                 #生成内容ID 羊ID+00(8+2)
    ConsumerId = models.CharField(max_length=10)              #加工人员ID 继承与消费者ID
#    ProcessPersonID = models.ForeignKey('ProcessorRegistry',on_delete=models.CASCADE,)
    ProcessLocation = models.CharField(max_length=7)               #加工地 (企业编号7)
    # ProcessTime = models.DateField(default=date.today)             #加工时间
    ProcessTime = models.DateTimeField(default=timezone.now())  # 加工时间
    ProductionKind = models.IntegerField()                         #生产内容类型(分割为几个)
    ReproductionID = models.CharField(max_length=16)              #生产内容ID演化
    QRCodeLink = models.CharField(max_length=50)                     #二维码地址
    Step = models.IntegerField(default=0)  # 阶段
    ProcessUCLLink = models.CharField(max_length=50)               #UCL
    Flag = models.IntegerField(default=3)
    def __str__(self): # print的时候好看，类似于C++的重载<<
        return self.ProcessID
    # model的内部写一个函数返回json
    def toJSON(self):
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]),cls=DateEncoder)


# 运输数据表
class TransportData(models.Model):
    TransactionID=models.CharField(max_length=50)
    # BatchNum = models.IntegerField(default=0)
    ProductionID=models.CharField(max_length=16)                      #生产内容ID
    TransactionPersonID=models.CharField(max_length=50,default='')    #运输人员ID(与信息表中的id建立关联)
    From=models.CharField(max_length=50)
    To=models.CharField(max_length=50)
    Flag=models.IntegerField(default=2)                               #环节标志
    # TransactionStartTime=models.DateTimeField(default=date.today)         #流通开始时间
    # TransactionEndTime=models.DateTimeField(default=date.today)
    TransactionStartTime = models.DateTimeField(default=timezone.now())  # 流通开始时间
    TransactionEndTime = models.DateTimeField(default=timezone.now())
    TransactionStartUCLLink=models.CharField(max_length=50)           #起点UCL索引
    TransactionEndUCLLink=models.CharField(max_length=50)
    Transport_Flag = models.IntegerField(default=0)
    def __str__(self):
        return self.TransactionID

    def info_dict(self):                                              #生成包含所有属性的字典
        dict2 = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return dict2

    def toJSON(self):
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]),cls=DateEncoder)


# 销售数据表
class SellData(models.Model):
    # SellID = models.BigIntegerField()                       #销售编号(销售点编号+销售/生产内容编号+销售点顺序号)
    SellID = models.CharField(max_length=30,unique=True,null=True,blank=True)  # 销售编号(销售点编号+销售/生产内容编号+销售点顺序号)
    # ProductionID = models.BigIntegerField()                 #生产内容ID/生产内容再加工ID(销售内容ID)
    ProductionID = models.CharField(max_length=16,null=True,blank=True)  # 生产内容ID/生产内容再加工ID(销售内容ID)
    # SellLocation = models.CharField(max_length=50,null=True,blank=True)  # 销售地
    # SPReceiveTime = models.DateTimeField()  # 销售点接收时间
    SPReceiveTime = models.DateTimeField(default=timezone.now())  # 销售点接收时间
    SPSelloutTime = models.DateTimeField(null=True,blank=True)  # 销售点售出时间(为空则未销售)
    Price = models.IntegerField()  # 销售价格(避免销售点恶意抬价)
    APApprovalRes = models.IntegerField(default=0)  # 被溯源次数
    AccountabilityFlag = models.IntegerField(default=0)  # 追责标志位
    SellUCLLink = models.CharField(max_length=100,null=True,blank=True)  # 销售UCL索引
    GoodsName = models.CharField(max_length=50,null=True,blank=True)      #商品名称
    ConsumerID = models.CharField(max_length=10,null=True,blank=True)   # 销售员ID
    Flag = models.IntegerField(default=4)


'''
    def __str__(self):  # print的时候好看，类似于C++的重载<<
        return self.SellID

    # model的内部写一个函数返回json
    def toJSON(self):
        import json
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]),cls=DateEncoder)
'''







# 各种Encoder 需要统一
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


class ComplexEncoder(json.JSONEncoder):                  #时间解析函数
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)



class DateEncoding(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return o.strftime('%Y/%m/%d')







