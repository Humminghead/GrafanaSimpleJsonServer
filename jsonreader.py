import os
import json
import time
from datetime import timezone, datetime
from filereader import BaseFileReader
from mediator import BaseComponent
import threading
from jsonrdata import JsonData


class JsonReader(BaseFileReader, BaseComponent):
    def __init__(self, scanPath='', fileExt='.out'):
        self.mPath = scanPath
        self.mJsonData = list()
        self.setFileExt(fileExt)
        self.mJsonFileExtension = fileExt

    def readFiles(self):
        while self.isActive:
            files = self.listDirectory(self.mPath)

            if files == None:
                self.isActive = False
                return

            self.mJsonDataMutex.acquire()

            for n in range(len(files)):
                file = files[n]
                fullPath = self.mPath+"/"+file
                if(not file.endswith(".tmp") and os.path.isfile(fullPath) and os.path.exists(fullPath) and file.endswith(self.mJsonFileExtension)):
                    data = self.readFile(fullPath)
                    if data:
                        try:
                            fileTimeS = datetime.now().timestamp()
                            jData = json.loads(data.encode())
                            mJsonDataLen = len(self.mJsonData)
                            if self.mJsonDataRecordsMaxCount > 0 and mJsonDataLen >= self.mJsonDataRecordsMaxCount:
                                self.mJsonData.pop(0)
                            self.mJsonData.append(JsonData(fileTimeS, jData))
                        except AttributeError as e:
                            print(e)
                        except TypeError as e:
                            print(e)
                        except json.JSONDecodeError as e:
                            print(e.lineno, e.msg, e.pos, e.doc)
                            continue

                        if self.enableDeleting:
                            self.deleteFile(fullPath)
            self.mJsonDataMutex.release()

            # self.mediator.notify(self, "DATA")
            time.sleep(self.scanInterval)

    def readDataInInterval(self, intervalS: float) -> list:
        result: list() = list()

        self.mJsonDataMutex.acquire()
        for d in range(len(self.mJsonData)):
            jItem = self.mJsonData[d]
            timestamp = jItem.mTime

            if timestamp == None:
                continue

            if(timestamp - intervalS <= timestamp <= timestamp + intervalS):
                result.append(jItem)

        self.mJsonDataMutex.release()
        return result

    def shutdouwn(self):
        self.isActive = False

    def getData(self):
        return self.mJsonData

    def clearData(self):
        self.mJsonDataMutex.acquire()
        self.mJsonData.clear()
        self.mJsonDataMutex.release()

    def setScanPath(self, path: str):
        if len(path) > 0:
            self.mPath = path

    def getScanPath(self):
        return self.mPath

    def setFileExt(self, ext: str):
        if(len(ext) > 0 and ext[0] != '.'):
            self.mJsonFileExtension = ""
            self.mJsonFileExtension = "." + ext

    def getFileExt(self):
        return self.mJsonFileExtension

    def SetEnableDeleting(self, enable: bool):
        self.enableDeleting = enable

    def SetDataRecordsMaxCount(self, count: int):
        self.mJsonDataRecordsMaxCount = count

    def GetDataRecordsMaxCount(self) -> int:
        return self.mJsonDataRecordsMaxCount

    def SetScanInterval(self, seconds: float):
        self.scanInterval = seconds

    def GetScanInterval(self) -> float:
        return self.scanInterval

    mPath = str
    mJsonData = list
    mJsonFileExtension = str
    mJsonDataRecordsMaxCount = 0
    isActive = True
    enableDeleting = True
    scanInterval = 1.0
    mJsonDataMutex = threading.Lock()
