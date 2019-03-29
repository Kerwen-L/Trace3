from __future__ import unicode_literals
from django.shortcuts import HttpResponse
from app import models
from datetime import datetime
from app.models import ComplexEncoder
from random import randint
import hashlib
from django.shortcuts import render_to_response
from django.template import Context
from django.forms.models import model_to_dict
import json
# Create your views here.


def quarantine_submit(request):
    if request.method=="POST":
        models.QuarantineData(**json.loads(request.body)).save()
        print("检疫数据上传数据库成功!")
    return HttpResponse("检疫数据上传数据库成功!")


def quarantine_inquiry(request):
    if request.method=="GET":
        production_id = request.GET.get("ProductionId")
        res = models.QuarantineData.objects.filter(ProductionId=production_id)
        ret = []
        if(res):
            for subres in res:
                ret.append(subres.toJSON())
            return HttpResponse(ret, content_type="application/json")
        else:
            return HttpResponse("No result found")
    #return HttpResponse(temp.toJSON(), content_type="application/json")


def quarantiner_inquiry(request):
    if request.method == "GET":
        quarantiner_id = request.GET.get("QuarantinePersonID")
        res = models.QuarantineRegistry.objects.get(QuarantinePersonID=quarantiner_id)
        if(res):
            includekey = ['QuarantinePersonID', 'QuarantinerName', 'IDNo', 'ContactNo_Quar', 'WorkPlaceID', \
                          'CertificateNo', 'CertificateSrc', 'LicensedVeterinaryQCNo', 'LicensedVeterinaryQCSrc', \
                          'QuarantineCounts ', 'PhotoSrc', 'Password']
            ret = model_to_dict(res, fields=includekey)
            return HttpResponse(json.dumps(ret, cls=ComplexEncoder), content_type="application/json")
        else:
            return HttpResponse("No result found")


def encrypt(pwd):
    # 密码加密
    h = hashlib.sha256()
    h.update(bytes(pwd, encoding='utf-8'))
    return pwd
    #return h.hexdigest()


def qurarantiner_application(request):
    if request.method == "GET":
        producer_id = request.GET.get("ProducerId")
        counts = models.QuarantineRegistry.objects.count()
        if counts > 0:
            randId = randint(1, counts)
            includekey = ['QuarantinePersonID', 'QuarantinerName', 'IDNo', 'ContactNo_Quar', 'WorkPlaceID',\
                          'CertificateNo', 'CertificateSrc', 'LicensedVeterinaryQCNo', 'LicensedVeterinaryQCSrc',\
                          'QuarantineCounts ', 'PhotoSrc']
            res = models.QuarantineRegistry.objects.get(id=randId)
            ret = model_to_dict(res, fields=includekey)
            return HttpResponse(json.dumps(ret, cls=ComplexEncoder), content_type="application/json")
        else:
            return HttpResponse("No registried quarantiner now!")


def quarantiner_registry(request):
    if request.method == "POST":
        items = json.loads(request.body)

        quarantiner_id = items.get("QuarantinePersonID")
        password = items.get("Password")
        registertime = items.get("RegisterTime", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        items['RegisterTime'] = registertime

        items['Password'] = encrypt(password)
        res = models.QuarantineRegistry.objects.filter(QuarantinePersonID=quarantiner_id)
        if(len(res)>0):
            return HttpResponse("已存在相同ID!")
        else:
            models.QuarantineRegistry(**items).save()
            return HttpResponse("检疫员注册成功!")


def checkPwd(quarantine_id, pwd):
    pwdEncrypted = encrypt(pwd)

    pwdSaved = models.QuarantineRegistry.objects.get(QuarantinePersonID=quarantine_id).Password
    return pwdSaved == pwdEncrypted


def quarantiner_alter(request):
    if request.method == "POST":
        items = json.loads(request.body)
        quarantine_id = items.get("QuarantinePersonID")
        password = items.get("Password")

        if checkPwd(quarantine_id, password) == True:
            if 'newpassword' in items and items['newpassword'] != None:
                items['Password'] = encrypt(items.pop('newpassword'))
            obj = models.QuarantineRegistry.objects.filter(QuarantinePersonID=quarantine_id).update(**items)
            return HttpResponse("检疫员数据修改成功!")
        else:
            return HttpResponse("密码错误!")


# test git 22223333
