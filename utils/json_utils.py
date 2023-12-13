import json

class Jsoner:

    def getJson(self):
        return self.mainHandler(self)

    def handleList(self, list_object):
        jsonstr = "["
        for elemnt in list_object:
            jsonstr =jsonstr + self.mainHandler(elemnt) + ","
        if len(jsonstr)>1:
            jsonstr=jsonstr[:-1]
        jsonstr=jsonstr+"]"

        return jsonstr

    def mainHandler(self, object):
        jsonstr = ""
        if isinstance(object, str):
            jsonstr=json.dumps(object)
        elif isinstance(object,bool):
            jsonstr = str(object).lower()
        elif isinstance(object,int):
            jsonstr = str(object)
        elif isinstance(object, float):
            jsonstr = str(object)
        elif isinstance(object,dict):
            jsonstr = self.handleDict(object)
        elif isinstance(object,list):
            jsonstr = self.handleList(object)
        else:
            jsonstr = self.handleObject(object)

        return jsonstr

    def handleDict(self, dict):
        jsonstr = "{"
        for key , value in dict.items():
            key = json.dumps()
            jsonstr = jsonstr + key +":" + self.mainHandler(value) + ","
        if len(jsonstr)>1:
            jsonstr = jsonstr[:-1]
        jsonstr = jsonstr + "}"

        return jsonstr

    def handleObject(self, object):
        jsonstr = "{"
        for key , value in object.__dict__.items():
            jsonstr = jsonstr + json.dumps(key) +":" + self.mainHandler(value) + ","
        if len(jsonstr)>1:
            jsonstr = jsonstr[:-1]
        jsonstr = jsonstr + "}"

        return jsonstr
    





