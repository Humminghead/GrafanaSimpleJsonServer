from array import array
from http.server import BaseHTTPRequestHandler
import json
from mediator import BaseComponent
from mediator import MediatorEvent


class HttpGetHandler(BaseHTTPRequestHandler, BaseComponent):
    def debugPrint(self):
        print("------------------BEGIN------------------------")
        print("Path: ", self.path)
        print(self.headers)
        # print("Data: ", self.getRequestContent())
        print("------------------END--------------------------")

    def sendJSON(self, content):
        comments = json.loads(content)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        dump = json.dumps(comments)
        self.wfile.write(dump.encode())

    def send200(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write('Test connection'.encode())

    def requestHandler(self):
        url = self.path
        try:
            content = self.getRequestContent()
        except:
            content = None

        if url == '/':
            self.send200()

        if url == '/search':
            if not content == None:
                jcontent = json.loads(content)
                target = jcontent.get('target')
                if not len(target) == 0:
                    self.mediator.notify(
                        self, MediatorEvent("search_target", target))
                else:
                    self.mediator.notify(
                        self, MediatorEvent("search_global", ""))

        if url == '/query':
            if not content == None:
                jcontent = json.loads(content)
                targets = jcontent.get('targets')
                intervalMs = jcontent.get("intervalMs")
                self.mediator.notify(self, MediatorEvent(
                    "query_targets", json.dumps(targets).encode(), intervalMs))

    def do_GET(self):
        # self.debugPrint()
        self.requestHandler()

    def do_POST(self):
        # self.debugPrint()
        self.requestHandler()

    def sendSearchResponce(self, rspData: json):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(rspData).encode())

    def sendQueryResponce(self, rspData: json):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        jDump = json.dumps(rspData).encode()
        self.wfile.write(jDump)

    def sendAnnoResponce(self):
        print("sendAnnotateResponce")

    def getRequestContent(self) -> array:
        cl = self.headers.get('Content-Length')
        length = 0

        if cl != None:
            length = int(cl)

            if length > 0:
                data = self.rfile.read(length)
                return data

        return array()
