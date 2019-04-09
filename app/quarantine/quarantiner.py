# 检疫员数据表操作
from django.db import models
from django.forms.models import model_to_dict
from random import randint
from app import models

def inquiry(personid , includekey=None):
    # 根据检疫人员ID查询记录，并字典形式返回需要包含的属性键值对
    res = models.QuarantineRegistry.objects.get(QuarantinePersonID=personid)
    if res is None:
        return "No result found"

    ret = model_to_dict(res, fields=includekey)
    return ret

def application(applicantid, includekey=None):
    # 申请检疫， 分派检疫人员，返回人员信息
    counts = models.QuarantineRegistry.objects.count()
    if counts > 0:
        randId = randint(0, counts - 1)
        res = models.QuarantineRegistry.objects.all()[randId]
        ret = model_to_dict(res, fields=includekey)
        return ret
    else:
        return "No available quarantiner now!"

def alter(personid, newdata):
    # 修改检疫人员信息

    obj = models.QuarantineRegistry.objects.filter(QuarantinePersonID=personid).update(**newdata)
    return "检疫员数据修改成功!"
