#coding=utf-8
import subprocess
import json
import os
import codecs
import base64

def unpack(uclstr, link= 'quarantine', productionid='3000000001', serial='40'):
    """
    ucl包解包函数
    link 环节名称，如‘quarantine’
    productionid(产品编号)与serial(UCL顺序号)组成UCL包的唯一标识
    """
    # 构造UCL存储路径, 并将UCL字符串存入txt文件
    ucldir = os.getcwd() + "\\app\\ucl\\"
    savedir = ucldir + "UCLPack\\" + link + "\\" + productionid
    if (os.path.exists(savedir ) == False):
        os.makedirs(savedir)
    uclpath = savedir + "\\" + serial + '.txt'
    with codecs.open(uclpath, 'w') as f:
        f.write(uclstr.strip())

    # 构造UCL解码java代码，并读取输出
    cmd = "java -jar " + ucldir + "UCL_Trace.jar -unpack"
    unpack_cmd = [cmd, uclpath]
    new_cmd = " ".join(unpack_cmd)
    res = subprocess.Popen(new_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    jsonstr = str(res.stdout.readline(), encoding='gbk')
    print(jsonstr)
    res.terminate()

    # 字典形式返回内容对象域数据
    ucldict = json.loads(jsonstr)
    contentdict = json.loads(ucldict['cdps']['content'])
    return contentdict, uclpath


def pack(jsonstr, flag, productionid, serial):
    # 示例 jsonstr = "{\"cdps\":{\"content\":{\"QuarantineID\":\"acx0\",\"QuarantineBatch\":\"axc023\",\"QuarantinePersonID\":\"09093\",\"ProductionId\":\"123\",\"QuarantineLocation\":\"nanjing\",\"Applicant\":\"wang\",\"QuarantinerName\":\"lin\",\"QuarantineRes\":\"***\"}}}"
    byte_base64 = base64.b64encode(bytes(jsonstr, encoding='utf-8'))
    jsonstr_base64 = str(byte_base64, 'utf-8')
    savedir = os.getcwd() + "\\app\\ucl\\"
    cmd = "java -jar " + savedir + "UCL_Trace.jar -pack"
    pack_cmd = [cmd, jsonstr_base64]
    new_cmd = " ".join(pack_cmd)
    res = subprocess.Popen(new_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    uclstr = str(res.stdout.readline(), encoding='gbk')
    print(uclstr)
    res.terminate()

    # 构造UCL存储路径, 并将UCL字符串存入txt文件
    ucldir = os.getcwd() + "\\app\\ucl\\"
    savedir = ucldir + "UCLPack\\" + flag + "\\" + productionid
    if (os.path.exists(savedir) == False):
        os.makedirs(savedir)
    uclpath = savedir + "\\" + serial + '.txt'
    with codecs.open(uclpath, 'w') as f:
        f.write(uclstr.strip())

    return uclstr,uclpath


def request_to_uclstr(jsondata):
    for key, value in jsondata.items():
       # if(key == 'quarantine'):
        link = key
        uclstr = value
    return uclstr, link
