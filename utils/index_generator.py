from utils.repository_module import Repository
from utils.json_utils import Jsoner
import random

charset = "abcdefghijklmnopqrstuvwxyz0123456789"

counter = 0

class IndexGenerator(Repository,Jsoner):
    def __init__(self):
        super().__init__()
        self.indexSet = set()
        dictForm =  self.loadFromRepo()
        if dictForm != None:
            self.indexSet.update(dictForm["indexSet"])
        self.persistChanges()

    def getNewIndex(self, persistInstantly = False):
        key = self.generateRandomKey()
        while key in self.indexSet:
            key = self.generateRandomKey()
        self.indexSet.add(key)
        if counter == 0 or persistInstantly:
            self.persistChanges()
        counter = (counter + 1) % 10
        return key

    def generateRandomKey(self) -> str:
        key = ""
        
        for i in range(10):
            index = random.randrange(0,len(charset))
            key = key + charset[index]
        
        return key


    
