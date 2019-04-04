#coding=utf-8
import subprocess
import json
import os
import codecs


def unpack(uclstr, link= 'quarantine', productionid='30000010', serial='40'):
    """
    jsonstr = "{\"cdps\":{\"content\":{\"QuarantineID\":\"acx0\",\"QuarantineBatch\":\"axc023\",\"QuarantinePersonID\":\"09093\",\"ProductionId\":\"123\",\"QuarantineLocation\":\"nanjing\",\"Applicant\":\"wang\",\"QuarantinerName\":\"lin\",\"QuarantineRes\":\"***\"}}}"
    jsonstr = jsonstr.replace("\"", "<@@>")
    uclstr = uclstr.replace("\"", "<@@>")*
    """
    uclstr = str(uclstr.encode())

    # 构造UCL存储路径, 并将UCL字符串存入txt文件

    savepath = "F:\\UCLPack\\quarantine\\" + productionid + "\\"
    if (os.path.exists(savepath) == False):
        os.makedirs(savepath)
    uclpath = savepath + serial + '.txt'
    with codecs.open(uclpath, 'w', encoding='utf-8') as f:
        f.write(uclstr)

    cmd = "java -jar F:\\UCL_JAVA_201805211135.jar"
    unpack_cmd = [cmd, uclpath]
    new_cmd = " ".join(unpack_cmd)
    res = subprocess.Popen(new_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    jsonstr = str(res.stdout.readline(), encoding='gbk')
    jsonstr = jsonstr.replace("<@@>", "\"")
    print(jsonstr)
    res.terminate()

    ucldict = json.loads(jsonstr)
    contentdict = ucldict['cdps']['content']
    return contentdict
