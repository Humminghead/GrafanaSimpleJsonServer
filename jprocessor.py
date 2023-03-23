import json
import time


class JsonDataProcessor:
    def flatJson(self, y):
        out = {}

        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '_')
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '_')
                    i += 1
            else:
                out[name[:-1]] = x

        flatten(y)
        return out

    def listDataRecords(self, inData: list):
        if len(inData) > 0:
            flatJ = self.flatJson(inData)
            values = r'['
            for name in flatJ:
                values = values + "\""+name+"\","

            values = values[:-1] + "]"
            return json.loads(values.encode())
        return json.loads("[]")

    def getTagetData(self, inData: list, eventData: str):
        values = json.loads(eventData)
        targetString = r'['
        for val in values:
            targetString += "{\"target\": \""
            # targetString += "{'target': '"
            targetString += val.get('target') + "\", \"datapoints\": ["

            if(len(inData) == 0):
                targetString += r']},'
            else:
                for data in inData:
                    flatJ = self.flatJson(data)
                    valTarget = val.get('target')
                    jval = None
                    jtime = None

                    if(flatJ.__contains__(valTarget)):
                        jval = flatJ[valTarget]

                    if jval == None:
                        return (targetString + r"]}]")

                    if(flatJ.__contains__('@timestamp')):
                        jtime = flatJ['@timestamp']*1000
                    else:
                        jtime = int(time.time()*1000)

                    if (type(jval) is float):
                        targetString += "[" + \
                            str(jval) + ", " + str(jtime) + "],"
                    else:
                        targetString += "[" + \
                            str(jval) + ".0, " + str(jtime) + "],"

                    # jval = str(flatJ[val.get('target')])
                    # jtime = flatJ['@timestamp']*1000
                    # targetString += "[" + jval + ".0, " + str(jtime) + "],"

                targetString = targetString[:-1] + r']},'
        return (targetString[:-1] + r']')

    def getDataPoints(self, inData: str, valueName: str):
        outStr = r'{"target": "'
        for data in inData:
            print(inData[valueName.encode()])
