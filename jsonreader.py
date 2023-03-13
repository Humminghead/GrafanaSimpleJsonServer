import os
import json
import time
from filereader import BaseFileReader
from mediator import BaseComponent
import threading


class JsonReader(BaseFileReader, BaseComponent):
    def __init__(self, scanPath='', fileExt='.out'):
        self.mPath = scanPath
        self.mJsonData = list()

        self.setFileExt(fileExt)

        self.mJsonFileExtension = fileExt

    def readFiles(self):
        while self.isActive:
            files = self.listDirectory(self.mPath)
            # print(files)

            self.mJsonDataMutex.acquire()
            for n in range(len(files)):
                file = files[n]
                fullPath = self.mPath+"/"+file
                if(not file.endswith(".tmp") and os.path.isfile(fullPath) and os.path.exists(fullPath) and file.endswith(self.mJsonFileExtension)):
                    data = self.readFile(fullPath)
                    if data:
                        try:
                            self.mJsonData.append(json.loads(data.encode()))
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

    def readDataInInterval(self, intervalMs: int, erase: bool = False) -> list:
        if intervalMs == 0:
            return self.mJsonData

        intervalS = intervalMs/1000

        self.mJsonDataMutex.acquire()
        result: list() = list()
        for d in self.mJsonData:
            timestamp = d.get('@timestamp')

            if(timestamp - intervalS < timestamp < timestamp + intervalS):
                result.append(d)
                if erase:
                    self.mJsonData.remove(d)

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

    mPath = str
    mJsonData = list
    mJsonFileExtension = str
    isActive = True
    enableDeleting = True
    scanInterval = 1
    mJsonDataMutex = threading.Lock()
