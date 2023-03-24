import json


class JsonData():
    def __init__(self, time: float, jData: json):
        self.mTime = time
        self.mJson = jData

    mTime = float
    mJson = json
