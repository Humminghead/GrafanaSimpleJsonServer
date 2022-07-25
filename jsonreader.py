import os
import json
# import list
import time
from filereader import BaseFileReader
from mediator import BaseComponent
import threading


class JsonReader(BaseFileReader, BaseComponent):
    def __init__(self, scanPath=''):
        self.mPath = scanPath
        self.mJsonData = list()

    def readFiles(self):
        while self.isActive:
            files = self.listDirectory(self.mPath)
            # print(files)

            self.mJsonDataMutex.acquire()
            for n in range(len(files)):
                file = files[n]
                fullPath = self.mPath+"/"+file
                if(not file.endswith(".tmp") and os.path.isfile(fullPath) and os.path.exists(fullPath)):
                    data = self.readFile(fullPath)
                    if data:
                        self.mJsonData.append(json.loads(data.encode()))
                        if self.enableDeleting:
                            self.deleteFile(fullPath)
            self.mJsonDataMutex.release()

            # self.mediator.notify(self, "DATA")
            time.sleep(self.scanInterval)

    def clearDataInInterval(self, intervalMs: int):
        if intervalMs == 0:
            return

        intervalS = intervalMs/1000

        self.mJsonDataMutex.acquire()
        for d in self.mJsonData:
            timestamp = d.get('@timestamp')
            if(not timestamp - intervalS < timestamp < timestamp + intervalS):
                self.mJsonData.remove(d)
        self.mJsonDataMutex.release()

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

    def getScanPath(self, path: str):
        return self.mPath

    mPath = str
    mJsonData = list
    isActive = True
    enableDeleting = True
    scanInterval = 1
    mJsonDataMutex = threading.Lock()
