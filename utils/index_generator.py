from utils.repository_module import Repository


class IndexGenerator(Repository,):
    def __init__(self):
        super().__init__()
        self.indexSet = {}
        dictForm =  self.loadFromRepo()
        if dictForm != None:
            self.indexSet.update(dictForm["indexSet"])
        self.persistChanges()
