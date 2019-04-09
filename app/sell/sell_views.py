from __future__ import unicode_literals
from django.shortcuts import HttpResponse, render, redirect
from app import models
# from TestSell import models
from django.shortcuts import render_to_response
from django.template import Context
#from django.utils import simplejson
import json

from django.forms.models import model_to_dict

from datetime import datetime


# Create your views here.
def add_seller(request):
    if request.method == "POST":
        models.SellerRegistry(**json.loads(request.body)).save()
        print("测试：销售人员信息已上传数据库")
    return HttpResponse("测试：销售人员信息已上传数据库")


def inquiry_seller(request):
    if request.method == "GET":
        seller_id = request.GET.get("ConsumerId")
        temp = models.SellerRegistry.objects.filter(ConsumerId=seller_id)
        # seller_id = request.GET.get("SellerID")
        # temp = models.SellerRegistry.objects.filter(SellerID=seller_id)
        ret = []
        if (temp):
            for sample in temp:
                # i = sample.to_dict()
                i = model_to_dict(sample)
                # i.pop("Password")
                i.pop("id")
                i.pop("imgID")
                i.pop("imgwork")
                ret.append(json.dumps(i,cls=models.DateEncoder))
            return HttpResponse(ret, content_type="application/json")
        else:
            return HttpResponse("测试：未查询到符合条件的销售人员信息")


def alter_seller(request):
    if request.method == "POST":
        alter = json.loads(request.body)
        # seller_id = alter.get("SellerID")
        seller_id = alter.get("ConsumerId")
        temp = models.SellerRegistry.objects.get(ConsumerId=seller_id)
        temp.ConsumerId = alter.get("ConsumerId")
        temp.ConsumerName = alter.get("ConsumerName")
        temp.ContactNo = alter.get("ContactNo")
        temp.RegisterTimeConsumer = alter.get("RegisterTimeConsumer")
        temp.SearchCounts = alter.get("SearchCounts")
        temp.VIP = alter.get("VIP")
        temp.Password = alter.get("Password")

        temp.CharacterFlag = alter.get("CharacterFlag")
        # temp.ContactNo = alter.get("ContactNo")
        temp.IDNo = alter.get("IDNo")
        temp.RegisterTime = alter.get("RegisterTime")
        temp.WorkPlaceID = alter.get("WorkPlaceID")
        temp.PhotoSrc = alter.get("PhotoSrc")
        temp.companyregistry = alter.get("companyregistry")
        temp.save()
        print("测试：已修改销售人员信息")
    return HttpResponse("测试：已修改销售人员信息")


'''
def complete_seller(request):
    if request.method=="POST":
        new = models.SellerRegistry(**json.loads(request.body))
        seller_id = new.SellerID
        temp = models.SellerRegistry.objects.get(SellerID=seller_id)
        temp.RegisterTime = datetime.now()
        temp.PhotoSrc = new.PhotoSrc
        temp.WorkPlaceID = new.WorkPlaceID
        temp.save()
        print("测试：已完善销售人员信息")
    return HttpResponse("测试：已完善销售人员信息")
'''


def add_supermarket(request):
    if request.method == "POST":
        models.CompanyRegistry(**json.loads(request.body)).save()
        print("测试：已上传超市信息")
    return HttpResponse("测试：已上传超市信息")


'''
def inquiry_supermarket(request):
    if request.method=="GET":
        supermarket_id = request.GET.get("CompanyID")
        temp = models.CompanyRegistry.objects.get(CompanyID=supermarket_id)
        print("测试：查询超市信息")
    return HttpResponse(temp.toJson(), content_type="application/json")
'''


def inquiry_supermarket(request):
    if request.method == "GET":
        supermarket_id = request.GET.get("CompanyID")
        temp = models.CompanyRegistry.objects.filter(CompanyID=supermarket_id)
        ret = []
        if (temp):
            for sample in temp:
                i = model_to_dict(sample)
                # i.pop("Password")
                # i.pop("SecretKeys")
                i.pop("id")
                ret.append(json.dumps(i,cls=models.DateEncoder))
            return HttpResponse(ret, content_type="application/json")
        else:
            return  HttpResponse("测试：未查询到符合条件的超市信息")
        # print("测试：查询超市信息")
    # return HttpResponse(temp.toJson(), content_type="application/json")


def alter_supermarket(request):
    if request.method == "POST":
        # supermarket_id = request.GET.get("CompanyID")
        # method = request.GET.get("method")
        alter = json.loads(request.body)
        supermarket_id = alter.get("CompanyID")
        temp = models.CompanyRegistry.objects.get(CompanyID=supermarket_id)
        temp.CorporateIDNo = alter.get("CorporateIDNo")
        temp.CorporateContactNo = alter.get("CorporateContactNo")
        temp.OperatingPlace = alter.get("OperatingPlace")
        temp.OperatingKind = alter.get("OperatingKind")
        temp.InvestigateRes = alter.get("InvestigateRes")
        temp.BLicenseRegisterNo = alter.get("BLicenseRegisterNo")
        temp.BLicenseSrc = alter.get("BLicenseSrc")
        temp.BLicenseDeadline = alter.get("BLicenseDeadline")
        temp.TaxRCNo = alter.get("TaxRCNo")
        temp.TaxRCSrc = alter.get("TaxRCSrc")
        temp.FoodDistributionLicenseNo = alter.get("FoodDistributionLicenseNo")
        temp.FoodDistributionLicenseSrc = alter.get("FoodDistributionLicenseSrc")
        temp.FoodHygienePermitNo = alter.get("FoodHygienePermitNo")
        temp.FoodHygienePermitSrc = alter.get("FoodHygienePermitSrc")
        temp.OrganizationCodeCertificateNo = alter.get("OrganizationCodeCertificateNo")
        temp.OrganizationCodeCertificateSrc = alter.get("OrganizationCodeCertificateSrc")
        temp.Password = alter.get("Password")

        '''
        if method=="BLicenseSrc":
            temp.BLicenseSrc = alter.get("BLicenseSrc")
        if method=="TaxRCSrc":
            temp.TaxRCSrc = alter.get("TaxRCSrc")
        if method=="FoodDistributionLicenseSrc":
            temp.FoodDistributionLicenseSrc = alter.get("FoodDistributionLicenseSrc")
        if method=="FoodHygienePermitSrc":
            temp.FoodHygienePermitSrc = alter.get("FoodHygienePermitSrc")
        if method=="OrganizationCodeCertificateSrc":
            temp.OrganizationCodeCertificateSrc = alter.get("OrganizationCodeCertificateSrc")
        '''
        temp.save()
        print("测试:已修改超市信息")
    return HttpResponse("测试:已修改超市信息")


'''
def complete_supermarket(request):
    if request.method=="POST":
        new = models.CompanyRegistry(**json.loads(request.body))
        supermarket_id = new.CompanyID
        temp = models.CompanyRegistry.objects.get(CompanyID=supermarket_id)
        temp.BLicenseRegisterNo = new.BLicenseRegisterNo

        temp.save()
        print("测试：已完善超市信息")
    return HttpResponse("测试：已完善超市信息")
'''


def register_commodity(request):
    if request.method == "POST":
        models.SellData(**json.loads(request.body)).save()
        print("测试：已录入商品信息")
    return HttpResponse("测试：已录入商品信息")


def sell_state(request):
    if request.method == "GET":
        # sell_id = request.GET.get("SellID")
        goods_name = request.GET.get("GoodsName")
        temp = models.SellData.objects.filter(GoodsName__contains=goods_name)
        # temp = models.SellData.objects.get(SellID=sell_id)
        # temp = models.SellData.objects.filter(SellID=sell_id)
        ret = []
        if (temp):
            for sample in temp:
                # i = json.loads(sample.toJSON())
                i = model_to_dict(sample)
                i.pop("id")
                ret.append(json.dumps(i,cls=models.DateEncoder))
                print("测试：查询商品信息")
            return HttpResponse(ret, content_type="application/json")
        else:
            return HttpResponse("测试：未查询到商品信息")


def sell_state_bylocation(request):
    if request.method == "GET":
        location = request.GET.get("location")
        temp = models.SellData.objects.filter(SellLocation__contains=location)
        # temp = models.TestSellData.objects.filter(SellLocation=location)
        ret = []
        if(temp):
            for sample in temp:
                # i = json.loads(sample.toJSON())
                i = model_to_dict(sample)
                i.pop("id")
                ret.append(json.dumps(i, cls=models.DateEncoder))
            return HttpResponse(ret, content_type="application/json")
        else:
            return HttpResponse("测试：未查询到商品信息")


'''
def alter_sell_state(request):
    if request.method == "POST":
        alter = json.loads(request.body)
        sell_id = alter.get("SellID")
        temp = models.SellData.objects.get(SellID=sell_id)
        temp.SellLocation = alter.get("SellLocation")
        temp.SPReceiveTime = alter.get("SPReceiveTime")
        temp.SPSelloutTime = alter.get("SPSelloutTime")
        temp.Price = alter.get("Price")
        temp.APApprovalRes = alter.get("APApprovalRes")
        temp.AccountabilityFlag = alter.get("AccountabilityFlag")
        temp.SellUCLLink = alter.get("SellUCLLink")
        temp.save()
        print("测试;已修改商品信息")
    return HttpResponse("测试;已修改商品信息")
'''
