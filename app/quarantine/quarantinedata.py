# 检疫数据表的操作
from django.db import models
from app import models
def submit(datadict):
    # 上传数据
    models.QuarantineData(**datadict).save()

def inquiry(productionid):
    # 根据产品ID查询记录
    res = models.QuarantineData.objects.filter(ProductionId=productionid)
    ret = []
    if (res):
    # 多条检疫记录
        for subres in res:
            ret.append(subres.toJSON())
        return ret
    return None

