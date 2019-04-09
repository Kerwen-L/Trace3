#coding=utf-8
import subprocess
import json
import os
import codecs
import base64

def unpack(uclstr, link= 'quarantine', productionid='30000010', serial='40'):
    """
    jsonstr = "{\"cdps\":{\"content\":{\"QuarantineID\":\"acx0\",\"QuarantineBatch\":\"axc023\",\"QuarantinePersonID\":\"09093\",\"ProductionId\":\"123\",\"QuarantineLocation\":\"nanjing\",\"Applicant\":\"wang\",\"QuarantinerName\":\"lin\",\"QuarantineRes\":\"***\"}}}"
    jsonstr = jsonstr.replace("\"", "<@@>")
    uclstr = uclstr.replace("\"", "<@@>")*
    """
    # 构造UCL存储路径, 并将UCL字符串存入txt文件
    savepath = "F:\\UCLPack\\" + link + "\\" + productionid + "\\"
    if (os.path.exists(savepath) == False):
        os.makedirs(savepath)
    uclpath = savepath + serial + '.txt'
    with codecs.open(uclpath, 'w') as f:
        f.write(uclstr)

    # 构造UCL解码java代码，并读取输出
    cmd = "java -jar F:\\UCL_JAVA_201805211135.jar -unpack"
    unpack_cmd = [cmd, uclpath]
    new_cmd = " ".join(unpack_cmd)
    res = subprocess.Popen(new_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    jsonstr = str(res.stdout.readline(), encoding='gbk')
    print(jsonstr)
    res.terminate()

    # 字典形式返回内容对象域数据
    ucldict = json.loads(jsonstr)
    contentdict = json.loads(ucldict['cdps']['content'])
    return contentdict


def pack(jsonstr):
    # 示例 jsonstr = "{\"cdps\":{\"content\":{\"QuarantineID\":\"acx0\",\"QuarantineBatch\":\"axc023\",\"QuarantinePersonID\":\"09093\",\"ProductionId\":\"123\",\"QuarantineLocation\":\"nanjing\",\"Applicant\":\"wang\",\"QuarantinerName\":\"lin\",\"QuarantineRes\":\"***\"}}}"
    byte_base64 = base64.b64encode(bytes(jsonstr, encoding='utf-8'))
    jsonstr_base64 = str(byte_base64, 'utf-8')
    cmd = "java -jar F:\\UCL_JAVA_201805211135.jar -pack"
    pack_cmd = [cmd, jsonstr_base64]
    new_cmd = " ".join(pack_cmd)
    res = subprocess.Popen(new_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    jsonstr = str(res.stdout.readline(), encoding='gbk')
    print(jsonstr)
    res.terminate()


def request_to_uclstr(jsondata):
    for key, value in jsondata.items():
       # if(key == 'quarantine'):
        link = key
        uclstr = value
    return uclstr, link
