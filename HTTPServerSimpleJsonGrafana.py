from cgitb import handler
from http.server import HTTPServer
from httpgethandler import HttpGetHandler
from jsonreader import JsonReader
from mediator import BaseComponent
from mediator import ConcreteMediator
from mediator import Mediator
from jprocessor import JsonDataProcessor

import threading
import time
import signal
from requests import delete
import sys
import getopt


class MainWorker(BaseComponent):
    def __init__(self, jreader: JsonReader, jprocessor: JsonDataProcessor, mediator: Mediator = None) -> None:
        self.json_reader = jreader
        self.json_processor = jprocessor
        self._mediator = mediator

    def primaryJob(self):
        threading.Thread(target=self.httpd.serve_forever).start()
        threading.Thread(target=self.json_reader.readFiles).start()

        while self.isActive:
            # print("Do JOB")
            if self.json_reader.isActive == False:
                self.isActive = False
                break
            time.sleep(1)

        self.httpd.shutdown()
        self.json_reader.shutdouwn()

        print("Bye")

    def runHttpdServer(self):
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            self.httpd.shutdown()

    def interrupt(self, sig, frame):
        print('You pressed Ctrl+C!')
        self.isActive = False
        self.httpd.server_address

    isActive = True
    httpd = HTTPServer
    json_reader = JsonReader
    json_processor = JsonDataProcessor
    mediator = ConcreteMediator


def run(worker: MainWorker):
    signal.signal(signal.SIGINT, worker.interrupt)
    worker.primaryJob()


def main(argv):
    helpStr = 'Usage: HTTPServerSimpleJsonGrafana.py -d <inputfiles_dir> --ip=127.0.0.1 --port=3003 --extension=.json --max_records_count=1000 --read_interval=1.0'

    json_reader = JsonReader()
    json_processor = JsonDataProcessor()
    worker = MainWorker(json_reader, json_processor)

    try:
        opts, args = getopt.getopt(
            argv, "hd:i:p:e:c:r:", ["idir=", "ip=", "port=", "extension=", "max_records_count=", "read_interval="])
    except:
        sys.exit(2)

    if len(opts) == 0:
        print(helpStr)
        sys.exit(0)

    path = ''
    ip = '127.0.0.1'
    port = 3003
    fileExt: str = '.json'
    maxRecordsCount: int = 0
    readInterval: float = 1

    for opt, arg in opts:
        if opt == '-h':
            print(helpStr)
            sys.exit()
        elif opt in ("-d", "--idir"):
            path = arg
        elif opt in ("-i", "--ip"):
            ip = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-e", "--extension"):
            fileExt = str(arg)
        elif opt in ("-c", "--max_records_count"):
            maxRecordsCount = int(arg)
        elif opt in ("-r", "--read_interval"):
            readInterval = float(arg)

    worker.json_reader.setScanPath(path)
    worker.json_reader.setFileExt(fileExt)
    worker.json_reader.SetDataRecordsMaxCount(maxRecordsCount)
    worker.json_reader.SetScanInterval(readInterval)

    handler = HttpGetHandler
    httpd = HTTPServer((ip, port), handler)
    worker.mediator = ConcreteMediator(handler, json_reader, json_processor)
    worker.httpd = httpd

    run(worker)


if __name__ == "__main__":
    main(sys.argv[1:])
