#coding=utf-8
from __future__ import unicode_literals

from django.forms import model_to_dict

from app import models
import subprocess
import json
import os
import codecs
import base64
import platform
from app import models
from django.shortcuts import HttpResponse

def getEncoding():
    if(platform.system() == 'Windows'):
        encode_way = 'gbk'
    elif(platform.system() == 'Linux'):
        encode_way = 'utf-8'
    else:
        encode_way = None
    return encode_way

def unpack(uclstr, flag= 'quarantine', productionid='3000000001', serial='40'):
    """
    ucl包解包函数
    link 环节名称，如‘quarantine’
    productionid(产品编号)与serial(UCL顺序号)组成UCL包的唯一标识
    {
	"ucl":"woEAOgQBAABABAQAAAAAAAAAIMKQw6nCgUEtAAAAAAAAACLCrgFEw54DAsKAAQDDjADCgC8Aw4d7IlF1YXJhbnRpbmVMb2NhdGlvbiI6Im5hbmppbmciLCJRdWFyYW50aW5lUGVyc29uSUQiOiIwOTA5MyIsIlF1YXJhbnRpbmVCYXRjaCI6ImF4YzAyMyIsIlByb2R1Y3Rpb25JZCI6IjEyMyIsIlF1YXJhbnRpbmVJRCI6ImFjeDAiLCJRdWFyYW50aW5lUmVzIjoiKioqIiwiQXBwbGljYW50Ijoid2FuZyIsIlF1YXJhbnRpbmVyTmFtZSI6ImxpbiJ9D0QMAwDCkBxMwoMBQTA6N0Q6MTI6QjE6RDM6MUQ6OTY6QzA6RkM6NTc6OTc6Mjk6MjQ6QTU6OEI6NEM6OTk6MDk6NkE6NkY6QUI6Nzk6MkY6NDI6Mjk6NDA6NDQ6NUQ6MjU6QUM6OTk6MzM6REY6MEY6OUQ6NDI6MTk6RjY6RDc6RDk6Rjk6REE6MjI6QTE6MkU6OEM6MDQ6NUQ6RjE6RUY6OEY6NzQ6RUQ6NUU6RUI6MTY6MTQ6RkY6ODI6MUU6NjA6Mjg6Mzg6Njc6Rjk6Q0E6QTk6QkE6MDk6NTQ6NUE6MzM6NUU6MEE6Qzg6ODU6NDM6RUQ6OTc6NTM6MTQ6OEQ6NTQ6NTk6MEU6RDQ6OTY6MTY6NDA6Qzc6NEM6MzE6N0U6MjE6MDA6RUU6NzI6QTg6NDU6QzU6NTQ6QkQ6NDk6N0U6RTU6Njg6NTM6REE6QzM6RDk6MTI6Mzg6RTE6Q0E6NTc6NDk6NzQ6ODE6QTU6Qzg6RjQ6MzY6QUY6NkI6REE6OUM6NTc6MjEfTMKDATc1OkVFOjhGOkJEOkZFOjYyOjAwOkYwOkQ1OjA3OjhCOkNCOkZBOkQyOjBDOkJDOkJDOkY3OjAwOkFCOjM1OkI1OjY3OjU4Ojc5OkM3OjQxOjFEOkE4OjJDOjE2OkZBOkEzOjEzOjBBOjUyOjNGOjMyOjc0OjkwOkVDOjc5OkM4Ojc0OkQzOjUxOjAzOjkzOkExOjIxOkE4OkY1OkZEOjdFOjJGOjdGOjQ1OjYzOkRBOjE2OjIxOkQyOjVEOkQ1OjZDOkNDOkM4OjI1OjAzOjdEOkEyOjFFOjY1OjA4OjJDOkM2OkE3OkVEOjhCOjY2OkYxOkQ1OkIyOkFDOkEzOjRFOkIxOjM0OkNFOjIwOjJBOjk2OjZDOkFGOjg1OkU2OkI4OjIxOjZFOjQ4OjE4OjY3OkY4OkVBOkUzOkE2OjBEOjM2OjA0OjE2OjlDOjRDOkNCOjQwOkJGOkI0Ojk4OjNBOjQyOjBDOjY2OkY5OjYwOkY0OjY4OjZDOjdDOjU2",
	"productionId": "3000000",
	"serialnumber": "40",
	"flag":"1"
    }
    """
    # 构造UCL存储路径, 并将UCL字符串存入txt文件
    ucldir = os.getcwd() + "/app/ucl/"
    savedir = ucldir + "UCLPack/" + flag + "/" + productionid
    if (os.path.exists(savedir ) == False):
        os.makedirs(savedir)
    uclpath = savedir + "/" + serial + '.txt'
    with codecs.open(uclpath, 'w') as f:
        f.write(uclstr.strip())

    # 构造UCL解码java代码，并读取输出
    cmd = "java -jar " + ucldir + "UCL_Trace.jar -unpack"
    unpack_cmd = [cmd, uclpath]
    new_cmd = " ".join(unpack_cmd)
    res = subprocess.Popen(new_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    encoding_str = getEncoding()
    if(encoding_str):
        jsonstr = str(res.stdout.readline(), encoding=encoding_str)
        print(jsonstr)
        res.terminate()

        # 字典形式返回内容对象域数据
        ucldict = json.loads(jsonstr)
        contentdict = json.loads(ucldict['cdps']['content'])
        return contentdict, ucldict, uclpath
    else:
        raise OSError('Unsupported system')


def pack(jsonstr, flag, productionid, serial):
    # 示例 jsonstr = "{\"cdps\":{\"content\":{\"QuarantineID\":\"acx0\",\"QuarantineBatch\":\"axc023\",\"QuarantinePersonID\":\"09093\",\"ProductionId\":\"123\",\"QuarantineLocation\":\"nanjing\",\"Applicant\":\"wang\",\"QuarantinerName\":\"lin\",\"QuarantineRes\":\"***\"}}}"
    byte_base64 = base64.b64encode(bytes(jsonstr, encoding='utf-8'))
    jsonstr_base64 = str(byte_base64, 'utf-8')
    savedir = os.getcwd() + "/app/ucl/"
    cmd = "java -jar " + savedir + "UCL_Trace.jar -pack"
    pack_cmd = [cmd, jsonstr_base64]
    new_cmd = " ".join(pack_cmd)
    res = subprocess.Popen(new_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    encoding_str = getEncoding()
    if(encoding_str):
        uclstr = str(res.stdout.readline(), encoding=encoding_str)
    else:
        raise OSError('Unsupported system')
    print(uclstr)
    res.terminate()

    # 构造UCL存储路径, 并将UCL字符串存入txt文件
    ucldir = os.getcwd() + "/app/ucl/"
    savedir = ucldir + "UCLPack/" + flag + "/" + productionid
    if (os.path.exists(savedir ) == False):
        os.makedirs(savedir)
    uclpath = savedir + "/" + serial + '.txt'
    with codecs.open(uclpath, 'w') as f:
        f.write(uclstr.strip())
        print('UCL存储本地服务器成功!')

    return uclstr

def get_ucl(request):
    if request.method == "GET":
        production_id = request.GET.get("ProductionID")
        res = models.UCLData.objects.get(ProductionId=production_id, isLatest=1)

        if res is None:
            return "No result found"
        ret = model_to_dict(res)
        for key, value in ret.items():
            ret[key] = str(value)
        return HttpResponse(json.dumps(ret), content_type="application/json")

def save_in_db(ucldict, flag, uclstr, uclpath):

    productionID = ucldict['cgps']['contentID']
    serialnumber = None
    ruclID = -1

    if('cgps' in ucldict):
        if('contentID' in ucldict['cgps']):
            productionID = ucldict['cgps']['contentID']
    else:
        print("No CGPS PropertySets in the UCL")


    if('cdps' in ucldict):
        serialnumber = ucldict['cdps']['tag']
        if('relatedUCL' in ucldict['cdps']):
            # 获取关联UCL
            relatedUCL = ucldict['cdps']['relatedUCL']
            relatedPid = relatedUCL.split(';')[0]
            relatedSn = relatedUCL.split(';')[1]

            # 当前productionID对应的产品出现新的UCL包, 更新标识
            rucl = models.UCLData.objects.get(ProductionId=relatedPid, SerialNum=relatedSn)
            ruclID = rucl.id
            if (rucl.ProductionId == productionID):
                rucl.isLatest = 0
                rucl.save()
    else:
        print("No CDPS PropertySets in the UCL")




    # 构建存入UCL数据表的数据字典
    data = {}
    data['ProductionId'] = productionID
    data['UCLPack'] = uclstr
    data['Flag'] = int(flag)
    data['isLatest'] = 1
    data['SerialNum'] = int(serialnumber)
    data['UCLSrc'] = uclpath
    data['RelatedUCLId'] = ruclID
    models.UCLData(**data).save()
    print('UCL存储数据库成功!')
