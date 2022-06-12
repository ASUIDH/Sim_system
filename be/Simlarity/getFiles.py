import json as js
from Simlarity.GetGraph import getId
import random
import datetime

def getFiles(fileSavePath , md5List):
    name_id, id_name, id_type = getId("D:\\MD-data\\vt\\vt\\graph.node")
    allFileDict = {}
    fileList = []
    with open(fileSavePath) as f:
        for line in f.readlines():
            malware = js.loads(line)
            addtion_info = malware['additional_info']
            exiftool = addtion_info["exiftool"]
            malDict = {}
            malDict["filename"] = malware["md5"]
            if malware["md5"] not in name_id: # 有几个PE文件 没有lable所以，没有加入图中
                continue
            malDict["md5"] = malware["md5"]
            timeStamp = exiftool["TimeStamp"]
            if malware["md5"] not in name_id:  # 有几个PE文件 没有lable所以，没有加入图中
                continue
            setTimeDict(malDict, timeStamp)
            malDict['status'] = 'unsafe'
            malDict["filesize"] = malware['size']
            malDict['count'] = 0
            malDict['user'] = 'Unknown'
            malDict['MachineType']  = exiftool['MachineType']
            malDict["FileType"]  = exiftool["FileType"]
            allFileDict[malDict['md5']] = malDict # md5作为key加入dict
    for md5 in md5List:
        fileList.append(allFileDict[md5])
    return fileList
def getFilesForAll(fileSavePath):
    ans = {}
    files = []
    name_id, id_name,id_type = getId("D:\\MD-data\\vt\\vt\\graph.node")
    with open(fileSavePath) as f:
        for line in f.readlines():
            malware = js.loads(line)
            addtion_info = malware['additional_info']
            exiftool = addtion_info["exiftool"]
            malDict = {}
            malDict["md5"] = malware["md5"]
            timeStamp = exiftool["TimeStamp"]
            if malware["md5"] not in name_id: # 有几个PE文件 没有lable所以，没有加入图中
                continue
            setTimeDict(malDict,timeStamp)
            malDict["filename"] = 'Unknow_' + str(name_id[malware["md5"]])
            malDict['status'] = 'unsafe'
            malDict["filesize"] = malware['size']
            malDict['count'] = random.randint(1,10)
            malDict['user'] = 'Unknown'
            malDict['MachineType'] = exiftool['MachineType']
            malDict["FileType"] = exiftool["FileType"]
            malDict["type"]= "sim",
            files.append(malDict)
    ans["fileList"] = files[0:min(37,len(files))]
    ans["total"] = min(37, len(files))
    return ans
def setTimeDict (malDict , timeStamp):
    dtArr = timeStamp.strip().split("+")[0]
    dtArr = dtArr.split()
    dateStr = dtArr[0]
    timeStr = dtArr[1]
    dateArr = [int(d) for d in dateStr.split(":")]
    timeArr = [int(t) for t in timeStr.split(":")]
    year = dateArr[0]
    mounth = dateArr[1]
    day = dateArr[2]
    hour = timeArr[0]
    minute = timeArr[1]
    sec = timeArr[2]
    if year == 0:
        datetime.datetime.now()
    else:
        timest = datetime.datetime(year, mounth, day, hour, minute, sec)
        malDict["time"] = timest
if __name__ == "__main__":
    ans = getFilesForAll("D:\\MD-data\\json.txt")
    print(ans)
    mal = {}
