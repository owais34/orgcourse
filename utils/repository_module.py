import os,json

class Repository:
    def __init__(self):
        pass

    def loadFromRepo(self):
        curpath = os.getcwd()
        persistance_folder = os.path.join(curpath,"repository")
        persistance_path = os.path.join(persistance_folder,self.__class__.__name__) + ".json"
        try:
            json_data_file = open(persistance_path,"r+")
            dictForm = json.loads(json_data_file.read())
            json_data_file.close()
            return dictForm
        except Exception as e:
            print(e)
            return None


    def persistChanges(self, jsonForm):
        curpath = os.getcwd()
        persistance_folder = os.path.join(curpath,"repository")
        persistance_path = os.path.join(persistance_folder,self.__class__.__name__) + ".json"
        json_data_file = open(persistance_path,"w")
        json_data_file.write(jsonForm)
        json_data_file.close()



if __name__ != "__main__":
    curpath = os.getcwd()
    try:
        persistance_folder = os.path.join(curpath,"repository")
        os.mkdir(persistance_folder)
        
    except:
        print("")
    